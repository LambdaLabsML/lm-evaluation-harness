# Reproduce Results


## Results

### GPQA-Diamond zeroshot CoT

| Method       | Qwen3-30B-A3B | Qwen3-235B-A22B | Llama-4-Scout-17B-16E-Instruct | Llama-4-Maverick-17B-128E-Instruct-FP8 | DeepSeek-R1-Distill-Llama-70B |
|--------------|----------:|-----------:|-----------:|-----------:|-----------:|
| Reference    |      n/a |       n/a | 57.2 | 69.8 | 65.2 |
| Standard |      61.40 |  69.71 | 49.50 | 62.00 | 62.02 |
| Optimized |      62.42 |  70.91 | 55.3 | 69.89 | 65.56 |
| Chattiness    |  7471.88 |   8025.15 | 754.14 | 868.19 | 5273.24 |

* Standard scores are produced with `temperature=0`. 
* Qwen3 and DeepSeek's optimized scores are produced with `temperature=0.6`.
* Llama4's optimizezd scores are produced with customized prompts from [llama-stack-evals](https://github.com/meta-llama/llama-stack-evals).
* We exclude Qwen3's [reference scores](https://arxiv.org/pdf/2505.09388) from this table because they were produced using 5-shot instead of zero-shot.
* Chattiness is the average number of tokens generated for a single problem.
* Raw outputs can be found in the `./ouptut` folder.


## Setup
```
git clone https://github.com/LambdaLabsML/lm-evaluation-harness.git

sudo docker run --rm -it  --gpus all   \
-v ~/.cache/huggingface:/root/.cache/huggingface   \
-v ./lm-evaluation-harness:/lm-evaluation-harness   \
--shm-size=512g --ipc=host   \
--entrypoint /bin/bash   \
vllm/vllm-openai:latest

cd /lm-evaluation-harness
sed -i '/vllm/d' pyproject.toml

pip install -e .
```


## Qwen3

```
# Standard

lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-30B-A3B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_standard/Qwen3-30B-A3B \
--log_samples --write_out

python compute_token.py \
./output/output_standard/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B

lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-235B-A22B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_standard/Qwen3-235B-A22B \
--log_samples --write_out

python compute_token.py \
./output/output_standard/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B


# Optimized
lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-30B-A3B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.6,"top_p":0.95,"top_k":20}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_optimized/Qwen3-30B-A3B \
--log_samples --write_out


python compute_token.py \
./output/output_optimized/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B

lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-235B-A22B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.6,"top_p":0.95,"top_k":20}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_optimized/Qwen3-235B-A22B \
--log_samples --write_out

python compute_token.py \
./output/output_optimized/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B

```


## Llama 4
```
# Standard
lm_eval \
--model vllm \
--model_args pretrained=meta-llama/Llama-4-Scout-17B-16E-Instruct,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_standard/Llama-4-Scout-17B-16E-Instruct \
--log_samples --write_out

python compute_token.py \
./output/output_standard/Llama-4-Scout-17B-16E-Instruct/meta-llama__Llama-4-Scout-17B-16E-Instruct/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
meta-llama/Llama-4-Scout-17B-16E-Instruct


lm_eval \
--model vllm \
--model_args pretrained=meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_standard/Llama-4-Maverick-17B-128E-Instruct-FP8 \
--log_samples --write_out 


python compute_token.py \
./output/output_standard/Llama-4-Maverick-17B-128E-Instruct-FP8/meta-llama__Llama-4-Maverick-17B-128E-Instruct-FP8/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8


# Optimized
# Llama4's optimized results were produced using https://github.com/meta-llama/llama-stack-evals
```

## DeepSeek-R1-Distill-Llama-70B
```
# Standard
lm_eval \
--model vllm \
--model_args pretrained=deepseek-ai/DeepSeek-R1-Distill-Llama-70B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<｜end▁of▁sentence｜>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_standard/DeepSeek-R1-Distill-Llama-70B \
--log_samples --write_out

python compute_token.py \
./output/output_standard/DeepSeek-R1-Distill-Llama-70B/deepseek-ai__DeepSeek-R1-Distill-Llama-70B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
deepseek-ai/DeepSeek-R1-Distill-Llama-70B

# Optimized
lm_eval \
--model vllm \
--model_args pretrained=deepseek-ai/DeepSeek-R1-Distill-Llama-70B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<｜end▁of▁sentence｜>"],"temperature":0.6,"top_p":0.95}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/output_optimized/DeepSeek-R1-Distill-Llama-70B \
--log_samples --write_out

python compute_token.py \
./output/output_optimized/DeepSeek-R1-Distill-Llama-70B/deepseek-ai__DeepSeek-R1-Distill-Llama-70B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
deepseek-ai/DeepSeek-R1-Distill-Llama-70B
```







## MMLU-Pro


### Optimized:
(Improved settings based on marketing material or technical reports)

| Method       | Qwen3-30B-A3B | Qwen3-235B-A22B | Llama-4-Scout-17B-16E-Instruct | Llama-4-Maverick-17B-128E-Instruct-FP8 | DeepSeek-R1-Distill-Llama-70B |
|--------------|----------:|-----------:|-----------:|-----------:|-----------:|
| Reference    | 65.54     | 68.18      | 74.3       | 80.5       | n/a        |
| Reproduction | 72.9±0.004| 79.5±0.004 | 73.3±0.003 | 80.2±0.004 | n/a        |

#### Setup

**For llama models**:
```sh
git clone https://github.com/LambdaLabsML/lm-evaluation-harness.git && cd lm-evaluation-harness && git checkout llama-4

sudo docker run --rm -it  --gpus all   \
-v ~/.cache/huggingface:/root/.cache/huggingface   \
-v ./lm-evaluation-harness:/lm-evaluation-harness   \
--shm-size=512g --ipc=host   \
--entrypoint /bin/bash   \
vllm/vllm-openai:latest

cd /lm-evaluation-harness
sed -i '/vllm/d' pyproject.toml

pip install -e .
```

**For non-llama models**:
```sh
git clone https://github.com/LambdaLabsML/lm-evaluation-harness.git && cd lm-evaluation-harness

sudo docker run --rm -it  --gpus all   \
-v ~/.cache/huggingface:/root/.cache/huggingface   \
-v ./lm-evaluation-harness:/lm-evaluation-harness   \
--shm-size=512g --ipc=host   \
--entrypoint /bin/bash   \
vllm/vllm-openai:latest

cd /lm-evaluation-harness
sed -i '/vllm/d' pyproject.toml

pip install -e .
```


#### Qwen3-30B-A3B 
```sh
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Qwen3-30B-A38 --model_args model=/mnt/models/Qwen/Qwen3-30B-A3B,pretrained=/mnt/models/Qwen/Qwen3-30B-A3B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true,enable_thinking=true --gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.6,"top_k":20,"top_p":0.95}' --num_fewshot 1
```


#### Qwen3-235B-A22B 
```sh
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Qwen3-235B-A22B --model_args model=/mnt/models/Qwen/Qwen3-235B-A22B,pretrained=/mnt/models/Qwen/Qwen3-235B-A22B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true,enable_thinking=true --gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.6,"top_k":20,"top_p":0.95}' --num_fewshot 1
```


#### Llama-4-Scout-17B-16E-Instruct
```sh
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Llama-4-Scout-17B-16E-Instruct --model_args model=/mnt/model/meta-llama/Llama-4-Scout-17B-16E-Instruct,pretrained=/mnt/model/meta-llama/Llama-4-Scout-17B-16E-Instruct,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true --gen_kwargs {"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0} --num_fewshot 1
```


#### Llama-4-Maverick-17B-128E-Instruct-FP8
```sh
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Llama-4-Maverick-17B-128E-Instruct-FP8 --model_args model=/mnt/model/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,pretrained=/mnt/model/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true --gen_kwargs {"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0} --num_fewshot 1
```



