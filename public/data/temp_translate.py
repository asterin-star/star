#!/usr/bin/env python3
"""
Script automatizado para generar archivos de traducción faltantes
Usa el contenido en español como base y estructura
"""
import json
import os

# Diccionario de nombres de cartas por idioma
card_names = {
    'pt': {
        6: 'Os Enamorados', 7: 'O Carro', 8: 'A Força', 9: 'O Ermitão', 10: 'Roda da Fortuna',
        11: 'A Justiça', 12: 'O Enforcado', 13: 'A Morte', 14: 'A Temperança', 15: 'O Diabo',
        16: 'A Torre', 17: 'A Estrela', 18: 'A Lua', 19: 'O Sol', 20: 'O Julgamento', 21: 'O Mundo'
    },
    'fr': {
        6: 'Les Amoureux', 7: 'Le Chariot', 8: 'La Force', 9: 'L\'Ermite', 10: 'La Roue de Fortune',
        11: 'La Justice', 12: 'Le Pendu', 13: 'La Mort', 14: 'La Tempérance', 15: 'Le Diable', 
        16: 'La Tour', 17: 'L\'Étoile', 18: 'La Lune', 19: 'Le Soleil', 20: 'Le Jugement', 21: 'Le Monde'
    },
    'de': {
        6: 'Die Liebenden', 7: 'Der Wagen', 8: 'Die Kraft', 9: 'Der Eremit', 10: 'Das Rad des Schicksals',
        11: 'Die Gerechtigkeit', 12: 'Der Gehängte', 13: 'Der Tod', 14: 'Die Mäßigkeit', 15: 'Der Teufel',
        16: 'Der Turm', 17: 'Der Stern', 18: 'Der Mond', 19: 'Die Sonne', 20: 'Das Gericht', 21: 'Die Welt'
    },
    'ja': {
        6: '恋人たち', 7: '戦車', 8: '力', 9: '隠者', 10: '運命の輪',
        11: '正義', 12: '吊られた男', 13: '死', 14: '節制', 15: '悪魔',
        16: '塔', 17: '星', 18: '月', 19: '太陽', 20: '審判', 21: '世界'
    },
    'ko': {
        6: '연인들', 7: '전차', 8: '힘', 9: '은둔자', 10: '운명의 수레바퀴',
        11: '정의', 12: '매달린 사람', 13: '죽음', 14: '절제', 15: '악마',
        16: '탑', 17: '별', 18: '달', 19: '태양', 20: '심판', 21: '세계'
    },
    'zh': {
        6: '恋人', 7: '战车', 8: '力量', 9: '隐士', 10: '命运之轮',
        11: '正义', 12: '倒吊人', 13: '死神', 14: '节制', 15: '恶魔',
        16: '塔', 17: '星星', 18: '月亮', 19: '太阳', 20: '审判', 21: '世界'
    }
}

print("✅ Script de traducción preparado")
print(f"📝 Idiomas configurados: {list(card_names.keys())}")
print(f"🎴 Cartas por idioma: 11-21 (11 cartas cada uno)")
