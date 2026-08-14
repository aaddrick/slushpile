# Role Analysis: {{Short Role Title}} — {{Company}}

**Assessed:** {{YYYY-MM-DD}}
**Fit:** pool position p{{N}} · **Tier {{N}}** via {{channel}}
**Kill criteria:** {{none | which one triggered}}

<!--
Written by `/slushpile:job-board-search`, extended by
`/slushpile:application-builder` and `/slushpile:adversarial-review`.

The header line is deliberately channel-conditional. "Tier 2" alone is not a
finding. "Tier 2 via warm referral, Tier 4 cold" is.
-->

## Calibration Prior

<!-- What your own application history predicts here, before any analysis of
this specific role. How many similar roles you have applied to, at what tier,
and what actually happened. If this is your first application at this company
tier, say so — an uncalibrated estimate should be labelled as one. -->

## Role Reality

<!-- What this job actually is, as opposed to what the posting says it is.
Postings are written by recruiters from a hiring manager's intake form and
drift toward the aspirational. What does the person in this seat do on a
Tuesday? Which of the listed responsibilities is 80% of the work? -->

## Week in the Life

<!-- Concretely: how this person spends five days. Written out. If you cannot
write it, you do not understand the role well enough to score it, and a fit
score built on a misunderstanding is worse than no score. -->

## Pool Estimation

**Estimated volume:** {{applications per week}}

| Percentile | Profile |
|---|---|
| Median (p50) |  |
| Strong (p75) |  |
| Rare-strong (p90) |  |

**Your position:** p{{N}}

**Differentiators — and whether they are actually rare in *this* pool:**

| Claimed differentiator | Absolute impressiveness | Percentile in this pool | Net |
|---|---|---|---|
|  |  |  |  |

**Filter exposure:**

<!-- Title-keyword ranking, years-of-experience dropdowns, degree parsing,
recency, pedigree. Probability of clearing each. -->

## Minimum Qualifications Match

| Requirement | MET / NOT MET / UNCLEAR | Evidence |
|---|---|---|
|  |  |  |

## Preferred Qualifications Match

| Requirement | MET / NOT MET / UNCLEAR | Evidence |
|---|---|---|
|  |  |  |

## Channel EV Matrix

| Channel | P(interview) | Verdict | What would have to be true |
|---|---|---|---|
| Cold submission |  |  |  |
| Warm referral |  |  |  |
| Cold outreach |  |  |  |
| Recruiter inbound |  |  |  |
| Public-visibility inbound |  |  |  |

**Highest-EV channel:** {{name}}

## Strengths

## Gaps

<!-- Honest. These do not go in the cover letter. They exist so the scoring is
real and so `/slushpile:explore-experience` knows where to dig. -->

## Risk Factors

<!-- Things that could sink this but are not disqualifying: clearance,
degree, relocation, level mismatch, gap in employment. Each with how you
would handle it if raised.

If sponsorship is needed and the posting says nothing either way, it belongs
here rather than in the kill check — as the question the form is going to ask,
so it is answered before the portal asks it and not during. -->


## Kill Criteria Check

<!-- Each hard constraint from preferences.yaml, checked. State the ones that
passed, not only the ones that failed — a kill check that only reports
failures is indistinguishable from one that did not run. -->

## Narrative Angle

<!-- One sentence. The argument for you in this seat, specific enough that it
breaks if you swap the company name. This becomes the cover letter thesis. -->

## Recommendation

<!-- Apply / apply via a specific channel only / hold for a referral / pass.
With the honest expected outcome and the reason to submit. -->

---

## Contrarian Review

<!-- A provenance stamp, not a changelog. That the gate ran, when, the net
call, and a pointer. The findings themselves — what was adopted, what was
struck, and the values they replaced — go in `assessment_history.md`.

Corrected values are applied above as current fact. They are not recorded
twice, and they are never written here as "was X, now Y". -->

**Gate run:** {{YYYY-MM-DD}}
**Net call:** {{SUBMIT | SUBMIT_AS_PORTFOLIO_ONLY | DO_NOT_SUBMIT}}
**Findings and struck legs:** `assessment_history.md`

---

## Adversarial Review — Round {{N}}

**Run:** {{YYYY-MM-DD}}

| Agent | Read |
|---|---|
| Triage screener |  |
| Requirements analyst |  |
| ATS simulator |  |
| Fatigued reader |  |
| Pool analyst |  |
| Hiring manager |  |
| Contrarian |  |

**Swap tests:** company {{PASS/FAIL}} · name {{PASS/FAIL}} · JD {{PASS/FAIL}}

**Materials quality:** {{N}}/10
**ATS score:** {{N}}/100

**Key quotes:**

**What changed after this round:**

<!--
No revision history below this line, and none above it either.

Every value in this file is the current one. Score trajectory, contrarian
findings, user corrections, and lifted instructions live in
`assessment_history.md`, which nothing downstream reads.

The reason is mechanical: `application-builder` and all seven review agents
read this file in full and treat everything in it as a live finding. Two
numbers for the same field, with no instruction about which is current, does
not reliably resolve to the later one.

If this file contains "corrected", "re-scored", "superseded", "previously", or
an arrow between two numbers, it is not finished.
-->
