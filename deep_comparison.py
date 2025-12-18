#!/usr/bin/env python3
"""
Deep inspection: Compare exact text lengths and content between ES, EN, PT
"""
import json
import os

def deep_comparison(es_file, en_file, pt_file):
    """Deep comparison of content across 3 languages"""
    results = {}
    
    with open(es_file, 'r', encoding='utf-8') as f:
        es_data = json.load(f)
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    with open(pt_file, 'r', encoding='utf-8') as f:
        pt_data = json.load(f)
    
    for es_card in es_data:
        card_id = es_card['id']
        card_key = es_card['key']
        
        # Find matching cards
        en_card = next((c for c in en_data if c['id'] == card_id), None)
        pt_card = next((c for c in pt_data if c['id'] == card_id), None)
        
        if not en_card or not pt_card:
            continue
            
        results[card_id] = {
            'key': card_key,
            'sections': {}
        }
        
        sections = ['arquetipo', 'sombra', 'misticismo', 'cotidiano', 'botanica', 'gnosis']
        
        for section in sections:
            es_text = es_card['contenido'].get(section, '')
            en_text = en_card['contenido'].get(section, '')
            pt_text = pt_card['contenido'].get(section, '')
            
            results[card_id]['sections'][section] = {
                'es_length': len(es_text),
                'en_length': len(en_text),
                'pt_length': len(pt_text),
                'en_ratio': round(len(en_text) / len(es_text), 2) if len(es_text) > 0 else 0,
                'pt_ratio': round(len(pt_text) / len(es_text), 2) if len(es_text) > 0 else 0
            }
    
    return results

# Analyze
base_path = '/home/star/star/public/data'
all_results = {}

print("="*80)
print("DEEP CONTENT COMPARISON - ALL CARDS")
print("="*80)

for file_range in ['0-5', '6-10', '11-15', '16-21']:
    es_path = os.path.join(base_path, f'{file_range}.json')
    en_path = os.path.join(base_path, f'{file_range}_en.json')
    pt_path = os.path.join(base_path, f'{file_range}_pt.json')
    
    if os.path.exists(es_path) and os.path.exists(en_path) and os.path.exists(pt_path):
        results = deep_comparison(es_path, en_path, pt_path)
        all_results.update(results)

# Print detailed results
print(f"\nTotal cards analyzed: {len(all_results)}")
print()

# Find problematic cards (where EN or PT < 70% of ES length)
problems = []

for card_id, data in sorted(all_results.items()):
    print(f"\n{'='*80}")
    print(f"Card {card_id}: {data['key']}")
    print(f"{'='*80}")
    
    for section, lengths in data['sections'].items():
        ratio_flag_en = "⚠️ " if lengths['en_ratio'] < 0.7 else "✅"
        ratio_flag_pt = "⚠️ " if lengths['pt_ratio'] < 0.7 else "✅"
        
        print(f"  {section:12} | ES: {lengths['es_length']:4}ch | EN: {lengths['en_length']:4}ch ({ratio_flag_en}{lengths['en_ratio']}) | PT: {lengths['pt_length']:4}ch ({ratio_flag_pt}{lengths['pt_ratio']})")
        
        if lengths['en_ratio'] < 0.7 or lengths['pt_ratio'] < 0.7:
            problems.append({
                'card': card_id,
                'key': data['key'],
                'section': section,
                'es_length': lengths['es_length'],
                'en_length': lengths['en_length'],
                'pt_length': lengths['pt_length'],
                'en_ratio': lengths['en_ratio'],
                'pt_ratio': lengths['pt_ratio']
            })

print(f"\n{'='*80}")
print("SUMMARY OF ISSUES")
print(f"{'='*80}")
print(f"Total issues found: {len(problems)}")
print()

for prob in problems:
    print(f"⚠️  Card {prob['card']} ({prob['key']}) - {prob['section']}")
    print(f"    ES: {prob['es_length']}ch | EN: {prob['en_length']}ch (ratio: {prob['en_ratio']}) | PT: {prob['pt_length']}ch (ratio: {prob['pt_ratio']})")
    print()

print("="*80)
