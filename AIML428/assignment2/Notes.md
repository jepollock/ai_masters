# TODO

Notes on code:

Uses tf32 - 32bit storage size, but actually only 19 bits wide.
Faster calculations on NVidia.
however this is only for NVidia GPUs, MPS has FP16 and FP32.


1) Figure out why perplexity of fixed string is 0.
2) Implement beam search.
  a) top-k
  b) take top-k, expand them to top-k
  c) when all previous expansions are done, pick top-k again.
3) Describe something?!?!?!
4) COMMENT THE CODE, they are going to read it.

# Notes

Dataset: https://huggingface.co/datasets/openai/gsm8k

The ### value indicates the correct, expected value.

python ./eval.py --init_from=resume --out_dir=out-gms8k --device=mps

python train.py config/finetune_gms8k.py --device=mps

./convert.py --split=False --in_file=data/gms8k/test-00000-of-00001.parquet --train_file=test.json --max_rows=10

Do two eval cycles:

1) What's the change in the log prob (perplexity) due to the training? 
2) Need to enable/disable the start/stop tokens.
3) Check for the calculator/answers. - debug calculator check.

Stop tokens are _really_ important - encoding the training data helps inference!

````
(base) jepollock@Jasons-MacBook-Pro nanoGPT % python train.py config/finetune_gms8k.py --device=mps
Overriding config with config/finetune_gms8k.py:
import time

out_dir = 'out-gms8k'
eval_interval = 5
eval_iters = 40
wandb_log = False # feel free to turn on
wandb_project = 'gms8k-428'
wandb_run_name = 'ft-' + str(time.time())

dataset = 'gms8k'
init_from = 'gpt2-large' # this is the largest GPT-2 model

# only save checkpoints if the validation loss improves
always_save_checkpoint = False

# the number of examples per iter:
# 1 batch_size * 32 grad_accum * 1024 tokens = 32,768 tokens/iter
# shakespeare has 301,966 tokens, so 1 epoch ~= 9.2 iters
batch_size = 1
gradient_accumulation_steps = 32
max_iters = 20

# finetune at constant LR
learning_rate = 3e-5
decay_lr = False

Overriding: device = mps
tokens per iteration will be: 32,768
Initializing from OpenAI GPT-2 weights: gpt2-large
loading weights from pretrained gpt: gpt2-large
forcing vocab_size=50257, block_size=1024, bias=True
overriding dropout rate to 0.0
number of parameters: 772.72M
Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████████████| 436/436 [00:00<00:00, 11714.81it/s]
/Users/jepollock/dev/ai_masters/AIML428/assignment2/nanoGPT/train.py:196: FutureWarning: `torch.cuda.amp.GradScaler(args...)` is deprecated. Please use `torch.amp.GradScaler('cuda', args...)` instead.
  scaler = torch.cuda.amp.GradScaler(enabled=(dtype == 'float16'))
/opt/anaconda3/lib/python3.13/site-packages/torch/cuda/amp/grad_scaler.py:31: UserWarning: torch.cuda.amp.GradScaler is enabled, but CUDA is not available.  Disabling.
  super().__init__(
num decayed parameter tensors: 146, with 773,428,480 parameters
num non-decayed parameter tensors: 290, with 601,600 parameters
using fused AdamW: False
compiling the model... (takes a ~minute)
W0511 09:29:33.134000 85646 site-packages/torch/_inductor/utils.py:1731] [0/0] Not enough SMs to use max_autotune_gemm mode
step 0: train loss 1.8203, val loss 1.8561
iter 0: loss 1.8194, time 242988.31ms, mfu -100.00%
iter 1: loss 1.6337, time 89820.05ms, mfu -100.00%
iter 2: loss 1.7566, time 89399.93ms, mfu -100.00%
iter 3: loss 1.6222, time 89671.80ms, mfu -100.00%
iter 4: loss 1.3808, time 89160.64ms, mfu -100.00%
step 5: train loss 1.4282, val loss 1.4176
saving checkpoint to out-gms8k
iter 5: loss 1.4068, time 234096.23ms, mfu 0.23%
iter 6: loss 1.4543, time 88461.74ms, mfu 0.27%
iter 7: loss 1.3241, time 89158.22ms, mfu 0.31%
iter 8: loss 1.2327, time 88661.21ms, mfu 0.34%
iter 9: loss 1.3601, time 89224.23ms, mfu 0.36%
step 10: train loss 1.2567, val loss 1.3427
saving checkpoint to out-gms8k
iter 10: loss 1.2401, time 233899.43ms, mfu 0.35%
iter 11: loss 1.3484, time 89114.04ms, mfu 0.38%
iter 12: loss 1.1901, time 88966.62ms, mfu 0.40%
iter 13: loss 1.0974, time 89077.34ms, mfu 0.42%
iter 14: loss 1.2333, time 88891.35ms, mfu 0.44%
step 15: train loss 1.2256, val loss 1.2622
saving checkpoint to out-gms8k
iter 15: loss 1.0742, time 235657.44ms, mfu 0.42%
iter 16: loss 1.3340, time 88907.80ms, mfu 0.44%
iter 17: loss 1.3048, time 88781.47ms, mfu 0.46%
iter 18: loss 1.0470, time 88986.08ms, mfu 0.47%
iter 19: loss 1.1168, time 88851.00ms, mfu 0.49%
step 20: train loss 1.1910, val loss 1.1986
saving checkpoint to out-gms8k
iter 20: loss 1.3181, time 238056.66ms, mfu 0.46%
```
