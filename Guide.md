# Reproduce Results


## Results

### GPQA-Diamond

| Method       | Qwen3-30B-A3B | Qwen3-235B-A22B | Llama-4-Scout-17B-16E-Instruct | Llama-4-Maverick-17B-128E-Instruct-FP8 | DeepSeek-R1-Distill-Llama-70B |
|--------------|----------:|-----------:|-----------:|-----------:|-----------:|
| Reference    |      65.8 |       n/a | 57.2 | 69.8 | 65.2 |
| Reproduction |      64.1±3.4 |  70.7±3.3 | 55.1±3.5 | 66.2±3.4 | 63.6±3.4 |
| Chattiness    |  7471.88 |   8025.15 | 754.14 | 868.19 | 5273.24 |


* Chattiness is the averaged number of tokens generated for a single problem.
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
# Notice enable_thinking=True is needed for lm-harness to use the thinking mode of Qwen

lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-30B-A3B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/gpqa_diamond_cot_zeroshot/Qwen3-30B-A3B \
--log_samples --write_out

python compute_token.py \
./output/gpqa_diamond_cot_zeroshot/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B

lm_eval \
--model vllm \
--model_args pretrained=Qwen/Qwen3-235B-A22B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_thinking=True,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|im_end|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/gpqa_diamond_cot_zeroshot/Qwen3-235B-A22B \
--log_samples --write_out

python compute_token.py \
./output/gpqa_diamond_cot_zeroshot/Qwen3-30B-A3B/Qwen__Qwen3-30B-A3B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
Qwen/Qwen3-235B-A22B
```

## Llama 4
```
lm_eval \
--model vllm \
--model_args pretrained=meta-llama/Llama-4-Scout-17B-16E-Instruct,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/gpqa_diamond_cot_zeroshot/Llama-4-Scout-17B-16E-Instruct \
--log_samples --write_out

python compute_token.py \
./output/gpqa_diamond_cot_zeroshot/Llama-4-Scout-17B-16E-Instruct/meta-llama__Llama-4-Scout-17B-16E-Instruct/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
meta-llama/Llama-4-Scout-17B-16E-Instruct


lm_eval \
--model vllm \
--model_args pretrained=meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/gpqa_diamond_cot_zeroshot/Llama-4-Maverick-17B-128E-Instruct-FP8 \
--log_samples --write_out 


python compute_token.py \
./output/gpqa_diamond_cot_zeroshot/Llama-4-Maverick-17B-128E-Instruct-FP8/meta-llama__Llama-4-Maverick-17B-128E-Instruct-FP8/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8

## DeepSeek-R1-Distill-Llama-70B
lm_eval \
--model vllm \
--model_args pretrained=deepseek-ai/DeepSeek-R1-Distill-Llama-70B,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,enable_prefix_caching=True \
--gen_kwargs '{"max_gen_toks":32768,"until":["<｜end▁of▁sentence｜>"],"temperature":0.0}' \
--tasks gpqa_diamond_cot_zeroshot --batch_size auto --apply_chat_template \
--output_path output/gpqa_diamond_cot_zeroshot/DeepSeek-R1-Distill-Llama-70B \
--log_samples --write_out


python compute_token.py \
./output/gpqa_diamond_cot_zeroshot/DeepSeek-R1-Distill-Llama-70B/deepseek-ai__DeepSeek-R1-Distill-Llama-70B/samples_gpqa_diamond_cot_zeroshot_<timestamp>.jsonl \
deepseek-ai/DeepSeek-R1-Distill-Llama-70B

```