# The RFT dataset

The report credits a task-balancing step for part of its score. The authors released the dataset that step produced. This page checks their claim against their own data. It needs no GPU.

The authors call it "our RFT dataset" in the repository README and link to it. The upload handle `delinqu` matches Delin Qu, a core contributor.

| Item | Value |
|---|---|
| Dataset | [`delinqu/comet-1.5k`](https://huggingface.co/datasets/delinqu/comet-1.5k) |
| Files read | `meta/episodes.jsonl`, `meta/info.json` |
| Episodes | 1469 |
| Tasks | 39 of 50 |

This is the artifact the method produced, not a reconstruction. Any claim about the balancing step must hold in it.

## The claim

| Stage | Q-score | Source |
|---|---|---|
| Pre-training | 0.192 | Table 2 |
| Post-training, at the challenge | 0.224 | Section 4.3 |
| Post-training, refined | **0.345** | Table 2 |
| Theoretical best | 0.611 | Table 2 |

The method runs 3 rounds. Each round makes about 8500 rollouts. It keeps 1469 trajectories from about 25,500.

A balancing step must make the kept set more even across tasks. This page tests that.

## The count matches

The dataset holds 1469 episodes. Section 4.3 gives the same number.

## Balancing caps the common tasks

Episodes kept per task, in order:

```
120 120 120 120 120 118 111 109 65 58 50 44 37 32 31 30 26 24 14
 12  11  11  10   9   8   8   8   7  7  6  6  4  4  2  2  2  1  1  1
```

Five tasks stop at exactly 120. Three more stop just below it. The step removes episodes from the common tasks. It adds none to the rare tasks.

| Measure | Value |
|---|---|
| Most to least | 120 to 1 |
| Share held by the top 5 tasks | 40.8% |
| Median task | 12 episodes |

The set is still uneven after the step.

## Short tasks supply most of the data

Spearman rank correlation between episodes kept and mean episode length: **-0.45**.

| Episodes kept | Tasks | Mean length |
|---|---|---|
| 100 or more | 8 | 7,457 frames (4.1 min) |
| 10 to 99 | 15 | 16,563 frames (9.2 min) |
| Fewer than 10 | 16 | 16,212 frames (9.0 min) |

The method takes most of its data from the short tasks. Section 5 of the report states that sampling efficiency is low. This number gives the size of that limit.

## Eleven tasks produced nothing

The dataset covers 39 tasks. The benchmark has 50. About 25,500 rollouts produced no kept episode for the other 11.

The method adds no data for the hardest tasks. It cannot raise the score on them. The gap to the theoretical best of 0.611 stays.

## The native resolution is 720 and 480

The dataset stores the head camera at 720x720. It stores each wrist camera at 480x480. Row #4 of Table 3 uses the same two settings.

| Image resolution | Report |
|---|---|
| Head 224, wrist 224 | 0.30 |
| Head 720, wrist 480 | **0.60** |

The 224x224 setting downsamples data that is native at 720 and 480. The gain in row #4 comes from keeping the native data.

## The frame count is stale

`info.json` gives `total_frames` as 12,226,350. The episode lengths in `episodes.jsonl` sum to 14,896,614. The difference is 2,670,264 frames, or 18%.

The count was probably not rebuilt after the last filter step. No result on this page depends on it.

## Summary

| Question | Answer |
|---|---|
| Does the balancing step make the set even? | No. It caps the common tasks at 120 and adds nothing to the rare ones |
| How uneven is the result? | 120 to 1. The top 5 tasks hold 40.8% of the data |
| What drives which tasks get data? | Episode length. Spearman -0.45 between episodes kept and mean length |
| How many tasks got nothing? | 11 of 50. About 25,500 rollouts produced no kept episode for them |
| Does this limit the method? | Yes. It adds no data for the hardest tasks, so it cannot raise the score on them |

The report credits task balancing. The data shows the step does little. The pattern in the data is a bias by episode length. The method collects where episodes are short and almost nothing where they are long.

For the measured claim about the released checkpoint, see the [experiment](index.html). For what hardware runs this benchmark, see the [hardware page](compute.html).
