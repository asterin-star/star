#!/bin/bash
# Renombrar imágenes de showcase a nombres más descriptivos

cd showcases

# Español (ES) - 3 imágenes
mv showcase_es_1_initial.png es_1_inicio.jpg 2>/dev/null || true
mv showcase_es_2_revealed.jpg es_2_carta_revelada.jpg 2>/dev/null || true
mv showcase_es_3_content.jpg es_3_lectura_completa.jpg 2>/dev/null || true

# English (EN) - 3 imágenes
mv showcase_en_1_initial.png en_1_initial.png 2>/dev/null || true
mv showcase_en_2_revealed.jpg en_2_card_revealed.jpg 2>/dev/null || true
mv showcase_en_3_content.jpg en_3_full_reading.jpg 2>/dev/null || true

# Portuguese (PT) - 3 imágenes
mv showcase_pt_1_initial.png pt_1_inicio.png 2>/dev/null || true
mv showcase_pt_2_revealed.jpg pt_2_carta_revelada.jpg 2>/dev/null || true
mv showcase_pt_3_content.jpg pt_3_leitura_completa.jpg 2>/dev/null || true

# French (FR) - 3 imágenes
mv showcase_fr_1_initial.jpg fr_1_initial.jpg 2>/dev/null || true
mv showcase_fr_2_revealed.png fr_2_carte_revelee.png 2>/dev/null || true
mv showcase_fr_3_content.png fr_3_lecture_complete.png 2>/dev/null || true

# German (DE) - 3 imágenes
mv showcase_de_1_initial.jpg de_1_anfang.jpg 2>/dev/null || true
mv showcase_de_2_revealed.jpg de_2_karte_enthullt.jpg 2>/dev/null || true
mv showcase_de_3_content.jpg de_3_vollstandige_lesung.jpg 2>/dev/null || true

# Japanese (JA) - 3 imágenes
mv showcase_ja_1_initial.jpg ja_1_shoki.jpg 2>/dev/null || true
mv showcase_ja_2_revealed.jpg ja_2_kaado_akirakanisareta.jpg 2>/dev/null || true
mv showcase_ja_3_content.jpg ja_3_kanzen_na_yomikata.jpg 2>/dev/null || true

# Korean (KO) - 3 imágenes
mv showcase_ko_1_initial.jpg ko_1_chogi.jpg 2>/dev/null || true
mv showcase_ko_2_revealed.jpg ko_2_kadeu_gongae.jpg 2>/dev/null || true
mv showcase_ko_3_content.jpg ko_3_wanjeon_han_dogseeo.jpg 2>/dev/null || true

# Chinese (ZH) - 3 imágenes
mv showcase_zh_1_initial.jpg zh_1_chuqi.jpg 2>/dev/null || true
mv showcase_zh_2_revealed.jpg zh_2_kapai_jielu.jpg 2>/dev/null || true
mv showcase_zh_3_content.jpg zh_3_wanzheng_yuedao.jpg 2>/dev/null || true

# Archivos legacy - renombrar también
mv showcase_1_initial.png legacy_1_inicio.png 2>/dev/null || true
mv showcase_1_spanish.png legacy_1_spanish.png 2>/dev/null || true
mv showcase_2_english.jpg legacy_2_english.jpg 2>/dev/null || true
mv showcase_2_revealed.jpg legacy_2_revelada.jpg 2>/dev/null || true
mv showcase_3_content.png legacy_3_contenido.png 2>/dev/null || true
mv showcase_3_portuguese.jpg legacy_3_portuguese.jpg 2>/dev/null || true
mv showcase_4_french.jpg legacy_4_french.jpg 2>/dev/null || true
mv showcase_5_german.jpg legacy_5_german.jpg 2>/dev/null || true
mv showcase_6_japanese.jpg legacy_6_japanese.jpg 2>/dev/null || true
mv showcase_7_korean.jpg legacy_7_korean.jpg 2>/dev/null || true
mv showcase_8_chinese.jpg legacy_8_chinese.jpg 2>/dev/null || true

echo "✅ Showcase images renamed successfully!"
ls -lh *.{jpg,png} 2>/dev/null | awk '{print $9, $5}'
