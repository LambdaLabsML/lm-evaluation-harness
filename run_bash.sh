#!/bin/bash

# Check if a model argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <model>"
    exit 1
fi

model="$1"
tp="$2"

declare -A model_map
model_map["deepseek8b"]="deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
model_map["deepseek8b_david_20250205"]="/shared/chuan/models/2_prepromptsbest2_64"
model_map["llama3_1_8b_instruct"]="meta-llama/Meta-Llama-3.1-8B-Instruct"

# Validate model
if [[ -z "${model_map[$model]}" ]]; then
    echo "Error: Model '$model' is not recognized."
    exit 1
fi

model_name="${model_map[$model]}"

tasks=(
    leaderboard_bbh
    leaderboard_gpqa
    leaderboard_ifeval
    leaderboard_math_hard
    leaderboard_mmlu_pro
    leaderboard_musr
)


mkdir -p results

for task in "${tasks[@]}"; do
    output_path="./results/${model}/${task}"
    echo "Running evaluation for task: $task with model: $model_name"
    lm_eval --model vllm \
    --trust_remote_code \
    --batch_size auto \
    --apply_chat_template \
    --fewshot_as_multiturn \
    --write_out \
    --log_samples \
    --output_path "$output_path" \
    --model_args pretrained="${model_name},tensor_parallel_size=${tp},dtype=auto,gpu_memory_utilization=0.9,data_parallel_size=1" \
    --tasks "$task"     
done
