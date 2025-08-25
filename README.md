# RL Project

This repository hosts reinforcement-learning experiments along with an
Agentica-style scaffold for running the **DeepSWE** agent.

## Repository Layout

```
agentica/
  agents/      # agent definitions
  envs/        # environment wrappers
  training/    # training utilities
  scripts/     # runnable helpers and demos
```

## Getting Started

1. **Clone rLLM** (forked to your GitHub account) and enter the repo:
   ```bash
   git clone https://github.com/<your-username>/rllm.git && cd rllm
   ```
2. **Create a Python 3.10 environment** and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare datasets** for SWE-Bench and R2E-Gym:
   ```bash
   python examples/swe/prepare_swe_data.py
   ```
4. **Serve the DeepSWE-Preview model** via vLLM:
   ```bash
   export MAX_CONTEXT_LEN=65536
   export TENSOR_PARALLEL_SIZE=8
   VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 \
       vllm serve agentica-org/DeepSWE-Preview \
       --tensor-parallel-size $TENSOR_PARALLEL_SIZE \
       --max-model-len $MAX_CONTEXT_LEN \
       --hf-overrides '{"max_position_embeddings": '$MAX_CONTEXT_LEN'}' \
       --enable_prefix_caching
   ```
5. **Run evaluation** on SWE-Bench-Verified:
   ```bash
   time python src/r2egym/agenthub/run/edit.py runagent_multiple \
       --traj_dir "./traj" --max_workers 48 --start_idx 0 --k 500 \
       --dataset "R2E-Gym/SWE-Bench-Verified" --split "test" \
       --llm_name "openai/agentica-org/DeepSWE-Preview" --scaffold "r2egym" \
       --use_fn_calling False --exp_name "deepswe-run" --temperature 1.0 \
       --max_steps_absolute 100 --backend "docker" --condense_history False \
       --max_reward_calc_time 1200 --max_tokens 65536
   ```
6. **Minimal local test** (assumes vLLM at `http://localhost:30000/v1`):
   ```bash
   python agentica/scripts/run_deepswe.py --dry-run
   ```

The `requirements.txt` file lists the core libraries (Torch, transformers,
accelerate, vLLM, verl, and rLLM) needed to experiment with DeepSWE.
