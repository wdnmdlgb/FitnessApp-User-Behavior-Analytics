# 健身APP用户行为数据分析 📊

> Fitness App User Behavior Analytics | Python + SQL + 数据可视化
>
> 个人数据分析项目，求职作品集

---

## 🎯 项目目标

基于AI健身APP（如Freeletics类产品）的用户行为数据，完整跑通**数据获取→清洗→SQL分析→可视化→产品优化建议**的数据分析全流程，挖掘用户活跃、留存、付费转化的核心规律，提出数据驱动的产品迭代方案。

---

## 📖 快速预览

| 文件 | 说明 | 链接 |
|------|------|------|
| 数据分析报告 | 完整分析报告（含5大发现+5条优化建议） | [查看报告](https://github.com/wdnmdlgb/FitnessApp-User-Behavior-Analytics/blob/master/report/数据分析报告.md) |
| SQL业务查询 | 15条真实业务场景SQL | [查看SQL](https://github.com/wdnmdlgb/FitnessApp-User-Behavior-Analytics/blob/master/sql/business_analysis.sql) |
| 数据字典 | 数据集字段说明 | [查看字典](https://github.com/wdnmdlgb/FitnessApp-User-Behavior-Analytics/blob/master/data/DATA_DICTIONARY.md) |

---

## 🛠️ 技术栈

| 工具 | 用途 |
|------|------|
| **Python Pandas** | 数据清洗、缺失值处理、衍生字段计算、统计分析 |
| **SQL** | 15条业务查询，覆盖活跃/留存/付费/功能/分群分析 |
| **Matplotlib** | 5张数据可视化图表 |
| **CSV** | 结构化数据存储 |

---

## 📁 仓库结构

```
FitnessApp-User-Behavior-Analytics/
├── README.md                          # 项目说明
├── .gitignore
├── data/
│   ├── raw_user_info.csv              # 原始用户信息表（3000条）
│   ├── raw_user_daily_activity.csv    # 原始用户行为表（48754条）
│   ├── cleaned_user_info.csv          # 清洗后用户信息
│   ├── cleaned_user_daily_activity.csv # 清洗后行为数据
│   ├── key_metrics.csv                # 核心指标汇总
│   └── DATA_DICTIONARY.md             # 数据字典
├── sql/
│   └── business_analysis.sql          # 15条SQL业务查询
├── dashboard/
│   ├── 01_dau_trend.png               # DAU趋势图
│   ├── 02_premium_vs_free.png         # 付费vs免费对比
│   ├── 03_country_distribution.png    # 国家分布图
│   ├── 04_feature_usage.png           # 功能使用率
│   └── 05_weekday_activity.png        # 周内活跃度
├── report/
│   └── 数据分析报告.md                 # 完整分析报告
└── scripts/
    ├── generate_dataset.py            # 数据集生成脚本
    ├── data_cleaning_analysis.py      # 数据清洗与分析脚本
    └── (可扩展: Jupyter Notebook)
```

---

## 📊 核心指标

| 指标 | 数值 |
|------|------|
| 总用户数 | 3,000 |
| 行为记录数 | 48,754 |
| 平均DAU | 813 |
| 7日留存率 | 81.4% |
| 30日留存率 | 57.6% |
| 付费率 | ~12% |
| 平均会话时长 | 27.5分钟 |
| AI教练使用率 | 25.5% |
| 训练计划访问率 | 34.9% |

---

## 🔍 五大关键发现

### 1. 付费用户活跃度显著高于免费用户
付费用户平均会话时长32.4分钟（+28.6%），AI教练使用率45%（免费用户仅20%），付费意愿与功能深度使用强相关。

### 2. 德国和英国是核心市场
德/英/法三国贡献超50%活跃用户；荷兰用户数第四但付费率最高（15%），是高价值市场。

### 3. AI教练功能渗透率不足
AI教练使用率仅25.5%，但使用者训练完成率提升20%，入口太深和引导不足是主要原因。

### 4. Influencer渠道付费转化率最高
KOL渠道付费转化率20%，是付费广告（8%）的2.5倍，应加大KOL合作投入。

### 5. 约15%用户注册后仅活跃1天
流失风险用户集中在Paid Ads渠道、首次会话时长短的人群，需建立召回机制。

---

## 💡 五条产品优化建议

1. **强化AI教练新手引导**：新用户强制体验+首页入口+个性化推送，目标使用率提升至40%
2. **优化免费→付费转化路径**：AI教练3次免费体验+连续活跃7天推送限时优惠
3. **加大Influencer渠道投入**：将Paid Ads预算30%转移至KOL分层合作
4. **流失用户召回机制**：注册第2天推送+3天未活跃召回+7天未付费免费会员体验
5. **周末差异化内容**：家庭/户外训练专题+线上挑战活动，提升周末DAU 10-15%

---

## 📝 SQL查询覆盖的业务问题

1. 整体核心指标概览（DAU/付费率/会话时长）
2. 各国活跃用户排名及付费率
3. 不同获取渠道的付费转化率
4. 付费vs免费用户行为差异
5. AI教练使用与训练完成率相关性
6. 周内活跃度分布
7. 注册后首周留存曲线
8. 不同年龄段行为差异
9. 高价值用户（Top 10%）识别
10. 训练计划访问与付费转化关系
11. 每日新增注册趋势
12. 用户流失分群分析
13. 会话时长与卡路里分群
14. 各国用户训练强度对比
15. 各渠道用户价值(LTV)估算

---

## 🚀 如何复现

```bash
# 1. 生成数据集
python scripts/generate_dataset.py

# 2. 数据清洗与分析（生成清洗后数据+图表+核心指标）
python scripts/data_cleaning_analysis.py

# 3. 查看SQL查询（可在SQLite/MySQL/PostgreSQL中运行）
# sql/business_analysis.sql
```

---

## ⚠️ 数据说明

本项目数据集基于AI健身APP的真实业务逻辑生成，字段设计参考公开的健身APP用户行为研究和行业基准数据。**非企业内部私有数据**，仅用于数据分析练习和求职作品集展示。

---

## 🔗 关联项目

- [项目1：Gymshark品牌深度研究](https://github.com/wdnmdlgb/Gymshark-Brand-Research) — 欧洲健身服饰DTC品牌竞品分析
- 项目3：欧洲居家健身Ins账号模拟运营 — 海外社媒运营全流程

---

*Made with Python & SQL for portfolio | 2026*
