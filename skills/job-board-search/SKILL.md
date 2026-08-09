---
name: job-board-search
description: Search a named company's careers board, or resolve a natural-language query into a company list and search each. Extract job descriptions, score pool-anchored and channel-conditional fit against the user's profile, run a contrarian gate before tiers are finalized, and create role folders with assessments. Updates the job search tracker.
argument-hint: "<company> [role keywords] | <query describing the work and where>"
license: MIT
---

# Job Board Search

Search a careers board, extract the postings, and score each one against the
**realistic applicant pool** rather than against the posting's own keywords.

Two ways in. Name a company and this skill searches that company. Describe the
work instead — a function, a place, a market — and Phase 0 resolves the
description into a list of companies and searches each one. Everything after
Phase 0 is identical either way, because the second mode's only job is producing
the company list the first mode is handed directly.

**Announce at start.** Company mode: "Searching $COMPANY for roles matching the
profile. Focus: $KEYWORDS. Scoring: pool-anchored, channel-conditional,
contrarian-gated." Query mode: the same sentence with the resolved company count
in place of `$COMPANY`, announced only after Phase 0e, so the user is never told
a number that a confirmation step might still change.

**Every `templates/...` path in this file is relative to the plugin, not to the workspace.** The working directory is the user's job-search directory and does not contain them, so a bare `templates/role_analysis.md` resolves to nothing. Resolve them against the directory this skill file was itself loaded from — that works on every harness, where a harness-specific plugin-root variable does not.

**Arguments:** one required argument, read as either a company or a query. See
Phase 0a for how to tell them apart and what to do when it is genuinely unclear.

- **Company mode** — `$1` is a company name, `$2+` are role keywords. Keywords
  default to `targeting.functions` in `preferences.yaml`.
- **Query mode** — the whole argument describes the work, the place, or the
  market. Constraints in the query are read on top of `preferences.yaml`, never
  instead of it.

**Examples:**
```
/slushpile:job-board-search Anthropic applied AI
/slushpile:job-board-search Rivian manufacturing NPI
/slushpile:job-board-search Stripe
/slushpile:job-board-search applied AI roles within 50 miles of Martinsville, VA that fit my profile
/slushpile:job-board-search remote staff platform engineering at Series B infra companies
/slushpile:job-board-search who is hiring manufacturing engineers near me
```

## Scoring Philosophy

Three properties, and skipping any one of them collapses the scoring back into keyword matching:

**Pool-anchored.** Fit is where the candidate sits in the realistic applicant pool for this specific role. Not their match against the job description. A 75% keyword match against a pool whose 75th-percentile applicant matches at 90% is a weak application, and grading it against the posting says the opposite.

**Channel-conditional.** Cold submission and warm referral are different gates with different pass rates. A role that is marginal cold and strong with a referral gets both numbers, not their average.

**Calibration-aware.** The user's own application history sets the priors. A pipeline blind to its own track record produces optimism rather than signal, indefinitely, because nothing ever contradicts it.

The contrarian pass is a **gate**, not an appendix. It runs before tier tables are written and its findings change them.

## Prerequisites

Read in full before assessing anything. Skipping these produces assessments that are confidently wrong about relocation, blockers, and domain overlap — the three things a user notices immediately and then stops trusting the tool over.

- **`profile.md`** — complete background. The primary reference for every fit judgment.
- **`preferences.yaml`** — constraints, compensation method, targeting, claimed differentiators. **Every hard kill in Phase 3j comes from this file.** Nothing here is hardcoded.
- **`job_search.md`** — the tracker. Referrals, cooldowns, and the calibration table.
- **`companies.md`** — whether this company has already been searched, and whether it is excluded. In query mode this file is load-bearing rather than advisory: it is the only thing standing between a market query and a list that re-searches everything the user already looked at last month.

If `preferences.yaml` does not exist, stop and run `/slushpile:onboard`.

## Phase 0: Resolve the Target Set

Skip this phase in company mode. It exists for a query that describes the work
rather than the employer, and its only output is a list of companies to hand to
Phase 1. Nothing downstream of here knows which mode it was reached from, which
is deliberate: a query mode that changed how roles get scored would produce
assessments that are not comparable against the ones a company-mode run
produced, and the calibration table cannot tell the two apart.

### 0a. Decide which mode you are in

A bare company name, with or without trailing role keywords, is company mode.
An argument that describes roles, a place, a market, or a hiring situation is
query mode.

When the argument reads both ways, ask. Some words are both a company and a
category, and the two readings send the run somewhere completely different.
Guessing wrong here does not fail loudly — it produces a complete, expensive,
internally consistent search of the wrong target set, and the user finds out
when they read a report about companies they never asked about.

**State the mode you chose and the reason, in one line, before anything else.**
A mode decision that is never stated is one the user cannot correct until the
run is over.

### 0b. Extract the constraints

Read out of the query:

- **Function and seniority.** Falls back to `targeting.functions` and
  `targeting.levels` when the query does not say.
- **Geography.** A named place with or without a radius, a region, or remote.
  Resolve anything relative — "near me", "within driving distance" — against
  `identity.location`.
- **Anything else stated:** industry, company stage, size, ownership.

**Query constraints are additional to `preferences.yaml`, never a replacement
for it.** A user asking for roles near one city has not withdrawn their
compensation floor, their excluded regions, or their excluded companies. Reading
the query as an override is the failure mode of this phase, and what it produces
looks responsive: a tidy list, on topic, containing roles the user already ruled
out and will now have to rule out again by hand.

The one exception is geography, and only when the query names a place that
`relocation` would otherwise exclude. Asking about a specific city is evidence
about that city that postdates the preferences file. Surface the conflict and
ask; do not silently apply either one.

**Write the resolved constraint set out before searching.** A radius the user
meant loosely and you applied strictly is the difference between thirty
candidates and three, and nothing in the output shows which happened.

### 0c. Generate candidate companies

Search for employers matching the constraint set. Vary the search the way 1b
does — one query returns one query's blind spot, and here the blind spot costs a
whole company rather than one posting.

- Employers by industry and place: `{industry} companies in {metro}`
- Aggregator boards, read for **employer names** rather than for postings
- `targeting.target_companies` in `preferences.yaml`, filtered to the query
- The Watchlist table in `companies.md`, filtered the same way

Prefer employers over postings at this stage. A posting on an aggregator is
often stale, duplicated, or a staffing agency reposting someone else's
requisition, and Phase 1 is going to read the company's own board regardless.
The aggregator is worth reading for the name it reveals, not the listing it
shows.

Aim for fifteen to thirty candidates before filtering. Below that the filter has
nothing to work with, and a thin candidate list is indistinguishable in the
output from a thorough search of a thin market.

### 0d. Filter, and count what each step removed

In this order:

1. In `targeting.excluded_companies`, or in the Excluded table of `companies.md`.
2. Searched inside its recheck window per `companies.md`, unless the user asked
   to refresh.
3. Ruled out by `relocation` — check `willing` and `target_regions` before
   dropping anything on location, and honor `remote_preference` before dropping
   a company for being in the wrong place at all.
4. No plausible opening for the target functions. Weak filter, applied last.
   This is a guess from outside the company's board; Phase 1 is what finds out.

**Report the count each step removed, not only the total that survived.**
"Twenty-two candidates: four searched recently, two excluded, three out of
region, thirteen to search" is checkable by the person reading it. "Searching
thirteen companies" is not, and it hides the case where one bad filter ate the
list.

### 0e. Confirm before spending the budget

Show the user the final list and the counts, and get a yes before Phase 1.

Phases 1 through 5 run per company, and they are where this skill spends nearly
everything: browser navigation, full posting capture, a per-role assessment, and
a share of the contrarian batch. A target list that is wrong in a way only the
user can see is worth exactly one question. Ask it before the spend, not after.

Cap the run at ten companies unless the user says otherwise, and **name the ones
you cut** rather than reporting a truncated list as the result. A silent cap
reads as "this is the market" when it is "this is the first ten."

Then run Phases 1 through 4 per company, and Phase 5 once across all of them,
per 5c.

## Phase 1: Discovery

### 1a. Find the careers URL

Careers sites fall into two categories, and getting this wrong wastes the most time of any error in this skill.

| Type | Behavior | Tool |
|---|---|---|
| Server-rendered | Full HTML in the response | WebFetch |
| JavaScript SPA | Response is a JS bundle, no listings | Playwright or the browser tools |

Most large-company career sites are SPAs. If WebFetch returns a page with no job titles in it, that is the signal — switch to browser automation rather than retrying.

Common platforms and their patterns: Greenhouse (`boards.greenhouse.io/{company}`), Lever (`jobs.lever.co/{company}`), Ashby (`jobs.ashbyhq.com/{company}`), Workday (`{company}.wd1.myworkdayjobs.com`), SmartRecruiters, and in-house boards at the largest companies. Greenhouse and Lever are usually server-rendered and cheap to search. Workday is always an SPA.

Find the board first by searching the web for `{company} careers` rather than guessing a URL.

### 1b. Run several queries

One query misses roles. Run three to five, varying:

- The function title and its synonyms — many roles that fit are titled something else entirely
- Seniority terms from `targeting.levels`
- Domain keywords from `targeting.industries`
- Location filters, and one unfiltered pass

### 1c. Extract the listing data

For each result: title, requisition ID, location, team or department, posted date, and URL.

### 1d. Triage on titles

Do not fetch every posting. From the first twenty to forty results, keep anything where the title plausibly maps to the target functions, and read the responsibilities before concluding a title is wrong-function. Adjacent titles are frequently the best fits — the posting's title reflects the company's internal taxonomy, not the work.

Discard on title alone only for unambiguous mismatches: a different profession entirely, or a seniority level several steps away.

## Phase 2: Extract the Postings

### 2a. Navigate to each posting

Use browser automation for SPA boards.

**Never run browser navigation in parallel agents.** The browser is a shared singleton and concurrent agents clobber each other's pages. Sequential navigation, always.

The singleton is shared **across sessions**, not just across this run's agents. Another session driving the same browser will move tabs out from under this one, and the failure is silent: the read succeeds, it just returns a page that is not the one navigated to. Before parsing any posting, confirm the page is the URL that was requested — check the title or the requisition ID against what the listing said. On a mismatch, re-navigate rather than parsing what is there. A posting captured from the wrong tab produces a role folder for a job that was never assessed, and nothing downstream can detect it.

### 2b. Capture verbatim

Write each posting to `job_description.md` using `templates/job_description.md`.

**Capture verbatim. Do not summarize.** Three agents parse this text directly — the ATS simulator counts keyword occurrences, the requirements analyst checks qualifications one at a time, and the pool analyst infers the pool from how the posting is written. All three degrade against a summary, and quietly.

Capture the compensation band exactly as posted. Note the application form's structure if visible: years-of-experience dropdowns, screening questions, whether a cover letter field exists. A hard "8+ years of X" dropdown is a completely different obstacle from the same sentence in prose, and only the pool analyst's filter-exposure estimate distinguishes them.

## Phase 3: Fit Assessment

Skipping 3a, 3d, 3h, 3i, or 3j reverts the scoring to absolute grading. Those five are the method.

### 3a. Calibration ingest — required

Read the Calibration section of `job_search.md` and the `calibration_priors` block in `preferences.yaml` before scoring anything.

Capture: this company's historical conversion rate, which verdict tiers are over- or under-converting, and any sharp mismatch — an INTERVIEW verdict that auto-rejected, or a pass that would have converted.

`calibration_priors` holds the same findings in the form the agents consume: observed per-channel rates with a sample size, free-text drift notes, and per-company overrides. Where it has a `by_company` entry for this company, that rate replaces the company-type prior in 3d. Where `drift_notes` describes a pattern this role fits, apply it and say you did.

How to use it:

- Historical conversion at this company below 5% → treat any Tier 1 score with suspicion. The pool likely outclasses the candidate regardless of the keyword match.
- No history at this company → use the closest peer in the table. Say which peer, and that the prior is borrowed.
- No history at all, first search → say so. An uncalibrated estimate labelled as uncalibrated is useful. One presented as calibrated is not.

### 3b. Role reality research — required

The posting describes the role the company wants to fill. It does not always describe what the team does.

Run two or three targeted searches: `"{Company} {Team}" what they do`, other postings from the same team (they leak org structure), and any engineering blog or talk from that team.

Answer four questions:

1. **Who are the customers?** External clients, internal teams, or both?
2. **Where in the value chain?** Research, product development, production, or post-sale delivery?
3. **What is the operating environment?** Offices, labs, data centers, production floors, customer sites?
4. **What creates the pressure?** Contract deadlines, launch dates, compliance, sales cycles?

This changes scores materially. "Data center operations" can mean customer-facing production management or internal research lab infrastructure. Those are different jobs with different pools, and the posting frequently does not distinguish them.

Budget five to ten minutes. If the search reveals nothing beyond the posting, write "no additional context found" and move on.

### 3c. Week in the life — required

Write three to five sentences describing what this person actually does in a normal week. Cadence, stakeholders, deliverables, and what breaks when they do the job badly.

This has teeth. If the week describes operating rhythms the candidate has never lived, that divergence reduces the pool position in 3h. It is an input to the score, not a section of the report.

If you cannot write it, you do not understand the role well enough to score it, and a score built on a misunderstanding is worse than no score because it looks the same as a good one.

### 3d. Pool estimation — required

This replaces keyword match as the primary signal.

Estimate, inline — a full pool-analyst agent dispatch is reserved for `/slushpile:adversarial-review` on finished materials:

1. **Volume.** Roughly how many applications per week?
2. **Median (p50).** Title history, years, recent employers, signature artifacts, credentials.
3. **Strong (p75).** Same dimensions, one tier up.
4. **Rare-strong (p90).** The candidates a hiring manager would be embarrassed to pass on.

**Priors by company type.** Starting points. Adjust for the specific role and say what you adjusted.

| Company type | Volume/wk | Pool character |
|---|---|---|
| Frontier AI lab | 80-200 | Deep, and self-selected. p50 is already ex-big-tech. Public technical work is common rather than rare. |
| Hyperscaler | 100-300 | Very deep, heavily credentialed. Pedigree filters are real. p75 has shipped at comparable scale. |
| Public mid-cap tech | 40-150 | Moderate depth. Engineering background weighs more than at hyperscalers. |
| Growth-stage startup | 20-80 | Shallower at p90. Breadth and shipping speed beat specialization. Referrals dominate. |
| Defense and aerospace | 40-120 | Clearance and program experience gate before anything else. Different pool entirely. |
| Regulated industry, non-tech | 15-60 | Shallowest pools. Domain and compliance experience outrank general technical strength. |
| Government and public sector | 20-100 | Credential-driven. Delivery history under public contract is the differentiator. |

Then **locate the candidate**. For each claimed differentiator in `preferences.yaml`:

- Is it rare *in this pool*, or median?
- What percentile does it place them in, relative to this pool?
- What would the p75 applicant claim instead?

Output an estimated **pool position** percentile.

The calibration that matters: a differentiator can be rare in absolute terms and median in a pool of people who self-selected into applying for this exact role. Ten years in a specialized manufacturing domain is rare on Earth, median for a hyperscaler manufacturing role where the pool is ex-contract-manufacturer at consumer scale, and p75+ for a defense role where that exact experience is the gate. Same fact, three answers, and only the pool question distinguishes them.

### 3e. Risk factors — not blockers

These reduce the score. They do not auto-pass. Whether any of them is a hard blocker is set in `preferences.yaml`, and by default none of them are.

- **Clearance requirement.** Note as a gap for the cover letter. Roughly 5-10 percentile points. Auto-pass only if `clearance.hard_blocker` is true.
- **Degree requirement**, even without "or equivalent". Same treatment. Auto-pass only if `education.degree_requirement_is_hard_blocker` is true.
- **Years-in-domain minimums.** Assess whether the pattern transfers. NOT MET only when no meaningful analog exists.
- **Location.** Check against `relocation`. Only a blocker if it falls in `excluded_regions` or the user is not willing to relocate.

The defaults here are deliberate: postings routinely list a clearance or a degree that the hiring manager does not enforce, and treating them as blockers silently removes roles the user would have gotten.

### 3f. Minimum qualifications

Rate each: **MET** (direct experience clearly demonstrates it), **PARTIAL** (related experience covering the pattern but not the domain), **NOT MET** (nothing to claim).

Count partials carefully. One is usually workable. Two or more raises rejection risk sharply at the screen.

Distinguish three kinds of gap, because they are not equally bridgeable:

- **Delivery pattern** — what they ran, coordinated, or shipped. Usually transfers across domains.
- **Domain vocabulary** — specific tools, standards, industry terms. Learnable, and weighs least.
- **Credential** — exact title, years in exact role, specific certification. Hardest to bridge and the most likely to gate.

"Experience managing ML programs" is PARTIAL for someone who ran AI pipeline delivery under another title.

### 3g. Preferred qualifications

Same rating. These shape the narrative angle. They do not gate.

### 3h. Pool-anchored fit score

| Pool position | Tier | Meaning |
|---|---|---|
| p75+ | **Tier 1** | Above the strong-applicant bar for this specific role |
| p55-p74 | **Tier 2** | Competitive, not differentiated. Needs a channel advantage. |
| p35-p54 | **Tier 3** | Below median. Pursue only through a strong channel. |
| below p35 | **Pass** | The pool outclasses the candidate. Cold submission is a wasted slot. |

Inputs, in priority order:

1. **Minimum qualification match.** Two or more NOT MET on critical quals drops the position one to two tiers regardless of everything else.
2. **Pool comparison.** Does the strongest claim actually rank here, or is it median?
3. **Week-in-the-life divergence.** Operating rhythms never lived reduce the position.
4. **Risk factors.** Roughly 5-10 percentile points each.
5. **Calibration prior.** Company conversion below 5% caps the position at p55 absent a specific reason this role differs.

**Record the pool percentile as the canonical fit number.** If you also want the keyword match, put it in a separate field. Collapsing them is the failure this whole rubric exists to prevent.

When passing, **name the single primary blocker.** If you cannot name one that independently justifies a pass, the role deserves a score instead.

### 3i. Channel EV matrix — required for every Tier 1-3 role

| Channel | Tier | Gate | Estimated screen pass |
|---|---|---|---|
| Cold submission | | none | 5-15%, varies with pool position |
| Warm referral | | a referrer must exist | 25-50%, pool-dependent |
| Cold outreach to a named employee | | an identifiable target | 5-15% |
| Inbound from public work | | an existing artifact, seeded | 20-40% if it lands |
| Recruiter inbound | | out of the candidate's control | n/a |

Use the user's own history from `job_search.md` where it exists. An empirical warm-referral rate at this company beats any prior.

**The role's tier is the highest tier across *available* channels.** Record which channel unlocks it and what gate must be cleared.

If no referrer currently exists, the warm-referral row is **informational only**. It does not unlock Tier 1. Inflating the tier by leaning on an unavailable channel is the most common way this matrix gets gamed, and it is self-inflicted.

### 3j. Kill criteria — required, auto-pass at scan time

Every one of these comes from `preferences.yaml`. Nothing is hardcoded.

**Hard kills. Mark the role passed, name the trigger, skip scoring.**

1. **Compensation floor.** Apply whatever method `compensation.method` specifies.
   - `nominal` — total compensation below `nominal.floor` kills the role.
   - `net_qol` — compute `net_qol = after_tax(total_comp) − annual_housing(where they would live) − healthcare_haircut`, then `delta = net_qol − current_baseline`. Below `minimum_delta` kills. Between `minimum_delta` and `comfortable_delta`, proceed with a `tight_band` flag. At or above `strong_delta`, flag `strong_comp`. In a `homecoming_corridor`, the threshold relaxes to `homecoming_minimum_delta`.
   - `none` — skip this check.

   Use total compensation, not base alone. If only base is posted, use base and note equity as upside. Estimate housing for where the candidate would **live**, not the office address — for a remote role that is their choice of location, and it frequently decides the outcome.

   For `net_qol`, do the arithmetic and show it. A one-line calculation in the role analysis is what makes this auditable later. Falling back to comparing nominal base is the failure this method exists to prevent, and it is invisible unless the arithmetic is written down.

2. **Extraction backstop.** During extraction there is no research budget for full compensation math. Quick-kill only on a posted maximum so far below the floor that no location clears it. Everything else proceeds to full assessment. A per-metro floor applied at extraction time wrongly kills roles that would have cleared — a nominally lower offer in a cheap metro often nets more than a higher one in an expensive metro, and that is the entire reason `net_qol` exists.

3. **Role closed.** A 404, a redirect to a different requisition, or a "no longer accepting applications" banner.

4. **Location excluded.** In `relocation.excluded_regions`, or requires relocation the user has ruled out.

5. **Function structurally wrong.** Genuinely different profession, not merely a different title. Check `targeting.functions` and read the responsibilities before concluding this.

6. **Company excluded.** In `targeting.excluded_companies` or the Excluded table in `companies.md`.

7. **Active cooldown.** Applied to this company within `application_policy.reapplication_cooldown_days`. Check `job_search.md`.

8. **Hard requirement violated.** Any entry in `constraints.hard_requirements` that the posting contradicts. Travel above `max_travel_percent`. A start date before `earliest_start`.

**Soft kills. Do not invest narrative effort. Bottom of Tier 3.**

- Two or more NOT MET minimum quals where the gap is credential rather than delivery pattern
- Pool position below p25
- Company conversion below 2% empirically, with no warm channel available

A soft kill means the expected value is low. **It is not an instruction to a downstream skill.** Record the finding; never write a prohibition into the role analysis. See Anti-Pattern 8.

Hard kills go to the search report's Passed table with the trigger named. They get no folder.

### 3k. Narrative angle

For every viable role, draft two or three sentences that lead with the strongest match, reframe the primary gap rather than ignoring it, and connect to a differentiator that **3d confirmed is actually rare here**.

If 3d found the claimed differentiator is median for this pool, the narrative cannot lean on it. Reach for one that is genuinely rare, or accept that the angle is weaker than hoped and say so.

### 3l. Domain precision

When claiming domain overlap, be precise about what transfers.

**Usually transfers:** delivery patterns, program structure, vendor management, cross-functional coordination, quality systems, delivery under compliance constraint, multi-stakeholder customer management.

**Usually does not transfer:** industry-specific tooling vocabulary, industry-specific standards and certifications, the operational particulars of a different production environment.

Claim "delivery pattern overlap", not "domain nativeness", unless the target's context is genuinely analogous. A hiring manager in the domain spots an overclaim in one line, and it costs more than the claim was worth.

## Phase 4: Output

### 4a. Search report — required for every search

Write to `searches/{YYYY-MM-DD}/{company-slug}_search.md`.

```markdown
# {Company} — Job Board Search

**Date:** {YYYY-MM-DD}
**Keywords:** {what was searched}
**Board:** {URL} ({platform}, {server-rendered | SPA})
**Results scanned:** {n} · **Assessed:** {n} · **Folders created:** {n}

## Company Context
{What they do, size, stage, hiring posture, anything from 3b that applies company-wide.}

## Calibration Prior
{Historical conversion at this company, or the borrowed peer prior and which peer.}

## Function Coverage
{Which target functions exist here at all. A function's absence is a
point-in-time observation — say so, and give a recheck trigger.}

## Tier 1 — Recommended
| Role | Req | Location | Pool position | Unlocking channel | Primary strength |

## Tier 2 — Assessed, Lower Priority
| Role | Req | Location | Pool position | Unlocking channel | Primary gap |

## Passed
| Role | Req | Primary blocker |

## Not Investigated
| Role | Why not |

## Company Verdict
{Worth pursuing? Through what channel? What would change the answer?}

## Strategic Notes
{Referral paths, timing, application limits, cooldowns, anything to remember
next time.}
```

### 4b. Role folders

For every role scoring Tier 1-3 with no hard kill:

```
applications/{Company}/{Function}/{Role-Slug}/
├── job_description.md      from templates/job_description.md
├── role_analysis.md        from templates/role_analysis.md
├── application.yaml        from templates/application.yaml
└── assessment_history.md   only if the assessment was revised — see below
```

Fill `application.yaml`'s `fit`, `channel_ev`, `kill_criteria`, and `calibration_prior` blocks. Leave `adversarial_review` empty — `/slushpile:adversarial-review` owns it.

**`assessment_history.md` is created only when the assessment changed** — a contrarian net call other than STAND, a user correction, or a materially revised score. A first-pass assessment that stands has no history worth keeping, and an empty history file in every folder trains the reader to skip the ones that have something in them.

It is a separate file rather than a section of `role_analysis.md` for a mechanical reason: `application-builder` and all seven review agents read the role analysis in full and treat every value in it as current. Two numbers for the same field, with no instruction about which is live, does not reliably resolve to the later one.

### 4c. Update the tracker

Add every assessed role to `job_search.md` under Active Applications or Assessed-Not-Applied.

### 4d. Update `companies.md`

Add the company to the right table. This is what makes "have I already looked at these people?" answerable in five seconds six months from now.

## Phase 5: Contrarian Gate

**This runs before the tier tables are written.** A contrarian whose findings are appended after the tables are published becomes commentary, and the upstream over-grading survives intact — which is the same as not running it.

### 5a. Run it

After all role analyses are drafted, dispatch `slushpile-contrarian`:

```
Read these draft role analyses: {paths}

Challenge each pool-anchored fit assessment.

Pool estimation:
- Is the p75 archetype realistic, or deflated to flatter the candidate?
- Are the claimed differentiators actually rare in this pool, or median?
- Was the right peer set used to characterize the pool?

Tier assignment:
- Was the channel matrix gamed by listing a warm referral when no referrer exists?
- Is the cold-submission tier honest, or inflated by an unavailable channel?
- Does the calibration prior support the assigned tier?

Kill criteria:
- Was a soft-kill condition ignored?
- Was the compensation method in preferences.yaml actually applied, with the
  arithmetic shown, or did the assessment fall back to comparing nominal base?
- Was cooldown checked against job_search.md?

Narrative angle:
- Does it lean on a differentiator the pool comparison flagged as median?
- Is "delivery pattern overlap" claimed where real domain depth is required?

Per role, produce a net call:
  STAND | DOWNGRADE_ONE_TIER | DOWNGRADE_TO_PASS | UPGRADE_ONE_TIER

Format as a table: | Role | Net call | Primary reason |
Then a 2-3 sentence rationale for every non-STAND call.
```

### 5b. Apply the calls

- **STAND** — no change. Record it.
- **DOWNGRADE_ONE_TIER** — adjust the tier and rewrite the affected sections of `role_analysis.md` **to the new values**.
- **DOWNGRADE_TO_PASS** — set status to `passed_after_contrarian`, move the role to the Passed table, keep the folder for the audit trail.
- **UPGRADE_ONE_TIER** — only when the case is concrete, such as a named peer comparator the analysis missed. Rare.

**Route the three kinds of output to three different places.** This is what keeps `role_analysis.md` usable by the skills downstream.

| Content | Destination |
|---|---|
| Corrected values — scores, tiers, comp, quals, angle | **`role_analysis.md`**, edited in place, as the current fact. No marker, no strikethrough, no "was X". |
| What was wrong and why, and which findings were struck | **`assessment_history.md`**, from `templates/assessment_history.md` |
| Net call, structured | **`application.yaml`** |
| Company-level gate narrative | **The search report** |

The Contrarian Review section of `role_analysis.md` gets a provenance stamp and nothing else: the date, the net call, and a pointer to `assessment_history.md`. Not a changelog.

**Record the struck findings, not only the adopted ones.** A gate that logs only what it changed cannot be audited for over-reach, and the struck legs are the data that makes the gate better across applications — invisible if you record outcomes alone.

**Never append corrections to a role analysis.** Rewrite the section. If the file still contains "corrected", "re-scored", "superseded", "previously", or an arrow between two numbers, it is not finished. `application-builder` and every review agent read this file and treat everything in it as a live finding — give a downstream reader three numbers and no instruction and it will not reliably pick the last one.

### 5c. Finalize

Only now write the tier tables. They reflect post-contrarian decisions.

**Searching several companies in sequence:** run Phases 1-4 for all of them, accumulate the drafts, run one contrarian batch, apply across all companies, then finalize every report.

## Phase 6: Report

Show the user: how many roles were scanned, assessed, and foldered; the Tier 1 list with pool positions and unlocking channels; anything killed and why; the company verdict; and the single next action.

## Anti-Patterns

1. **Do not run browser navigation in parallel agents.** The browser is a singleton. Concurrent agents clobber each other.
2. **Do not fetch every result.** Triage from the first twenty to forty titles.
3. **Do not assess a role inside its cooldown.** Check `job_search.md` first.
4. **Do not spend a referral on a Tier 2 role** while a Tier 1 exists.
5. **Do not treat clearance or degree requirements as hard blockers** unless `preferences.yaml` says so.
6. **Do not declare a company-wide blocker without reading postings.** Read the two or three most promising before concluding nothing fits. A company being in a regulated industry does not mean every role requires domain expertise.
7. **Do not stack weak reasons to justify a pass.** Name one primary blocker that independently justifies it, or score the role instead.
8. **Do not write a prohibition into `role_analysis.md`.** A soft kill means expected value is low. Written as "do not build materials for this role", it becomes a standing order to `application-builder`, which will refuse to run on that folder later — when the tier-time judgment may no longer hold. Findings describe the role. They do not issue orders to other skills.
9. **Do not put revision history in `role_analysis.md`.** Apply findings as values there; record them in `assessment_history.md`. A role analysis containing an arrow between two scores is not finished.
10. **Do not grade against the posting when you should be grading against the pool.** If you are writing a fit score and have not estimated p50, p75, and p90, you skipped 3d.
11. **Do not inflate the cold tier using an unavailable channel.** The tier is the highest across *available* channels.
12. **Do not write tier tables before the contrarian gate.** Phase 5 is a gate.
13. **Do not skip the calibration ingest.** Scoring without it is scoring blind to the user's own conversion history, which is the only data in the system that is actually about them.
14. **Do not skip the compensation check, and do not shortcut it to nominal base.** Both directions fail: a role scored Tier 2 on fit that barely beats the candidate's current life, and a good role killed on a nominal number in a cheap metro. Do the arithmetic the method calls for and write it down.
15. **Do not overclaim domain overlap.** Say "delivery pattern overlap", not "domain nativeness".
16. **Do not let a query silently override `preferences.yaml`.** A query adds constraints. It does not withdraw the ones already on file, and a list built as though it did looks correct while containing roles the user ruled out months ago.
17. **Do not start Phase 1 in query mode without the user confirming the company list.** Everything expensive is downstream of that list, and it is the one artifact only the user can check.
18. **Do not report a capped or filtered company list as the market.** Name what was cut and why. "Thirteen companies" and "thirteen companies, nine cut for cooldown" describe very different searches and read identically.
