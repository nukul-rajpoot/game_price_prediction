# batch_process.py
import os
import subprocess
import shutil
from datetime import datetime

# Define paths
GAME_PRICE_PREDICTION_PATH = os.environ.get('GAME_PRICE_PREDICTION_PATH', '')
config_path = os.path.join(GAME_PRICE_PREDICTION_PATH, 'python_scripts/sentiment_analysis/config.py')

# List of items to process
items_to_process = [
    {
        'ITEM': "M4A1-S | Golden Coil (Factory New)",
        'ITEMS': [
            "M4A1-S | Golden Coil", "Golden Coil", "GoldenCoil", "M4A1-S Golden Coil", "M4A1S GoldenCoil",
            "Golden Coil M4A1-S", "GoldenCoil M4A1-S", "Golden Coil M4A1S",
            "GoldenCoil M4A1S", "M4A1S Golden Coil", "GoldenCoil M4A1 S",
            "Golden Cool", "GoldenCoil M4AIS",
            "M4A1-S Golden Coi", "M4A1-S Goldon Coil", "M4A1S Goldon Coil"
        ]
    },
    {
        'ITEM': "AK-47 | Redline (Field-Tested)",
        'ITEMS': [
            "AK-47 | Redline", "Redline", "Red line", "AK47 Redline", "AK-47 Red line",
            "Redline AK-47", "Red line AK-47", "AK47 Red line", "AK 47 Redline", "AK 47 Red line"
        ]
    }
]

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