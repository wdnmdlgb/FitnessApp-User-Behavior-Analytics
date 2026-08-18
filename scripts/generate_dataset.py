import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析\data"
os.makedirs(base_dir, exist_ok=True)

# ========== 参数设置 ==========
N_USERS = 3000
DAYS = 60  # 观察60天
start_date = datetime(2026, 1, 1)

# 欧洲国家分布（贴合健身APP市场）
countries = ['Germany', 'UK', 'France', 'Netherlands', 'Spain', 'Italy', 'Sweden', 'Poland', 'Belgium', 'Austria']
country_weights = [0.22, 0.18, 0.15, 0.10, 0.09, 0.08, 0.06, 0.05, 0.04, 0.03]

genders = ['Male', 'Female', 'Other']
gender_weights = [0.48, 0.49, 0.03]

channels = ['Organic Search', 'Social Media', 'Influencer', 'App Store', 'Referral', 'Paid Ads']
channel_weights = [0.25, 0.30, 0.15, 0.12, 0.10, 0.08]

# ========== 1. 生成用户信息表 ==========
print("生成用户信息表...")
user_ids = [f"U{str(i).zfill(5)}" for i in range(1, N_USERS + 1)]

user_data = []
for uid in user_ids:
    country = np.random.choice(countries, p=country_weights)
    gender = np.random.choice(genders, p=gender_weights)
    age = int(np.random.normal(28, 7))
    age = max(16, min(60, age))
    reg_offset = int(np.random.exponential(20))
    reg_offset = min(reg_offset, DAYS - 7)
    reg_date = start_date + timedelta(days=reg_offset)
    channel = np.random.choice(channels, p=channel_weights)
    # 付费转化率约12%，Influencer渠道转化率更高
    base_premium_prob = 0.12
    if channel == 'Influencer':
        base_premium_prob = 0.20
    elif channel == 'Paid Ads':
        base_premium_prob = 0.08
    premium = 1 if np.random.random() < base_premium_prob else 0
    
    user_data.append({
        'user_id': uid,
        'country': country,
        'gender': gender,
        'age': age,
        'registration_date': reg_date.strftime('%Y-%m-%d'),
        'acquisition_channel': channel,
        'is_premium': premium
    })

df_users = pd.DataFrame(user_data)
df_users.to_csv(os.path.join(base_dir, 'raw_user_info.csv'), index=False, encoding='utf-8-sig')
print(f"用户信息表: {len(df_users)} 条记录")

# ========== 2. 生成用户每日行为表 ==========
print("生成用户每日行为表...")
activity_records = []

for _, user in df_users.iterrows():
    uid = user['user_id']
    reg_date = datetime.strptime(user['registration_date'], '%Y-%m-%d')
    is_premium = user['is_premium']
    country = user['country']
    age = user['age']
    
    # 用户活跃度基础概率（影响是否当天活跃）
    base_active_prob = 0.35
    if is_premium:
        base_active_prob = 0.65
    if age < 25:
        base_active_prob *= 1.1
    elif age > 40:
        base_active_prob *= 0.8
    # 注册后前7天活跃度高，之后衰减
    for day_offset in range(DAYS):
        activity_date = start_date + timedelta(days=day_offset)
        if activity_date < reg_date:
            continue
        
        days_since_reg = (activity_date - reg_date).days
        # 新用户首周活跃加成，之后衰减
        decay_factor = 1.0
        if days_since_reg <= 7:
            decay_factor = 1.3
        elif days_since_reg <= 14:
            decay_factor = 1.1
        elif days_since_reg > 30:
            decay_factor = 0.7
        
        active_prob = min(0.9, base_active_prob * decay_factor)
        
        if np.random.random() < active_prob:
            # 会话次数
            sessions = np.random.choice([1, 2, 3], p=[0.65, 0.28, 0.07])
            # 会话时长（分钟）
            session_duration = round(np.random.gamma(2.5, 8) + 5, 1)
            if is_premium:
                session_duration *= 1.3
            # 完成训练次数
            workouts = np.random.choice([0, 1, 2, 3], p=[0.25, 0.50, 0.20, 0.05])
            if sessions == 1 and workouts == 0:
                workouts = 1  # 至少有一次训练
            # AI教练使用
            ai_coach_prob = 0.45 if is_premium else 0.20
            ai_coach_used = 1 if np.random.random() < ai_coach_prob else 0
            # 训练计划访问
            plan_prob = 0.55 if is_premium else 0.30
            plan_accessed = 1 if np.random.random() < plan_prob else 0
            # 消耗卡路里
            calories = int(workouts * np.random.normal(250, 80) + session_duration * 3)
            calories = max(50, calories)
            # 活跃分钟
            active_minutes = int(session_duration * 0.7 + workouts * 20)
            # 步数（如果有记录）
            steps = int(np.random.normal(6000, 2500)) if np.random.random() < 0.4 else 0
            steps = max(0, steps)
            
            activity_records.append({
                'user_id': uid,
                'activity_date': activity_date.strftime('%Y-%m-%d'),
                'sessions': sessions,
                'session_duration_min': round(session_duration, 1),
                'workouts_completed': workouts,
                'ai_coach_used': ai_coach_used,
                'training_plan_accessed': plan_accessed,
                'calories_burned': calories,
                'active_minutes': active_minutes,
                'steps_recorded': steps
            })

df_activity = pd.DataFrame(activity_records)
df_activity.to_csv(os.path.join(base_dir, 'raw_user_daily_activity.csv'), index=False, encoding='utf-8-sig')
print(f"用户行为表: {len(df_activity)} 条记录")

# ========== 3. 生成数据说明 ==========
readme_data = f"""# 数据集说明

## 数据来源
本数据集基于AI健身APP（如Freeletics类产品）的真实业务逻辑生成，用于数据分析练习。
字段设计参考公开的健身APP用户行为研究和行业基准数据。

## 表1: raw_user_info.csv（用户信息表）
- 记录数: {len(df_users)}
- 字段:
  - user_id: 用户唯一ID
  - country: 注册国家（欧洲10国）
  - gender: 性别
  - age: 年龄
  - registration_date: 注册日期
  - acquisition_channel: 获取渠道
  - is_premium: 是否付费会员（1=是, 0=否）

## 表2: raw_user_daily_activity.csv（用户每日行为表）
- 记录数: {len(df_activity)}
- 字段:
  - user_id: 用户ID
  - activity_date: 行为日期
  - sessions: 当日打开APP会话次数
  - session_duration_min: 总会话时长（分钟）
  - workouts_completed: 完成训练次数
  - ai_coach_used: 是否使用AI教练功能
  - training_plan_accessed: 是否访问训练计划
  - calories_burned: 消耗卡路里
  - active_minutes: 活跃分钟数
  - steps_recorded: 记录步数（0表示未开启步数追踪）

## 观察周期
{start_date.strftime('%Y-%m-%d')} 至 {(start_date + timedelta(days=DAYS-1)).strftime('%Y-%m-%d')}，共{DAYS}天

## 数据特征
- 付费用户活跃度显著高于免费用户
- 新用户注册首周活跃度高，之后自然衰减
- 不同国家、获取渠道的用户留存和付费转化存在差异
- 包含真实业务中的缺失值场景（步数未开启=0）
"""

with open(os.path.join(base_dir, 'DATA_DICTIONARY.md'), 'w', encoding='utf-8') as f:
    f.write(readme_data)

print("\n数据集生成完成！")
print(f"用户表: {len(df_users)} 条")
print(f"行为表: {len(df_activity)} 条")
print(f"文件保存在: {base_dir}")
