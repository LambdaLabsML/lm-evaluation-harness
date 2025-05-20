# Reproduce Results


## Results

### MMLU-Pro

| Method       | Llama-4-Scout-17B-16E-Instruct | Llama-4-Maverick-17B-128E-Instruct-FP8 | Llama-3.3-70B |
|--------------|-----------:|-----------:|-----------:|
| Reference    | 68.9 | 74.3 | 80.5 |
| Reproduction | 71.2±0.004 | 73.3±0.003 | 80.2±0.004 |

* Raw outputs can be found in the `./ouptut` folder.


## Setup (Llama models)
```
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


## Llama 3.3 70B
```
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Llama-3.3-70B-Instruct --model_args model=/mnt/model/meta-llama/Llama-3.3-70B-Instruct,pretrained=/mnt/model/meta-llama/Llama-3.3-70B-Instruct,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true --gen_kwargs {"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0} --num_fewshot 1
```

## Llama 4 Scout
```
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Llama-4-Scout-17B-16E-Instruct --model_args model=/mnt/model/meta-llama/Llama-4-Scout-17B-16E-Instruct,pretrained=/mnt/model/meta-llama/Llama-4-Scout-17B-16E-Instruct,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true --gen_kwargs {"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0} --num_fewshot 1
```

## Llama 4 Maverick FP8
```
lm_eval --log_samples --apply_chat_template --batch_size auto --model vllm --task=mmlu_pro --output_path output/mmlu_pro/Llama-4-Maverick-17B-128E-Instruct-FP8 --model_args model=/mnt/model/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,pretrained=/mnt/model/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8,tensor_parallel_size=8,max_model_len=32768,gpu_memory_utilization=0.9,trust_remote_code=true --gen_kwargs {"max_gen_toks":32768,"until":["<|eot|>"],"temperature":0.0} --num_fewshot 1
```
