#!/usr/bin/env python3
"""Install the vendored document fonts so the templates find them by name.

    python3 scripts/install_fonts.py           # install
    python3 scripts/install_fonts.py --check   # report, change nothing
    python3 scripts/install_fonts.py --uninstall

templates/resume.tex and templates/cover_letter.tex ask for "Public Sans" and
"IBM Plex Mono" by family name, not by path. That is deliberate and it is the
only arrangement that survives the templates being copied: application-builder
copies them into a per-role folder inside the user's workspace, at a directory
depth this repository does not control and cannot predict, so a relative Path=
would resolve to nothing and an absolute one would name a plugin checkout that
the next update replaces.

Family-name lookup goes through fontconfig, so the fix is to put the files
somewhere fontconfig already looks. That is what this does: copy the vendored
faces into the user font directory and refresh the cache.

Not installing them is a supported outcome, not a broken one. Both templates
wrap every font in \\IfFontExistsTF and fall back to DejaVu, so a user who never
runs this gets documents that build and look different. That is why this script
is not wired into any gate and nothing calls it automatically -- writing files
into a user's home directory is not a thing a documentation check should do
behind their back.

Only the faces the templates actually use are installed. assets/fonts/ also
holds Saira Condensed and IBM Plex Mono Medium, which exist for the README card
and have no business on someone's system as a side effect of building a resume.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDORED = ROOT / "assets" / "fonts"

# The faces named in the two templates' preambles, and nothing else. Public Sans
# supplies the body (Regular/Bold/Italic/BoldItalic) plus ExtraBold for \heavy;
# IBM Plex Mono supplies the eyebrows and datelines at Regular and SemiBold.
#
# Adding a weight to a template means adding it here. A template that names a
# face this list does not carry silently takes the DejaVu fallback branch on a
# machine where the user did everything right, which reads as the script being
# broken rather than the list being short.
FACES = (
    "PublicSans-Regular.ttf",
    "PublicSans-Bold.ttf",
    "PublicSans-Italic.ttf",
    "PublicSans-BoldItalic.ttf",
    "PublicSans-ExtraBold.ttf",
    "IBMPlexMono-Regular.ttf",
    "IBMPlexMono-SemiBold.ttf",
)

LICENSES = ("OFL-PublicSans.txt", "OFL-IBMPlexMono.txt")

# A subdirectory rather than the font root, so uninstalling is a directory
# removal that cannot take an unrelated font with it.
SUBDIR = "slushpile"


def target_dir() -> Path:
    """Where this platform expects user-installed fonts to live."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Fonts" / SUBDIR
    if sys.platform.startswith("win"):
        # No supported user-level install path that XeLaTeX picks up reliably.
        # Say so rather than writing somewhere hopeful.
        raise SystemExit(
            "Windows: install the fonts by hand. Select the .ttf files in\n"
            f"  {VENDORED}\n"
            "right-click, and choose Install. Or skip it: both templates fall\n"
            "back to a font you already have."
        )
    return Path.home() / ".local" / "share" / "fonts" / SUBDIR


def check_dir() -> Path | None:
    """Where --check should look, or None where the platform has no such place.

    --check changes nothing, and the half of its report that matters most on an
    unsupported platform — whether the vendored sources are complete — does not
    depend on a destination at all. Calling target_dir() here instead would make
    the one read-only mode the one mode a Windows user cannot run.
    """
    if sys.platform.startswith("win"):
        return None
    return target_dir()


def refresh_cache(destination: Path) -> str:
    """Rebuild the fontconfig cache. macOS has no fc-cache and needs none."""
    if sys.platform == "darwin":
        return "macOS registers new fonts without a cache rebuild."
    if shutil.which("fc-cache") is None:
        return (
            "fc-cache not found, so the cache was not refreshed. The files are "
            "in place; log out and back in, or install fontconfig."
        )
    subprocess.run(["fc-cache", "-f", str(destination)], check=True,
                   capture_output=True)
    return f"fc-cache refreshed {destination}."


def missing_sources() -> list[str]:
    return [name for name in (*FACES, *LICENSES) if not (VENDORED / name).is_file()]


def check(destination: Path | None) -> int:
    absent = missing_sources()
    if absent:
        print("Vendored fonts are incomplete. Missing from assets/fonts/:",
              file=sys.stderr)
        for name in absent:
            print(f"  {name}", file=sys.stderr)
        return 1

    if destination is None:
        print(f"{len(FACES)} faces vendored in {VENDORED.relative_to(ROOT)}, "
              f"all present.")
        print("\nThis platform has no user-level font directory XeLaTeX picks "
              "up reliably, so there is nothing to install into and nothing to "
              "report on. Install by hand: select the .ttf files in")
        print(f"  {VENDORED}")
        print("right-click, and choose Install. Or skip it: both templates fall "
              "back to a font you already have.")
        return 0

    installed = [name for name in FACES if (destination / name).is_file()]
    print(f"{len(FACES)} faces vendored in {VENDORED.relative_to(ROOT)}.")
    print(f"{len(installed)} of {len(FACES)} installed in {destination}.")

    if len(installed) < len(FACES):
        print("\nThe templates will use the DejaVu fallback. That builds and it "
              "is not the house style.")
        print("Run without --check to install.")
    return 0


def install(destination: Path) -> int:
    absent = missing_sources()
    if absent:
        print("Refusing to install: vendored fonts are incomplete.", file=sys.stderr)
        for name in absent:
            print(f"  missing {name}", file=sys.stderr)
        return 1

    destination.mkdir(parents=True, exist_ok=True)

    for name in FACES:
        shutil.copy2(VENDORED / name, destination / name)

    # The OFL requires the license to travel with the font. Copying the files
    # without it is the one step here that is not merely untidy to skip.
    for name in LICENSES:
        shutil.copy2(VENDORED / name, destination / name)

    print(f"Installed {len(FACES)} faces to {destination}")
    print(refresh_cache(destination))
    print("\nVerify:  fc-list | grep -iE 'public sans|plex mono'")
    print("Then rebuild any document already compiled against the fallback.")
    return 0


def uninstall(destination: Path) -> int:
    if not destination.exists():
        print(f"Nothing installed at {destination}.")
        return 0

    shutil.rmtree(destination)
    print(f"Removed {destination}")
    print(refresh_cache(destination.parent))
    print("The templates fall back to DejaVu from here. They still build.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="report what is installed, change nothing")
    mode.add_argument("--uninstall", action="store_true",
                      help="remove the fonts this script installed")
    args = parser.parse_args()

    # target_dir() raises on a platform with no supported install path, so it is
    # called only by the two modes that actually need somewhere to write.
    if args.check:
        return check(check_dir())
    if args.uninstall:
        return uninstall(target_dir())
    return install(target_dir())


if __name__ == "__main__":
    raise SystemExit(main())
