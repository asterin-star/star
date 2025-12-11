import os
import json

DATA_DIR = '/home/star/star/public/data'
LANGUAGES = ['fr', 'de', 'ja', 'ko', 'zh']
RANGES = ['6-10', '11-15', '16-21']

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Saved {filepath}")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

def fix_translations():
    for range_name in RANGES:
        # Load source (es) to get correct keys and structure reference
        source_path = os.path.join(DATA_DIR, f"{range_name}.json")
        source_data = load_json(source_path)
        
        if not source_data:
            print(f"Skipping {range_name} because source is missing.")
            continue

        # Create a map of ID -> Source Card for easy lookup
        source_map = {card['id']: card for card in source_data}

        for lang in LANGUAGES:
            target_filename = f"{range_name}_{lang}.json"
            target_path = os.path.join(DATA_DIR, target_filename)
            target_data = load_json(target_path)

            if not target_data:
                print(f"Skipping {target_filename} (not found or error).")
                continue

            # Check if it's already a list (likely correct)
            if isinstance(target_data, list):
                print(f"{target_filename} is already a list. Skipping.")
                continue

            print(f"Fixing {target_filename}...")
            new_data = []

            # Iterate through source IDs to ensure order and completeness
            for card_id in sorted(source_map.keys()):
                source_card = source_map[card_id]
                str_id = str(card_id)
                
                # Get data from the broken dictionary
                # The broken dict uses string IDs as keys
                broken_card = target_data.get(str_id)

                if not broken_card:
                    print(f"  Warning: ID {card_id} missing in {target_filename}. Using source data as placeholder.")
                    # Fallback to source data if missing
                    new_card = source_card.copy()
                    # Maybe mark name as NEEDS TRANSLATION?
                    # new_card['nombre'] = f"[NEED TRANS] {new_card['nombre']}"
                    new_data.append(new_card)
                    continue

                # Construct new card object
                new_card = {
                    "id": card_id,
                    "key": source_card["key"], # Keep the key constant
                    "nombre": broken_card.get("name", source_card["nombre"]),
                    "contenido": {
                        # Map available fields
                        "arquetipo": broken_card.get("categories", {}).get("psychological", "") or source_card["contenido"]["arquetipo"],
                        "sombra": source_card["contenido"]["sombra"], # Missing in broken, use source or empty? Using source is safer for UI not to break, but might be mixed language.
                        # Actually, if I use source, it will show Spanish text. If I use empty, it hides the section.
                        # User wants "translations". Mixed is better than empty?
                        # Let's use empty string for missing sections so they are hidden, 
                        # BUT `arquetipo` is mandatory for the "Negative" section in UI.
                        # `misticismo` is mandatory for "Ampliado".
                        
                        # Let's map what we have:
                        "misticismo": broken_card.get("categories", {}).get("esoteric", "") or source_card["contenido"]["misticismo"],
                        
                        # "theological" -> resonancia_biblica.conexion
                        "resonancia_biblica": {
                            "cita": source_card["contenido"]["resonancia_biblica"]["cita"], # Keep source quote
                            "referencia": source_card["contenido"]["resonancia_biblica"]["referencia"], # Keep source ref
                            "conexion": broken_card.get("categories", {}).get("theological", "") or source_card["contenido"]["resonancia_biblica"]["conexion"]
                        },

                        # Missing fields - Use source content but maybe mark it? 
                        # Or just use source content. The user said "deben estar todas las traducciones".
                        # If I leave them empty, the UI hides them. That might be "cleaner" than showing Spanish.
                        # But `sombra` is used for `textoSignificado` (Shadows and Dangers).
                        # `arquetipo` is used for `textoNegativo` (Shadow).
                        # Wait, in index.html:
                        # textoSignificado.textContent = getRandomItem('sombra');
                        # textoNegativo.textContent = getRandomItem('arquetipo');
                        
                        # In broken file:
                        # psychological -> "Psychologiquement..." -> seems like Arquetipo/Psychological analysis.
                        # description -> "La Justice siège..." -> General description.
                        
                        # Let's map:
                        # arquetipo <- psychological
                        # sombra <- description (It's not perfect, but description is usually the main text)
                        # OR:
                        # sombra <- psychological
                        # arquetipo <- description
                        
                        # Let's look at `es` 0-5:
                        # Arquetipo: "The Puer Aeternus..." (Deep psychological)
                        # Sombra: "Pathological Recklessness..." (Negative)
                        
                        # Broken `fr`:
                        # Description: "La Justice siège..." (General)
                        # Psychological: "Psychologiquement, La Justice représente..." (Deep)
                        
                        # So `Psychological` maps well to `Arquetipo`.
                        # `Description` is general. `Sombra` is negative.
                        # `fr` doesn't have a specific "Negative" section.
                        # I will map `Description` to `Sombra` just to have text there, even if it's not strictly "Shadow".
                        # Or I can leave `Sombra` as source (Spanish) so the user knows it's missing.
                        # I'll use `Description` for `Sombra` to avoid mixed languages, even if semantically slightly off.
                        
                        "sombra": broken_card.get("description", "") or source_card["contenido"]["sombra"],
                        
                        "cotidiano": "", # Hide
                        "botanica": "", # Hide
                        "gnosis": "" # Hide
                    }
                }
                new_data.append(new_card)

            save_json(target_path, new_data)

if __name__ == "__main__":
    fix_translations()
