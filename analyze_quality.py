#!/usr/bin/env python3
"""
Comprehensive quality and coherence analysis for tarot translations
"""
import json
import os
from collections import defaultdict

def analyze_file(filepath):
    """Analyze a single JSON file for quality and structure"""
    results = {
        'file': os.path.basename(filepath),
        'valid_json': False,
        'card_count': 0,
        'cotidiano_count': 0,
        'avg_length': 0,
        'errors': [],
        'cards': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results['valid_json'] = True
            results['card_count'] = len(data)
            
            cotidiano_lengths = []
            for card in data:
                card_info = {
                    'id': card.get('id'),
                    'key': card.get('key'),
                    'has_cotidiano': False,
                    'cotidiano_length': 0
                }
                
                if 'contenido' in card and 'cotidiano' in card['contenido']:
                    cotidiano_text = card['contenido']['cotidiano']
                    card_info['has_cotidiano'] = True
                    card_info['cotidiano_length'] = len(cotidiano_text)
                    cotidiano_lengths.append(len(cotidiano_text))
                    results['cotidiano_count'] += 1
                    
                results['cards'].append(card_info)
            
            if cotidiano_lengths:
                results['avg_length'] = sum(cotidiano_lengths) / len(cotidiano_lengths)
                results['min_length'] = min(cotidiano_lengths)
                results['max_length'] = max(cotidiano_lengths)
                
    except json.JSONDecodeError as e:
        results['errors'].append(f"JSON Error: {str(e)}")
    except Exception as e:
        results['errors'].append(f"Error: {str(e)}")
    
    return results

def compare_languages(es_file, en_file, pt_file):
    """Compare content across three language versions"""
    comparison = {
        'matching_cards': 0,
        'mismatches': [],
        'quality_issues': []
    }
    
    try:
        with open(es_file, 'r', encoding='utf-8') as f:
            es_data = json.load(f)
        with open(en_file, 'r', encoding='utf-8') as f:
            en_data = json.load(f)
        
        # Check if Portuguese file exists
        pt_data = []
        if os.path.exists(pt_file):
            with open(pt_file, 'r', encoding='utf-8') as f:
                pt_data = json.load(f)
        
        # Create card lookup by ID
        es_cards = {card['id']: card for card in es_data}
        en_cards = {card['id']: card for card in en_data}
        pt_cards = {card['id']: card for card in pt_data} if pt_data else {}
        
        for card_id in es_cards.keys():
            if card_id in en_cards:
                es_cotidiano = es_cards[card_id].get('contenido', {}).get('cotidiano', '')
                en_cotidiano = en_cards[card_id].get('contenido', {}).get('cotidiano', '')
                
                # Check if both have content
                if es_cotidiano and en_cotidiano:
                    comparison['matching_cards'] += 1
                    
                    # Simple quality check: English should be roughly similar length
                    length_ratio = len(en_cotidiano) / len(es_cotidiano) if len(es_cotidiano) > 0 else 0
                    if length_ratio < 0.7 or length_ratio > 1.3:
                        comparison['quality_issues'].append({
                            'card_id': card_id,
                            'issue': f'Length mismatch: ES={len(es_cotidiano)}, EN={len(en_cotidiano)}, ratio={length_ratio:.2f}'
                        })
                else:
                    comparison['mismatches'].append({
                        'card_id': card_id,
                        'issue': 'Missing cotidiano content'
                    })
            else:
                comparison['mismatches'].append({
                    'card_id': card_id,
                    'issue': 'Card missing in English'
                })
                
    except Exception as e:
        comparison['error'] = str(e)
    
    return comparison

# File paths
base_path = '/home/star/star/public/data'
file_groups = [
    ('0-5.json', '0-5_en.json', '0-5_pt.json'),
    ('6-10.json', '6-10_en.json', '6-10_pt.json'),
    ('11-15.json', '11-15_en.json', '11-15_pt.json'),
    ('16-21.json', '16-21_en.json', '16-21_pt.json'),
]

print("="*80)
print("TAROT TRANSLATION QUALITY & COHERENCE ANALYSIS")
print("="*80)
print()

# Analyze each file group
for es_file, en_file, pt_file in file_groups:
    es_path = os.path.join(base_path, es_file)
    en_path = os.path.join(base_path, en_file)
    pt_path = os.path.join(base_path, pt_file)
    
    print(f"\n{'='*80}")
    print(f"Analyzing: {es_file}")
    print(f"{'='*80}")
    
    # Analyze Spanish
    print("\n[SPANISH SOURCE]")
    es_results = analyze_file(es_path)
    print(f"  Valid JSON: {es_results['valid_json']}")
    print(f"  Cards: {es_results['card_count']}")
    print(f"  With 'cotidiano': {es_results['cotidiano_count']}")
    print(f"  Avg length: {es_results['avg_length']:.0f} chars")
    if es_results.get('min_length'):
        print(f"  Range: {es_results['min_length']}-{es_results['max_length']} chars")
    
    # Analyze English
    print("\n[ENGLISH TRANSLATION]")
    en_results = analyze_file(en_path)
    print(f"  Valid JSON: {en_results['valid_json']}")
    print(f"  Cards: {en_results['card_count']}")
    print(f"  With 'cotidiano': {en_results['cotidiano_count']}")
    print(f"  Avg length: {en_results['avg_length']:.0f} chars")
    if en_results.get('min_length'):
        print(f"  Range: {en_results['min_length']}-{en_results['max_length']} chars")
    
    # Analyze Portuguese
    print("\n[PORTUGUESE TRANSLATION]")
    if os.path.exists(pt_path):
        pt_results = analyze_file(pt_path)
        print(f"  Valid JSON: {pt_results['valid_json']}")
        print(f"  Cards: {pt_results['card_count']}")
        print(f"  With 'cotidiano': {pt_results['cotidiano_count']}")
        print(f"  Avg length: {pt_results['avg_length']:.0f} chars")
        if pt_results.get('min_length'):
            print(f"  Range: {pt_results['min_length']}-{pt_results['max_length']} chars")
    else:
        print(f"  File not found: {pt_path}")
    
    # Compare languages
    print("\n[COHERENCE CHECK]")
    comparison = compare_languages(es_path, en_path, pt_path)
    print(f"  Matching cards: {comparison['matching_cards']}")
    if comparison.get('mismatches'):
        print(f"  Mismatches: {len(comparison['mismatches'])}")
        for mismatch in comparison['mismatches'][:3]:
            print(f"    - Card {mismatch['card_id']}: {mismatch['issue']}")
    if comparison.get('quality_issues'):
        print(f"  Quality issues: {len(comparison['quality_issues'])}")
        for issue in comparison['quality_issues']:
            print(f"    - Card {issue['card_id']}: {issue['issue']}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
