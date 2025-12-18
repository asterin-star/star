#!/usr/bin/env python3
"""
Verificar que TODO el contenido completo está presente en todos los campos
"""
import json
import os

def verify_complete_content(filepath):
    """Verify all content fields are present and complete"""
    results = {
        'file': os.path.basename(filepath),
        'cards': [],
        'issues': [],
        'total_sections': 0,
        'complete_sections': 0
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            for card in data:
                card_result = {
                    'id': card.get('id'),
                    'key': card.get('key'),
                    'sections': {}
                }
                
                contenido = card.get('contenido', {})
                required_sections = ['arquetipo', 'sombra', 'misticismo', 'cotidiano', 'botanica', 'gnosis', 'resonancia_biblica']
                
                for section in required_sections:
                    results['total_sections'] += 1
                    if section in contenido:
                        value = contenido[section]
                        if section == 'resonancia_biblica':
                            # Check if it has cita, referencia, conexion
                            is_complete = all(k in value for k in ['cita', 'referencia', 'conexion'])
                            card_result['sections'][section] = {
                                'present': True,
                                'complete': is_complete,
                                'length': len(str(value))
                            }
                        else:
                            # Check if text is substantial (>100 chars)
                            is_complete = len(value) > 100
                            card_result['sections'][section] = {
                                'present': True,
                                'complete': is_complete,
                                'length': len(value)
                            }
                            
                        if card_result['sections'][section]['complete']:
                            results['complete_sections'] += 1
                    else:
                        card_result['sections'][section] = {
                            'present': False,
                            'complete': False,
                            'length': 0
                        }
                        results['issues'].append(f"Card {card['id']} missing section: {section}")
                
                results['cards'].append(card_result)
                
    except Exception as e:
        results['error'] = str(e)
    
    return results

# Verify all files
base_path = '/home/star/star/public/data'
files_to_check = [
    '0-5.json', '0-5_en.json', '0-5_pt.json',
    '6-10.json', '6-10_en.json', '6-10_pt.json',
    '11-15.json', '11-15_en.json', '11-15_pt.json',
    '16-21.json', '16-21_en.json', '16-21_pt.json',
]

print("="*80)
print("VERIFICACIÓN DE CONTENIDO COMPLETO")
print("="*80)
print()

for filename in files_to_check:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"\n⚠️  {filename}: FILE NOT FOUND")
        continue
        
    results = verify_complete_content(filepath)
    
    completion_rate = (results['complete_sections'] / results['total_sections'] * 100) if results['total_sections'] > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"📄 {filename}")
    print(f"{'='*80}")
    print(f"  Total sections: {results['total_sections']}")
    print(f"  Complete sections: {results['complete_sections']}")
    print(f"  Completion rate: {completion_rate:.1f}%")
    
    if results.get('issues'):
        print(f"  ⚠️  Issues found: {len(results['issues'])}")
        for issue in results['issues'][:5]:
            print(f"    - {issue}")
    else:
        print(f"  ✅ All sections present and complete!")
    
    # Show detailed card info for first card
    if results['cards']:
        card = results['cards'][0]
        print(f"\n  Sample (Card {card['id']}):")
        for section, info in card['sections'].items():
            status = "✅" if info['complete'] else "⚠️ "
            print(f"    {status} {section}: {info['length']} chars")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
