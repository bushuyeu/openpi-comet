# The radio probe

A test of one claim from *Openpi Comet* (arXiv:2512.10071v3).

## The claim

Figure 4 of the report gives a success rate of **1.00** for the task `turning_on_radio`. The report also uses this task for every cell of Table 3 and Table 4.

Figure 4 reports 25 tasks with a non-zero rate, out of 50. The spread:

| Success rate | Number of tasks |
|---|---|
| **1.00** | **8** (includes `turning_on_radio`) |
| 0.80 | 2 |
| 0.60, 0.50 | 1 each |
| 0.40, 0.30 | 2 each |
| 0.20 | 4 |
| 0.10 | 5 |
| 0.00 | 25 (not plotted) |

Table 2 gives the Q-scores for the whole benchmark.

| Stage | Q-score |
|---|---|
| Pre-training | 0.192 |
| Post-training | **0.345** |
| Theoretical best | 0.611 |

Figure 4 shows the post-training model at Q 0.345.

## Why this task

- The authors chose it. Their own ablations run on it.
- The claim is exact. A rate of 1.00 is easy to disprove.
- It is the shortest task in the benchmark. 934 frames is 31 seconds at 30 fps. The next shortest task is 2.5 times longer.

## Setup

| Item | Value |
|---|---|
| Machine | RTX 3090, 24 GB. A second run used an RTX 5090, 32 GB |
| Stack | BEHAVIOR-1K v3.7.2, Isaac Sim 4.5, numpy 1.26.4. torch 2.6.0+cu124 on the RTX 3090, torch 2.7.0+cu128 on the RTX 5090 |
| Policy | Released checkpoint `pi05-b1kpt50-cs32` |
| Control mode | Receding horizon, `max_len=32` |
| Resolution | Native. Head 720x720, wrist 480x480 |
| Instances | 20 public test instances |

The report used 10 instances. The public file supplies 20. We use all 20. This makes the confidence interval half as wide.

## Result

| Config | Report | n | Ours | 95% CI |
|---|---|---|---|---|
| Baseline, RTX 3090 | **1.00** | 20 | **0.00** | [0.00, 0.16] |
| Baseline, RTX 5090 | **1.00** | 20 | **0.00** | [0.00, 0.16] |

The policy failed every instance. Each episode ran to the step limit of 4300 steps. The partial-credit Q-score was 0.000 every time. The step limit is the default, which is two times the average human demo length.

A second machine gives the same result. The RTX 5090 run used the same policy, the same native resolution and the same 20 test instances. The card, the driver and the torch build differ. The simulator is the same version.

## Is the test harness good?

This is the first question to ask, because a broken harness also gives zero.

We ran the same policy on **training instances**. The policy saw this data during training, so it must do better here.

| Run | Instances | Runs | Successes | Rate per run | 95% CI |
|---|---|---|---|---|---|
| Train instances | 16 | 20 | 2 | 0.10 | [0.03, 0.30] |
| Test instances | 20 | 20 | 0 | 0.00 | [0.00, 0.16] |

The train set covers 16 instances in 20 runs. Four instances ran twice.

The harness can record a success. It is not dead. Both successes scored a full `q_score` of 1.000, not partial credit.

The two intervals overlap. At 20 instances each, we cannot show that the train rate differs from the test rate. The control proves the harness works. It does not prove a train and test gap.

A failed episode runs to the 4300-step cap. The two successful episodes stopped at 1329 and 1632 steps. The episode ends when the task is complete, so the harness detects completion.

## The same instance gives different results

Four training instances ran twice. Two of them changed outcome between runs.

| Instance | First run | Second run |
|---|---|---|
| 1 | 0.000 | **1.000** |
| 2 | 0.000 | 0.000 |
| 3 | 0.000 | 0.000 |
| 4 | **1.000** | 0.000 |

Both successes come from instances that failed on their other run. One run per instance is a noisy measurement.

This applies to the report as well. Figure 4 gives 1.00 from ten single runs. Table 3 and Table 4 give values that move in steps of 0.05 to 0.10. If a run can change outcome, those values carry more variance than the tables show.

## What went wrong first

The first run gave 0/20 at 224x224 resolution. That result was wrong, and the error was ours.

The released checkpoint needs native resolution. At 224x224 it scores zero even on training data. We changed the default wrapper to 224x224 to match Table 3. That was a mistake. The 224x224 numbers in Table 3 come from single-task models trained at that resolution. Those models are not public.

The positive control found this error. Without the control, we would have reported a false result about the authors' work.

The RTX 5090 run started at 224x224 and gave 0/20. It then gave 0/20 at native resolution as well. On the test instances both resolutions score zero, so that run cannot separate the two. The evidence that 224x224 zeroes the checkpoint comes from the train instances, not from the test instances.

## Three readings of 0/20

1. The claim does not reproduce.
2. The released checkpoint is not the model in Figure 4.
3. Our setup is still wrong in some way we did not find.

We checked reading 2. The evidence does not support it.

| Evidence | Points to |
|---|---|
| Checkpoint built 2025-12-30 | Between the Dec 06 release and the Jan 03 release of the Q 0.345 model |
| Model card text | "the latest model weights of Team Comet" |
| Directory name `pi05-b1kpt50-cs32` | Matches the pre-training config name |
| README model zoo text | "base VLA model checkpoints ... ideal for fine-tuning" |

The build date and the model card point to the Q 0.345 model. The directory name and the model-zoo text point to the pre-training model. The README calls the same files both things. We cannot settle this from the public record.

Reading 3 is limited by the control. The policy succeeds on training instances at native resolution. A dead harness cannot do that.

## What we cannot test

Table 3 row #4 compares the two resolutions.

| Image resolution | Report |
|---|---|
| Head 224, wrist 224 | 0.30 |
| Head 720, wrist 480 | **0.60** |

We cannot repeat this for two reasons.

1. The 224x224 models are not public.
2. At 10 instances the two intervals overlap. At 20 they still overlap. The comparison is not resolvable at either sample size.

## Setup problems found

Three faults block the documented path. Each one stops evaluation.

1. `base_config.yaml` points at `behavior.learning.wrappers.RGBWrapper`. After the install step in the README, the package is `omnigibson.learning`. Hydra raises `InstantiationException`.
2. `setup.sh` installs numpy 1.26.4. The `--joylo` dependencies then upgrade numpy to 2.x. This breaks the ABI, and `og.launch()` gives a segmentation fault.
3. `setup.sh` downloads the 2026 task instances. `eval_custom.py` reads the 2025 instances. Nothing downloads them.

Fixes for all three are in this fork.

## Hardware note

Isaac Sim needs RT Cores. The A100, H100 and V100 do not have them and cannot run this benchmark. An RTX 5090 has RT Cores and runs the benchmark. It needs torch 2.7.0+cu128, because the pinned cu124 build has no sm_120 kernels. It also needs a driver that the Kit build supports. We tested two. Driver 580.173.02 works. Driver 595.84 gives a segmentation fault in the Omniverse RTX renderer. See the [hardware page](compute.html).

## What we did not run

We stopped the control-mode arm of Table 3 after 1 instance. Table 3 row #1 gives 0.00 for temporal ensemble and 0.00 for receding temporal.

| Control mode | Report |
|---|---|
| Temporal ensemble | 0.00 |
| Receding temporal | 0.00 |
| Receding horizon | 0.25 |

We used the time for the positive control instead. The reason is that this policy gives 0.00 in every condition we tested. If the two control modes also give 0.00, they agree with the report, but the agreement means little. A policy that always fails matches every prediction of zero.

The control tells us something the arm cannot. It shows the harness can score above zero.
