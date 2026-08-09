# Scoring

<!-- BEGIN GENERATED language-nav: scripts/sync_docs.py -->

<p align="center">
  <strong>English</strong> ·
  <a href="../../translations/zh-CN/docs/architecture/scoring.md">简体中文</a> ·
  <a href="../../translations/es/docs/architecture/scoring.md">Español</a> ·
  <a href="../../translations/pt-BR/docs/architecture/scoring.md">Português (BR)</a> ·
  <a href="../../translations/vi/docs/architecture/scoring.md">Tiếng Việt</a> ·
  <a href="../../translations/en-x-aibro/docs/architecture/scoring.md">AI Bro</a>
</p>

<!-- END GENERATED language-nav -->

Every number this pipeline produces is an answer to one of two questions: where
does the candidate sit in the queue for this specific role, and what is an
application through a given channel actually worth. Nothing here scores a
document against a posting in isolation, because that is a real number about the
wrong question.

## Pool anchoring

A keyword match score compares a resume to a job description. Nobody is hired by
a job description. The comparison that decides the outcome is against the other
applicants in the queue, and a match score cannot see them.

So the search stage estimates the pool first: who else applies to this
requisition, and what do the median, 75th-percentile, and 90th-percentile
applicants look like. The candidate is then located in that distribution, and
**the pool percentile is recorded as the canonical fit number.** Keyword match,
if it is wanted at all, goes in a separate field. Collapsing them is the exact
failure the rubric exists to prevent.

| Pool position | Tier | Meaning |
| --- | --- | --- |
| p75+ | Tier 1 | Above the strong-applicant bar for this specific role |
| p55–p74 | Tier 2 | Competitive, not differentiated. Needs a channel advantage. |
| p35–p54 | Tier 3 | Below median. Pursue only through a strong channel. |
| below p35 | Pass | The pool outclasses the candidate. A cold submission is a wasted slot. |

The inputs are ordered. Two or more unmet critical minimum qualifications drop
the position one to two tiers regardless of everything else. Then the pool
comparison: does the strongest claim actually rank here, or is it median? Then
divergence from the role's real operating rhythm, then risk factors at roughly
five to ten percentile points each, then the calibration prior for the company.

The most useful output of this stage is a claimed differentiator coming back
marked pool-median. That is information the candidate cannot get from a document
scanner, and it is usually the thing that changes what they write.

## Channel-conditional verdicts

The same materials convert at very different rates depending on how they arrive.
A single verdict averages over that difference and reports the average as though
it were a fact about the application.

Every Tier 1–3 role therefore gets a matrix rather than a verdict:

| Channel | Gate | Rough screen-pass range |
| --- | --- | --- |
| Cold submission | none | 5–15%, varies with pool position |
| Warm referral | a referrer must exist | 25–50%, pool-dependent |
| Cold outreach to a named employee | an identifiable target | 5–15% |
| Inbound from public work | an existing artifact, seeded | 20–40% if it lands |
| Recruiter inbound | outside the candidate's control | not estimated |

Two rules keep this from being decorative.

**The role's tier is the highest tier across *available* channels**, and the
matrix records which channel unlocks it and what gate has to be cleared. If no
referrer currently exists, the warm-referral row is informational only and does
not unlock Tier 1. Inflating a tier by leaning on an unavailable channel is the
most common way this matrix gets gamed, and it is self-inflicted.

**The user's own history beats any prior.** Where `job_search.md` records a real
warm-referral rate at this company, that number is used instead of the generic
one. See [memory-and-calibration.md](memory-and-calibration.md).

## Materials quality is not expected value

The review reports these as two separate numbers because they routinely
disagree. Excellent materials sent to a wrong-fit role still have low expected
value; adequate materials sent through a referral to a well-fit role have high
expected value.

Collapsing them tells the user to spend another hour editing when the honest
recommendation is to spend that hour finding a referrer. A materials score of
8/10 next to a 1–3% cold conversion is not a contradiction — it is the whole
finding.

## Kill criteria

Kill criteria run at scan time and are checked against `preferences.yaml`:
compensation, location, clearance, and whatever else the user recorded as a
constraint.

Two properties matter more than the list itself.

**Passes are stated, not only failures.** A check that reports only what failed
is indistinguishable from a check that did not run, and there is no interpreter
here to prove it ran.

**A pass names its single primary blocker.** If no one blocker independently
justifies passing on the role, the role gets a score instead of a pass. A pass
justified by an accumulation of small doubts is a mood, and it will not survive
the user's own re-reading a week later.

Compensation is assessed on the **posted band**, using the method recorded in
`preferences.yaml`. Offer-stage terms are explicitly out of scope here for the
same reason they are struck in the review: see
[the-review.md](the-review.md#the-gatekeeper).

## Probability ranges, not verdict words

Output is "1–3% interview" rather than "MAYBE". A range carries its own
uncertainty and can be checked against what actually happened; a verdict word
carries neither and cannot.

This is also what makes the calibration loop possible. "MAYBE" cannot be
regressed against outcomes. A percentage can, and
[memory-and-calibration.md](memory-and-calibration.md) is where that regression
happens.
