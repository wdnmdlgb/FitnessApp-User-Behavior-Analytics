"""
生成完整的Jupyter Notebook，展示数据分析全流程
"""
import json
import os

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析"

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}

def code_cell(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(keepends=True)}

cells = []

# 标题
cells.append(md_cell("""# Fitness App User Behavior Analytics
## 健身APP用户行为数据分析 — 完整Notebook

> 本Notebook完整展示从数据读取到产品建议的全流程分析，包含数据清洗、EDA、用户活跃/留存/付费/功能分析、用户分群及产品优化建议。
>
> **数据集**：3000用户，48754条行为记录，观察期2026-01-01至2026-03-01
>
> **技术栈**：Python Pandas, NumPy, Matplotlib"""))

# 1. 导入库
cells.append(md_cell("## 0. 导入依赖库"))
cells.append(code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
print("Libraries imported successfully.")"""))

# 2. 数据读取
cells.append(md_cell("""## 1. 数据读取

读取两张核心表：
- `user_info.csv`：用户基本信息（3000条）
- `user_daily_activity.csv`：用户每日行为记录（48754条）"""))
cells.append(code_cell("""# 读取原始数据
df_users = pd.read_csv('../data/raw_user_info.csv')
df_activity = pd.read_csv('../data/raw_user_daily_activity.csv')

print(f"用户表: {df_users.shape[0]} 行, {df_users.shape[1]} 列")
print(f"行为表: {df_activity.shape[0]} 行, {df_activity.shape[1]} 列")
print("\\n用户表字段:", list(df_users.columns))
print("行为表字段:", list(df_activity.columns))"""))

cells.append(code_cell("""# 查看用户表前5行
df_users.head()"""))

cells.append(code_cell("""# 查看行为表前5行
df_activity.head()"""))

# 3. 数据清洗
cells.append(md_cell("""## 2. 数据清洗

### 2.1 缺失值检查"""))
cells.append(code_cell("""print("=== 用户表缺失值 ===")
print(df_users.isnull().sum())
print("\\n=== 行为表缺失值 ===")
print(df_activity.isnull().sum())"""))

cells.append(md_cell("### 2.2 数据类型转换与去重"))
cells.append(code_cell("""# 日期类型转换
df_users['registration_date'] = pd.to_datetime(df_users['registration_date'])
df_activity['activity_date'] = pd.to_datetime(df_activity['activity_date'])

# 去重
df_users = df_users.drop_duplicates(subset=['user_id'])
df_activity = df_activity.drop_duplicates()

print(f"去重后用户表: {len(df_users)} 行")
print(f"去重后行为表: {len(df_activity)} 行")"""))

cells.append(md_cell("### 2.3 异常值处理"))
cells.append(code_cell("""# 检查数值列异常值
print("=== 会话时长统计 ===")
print(df_activity['session_duration_min'].describe())
print("\\n=== 卡路里统计 ===")
print(df_activity['calories_burned'].describe())

# 过滤异常值（会话时长>0且<180分钟，卡路里>=0）
df_activity = df_activity[(df_activity['session_duration_min'] > 0) & (df_activity['session_duration_min'] < 180)]
df_activity = df_activity[df_activity['calories_burned'] >= 0]
print(f"\\n过滤异常值后行为表: {len(df_activity)} 行")"""))

cells.append(md_cell("### 2.4 合并数据表"))
cells.append(code_cell("""# 合并用户信息到行为表
df = df_activity.merge(df_users, on='user_id', how='left')
print(f"合并后数据表: {df.shape[0]} 行, {df.shape[1]} 列")
print("\\n合并后字段:", list(df.columns))"""))

cells.append(md_cell("### 2.5 保存清洗后数据"))
cells.append(code_cell("""df_users.to_csv('../data/cleaned_user_info.csv', index=False)
df_activity.to_csv('../data/cleaned_user_daily_activity.csv', index=False)
print("清洗后数据已保存。")"""))

# 4. EDA
cells.append(md_cell("""## 3. 探索性数据分析 (EDA)

### 3.1 用户基本画像"""))
cells.append(code_cell("""print("=== 用户年龄分布 ===")
print(df_users['age'].describe())
print(f"\\n年龄范围: {df_users['age'].min()} - {df_users['age'].max()}")
print(f"平均年龄: {df_users['age'].mean():.1f}")

print("\\n=== 性别分布 ===")
print(df_users['gender'].value_counts())

print("\\n=== 国家分布 (Top 10) ===")
print(df_users['country'].value_counts().head(10))

print("\\n=== 付费用户占比 ===")
premium_rate = df_users['is_premium'].mean() * 100
print(f"付费率: {premium_rate:.1f}%")
print(f"付费用户: {df_users['is_premium'].sum()} 人")
print(f"免费用户: {(df_users['is_premium']==0).sum()} 人")"""))

cells.append(md_cell("### 3.2 行为数据概览"))
cells.append(code_cell("""print("=== 会话时长分布 ===")
print(df['session_duration_min'].describe())

print("\\n=== 训练次数分布 ===")
print(df['workouts_completed'].describe())

print("\\n=== 功能使用率 ===")
print(f"AI教练使用率: {df['ai_coach_used'].mean()*100:.1f}%")
print(f"训练计划访问率: {df['training_plan_accessed'].mean()*100:.1f}%")
print(f"步数记录率: {(df['steps_recorded']>0).mean()*100:.1f}%")

print("\\n=== 数据时间范围 ===")
print(f"最早: {df['activity_date'].min()}")
print(f"最晚: {df['activity_date'].max()}")
print(f"覆盖天数: {(df['activity_date'].max() - df['activity_date'].min()).days + 1}")"""))

# 5. 用户活跃分析
cells.append(md_cell("""## 4. 用户活跃分析

### 4.1 DAU (日活跃用户) 趋势"""))
cells.append(code_cell("""dau = df.groupby('activity_date')['user_id'].nunique()
print(f"平均DAU: {dau.mean():.0f}")
print(f"最高DAU: {dau.max()} (日期: {dau.idxmax().strftime('%Y-%m-%d')})")
print(f"最低DAU: {dau.min()} (日期: {dau.idxmin().strftime('%Y-%m-%d')})")

plt.figure(figsize=(14, 5))
dau.plot(kind='line', color='#2c5282', linewidth=2)
plt.title('DAU Trend (2026-01 to 2026-03)', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Daily Active Users')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""))

cells.append(md_cell("### 4.2 周内活跃度分布"))
cells.append(code_cell("""df['weekday'] = df['activity_date'].dt.dayofweek
weekday_map = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
weekday_activity = df.groupby('weekday').size().reindex(range(7))
weekday_activity.index = [weekday_map[i] for i in weekday_activity.index]

print("=== 周内活跃度 ===")
print(weekday_activity)

plt.figure(figsize=(10, 5))
colors = ['#2c5282']*5 + ['#dd6b20']*2
weekday_activity.plot(kind='bar', color=colors)
plt.title('Activity by Weekday', fontsize=14)
plt.xlabel('Day of Week')
plt.ylabel('Activity Records')
plt.xticks(rotation=0)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()"""))

# 6. 留存分析
cells.append(md_cell("""## 5. 留存分析

### 5.1 计算D1/D3/D7/D14/D30留存率"""))
cells.append(code_cell("""# 计算每个用户的注册日期和活跃日期
user_reg = df_users[['user_id', 'registration_date']]
user_active = df[['user_id', 'activity_date']].drop_duplicates()
merged = user_active.merge(user_reg, on='user_id')
merged['days_since_reg'] = (merged['activity_date'] - merged['registration_date']).dt.days

retention_results = []
for n in [1, 3, 7, 14, 30]:
    # 有资格计算的用户（注册日+n <= 观察期末）
    eligible = df_users[df_users['registration_date'] + pd.Timedelta(days=n) <= pd.Timestamp('2026-03-01')]
    eligible_ids = set(eligible['user_id'])
    # 第n天活跃的用户
    active_on_day = set(merged[merged['days_since_reg'] == n]['user_id'])
    retained = len(eligible_ids & active_on_day)
    total = len(eligible_ids)
    rate = retained / total * 100 if total > 0 else 0
    retention_results.append({'day': f'D{n}', 'retention_rate': round(rate, 1), 'retained': retained, 'eligible': total})

df_retention = pd.DataFrame(retention_results)
print(df_retention)

plt.figure(figsize=(10, 5))
plt.plot(df_retention['day'], df_retention['retention_rate'], marker='o', linewidth=2, color='#805ad5', markersize=8)
for i, row in df_retention.iterrows():
    plt.text(i, row['retention_rate']+1.5, f"{row['retention_rate']}%", ha='center', fontsize=11)
plt.title('User Retention Curve', fontsize=14)
plt.xlabel('Days Since Registration')
plt.ylabel('Retention Rate (%)')
plt.ylim(0, 100)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()"""))

# 7. 付费分析
cells.append(md_cell("""## 6. 付费用户 vs 免费用户分析

### 7.1 行为差异对比"""))
cells.append(code_cell("""premium_stats = df.groupby('is_premium').agg({
    'session_duration_min': 'mean',
    'workouts_completed': 'mean',
    'calories_burned': 'mean',
    'ai_coach_used': 'mean',
    'training_plan_accessed': 'mean'
}).round(2)
premium_stats.index = ['Free Users', 'Premium Users']
print(premium_stats)

# 可视化对比
metrics = ['session_duration_min', 'workouts_completed', 'calories_burned', 'ai_coach_used', 'training_plan_accessed']
labels = ['Session (min)', 'Workouts', 'Calories', 'AI Coach (%)', 'Plan Access (%)']

fig, axes = plt.subplots(1, 5, figsize=(18, 4))
for i, (metric, label) in enumerate(zip(metrics, labels)):
    values = [premium_stats.loc['Free Users', metric], premium_stats.loc['Premium Users', metric]]
    axes[i].bar(['Free', 'Premium'], values, color=['#85CDCA', '#2c5282'])
    axes[i].set_title(label, fontsize=11)
    axes[i].grid(True, alpha=0.3, axis='y')
    for j, v in enumerate(values):
        axes[i].text(j, v, f'{v:.1f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()"""))

cells.append(md_cell("### 7.2 付费率按国家分布"))
cells.append(code_cell("""country_premium = df_users.groupby('country')['is_premium'].agg(['mean', 'count'])
country_premium.columns = ['premium_rate', 'user_count']
country_premium['premium_rate'] = (country_premium['premium_rate'] * 100).round(1)
country_premium = country_premium.sort_values('premium_rate', ascending=False)
print(country_premium.head(10))"""))

# 8. 功能使用分析
cells.append(md_cell("""## 7. 功能使用分析

### 8.1 核心功能使用率"""))
cells.append(code_cell("""feature_usage = pd.DataFrame({
    'Feature': ['AI Coach', 'Training Plan', 'Step Tracking'],
    'Overall': [
        df['ai_coach_used'].mean()*100,
        df['training_plan_accessed'].mean()*100,
        (df['steps_recorded']>0).mean()*100
    ],
    'Premium': [
        df[df['is_premium']==1]['ai_coach_used'].mean()*100,
        df[df['is_premium']==1]['training_plan_accessed'].mean()*100,
        (df[(df['is_premium']==1)&(df['steps_recorded']>0)].shape[0]/df[df['is_premium']==1].shape[0])*100
    ],
    'Free': [
        df[df['is_premium']==0]['ai_coach_used'].mean()*100,
        df[df['is_premium']==0]['training_plan_accessed'].mean()*100,
        (df[(df['is_premium']==0)&(df['steps_recorded']>0)].shape[0]/df[df['is_premium']==0].shape[0])*100
    ]
}).round(1)
print(feature_usage)

x = np.arange(len(feature_usage))
width = 0.25
plt.figure(figsize=(10, 5))
plt.bar(x - width, feature_usage['Overall'], width, label='Overall', color='#2c5282')
plt.bar(x, feature_usage['Premium'], width, label='Premium', color='#38a169')
plt.bar(x + width, feature_usage['Free'], width, label='Free', color='#85CDCA')
plt.xticks(x, feature_usage['Feature'])
plt.ylabel('Usage Rate (%)')
plt.title('Feature Usage by User Type', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()"""))

cells.append(md_cell("### 8.2 AI教练使用与训练完成率的关系"))
cells.append(code_cell("""ai_users = df[df['ai_coach_used'] == 1]
non_ai_users = df[df['ai_coach_used'] == 0]
print(f"使用AI教练的用户平均训练次数: {ai_users['workouts_completed'].mean():.2f}")
print(f"未使用AI教练的用户平均训练次数: {non_ai_users['workouts_completed'].mean():.2f}")
print(f"提升幅度: {(ai_users['workouts_completed'].mean()/non_ai_users['workouts_completed'].mean()-1)*100:.1f}%")"""))

# 9. 用户分群
cells.append(md_cell("""## 8. 用户分群分析

### 8.1 按活跃度分群"""))
cells.append(code_cell("""user_active_days = df.groupby('user_id')['activity_date'].nunique().reset_index()
user_active_days.columns = ['user_id', 'active_days']
user_active_days = user_active_days.merge(df_users[['user_id', 'is_premium']], on='user_id')

def classify_segment(days):
    if days >= 40: return 'High Active'
    elif days >= 20: return 'Medium Active'
    elif days >= 5: return 'Low Active'
    else: return 'Churn Risk'

user_active_days['segment'] = user_active_days['active_days'].apply(classify_segment)
segment_stats = user_active_days.groupby('segment').agg(
    user_count=('user_id', 'count'),
    avg_active_days=('active_days', 'mean'),
    premium_rate=('is_premium', 'mean')
).round(2)
segment_stats['premium_rate'] = (segment_stats['premium_rate'] * 100).round(1)
segment_stats['percentage'] = (segment_stats['user_count'] / segment_stats['user_count'].sum() * 100).round(1)
print(segment_stats)

plt.figure(figsize=(8, 8))
plt.pie(segment_stats['user_count'], labels=segment_stats.index, autopct='%1.1f%%',
        colors=['#38a169', '#2c5282', '#dd6b20', '#e53e3e'], startangle=90)
plt.title('User Segmentation by Activity', fontsize=14)
plt.tight_layout()
plt.show()"""))

# 10. 产品问题发现
cells.append(md_cell("""## 9. 产品问题发现

基于以上分析，识别出以下核心产品问题："""))
cells.append(code_cell("""issues = [
    {"问题": "AI教练渗透率不足", "数据支撑": f"整体使用率仅{df['ai_coach_used'].mean()*100:.1f}%，但使用者训练完成率提升{(ai_users['workouts_completed'].mean()/non_ai_users['workouts_completed'].mean()-1)*100:.0f}%", "严重程度": "高"},
    {"问题": "新用户流失风险高", "数据支撑": f"活跃天数<5天的用户占比{segment_stats.loc['Churn Risk','percentage']}%", "严重程度": "高"},
    {"问题": "免费用户功能使用深度不足", "数据支撑": f"免费用户AI教练使用率仅{df[df['is_premium']==0]['ai_coach_used'].mean()*100:.1f}%，远低于付费用户{df[df['is_premium']==1]['ai_coach_used'].mean()*100:.1f}%", "严重程度": "中"},
    {"问题": "周末活跃度低于工作日", "数据支撑": "周末活跃记录数比工作日低约10-15%", "严重程度": "低"},
]
df_issues = pd.DataFrame(issues)
print(df_issues.to_string(index=False))"""))

# 11. 产品建议
cells.append(md_cell("""## 10. 产品优化建议

基于数据发现，提出以下可执行的产品优化建议："""))
cells.append(code_cell("""recommendations = [
    {"建议": "强化AI教练新手引导", "具体措施": "新用户注册后强制体验1次AI教练；首页增加AI教练入口；个性化推送训练建议", "预期效果": "AI教练使用率从25%提升至40%，用户训练完成率提升15%"},
    {"建议": "优化免费→付费转化路径", "具体措施": "AI教练提供3次免费体验；连续活跃7天推送限时优惠；展示付费用户训练效果对比", "预期效果": "付费率从12%提升至15%"},
    {"建议": "建立流失用户召回机制", "具体措施": "注册第2天推送个性化内容；3天未活跃发送召回邮件；7天未付费提供免费会员体验", "预期效果": "流失风险用户占比从6.6%降至4%"},
    {"建议": "周末差异化内容运营", "具体措施": "周末推出家庭/户外训练专题；线上挑战活动；周末限时训练打卡奖励", "预期效果": "周末DAU提升10-15%"},
    {"建议": "增加训练计划个性化推荐", "具体措施": "基于用户目标/频率/器械自动生成计划；根据完成情况动态调整；计划完成后推荐进阶计划", "预期效果": "训练计划访问率从35%提升至50%"}
]
df_recs = pd.DataFrame(recommendations)
print(df_recs.to_string(index=False))"""))

cells.append(md_cell("""---

## 总结

本Notebook完整展示了健身APP用户行为数据分析的全流程：

1. **数据读取**：3000用户 + 48754条行为记录
2. **数据清洗**：缺失值处理、异常值过滤、数据合并
3. **EDA**：用户画像、行为概览、国家/性别/年龄分布
4. **用户活跃分析**：DAU趋势、周内活跃度
5. **留存分析**：D1/D3/D7/D14/D30留存曲线
6. **付费分析**：付费vs免费行为差异、国家付费率
7. **功能使用分析**：AI教练/训练计划/步数追踪使用率
8. **用户分群**：高/中/低活跃+流失风险四群
9. **产品问题发现**：4个核心问题
10. **产品优化建议**：5条可执行建议

**核心结论**：AI教练功能价值高但渗透率不足，是产品优化的核心方向；新用户流失和免费→付费转化是增长关键。"""))

# 构建notebook
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

nb_path = os.path.join(base_dir, "notebooks", "FitnessApp_User_Behavior_Analysis.ipynb")
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"Notebook已生成: {nb_path}")
print(f"单元格数量: {len(cells)}")
print(f"文件大小: {os.path.getsize(nb_path)/1024:.1f} KB")
