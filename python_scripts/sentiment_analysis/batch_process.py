import os
import subprocess
import shutil
from datetime import datetime
import csv

"""
automating batch proccessong of CS:GO item analysis
using config -> updates and backups
and iterates over @accepted_item_raw.csv which contains ITEM 
"""

# Define paths
GAME_PRICE_PREDICTION_PATH = os.environ.get('GAME_PRICE_PREDICTION_PATH', '')
config_path = os.path.join(GAME_PRICE_PREDICTION_PATH, 'python_scripts/sentiment_analysis/config.py')
csv_path = os.path.join(GAME_PRICE_PREDICTION_PATH, 'data/item_lists/accepted_item_raw.csv')

# Read items from CSV
def load_items_from_csv():
    items_to_process = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            if len(row) >= 2:  # Ensure row has both ITEM and ITEMS
                item = row[0].strip('"')
                # Split ITEMS string and clean up each item
                items = [item.strip() for item in row[1].strip('"').split(',')]
                items_to_process.append({
                    'ITEM': item,
                    'ITEMS': items
                })
    return items_to_process

# Replace the hardcoded items_to_process with the function call
items_to_process = load_items_from_csv()

def format_items_list(items):
    """Format the ITEMS list with proper indentation"""
    items_str = "ITEMS = [\n"
    for item in items:
        items_str += f'    "{item}",\n'
    items_str = items_str.rstrip(',\n') + "\n]"
    return items_str

def main():
    # Create backup of original config
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    config_backup = f"{config_path}.backup_{timestamp}"
    shutil.copy2(config_path, config_backup)
    print(f"Created config backup: {config_backup}")

    try:
        for item in items_to_process:
            ITEM = item['ITEM']
            ITEMS = item['ITEMS']
            print(f"\nProcessing item: {ITEM}")

            # Read original config
            with open(config_path, 'r') as file:
                config_contents = file.readlines()

            # Prepare new config contents
            new_config = []
            in_items_block = False
            
            for line in config_contents:
                if line.strip().startswith('ITEM ='):
                    new_config.append(f'ITEM = "{ITEM}"\n')
                elif line.strip().startswith('ITEMS ='):
                    new_config.append(format_items_list(ITEMS) + '\n')
                    in_items_block = True
                elif in_items_block and ']' in line:
                    in_items_block = False
                    continue
                elif not in_items_block:
                    new_config.append(line)

            # Write new config
            with open(config_path, 'w') as file:
                file.writelines(new_config)

            try:
                # Execute mentions_graphs.ipynb
                print(f"Running analysis for {ITEM}...")
                result = subprocess.run([
                    'jupyter', 'nbconvert', '--to', 'notebook', '--execute',
                    os.path.join(GAME_PRICE_PREDICTION_PATH, 'python_scripts/sentiment_analysis/mentions_graphs.ipynb'),
                    '--output', f'mentions_graphs_{ITEM.replace(" | ", "_").replace("(", "").replace(")", "")}.ipynb'
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"Error processing {ITEM}:")
                    print(result.stderr)
                else:
                    print(f"Successfully processed {ITEM}")

            except Exception as e:
                print(f"Error processing {ITEM}: {str(e)}")

    finally:
        # Restore original config
        shutil.copy2(config_backup, config_path)
        print(f"\nRestored original config from backup")

if __name__ == "__main__":
    main()