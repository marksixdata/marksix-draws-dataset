# Mark Six Draw Dataset | 六合彩开奖数据集

澳门六合彩（Macau Mark Six）与香港六合彩（Hong Kong Mark Six）的完整历史开奖数据，CSV + JSON 两种格式，持续更新。

Complete historical draw results for Macau Mark Six and Hong Kong Mark Six, in CSV and JSON, updated after every draw.

**数据来源 / Source:** [彩友圈 CaiYouQuan](https://cyq369.com) — 澳门/香港六合彩开奖、走势与心水社区。

## 数据内容 / Contents

| 文件 File | 彩种 Lottery | 期数 Draws | 范围 Range |
|---|---|---|---|
| `data/macau.csv` / `data/macau.json` | 澳门六合彩 Macau Mark Six | 2443 | 2020067 – 2026328 |
| `data/hkjc.csv` / `data/hkjc.json` | 香港六合彩 Hong Kong Mark Six | 808 | 2020001 – 2026124 |

更新频率：澳门每晚开奖后、香港每期开奖后同步追加。
Update frequency: appended after each Macau (nightly) and Hong Kong draw.

## 字段说明 / Fields

JSON 每条记录 / Each JSON record:

| 字段 Field | 说明 Description |
|---|---|
| `issue` | 期号 Issue number |
| `date` | 开奖日期 Draw date (YYYY-MM-DD) |
| `draw_time` | 开奖时间 Draw time (Asia/Shanghai) |
| `numbers` | 6 个正码（开奖顺序）Six main numbers, in draw order |
| `special` | 特码 Special number |
| `zodiac` | 7 个号码对应生肖（按开奖当年农历生肖年）Zodiac for each of the 7 numbers, by lunar year of the draw |
| `wave` | 7 个号码波色 `red`/`blue`/`green` Wave colour of each number |
| `wave_zh` | 波色中文：红波/蓝波/绿波 Wave colour in Chinese |
| `element` | 7 个号码五行：金/木/水/火/土 Five-element of each number |

CSV 列：`issue,date,n1..n6,special,z1..z6,z_special,w1..w6,w_special,e1..e6,e_special`
（n=号码，z=生肖，w=波色，e=五行；special 为特码对应列）

## 号码属性对照 / Number attributes

- 波色 Wave: 红波 Red 17 个、蓝波 Blue 16 个、绿波 Green 16 个（32 号为绿波）
- 生肖按农历年轮换，数据集中每期生肖均为开奖当年的实际对应生肖
- 五行 Five elements: 金 10 / 木 10 / 水 9 / 火 12 / 土 8

## 使用示例 / Usage

```python
import json, urllib.request
# 本地文件 / local file
data = json.load(open('data/macau.json', encoding='utf-8'))
latest = data[-1]
print(latest['issue'], latest['numbers'], '+', latest['special'])
```

## 引用 / Citation

使用本数据集时请注明来源：
Please cite the source when using this dataset:

> 数据来源：彩友圈 https://cyq369.com

## 许可 / License

[CC BY 4.0](LICENSE) — 可自由使用、修改、分发（含商业用途），须注明来源。
Free to use, modify and redistribute (including commercially) with attribution.

## 免责声明 / Disclaimer

本数据集为历史开奖记录整理，仅供数据分析与学习研究，不构成任何投注建议。开奖结果以官方公布为准。
Historical records for analysis and research only. Not betting advice. Official results prevail.
