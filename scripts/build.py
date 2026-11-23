#!/usr/bin/env python3
"""Build Mark Six draw dataset files (CSV + JSON) from a raw lottery_draws export.

Usage: python3 scripts/build.py [raw_export.json]
Default raw path: /tmp/cyq-dataset/draws-raw.json
Outputs into data/: macau.csv, macau.json, hkjc.csv, hkjc.json
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/tmp/cyq-dataset/draws-raw.json')

# Fixed number facts (do not change)
WAVE = {}
for n in [1, 2, 7, 8, 12, 13, 18, 19, 23, 24, 29, 30, 34, 35, 40, 45, 46]:
    WAVE[n] = 'red'
for n in [3, 4, 9, 10, 14, 15, 20, 25, 26, 31, 36, 37, 41, 42, 47, 48]:
    WAVE[n] = 'blue'
for n in [5, 6, 11, 16, 17, 21, 22, 27, 28, 32, 33, 38, 39, 43, 44, 49]:
    WAVE[n] = 'green'

ELEMENT = {}
for n in [4, 5, 12, 13, 26, 27, 34, 35, 42, 43]:
    ELEMENT[n] = '金'
for n in [8, 9, 16, 17, 24, 25, 38, 39, 46, 47]:
    ELEMENT[n] = '木'
for n in [1, 14, 15, 22, 23, 30, 31, 44, 45]:
    ELEMENT[n] = '水'
for n in [2, 3, 10, 11, 18, 19, 32, 33, 40, 41, 48, 49]:
    ELEMENT[n] = '火'
for n in [6, 7, 20, 21, 28, 29, 36, 37]:
    ELEMENT[n] = '土'

# 2026 zodiac mapping (for cross-check only; dataset uses per-draw zodiac from DB)
ZODIAC_2026 = {}
for z, nums in {
    '马': [1, 13, 25, 37, 49], '蛇': [2, 14, 26, 38], '龙': [3, 15, 27, 39],
    '兔': [4, 16, 28, 40], '虎': [5, 17, 29, 41], '牛': [6, 18, 30, 42],
    '鼠': [7, 19, 31, 43], '猪': [8, 20, 32, 44], '狗': [9, 21, 33, 45],
    '鸡': [10, 22, 34, 46], '猴': [11, 23, 35, 47], '羊': [12, 24, 36, 48],
}.items():
    for n in nums:
        ZODIAC_2026[n] = z

TRAD_TO_SIMP = {'龍': '龙', '馬': '马', '雞': '鸡', '豬': '猪', '鴨': '鸭'}
WAVE_ZH = {'red': '红波', 'blue': '蓝波', 'green': '绿波'}
LOTTERY_NAME = {'macaujc2': ('macau', '澳门六合彩', 'Macau Mark Six'),
                'hkjc': ('hkjc', '香港六合彩', 'Hong Kong Mark Six')}


def simp(z):
    return ''.join(TRAD_TO_SIMP.get(ch, ch) for ch in str(z))


def main():
    rows = json.loads(RAW.read_text(encoding='utf-8'))
    out = {}
    wave_mismatch = 0
    zodiac2026_mismatch = 0
    for r in rows:
        code = r['lottery_code']
        if code not in LOTTERY_NAME:
            continue
        slug = LOTTERY_NAME[code][0]
        numbers = json.loads(r['numbers_json'])
        zodiacs = [simp(z) for z in json.loads(r['zodiac_json'])]
        waves = json.loads(r['wave_json'])
        if len(numbers) != 7:
            print(f"SKIP bad numbers {code} {r['issue_no']}: {numbers}")
            continue
        for n, w in zip(numbers, waves):
            if WAVE.get(int(n)) != w:
                wave_mismatch += 1
        if str(r['issue_no']).startswith('2026'):
            for n, z in zip(numbers, zodiacs):
                if ZODIAC_2026.get(int(n)) != z:
                    zodiac2026_mismatch += 1
        rec = {
            'issue': str(r['issue_no']),
            'date': str(r['draw_time'])[:10],
            'draw_time': str(r['draw_time']),
            'numbers': [int(x) for x in numbers[:6]],
            'special': int(numbers[6]),
            'zodiac': zodiacs,
            'wave': waves,
            'wave_zh': [WAVE_ZH[w] for w in waves],
            'element': [ELEMENT[int(x)] for x in numbers],
        }
        out.setdefault(slug, []).append(rec)

    data_dir = ROOT / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    for slug, recs in out.items():
        recs.sort(key=lambda x: x['issue'])
        (data_dir / f'{slug}.json').write_text(
            json.dumps(recs, ensure_ascii=False, indent=1), encoding='utf-8')
        with open(data_dir / f'{slug}.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(['issue', 'date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'special',
                        'z1', 'z2', 'z3', 'z4', 'z5', 'z6', 'z_special',
                        'w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w_special',
                        'e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e_special'])
            for rec in recs:
                w.writerow([rec['issue'], rec['date'], *rec['numbers'], rec['special'],
                            *rec['zodiac'], *rec['wave'], *rec['element']])
        print(f'{slug}: {len(recs)} draws, {recs[0]["issue"]}..{recs[-1]["issue"]}')
    print(f'wave mismatches vs fixed table: {wave_mismatch}')
    print(f'zodiac(2026) mismatches vs fixed table: {zodiac2026_mismatch}')


if __name__ == '__main__':
    main()
