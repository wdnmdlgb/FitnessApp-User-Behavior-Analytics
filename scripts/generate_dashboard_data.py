"""
生成交互式数据看板所需的聚合数据（JSON格式，内嵌到HTML中）
"""
import pandas as pd
import json
import os

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析"
data_dir = os.path.join(base_dir, "data")

df_users = pd.read_csv(os.path.join(data_dir, 'cleaned_user_info.csv'))
df_activity = pd.read_csv(os.path.join(data_dir, 'cleaned_user_daily_activity.csv'))

df_users['registration_date'] = pd.to_datetime(df_users['registration_date'])
df_activity['activity_date'] = pd.to_datetime(df_activity['activity_date'])

# 合并
df = df_activity.merge(df_users[['user_id', 'country', 'gender', 'age', 'is_premium', 'acquisition_channel']], on='user_id', how='left')

# 1. DAU趋势（按日期）
dau_trend = df.groupby('activity_date')['user_id'].nunique().reset_index()
dau_trend['date'] = dau_trend['activity_date'].dt.strftime('%Y-%m-%d')
dau_data = [{'date': r['date'], 'dau': int(r['user_id'])} for _, r in dau_trend.iterrows()]

# 2. 国家分布
country_data = df.groupby('country')['user_id'].nunique().sort_values(ascending=False).reset_index()
country_list = [{'country': r['country'], 'users': int(r['user_id'])} for _, r in country_data.iterrows()]

# 3. 付费vs免费对比
premium_compare = df.groupby('is_premium').agg({
    'session_duration_min': 'mean',
    'workouts_completed': 'mean',
    'calories_burned': 'mean',
    'ai_coach_used': 'mean',
    'training_plan_accessed': 'mean'
}).round(2).reset_index()
premium_data = []
for _, r in premium_compare.iterrows():
    premium_data.append({
        'type': '付费用户' if r['is_premium'] == 1 else '免费用户',
        'session_duration': float(r['session_duration_min']),
        'workouts': float(r['workouts_completed']),
        'calories': float(r['calories_burned']),
        'ai_usage': float(r['ai_coach_used']),
        'plan_usage': float(r['training_plan_accessed'])
    })

# 4. 功能使用率
feature_data = [
    {'feature': 'AI教练', 'usage': round(df['ai_coach_used'].mean() * 100, 1)},
    {'feature': '训练计划', 'usage': round(df['training_plan_accessed'].mean() * 100, 1)},
    {'feature': '步数追踪', 'usage': round((df['steps_recorded'] > 0).mean() * 100, 1)}
]

# 5. 周内活跃度
weekday_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
df['weekday'] = df['activity_date'].dt.dayofweek
weekday_data = df.groupby('weekday')['user_id'].count().reindex(range(7)).reset_index()
weekday_list = [{'day': weekday_map[r['weekday']], 'count': int(r['user_id'])} for _, r in weekday_data.iterrows()]

# 6. 核心指标
metrics = {
    'total_users': int(len(df_users)),
    'total_records': int(len(df_activity)),
    'avg_dau': int(dau_trend['user_id'].mean()),
    'max_dau': int(dau_trend['user_id'].max()),
    'premium_rate': round(df_users['is_premium'].mean() * 100, 1),
    'avg_session': round(df['session_duration_min'].mean(), 1),
    'avg_workouts': round(df['workouts_completed'].mean(), 2),
    'ai_usage': round(df['ai_coach_used'].mean() * 100, 1),
    'plan_usage': round(df['training_plan_accessed'].mean() * 100, 1)
}

# 7. 按国家的详细数据（用于筛选联动）
country_detail = []
for country in df['country'].unique():
    cdf = df[df['country'] == country]
    country_detail.append({
        'country': country,
        'users': int(cdf['user_id'].nunique()),
        'avg_session': round(cdf['session_duration_min'].mean(), 1),
        'avg_workouts': round(cdf['workouts_completed'].mean(), 2),
        'premium_rate': round(cdf['is_premium'].mean() * 100, 1),
        'ai_usage': round(cdf['ai_coach_used'].mean() * 100, 1),
        'dau_series': [
            {'date': d.strftime('%Y-%m-%d'), 'dau': int(g)}
            for d, g in cdf.groupby('activity_date')['user_id'].nunique().items()
        ]
    })

# 输出JSON
output = {
    'metrics': metrics,
    'dau_trend': dau_data,
    'countries': country_list,
    'premium_compare': premium_data,
    'feature_usage': feature_data,
    'weekday_activity': weekday_list,
    'country_detail': country_detail
}

json_path = os.path.join(base_dir, 'dashboard', 'dashboard_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"聚合数据已生成: {json_path}")
print(f"核心指标: {json.dumps(metrics, ensure_ascii=False, indent=2)}")
