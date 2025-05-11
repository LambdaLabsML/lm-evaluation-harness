#!/usr/bin/env python3
import json
import sys

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]

    with open(input_path, "r", encoding="utf-8") as infile:
        count = 0
        for line in infile:
            if count < 192:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                # Check exact_match == 0.0
                if record.get("exact_match") == 0.0:
                    # Print the filtered_resps field
                    filtered = record.get("filtered_resps")
                    print(json.dumps(filtered, ensure_ascii=False))
                # filtered = record.get("filtered_resps")
                # print(json.dumps(filtered, ensure_ascii=False))
                count = count + 1

if __name__ == "__main__":
    main()
