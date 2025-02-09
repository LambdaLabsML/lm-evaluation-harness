import os
import json
import pandas as pd
import argparse
import numpy as np

def find_json_file(folder):
    """Recursively find the JSON file starting with 'results_'"""
    for root, _, files in os.walk(folder):
        for file in files:
            if file.startswith("results_") and file.endswith(".json"):
                return os.path.join(root, file)
    return None

def extract_acc_norm_values(json_path):
    """Extract acc_norm,none, *_acc,none, and exact_match,none values from the JSON results field"""
    with open(json_path, "r") as f:
        data = json.load(f)
    
    results = {}
    if "results" in data:
        for task, task_data in data["results"].items():
            if isinstance(task_data, dict):
                # Check for acc_norm,none
                if "acc_norm,none" in task_data:
                    results[task] = task_data["acc_norm,none"]
                # Check for *_acc,none
                for key in task_data:
                    if key.endswith("_acc,none"):
                        results[f"{task}_{key}"] = task_data[key]
                # Check for exact_match,none
                if "exact_match,none" in task_data:
                    results[f"{task}_exact_match,none"] = task_data["exact_match,none"]
    
    return results

def process_folders(folders):
    """Process all folders and extract acc_norm values"""
    results_dict = {}
    all_tasks = set()
    
    for folder in folders:
        folder_name = os.path.basename(folder)
        results_dict[folder_name] = {}
        for subfolder in os.listdir(folder):
            subfolder_path = os.path.join(folder, subfolder)
            if os.path.isdir(subfolder_path):
                json_path = find_json_file(subfolder_path)
                if json_path:
                    acc_norm_values = extract_acc_norm_values(json_path)
                    results_dict[folder_name].update(acc_norm_values)
                    all_tasks.update(acc_norm_values.keys())
    
    return results_dict, all_tasks


def save_results(results_dict, all_tasks, output):
    """Save the extracted values into CSV and markdown files"""
    # Create DataFrame with tasks in original order
    df = pd.DataFrame(index=sorted(all_tasks))
    df.index.name = "task_name"
    
    # Add data for each folder while preserving task order
    for folder, results in results_dict.items():
        folder_name = os.path.basename(folder)
        df[folder_name] = [results.get(task, "N/A") for task in all_tasks]
    
    # Reset index to make task_name a column
    df = df.reset_index()
    

    
    # Create markdown with bold highest values
    md_df = df.copy()
    numeric_columns = md_df.select_dtypes(include=[np.number]).columns
    
    # Round all numeric values to 3 decimal places
    md_df[numeric_columns] = md_df[numeric_columns].round(3)

    # Save CSV
    md_df.to_csv(output + ".csv", index=False)
    print(f"Results saved to {output}.csv")

    # For each row, bold the highest value
    for idx in md_df.index:
        row_values = md_df.loc[idx, numeric_columns]
        max_value = row_values.max()
        for col in numeric_columns:
            if md_df.loc[idx, col] == max_value:
                md_df.loc[idx, col] = f"**{md_df.loc[idx, col]}**"
    
    # Save markdown
    md_file = output + ".md"
    with open(md_file, 'w') as f:
        f.write(md_df.to_markdown(index=False))
    print(f"Markdown table saved to {md_file}")




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs='+', help="List of folders to process")
    parser.add_argument("--output", default="results_comparison", help="Output file name")
    args = parser.parse_args()
    
    results_dict, all_tasks = process_folders(args.folders)
    save_results(results_dict, all_tasks, args.output)

if __name__ == "__main__":
    main()
