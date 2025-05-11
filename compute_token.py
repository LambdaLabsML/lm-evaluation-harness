#!/usr/bin/env python3
import json
import sys
from transformers import AutoTokenizer

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.jsonl> [model_name]")
        sys.exit(1)

    input_path = sys.argv[1]
    model_name = sys.argv[2]

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

    total_tokens = 0
    item_count = 0
    max_token = 0

    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            resps = record.get("resps", [])

            # flatten and count
            item_tokens = 0
            for sublist in resps:
                for s in sublist:
                    num_tokens = len(tokenizer.encode(s, add_special_tokens=False))
                    if max_token < num_tokens:
                        max_token = num_tokens
                    item_tokens += num_tokens

            total_tokens += item_tokens
            item_count += 1

    if item_count == 0:
        print("No valid items found in the file.")
        sys.exit(1)

    avg_tokens = total_tokens / item_count
    print(f"Processed {item_count} items.")
    print(f"Average tokens per item: {avg_tokens:.2f}")
    print(f"Max token {max_token}")

if __name__ == "__main__":
    main()