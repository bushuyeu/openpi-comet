# The radio probe

*Openpi Comet* ([arXiv:2512.10071v3](https://arxiv.org/abs/2512.10071)) took second place in the 2025 BEHAVIOR Challenge. The team released the code, two checkpoints and their post-training dataset.

This page tests one claim from the report. Figure 4 gives a success rate of **1.00** for the task `turning_on_radio`. We pick that claim for three reasons.

- The authors chose the task. Every cell of Table 3 and Table 4 uses it.
- The claim is exact. A rate of 1.00 is easy to disprove.
- The task is the shortest in the benchmark. 934 frames is 31 seconds at 30 fps. The next shortest task is 2.5 times longer.

We run the released checkpoint on the 20 public test instances, at the settings the report picks, on two machines.

## Result

The report gives **1.00** for `turning_on_radio`. We measure **0 successes in 40 runs**.

| Run | Report | n | Ours | 95% CI |
|---|---|---|---|---|
| RTX 3090 | 1.00 | 20 | 0.00 | [0.00, 0.16] |
| RTX 5090 | 1.00 | 20 | 0.00 | [0.00, 0.16] |
| **Combined** | **1.00** | **40** | **0.00** | **[0.00, 0.09]** |

A rate of 1.00 cannot produce 40 failures.

## The claim

![Figure 4 from the report](fig4.png)

*Figure 4 from the report. `turning_on_radio` is the first bar, at 100.*

## The settings are the ones the report picks

![Table 3 from the report](table3.png)

*Table 3 from the report. All rows use `turning_on_radio`.*

| Item | Value | Why |
|---|---|---|
| Control mode | Receding horizon | Best in row #1. The other two give 0.00 |
| `max_len` | 32 | Matches the checkpoint chunk size |
| Resolution | Native, 720 and 480 | Better in row #4. 0.60 against 0.30 |
| Policy | `pi05-b1kpt50-cs32` | The released checkpoint |
| Instances | 20 | The public file supplies 20. The report used 10 |

Stack: BEHAVIOR-1K v3.7.2, Isaac Sim 4.5, numpy 1.26.4.

## The harness works

We ran the same policy on training instances.

| Set | Runs | Successes | Rate | 95% CI |
|---|---|---|---|---|
| Train | 67 | 4 | 0.06 | [0.02, 0.14] |
| Test | 40 | 0 | 0.00 | [0.00, 0.09] |

All four successes scored a full 1.000. A failed episode runs to the 4300-step cap. The successes stopped at 1329 and 1632 steps, so the harness detects completion.

The intervals overlap. We do not claim a train and test gap.

## One run per instance is noisy

Four training instances ran twice. Two changed outcome.

| Instance | First run | Second run |
|---|---|---|
| 1 | 0.000 | **1.000** |
| 4 | **1.000** | 0.000 |

Both successes come from instances that failed on their other run. Figure 4 gives 1.00 from ten single runs. Table 3 values move in steps of 0.05 to 0.10. Those values carry variance the tables do not show.

## Why 0/40 and not 1.00

Three readings.

1. The claim does not reproduce.
2. The released checkpoint is not the model in Figure 4.
3. Our setup is wrong in a way we did not find.

Reading 2 does not resolve. The README calls the same files both things.

| Evidence | Points to |
|---|---|
| Built 2025-12-30, between the two releases | The Q 0.345 model |
| Model card: "the latest model weights" | The Q 0.345 model |
| Directory name `pi05-b1kpt50-cs32` | The pre-training config |
| README: "base ... ideal for fine-tuning" | The pre-training model |

Reading 3 is limited by the control. A dead harness cannot score 1.000.

## What we cannot test

Table 3 row #4 compares 224x224 against native. We cannot repeat it.

1. The 224x224 models are single-task models trained at that resolution. They are not public.
2. The intervals overlap at 10 instances and at 20. The comparison is not resolvable at either size.

## Setup faults

Three faults block the documented path.

1. `base_config.yaml` points at `behavior.learning.wrappers.RGBWrapper`. After the README install step the package is `omnigibson.learning`. Hydra raises `InstantiationException`.
2. `setup.sh` installs numpy 1.26.4. The `--joylo` dependencies upgrade it to 2.x. This breaks the ABI and `og.launch()` gives a segmentation fault.
3. `setup.sh` downloads the 2026 task instances. `eval_custom.py` reads the 2025 instances. Nothing downloads them.

Fixes are in this fork.

## Hardware

Isaac Sim needs RT Cores. The A100, H100 and V100 do not have them.

The RTX 5090 runs the benchmark on driver 580.173.02. It gives a segmentation fault on driver 595.84. See the [hardware page](compute.html).

---

Figures are from the report, used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
