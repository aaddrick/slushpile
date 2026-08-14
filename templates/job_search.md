# Job Search

<!--
The running tracker. Every skill in the pipeline reads and updates it.

Keep it in one file. A tracker split across a spreadsheet, a notes app, and
your memory is a tracker that no agent can read, which means every assessment
starts from zero and your own history never calibrates anything.
-->

**Started:** {{YYYY-MM-DD}}
**Last updated:** {{YYYY-MM-DD}}

## Current Posture

<!-- Active, passive, or paused. What you are targeting right now, and any
change from last month. Search targets drift, and an assessment run against a
stale target is worse than no assessment. -->

## Constraints

<!-- The narrative version of the hard constraints in preferences.yaml.
Anything that changed recently, with the date it changed. -->

## Referrals and Warm Channels

<!-- Who you know where, how strong the relationship actually is, and whether
you have used it. This is the single highest-leverage section in the file:
warm referral converts at roughly five to ten times cold submission in most
pools, and the pipeline can only route to a channel it knows exists.

`/slushpile:outreach` writes rows here and you can add your own at any time.
Every review of every role at a company reads this section to decide whether
the warm-referral channel is available, so an empty row is not neutral: it
prices that channel as closed.

Relationship strength is one of `strong`, `moderate`, `weak`, or `none`, and
the difference is what the person could actually say about your work rather
than how much you like them. Only `strong` and `moderate` are referrals.
Status is one of `not asked`, `asked YYYY-MM-DD`, `agreed`, `declined`, or
`used YYYY-MM-DD`. -->

| Company | Contact | Relationship strength | Status | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Cooldowns

<!-- Companies you applied to recently and should not re-approach yet.
Cooldown length comes from preferences.yaml. -->

| Company | Last applied | Outcome | Eligible again |
|---|---|---|---|
|  |  |  |  |

## Active Applications

| Company | Role | Applied | Channel | Status | Last movement |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Assessed, Not Applied

| Company | Role | Tier | Why not applied | Revisit? |
|---|---|---|---|---|
|  |  |  |  |  |

## Closed

| Company | Role | Applied | Outcome | Stage reached | Days to response |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Calibration

<!-- The regression of the pipeline's predictions against reality. Update
after every batch of applications resolves.

Without this, the pipeline runs blind to its own track record. A pipeline that
grades most applications INTERVIEW and converts 5% is not producing signal, it
is producing optimism, and it will keep doing so indefinitely unless something
checks it. -->

| Predicted verdict | Applications | Got a response | Got an interview | Actual rate |
|---|---|---|---|---|
| INTERVIEW |  |  |  |  |
| MAYBE |  |  |  |  |
| REJECT |  |  |  |  |

**By channel:**

| Channel | Sent | Interviews | Actual rate | Pipeline's estimate |
|---|---|---|---|---|
| Cold submission |  |  |  |  |
| Warm referral |  |  |  |  |
| Cold outreach |  |  |  |  |

**Drift notes:**

<!-- Where the pipeline is systematically wrong, and in which direction.
Feed these back into the priors. -->

## Lessons

<!-- Dated. What you learned, from what. Most useful when it contradicts
something the pipeline told you. -->
