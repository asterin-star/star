import os
import json
import sys

DATA_DIR = '/home/star/star/public/data'

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def verify_translations():
    files = os.listdir(DATA_DIR)
    source_files = [f for f in files if f.endswith('.json') and '_' not in f]
    
    all_passed = True

    for source_file in source_files:
        print(f"Verifying translations for source: {source_file}")
        source_path = os.path.join(DATA_DIR, source_file)
        source_data = load_json(source_path)
        
        if source_data is None:
            print(f"Skipping {source_file} due to load error.")
            all_passed = False
            continue

        # Find corresponding translations
        base_name = source_file.replace('.json', '')
        translation_files = [f for f in files if f.startswith(base_name + '_') and f.endswith('.json')]
        
        for trans_file in translation_files:
            trans_path = os.path.join(DATA_DIR, trans_file)
            trans_data = load_json(trans_path)
            
            if trans_data is None:
                all_passed = False
                continue
            
            # Check for missing keys (assuming flat structure or list of objects)
            # The structure seems to be a list of card objects based on file names like 0-5.json
            
            if isinstance(source_data, list) and isinstance(trans_data, list):
                if len(source_data) != len(trans_data):
                    print(f"  [FAIL] {trans_file}: Length mismatch. Source: {len(source_data)}, Trans: {len(trans_data)}")
                    all_passed = False
                else:
                    for i, (src_item, trans_item) in enumerate(zip(source_data, trans_data)):
                        src_keys = set(src_item.keys())
                        trans_keys = set(trans_item.keys())
                        
                        missing_keys = src_keys - trans_keys
                        if missing_keys:
                            print(f"  [FAIL] {trans_file} (Item {i}): Missing keys: {missing_keys}")
                            all_passed = False
            elif isinstance(source_data, dict) and isinstance(trans_data, dict):
                 src_keys = set(source_data.keys())
                 trans_keys = set(trans_data.keys())
                 missing_keys = src_keys - trans_keys
                 if missing_keys:
                    print(f"  [FAIL] {trans_file}: Missing keys: {missing_keys}")
                    all_passed = False
            else:
                print(f"  [FAIL] {trans_file}: Structure mismatch with source.")
                all_passed = False

    if all_passed:
        print("\nAll checks passed!")
    else:
        print("\nSome checks failed.")

if __name__ == "__main__":
    verify_translations()
