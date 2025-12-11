#!/usr/bin/env python3
"""
Renombrar imágenes de showcase a nombres descriptivos
"""
import os
import shutil

showcases_dir = "/home/star/star/showcases"
os.chdir(showcases_dir)

# Mapeo de nombres antiguos a nuevos nombres descriptivos
rename_map = {
    # Español (ES)
    "showcase_es_1_initial.png": "es_01_pantalla_inicio.png",
    "showcase_es_2_revealed.jpg": "es_02_carta_revelada.jpg",
    "showcase_es_3_content.jpg": "es_03_lectura_completa.jpg",
    
    # English (EN)
    "showcase_en_1_initial.png": "en_01_initial_screen.png",
    "showcase_en_2_revealed.jpg": "en_02_card_revealed.jpg",
    "showcase_en_3_content.jpg": "en_03_full_reading.jpg",
    
    # Portuguese (PT)
    "showcase_pt_1_initial.png": "pt_01_tela_inicial.png",
    "showcase_pt_2_revealed.jpg": "pt_02_carta_revelada.jpg",
    "showcase_pt_3_content.jpg": "pt_03_leitura_completa.jpg",
    
    # French (FR)
    "showcase_fr_1_initial.jpg": "fr_01_ecran_initial.jpg",
    "showcase_fr_2_revealed.png": "fr_02_carte_revelee.png",
    "showcase_fr_3_content.png": "fr_03_lecture_complete.png",
    
    # German (DE)
    "showcase_de_1_initial.jpg": "de_01_startbildschirm.jpg",
    "showcase_de_2_revealed.jpg": "de_02_karte_enthullt.jpg",
    "showcase_de_3_content.jpg": "de_03_vollstandige_lesung.jpg",
    
    # Japanese (JA)
    "showcase_ja_1_initial.jpg": "ja_01_shoki_gamen.jpg",
    "showcase_ja_2_revealed.jpg": "ja_02_kaado_akirakanisareta.jpg",
    "showcase_ja_3_content.jpg": "ja_03_kanzen_na_yomikata.jpg",
    
    # Korean (KO)
    "showcase_ko_1_initial.jpg": "ko_01_chogi_hwamyeon.jpg",
    "showcase_ko_2_revealed.jpg": "ko_02_kadeu_gongae.jpg",
    "showcase_ko_3_content.jpg": "ko_03_wanjeon_han_dogseeo.jpg",
    
    # Chinese (ZH)
    "showcase_zh_1_initial.jpg": "zh_01_chuqi_pingmu.jpg",
    "showcase_zh_2_revealed.jpg": "zh_02_kapai_jielu.jpg",
    "showcase_zh_3_content.jpg": "zh_03_wanzheng_yuedao.jpg",
    
    # Legacy files (archivos antiguos)
    "showcase_1_initial.png": "legacy_01_inicio.png",
    "showcase_1_spanish.png": "legacy_01_spanish.png",
    "showcase_2_english.jpg": "legacy_02_english.jpg",
    "showcase_2_revealed.jpg": "legacy_02_revelada.jpg",
    "showcase_3_content.png": "legacy_03_contenido.png",
    "showcase_3_portuguese.jpg": "legacy_03_portuguese.jpg",
    "showcase_4_french.jpg": "legacy_04_french.jpg",
    "showcase_5_german.jpg": "legacy_05_german.jpg",
    "showcase_6_japanese.jpg": "legacy_06_japanese.jpg",
    "showcase_7_korean.jpg": "legacy_07_korean.jpg",
    "showcase_8_chinese.jpg": "legacy_08_chinese.jpg",
}

renamed_count = 0
errors = []

for old_name, new_name in rename_map.items():
    if os.path.exists(old_name):
        try:
            shutil.move(old_name, new_name)
            print(f"✅ {old_name} → {new_name}")
            renamed_count += 1
        except Exception as e:
            error_msg = f"❌ Error renaming {old_name}: {str(e)}"
            print(error_msg)
            errors.append(error_msg)
    else:
        print(f"⚠️  {old_name} not found, skipping...")

print(f"\n{'='*60}")
print(f"✅ Renamed {renamed_count} files successfully!")
if errors:
    print(f"❌ {len(errors)} errors occurred")
    for error in errors:
        print(f"   {error}")
print(f"{'='*60}\n")

# List final files
print("Final showcase files:")
for file in sorted(os.listdir(".")):
    if file.endswith(('.jpg', '.png', '.jpeg')):
        size_kb = os.path.getsize(file) / 1024
        print(f"  {file:45s} {size_kb:6.0f} KB")
