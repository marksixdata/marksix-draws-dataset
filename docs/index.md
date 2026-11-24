# Mark Six Draw Dataset | 六合彩开奖数据集

澳门六合彩与香港六合彩的历史开奖记录，CSV + JSON 两种格式，每期开奖后追加更新。本页说明数据集的字段、来源、更新频率与下载方式；统计方法与算例见[工具文档](tools.html)。

## 数据概况

数据截至 2026-11-24（以仓库 `data/` 目录实测为准）：

| 彩种 | 期数 | 范围 | 最新一期 |
| --- | --- | --- | --- |
| 澳门六合彩 | 2443 期 | 2020067 期（2020-03-07）— 2026328 期（2026-11-24） | 2026328 期：15、21、31、05、12、47，特码 06 |
| 香港六合彩 | 808 期 | 2020001 期（2020-01-02）— 2026124 期（2026-11-24） | 2026124 期：41、01、28、20、35、26，特码 36 |

每期记录 6 个平码与 1 个特码（共 7 个号码，取值 1–49），并附每个号码的生肖、波色与五行。

## 字段说明

### JSON（每期一条记录）

| 字段 | 说明 |
| --- | --- |
| `issue` | 期号 |
| `date` | 开奖日期（YYYY-MM-DD） |
| `draw_time` | 开奖时间（Asia/Shanghai） |
| `numbers` | 6 个平码（开奖顺序） |
| `special` | 特码 |
| `zodiac` | 7 个号码对应的生肖（按开奖当年农历生肖年） |
| `wave` | 7 个号码的波色，`red` / `blue` / `green` |
| `wave_zh` | 波色中文：红波 / 蓝波 / 绿波 |
| `element` | 7 个号码的五行：金 / 木 / 水 / 火 / 土 |

### CSV（列名）

`issue,date,n1..n6,special,z1..z6,z_special,w1..w6,w_special,e1..e6,e_special`

其中 n = 号码，z = 生肖，w = 波色，e = 五行；`special` 相关列为特码对应的属性。

### 号码属性对照

- 波色：红波 17 个号码、蓝波 16 个、绿波 16 个（32 号为绿波）。
- 生肖按农历年轮换，数据集中每期生肖均为开奖当年的实际对应生肖。
- 五行：金 10 个、木 10 个、水 9 个、火 12 个、土 8 个。

## 数据来源与更新

- 来源：澳门与香港六合彩官方公布的开奖结果整理。本数据集只记录已经公布的开奖结果，不做任何号码推荐。
- 更新频率：澳门每晚开奖后、香港每期开奖后同步追加。澳门固定每晚 21:30 开奖，香港按官方排期。
- 核对：CSV 与 JSON 由同一份记录生成，期数一致（澳门 2443 期、香港 808 期）；最新一期号码与档案站公布一致。

## 下载方式

直接下载单个文件：

- 澳门 CSV：`https://raw.githubusercontent.com/marksixdata/marksix-draws-dataset/main/data/macau.csv`
- 澳门 JSON：`https://raw.githubusercontent.com/marksixdata/marksix-draws-dataset/main/data/macau.json`
- 香港 CSV：`https://raw.githubusercontent.com/marksixdata/marksix-draws-dataset/main/data/hkjc.csv`
- 香港 JSON：`https://raw.githubusercontent.com/marksixdata/marksix-draws-dataset/main/data/hkjc.json`

或克隆整个仓库：

```bash
git clone https://github.com/marksixdata/marksix-draws-dataset.git
```

本地读取示例（Python）：

```python
import json
data = json.load(open('data/macau.json', encoding='utf-8'))
latest = data[-1]
print(latest['issue'], latest['numbers'], '+', latest['special'])
# 2026328 [15, 21, 31, 5, 12, 47] + 6
```

## 相关站点

- [369123](https://369123.cc)：开奖档案站，按期号归档澳门与香港往期开奖记录，可按期号查询、按月浏览，并有近 100 期冷热与遗漏统计。
- [369777](https://369777.cc)：号码工具站，提供号码查询、挑码助手与生肖对照，统计口径与本数据集一致。

## 许可与联系

- 许可：[CC BY 4.0](../LICENSE)，可自由使用、修改、分发（含商业用途），须注明来源。
- 联系：3606700@gmail.com
- 声明：本数据集为历史开奖记录整理，仅供数据分析与学习研究。开奖结果以官方公布为准。
