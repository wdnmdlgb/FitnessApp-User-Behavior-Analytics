"""
健身APP用户行为数据分析 - 数据清洗与探索性分析
Data Cleaning & Exploratory Data Analysis
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析"
data_dir = os.path.join(base_dir, "data")
dashboard_dir = os.path.join(base_dir, "dashboard")
os.makedirs(dashboard_dir, exist_ok=True)

# ========== 1. 数据读取 ==========
print("=" * 60)
print("1. 数据读取")
print("=" * 60)
df_users = pd.read_csv(os.path.join(data_dir, 'raw_user_info.csv'))
df_activity = pd.read_csv(os.path.join(data_dir, 'raw_user_daily_activity.csv'))

print(f"用户表: {df_users.shape[0]} 行, {df_users.shape[1]} 列")
print(f"行为表: {df_activity.shape[0]} 行, {df_activity.shape[1]} 列")

# ========== 2. 数据清洗 ==========
print("\n" + "=" * 60)
print("2. 数据清洗")
print("=" * 60)

# 2.1 检查缺失值
print("\n用户表缺失值:")
print(df_users.isnull().sum())
print("\n行为表缺失值:")
print(df_activity.isnull().sum())

# 2.2 日期格式转换
df_users['registration_date'] = pd.to_datetime(df_users['registration_date'])
df_activity['activity_date'] = pd.to_datetime(df_activity['activity_date'])

# 2.3 去除重复记录
before = len(df_activity)
df_activity = df_activity.drop_duplicates(subset=['user_id', 'activity_date'])
after = len(df_activity)
print(f"\n去除重复记录: {before - after} 条")

# 2.4 异常值处理 - 会话时长上限300分钟
df_activity.loc[df_activity['session_duration_min'] > 300, 'session_duration_min'] = 300
# 卡路里上限2000
df_activity.loc[df_activity['calories_burned'] > 2000, 'calories_burned'] = 2000

# 2.5 衍生字段
# 用户生命周期天数
df_activity = df_activity.merge(df_users[['user_id', 'registration_date']], on='user_id', how='left')
df_activity['days_since_reg'] = (df_activity['activity_date'] - df_activity['registration_date']).dt.days
df_activity['week_number'] = df_activity['activity_date'].dt.isocalendar().week.astype(int)
df_activity['day_of_week'] = df_activity['activity_date'].dt.day_name()

# 是否周末
df_activity['is_weekend'] = df_activity['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)

# 保存清洗后数据
df_users.to_csv(os.path.join(data_dir, 'cleaned_user_info.csv'), index=False, encoding='utf-8-sig')
df_activity.to_csv(os.path.join(data_dir, 'cleaned_user_daily_activity.csv'), index=False, encoding='utf-8-sig')
print(f"\n清洗后用户表: {len(df_users)} 条")
print(f"清洗后行为表: {len(df_activity)} 条")
print("清洗后数据已保存")

# ========== 3. 核心指标计算 ==========
print("\n" + "=" * 60)
print("3. 核心指标计算")
print("=" * 60)

# 3.1 整体DAU趋势
daily_active = df_activity.groupby('activity_date')['user_id'].nunique().reset_index()
daily_active.columns = ['date', 'dau']
print(f"\n平均DAU: {daily_active['dau'].mean():.0f}")
print(f"最高DAU: {daily_active['dau'].max()}")
print(f"最低DAU: {daily_active['dau'].min()}")

# 3.2 留存率计算（注册后7日/30日留存）
def calc_retention(df_act, df_usr, day_n):
    """计算注册后第N天留存率"""
    retained = 0
    total = 0
    for _, user in df_usr.iterrows():
        uid = user['user_id']
        reg_date = user['registration_date']
        target_date = reg_date + pd.Timedelta(days=day_n)
        # 检查用户是否在目标日期前后3天内活跃（放宽窗口）
        user_activities = df_act[df_act['user_id'] == uid]['activity_date']
        if len(user_activities) > 0:
            total += 1
            if any(abs((d - target_date).days) <= 1 for d in user_activities):
                retained += 1
    return retained / total if total > 0 else 0

# 抽样计算留存（为了速度，取500用户样本）
sample_users = df_users.sample(n=min(500, len(df_users)), random_state=42)
retention_7d = calc_retention(df_activity, sample_users, 7)
retention_30d = calc_retention(df_activity, sample_users, 30)
print(f"\n7日留存率: {retention_7d:.1%}")
print(f"30日留存率: {retention_30d:.1%}")

# 3.3 付费 vs 免费用户行为对比
premium_stats = df_activity.merge(df_users[['user_id', 'is_premium']], on='user_id')
premium_compare = premium_stats.groupby('is_premium').agg({
    'session_duration_min': 'mean',
    'workouts_completed': 'mean',
    'ai_coach_used': 'mean',
    'training_plan_accessed': 'mean',
    'calories_burned': 'mean'
}).round(2)
premium_compare.index = ['免费用户', '付费用户']
print("\n付费 vs 免费用户行为对比:")
print(premium_compare)

# 3.4 国家维度分析
country_stats = df_activity.merge(df_users[['user_id', 'country']], on='user_id')
country_dau = country_stats.groupby('country')['user_id'].nunique().sort_values(ascending=False)
print("\n各国活跃用户数Top5:")
print(country_dau.head())

# 3.5 功能使用率
ai_usage_rate = df_activity['ai_coach_used'].mean()
plan_usage_rate = df_activity['training_plan_accessed'].mean()
print(f"\nAI教练功能使用率: {ai_usage_rate:.1%}")
print(f"训练计划访问率: {plan_usage_rate:.1%}")

# ========== 4. 数据可视化 ==========
print("\n" + "=" * 60)
print("4. 数据可视化")
print("=" * 60)

# 图1: DAU趋势
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(daily_active['date'], daily_active['dau'], color='#2F5496', linewidth=2)
ax.fill_between(daily_active['date'], daily_active['dau'], alpha=0.15, color='#2F5496')
ax.set_title('健身APP日活跃用户(DAU)趋势', fontsize=14, fontweight='bold')
ax.set_ylabel('活跃用户数')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(dashboard_dir, '01_dau_trend.png'), dpi=150, facecolor='white')
plt.close()
print("图1: DAU趋势图已保存")

# 图2: 付费vs免费用户对比
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
metrics = ['session_duration_min', 'workouts_completed', 'calories_burned']
titles = ['平均会话时长(分钟)', '平均完成训练次数', '平均消耗卡路里']
for i, (metric, title) in enumerate(zip(metrics, titles)):
    free_val = premium_compare.loc['免费用户', metric]
    premium_val = premium_compare.loc['付费用户', metric]
    axes[i].bar(['免费用户', '付费用户'], [free_val, premium_val], color=['#85CDCA', '#2F5496'])
    axes[i].set_title(title, fontsize=12, fontweight='bold')
    axes[i].grid(axis='y', alpha=0.3)
    for j, v in enumerate([free_val, premium_val]):
        axes[i].text(j, v, f'{v:.1f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(dashboard_dir, '02_premium_vs_free.png'), dpi=150, facecolor='white')
plt.close()
print("图2: 付费vs免费对比图已保存")

# 图3: 各国活跃用户分布
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(country_dau)))
ax.barh(country_dau.index[::-1], country_dau.values[::-1], color=colors)
ax.set_title('各国活跃用户数分布', fontsize=14, fontweight='bold')
ax.set_xlabel('活跃用户数')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(country_dau.values[::-1]):
    ax.text(v, i, f' {v}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(dashboard_dir, '03_country_distribution.png'), dpi=150, facecolor='white')
plt.close()
print("图3: 国家分布图已保存")

# 图4: 功能使用率
fig, ax = plt.subplots(figsize=(8, 5))
features = ['AI教练', '训练计划', '步数追踪']
rates = [ai_usage_rate, plan_usage_rate, (df_activity['steps_recorded'] > 0).mean()]
bars = ax.bar(features, rates, color=['#2F5496', '#E8A87C', '#85CDCA'])
ax.set_title('核心功能使用率', fontsize=14, fontweight='bold')
ax.set_ylabel('使用率')
ax.set_ylim(0, 1)
ax.grid(axis='y', alpha=0.3)
for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width()/2, rate, f'{rate:.1%}', ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(dashboard_dir, '04_feature_usage.png'), dpi=150, facecolor='white')
plt.close()
print("图4: 功能使用率图已保存")

# 图5: 周内活跃度分布
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_activity = df_activity.groupby('day_of_week')['user_id'].count().reindex(weekday_order)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(weekday_activity.index, weekday_activity.values, marker='o', color='#2F5496', linewidth=2)
ax.fill_between(range(7), weekday_activity.values, alpha=0.15, color='#2F5496')
ax.set_title('周内活跃度分布', fontsize=14, fontweight='bold')
ax.set_ylabel('活跃记录数')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(dashboard_dir, '05_weekday_activity.png'), dpi=150, facecolor='white')
plt.close()
print("图5: 周内活跃度图已保存")

# 保存统计结果
stats_summary = {
    'total_users': len(df_users),
    'total_activity_records': len(df_activity),
    'avg_dau': round(daily_active['dau'].mean()),
    'retention_7d': round(retention_7d, 4),
    'retention_30d': round(retention_30d, 4),
    'premium_rate': round(df_users['is_premium'].mean(), 4),
    'ai_coach_usage': round(ai_usage_rate, 4),
    'training_plan_usage': round(plan_usage_rate, 4),
    'avg_session_duration': round(df_activity['session_duration_min'].mean(), 1),
    'avg_workouts_per_day': round(df_activity['workouts_completed'].mean(), 2)
}
pd.Series(stats_summary).to_csv(os.path.join(data_dir, 'key_metrics.csv'), header=['value'])
print("\n核心指标已保存到 key_metrics.csv")

print("\n" + "=" * 60)
print("数据清洗与分析完成！")
print("=" * 60)
