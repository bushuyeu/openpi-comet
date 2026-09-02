# Hardware

What it takes to run this benchmark, and what does not work.

## Isaac Sim needs RT Cores

BEHAVIOR-1K runs on OmniGibson, which runs on Isaac Sim. Isaac Sim draws the scene with hardware ray tracing. It needs RT Cores.

NVIDIA lists the A100 and the H100 as not supported. The V100 is older still.

| Architecture | Example | RT Cores | Runs the benchmark |
|---|---|---|---|
| Volta | V100 | No | No |
| Ampere GA100 | A100 | No | No |
| Hopper | H100, H200, GH200 | No | No |
| Ampere GA102 | A40, A10, RTX 3090 | Yes | Yes |
| Ada | L40S, RTX 4090 | Yes | Yes |
| Blackwell | RTX 5090 | Yes | Yes, on driver 580.173.02 |

This reverses the usual order. The report trained on H200 cards. You cannot evaluate on an H200.

The report states the same constraint in Section 4.3. It gives this as the reason to choose rejection sampling over online reinforcement learning. Online training needs both GPU types at the same time.

## The RTX 5090 works

An earlier version of this page said the RTX 5090 fails. That was wrong. The cause of the renderer crash was the NVIDIA driver. We replaced the driver, changed nothing else, and the crash stopped. The card still needs a torch build with sm_120 kernels, but that change alone did not stop the crash.

| Cause | Test | Result |
|---|---|---|
| PhysX GPU kernels for sm_120 | `USE_GPU_DYNAMICS` is already off by default | Not the cause |
| torch has no sm_120 kernels | torch 2.6.0+cu124 stops at sm_90. We installed 2.7.0+cu128 | Needed, but not enough alone |
| numpy ABI | OmniGibson needs numpy below 2.0. Both machines had 2.2.6 | This fixed the RTX 3090 |
| NVIDIA driver | We replaced driver 595.84 with 580.173.02 | This fixed the RTX 5090 |

Driver 595.84 breaks the Omniverse RTX renderer. It breaks two Isaac Sim versions at the same point.

| Isaac Sim | Kit | Driver 595.84 | Driver 580.173.02 |
|---|---|---|---|
| 4.5.0.0, the pinned version | 106.5 | Segmentation fault | Starts |
| 5.1.0.0 | 107.3.3 | Segmentation fault | Starts |

Isaac Sim 5.1 supports Blackwell, and it also failed on driver 595.84. The fault repeats across two Kit versions, which makes a limit of one Kit version unlikely.

A stock Isaac Sim script gives the same fault. OmniGibson is not needed to reproduce it:

```
from isaacsim import SimulationApp
app = SimulationApp({"headless": True})
```

The crash reporter in Isaac Sim 5.1 names the faulting module as `librtx.scenedb.plugin.so`, called from `libcarb.scenerenderer-rtx.plugin.so`. A faulting module is not always the root cause. Four renderer settings changed nothing: path tracing, async rendering off, renderer off, and ray tracing off.

| Card | Compute capability | Driver | `og.launch()` |
|---|---|---|---|
| RTX 3090 | sm_86 | 580.126.09 | Returns 0 |
| RTX 5090 | sm_120 | 595.84 | Segmentation fault |
| RTX 5090 | sm_120 | 580.173.02 | Returns 0 |

The RTX 5090 still needs a torch build with sm_120 kernels. Use torch 2.7.0+cu128. The pinned cu124 build stops at sm_90.

We did not test the RTX 3090 on driver 595.84, so we cannot say whether that driver also breaks Ampere. Both working machines run a 580 driver. The two machines never had the same driver. The earlier version of this page read that difference as a difference between the cards.

## What we used

RTX 3090, 24 GB, driver 580.126.09. The policy server takes about 9 GB. Isaac Sim takes about 8 GB.

RTX 5090, 32 GB, driver 580.173.02, torch 2.7.0+cu128. At native resolution the policy server takes about 9 GB. Each Isaac Sim shard takes about 10 GB.

## Cluster note

We checked the ACCESS-CI catalog. The A40 nodes on NCSA Delta are the only clear RT-Core GPUs in it. DeltaAI, Vista, Lonestar6, Bridges-2, Expanse, Anvil and ACES all use A100, H100, V100 or GH200 cards.

The National Research Platform (nrp.ai) is a better source. It schedules A40, RTX A6000, RTX 8000 and RTX PRO 6000 cards by name, and it is free.

## Summary

| Question | Answer |
|---|---|
| What does Isaac Sim require? | RT Cores. The A100, H100, V100 and GH200 do not have them |
| Does the RTX 5090 work? | Yes, on driver 580.173.02. Driver 595.84 gives a segmentation fault |
| Was it the GPU generation? | No. That was our first reading and it was wrong. The driver is the cause |
| What else is needed on the RTX 5090? | torch 2.7.0+cu128. The pinned cu124 build has no sm_120 kernels |
| Which clusters can run this? | Few. In the ACCESS-CI catalog only the A40 nodes on NCSA Delta are clearly RT-capable |

For the measurement these machines produced, see the [experiment](index.html). For the dataset check that needs no GPU, see the [RFT dataset page](rft-dataset.html).
