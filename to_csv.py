import json
import csv
import os
import glob
from json.decoder import JSONDecodeError

def jsonl_to_csv(input_file, output_file):
    data = []
    # Read JSONL file
    with open(input_file, 'r') as jsonl_file:
        for line_number, line in enumerate(jsonl_file, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            try:
                data.append(json.loads(line))
            except JSONDecodeError as e:
                print(f"Error parsing JSON in {input_file} at line {line_number}: {e}")
                print(f"Problematic line: {line}")
                continue  # Skip this line and continue with the next

    if not data:
        print(f"No valid data found in {input_file}. Skipping.")
        return

    # Get all unique keys from all JSON objects
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print(f"Converted {input_file} to {output_file}")

def process_directory(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all JSONL files in the input directory
    for jsonl_file in glob.glob(os.path.join(input_dir, '*.jsonl')):
        base_name = os.path.basename(jsonl_file)
        csv_file = os.path.join(output_dir, os.path.splitext(base_name)[0] + '.csv')
        jsonl_to_csv(jsonl_file, csv_file)


if __name__ == "__main__":
    input_directory = "data"  # Replace with your input directory path
    output_directory = "data/json_to_csv"  # Replace with your output directory path
    process_directory(input_directory, output_directory)