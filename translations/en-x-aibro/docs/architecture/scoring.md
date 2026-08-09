# Scoring

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <a href="../../../../docs/architecture/scoring.md">English</a> ·
  <a href="../../../zh-CN/docs/architecture/scoring.md">简体中文</a> ·
  <a href="../../../es/docs/architecture/scoring.md">Español</a> ·
  <a href="../../../pt-BR/docs/architecture/scoring.md">Português (BR)</a> ·
  <a href="../../../vi/docs/architecture/scoring.md">Tiếng Việt</a> ·
  <strong>AI Bro</strong>
</p>

<!-- END GENERATED language-nav -->

Every number this pipeline emits answers one of two questions.

Where does the candidate sit in the queue for this specific role, and what is an
application through a given channel actually worth.

Nothing here scores a document against a posting in isolation. That is a real
number about the wrong variable, and the entire category ships it as the
headline.

## Pool anchoring

A keyword match score compares a resume to a job description.

Nobody is hired by a job description.

The comparison that decides the outcome is against the other applicants in the
queue, and a match score has no representation of them anywhere in its state. It
is not underfit. It is not modeling the problem.

So the search stage estimates the pool first. Who else applies to this
requisition, and what do the p50, p75 and p90 applicants look like. Then it
locates the candidate in that distribution, and **the pool percentile is recorded
as the canonical fit number.** Keyword match, if anybody wants it, goes in a
separate field. Collapsing the two is the exact failure the rubric exists to
prevent.

| Pool position | Tier | Meaning |
| --- | --- | --- |
| p75+ | Tier 1 | Above the strong-applicant bar for this specific role |
| p55–p74 | Tier 2 | Competitive, not differentiated. Needs a channel advantage. |
| p35–p54 | Tier 3 | Below median. Pursue only through a strong channel. |
| below p35 | Pass | The pool outclasses the candidate. A cold submission is a wasted slot. |

The inputs are ordered, and the order is the model. Two or more unmet critical
minimums drop the position one to two tiers regardless of everything else. Then
the pool comparison: does the strongest claim actually rank here, or is it median?
Then divergence from the role's real operating rhythm. Then risk factors at
roughly five to ten percentile points each. Then the calibration prior for the
company.

The single most valuable output of this stage is a claimed differentiator coming
back marked pool-median.

That is information you cannot buy from a document scanner at any price, and it is
usually the thing that changes what you write. It is also the thing nobody wants
to hear, which is why nobody else ships it.

## Channel-conditional verdicts

Same materials. Wildly different conversion depending on how they arrive. A single
verdict averages over that and then reports the average as a fact about the
application.

Every Tier 1–3 role gets a matrix instead:

| Channel | Gate | Rough screen-pass range |
| --- | --- | --- |
| Cold submission | none | 5–15%, varies with pool position |
| Warm referral | a referrer must exist | 25–50%, pool-dependent |
| Cold outreach to a named employee | an identifiable target | 5–15% |
| Inbound from public work | an existing artifact, seeded | 20–40% if it lands |
| Recruiter inbound | outside the candidate's control | not estimated |

Two rules keep that from being decorative.

**Tier is the highest tier across *available* channels.** The matrix records which
channel unlocks it and what gate has to clear. No referrer today means the
warm-referral row is informational and does not unlock Tier 1. Inflating a tier by
leaning on an unavailable channel is the most common way this gets gamed, and the
person gaming it is you, against yourself, for free.

**Your history beats any prior.** Where `job_search.md` records a real
warm-referral rate at this company, that number replaces the generic one. Your
data outranks the shipped defaults the moment there is enough of it. See
[memory-and-calibration.md](memory-and-calibration.md).

## Materials quality is not expected value

Two numbers, reported independently, because they disagree constantly.

Excellent materials into a wrong-fit role: low EV. Adequate materials through a
referral into a well-fit role: high EV.

Collapse them and the tool tells you to spend another hour editing when the honest
recommendation is to spend that hour finding a referrer. A materials score of 8/10
next to a 1–3% cold conversion is not a contradiction to resolve.

It is the entire finding.

## Kill criteria

Run at scan time, checked against `preferences.yaml`: compensation, location,
clearance, and whatever else the user recorded as a constraint.

Two properties matter more than the list.

**Passes are stated, not only failures.** A check that reports only what failed is
indistinguishable from a check that did not run. No interpreter here to prove
otherwise.

**A pass names its single primary blocker.** If no one blocker independently
justifies passing, the role gets a score instead of a pass. A pass justified by an
accumulation of small doubts is a mood, and it will not survive your own
re-reading a week later.

Compensation is assessed on the **posted band**, using the method in
`preferences.yaml`. Offer-stage terms are out of scope here for the same reason
they are struck in the review: see
[the-review.md](the-review.md#the-gatekeeper).

## Ranges, not verdict words

Output is "1–3% interview", not "MAYBE".

A range carries its own uncertainty and can be scored against what happened. A
verdict word carries neither and cannot be scored at all.

That is also what makes the calibration loop possible. You cannot regress "MAYBE"
against outcomes. You can regress a percentage, and
[memory-and-calibration.md](memory-and-calibration.md) is where that runs.

Unmeasurable output is not a softer answer. It is an answer that has opted out of
ever being wrong.
