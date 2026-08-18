# 数据集说明

## 数据来源
本数据集基于AI健身APP（如Freeletics类产品）的真实业务逻辑生成，用于数据分析练习。
字段设计参考公开的健身APP用户行为研究和行业基准数据。

## 表1: raw_user_info.csv（用户信息表）
- 记录数: 3000
- 字段:
  - user_id: 用户唯一ID
  - country: 注册国家（欧洲10国）
  - gender: 性别
  - age: 年龄
  - registration_date: 注册日期
  - acquisition_channel: 获取渠道
  - is_premium: 是否付费会员（1=是, 0=否）

## 表2: raw_user_daily_activity.csv（用户每日行为表）
- 记录数: 48754
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
2026-01-01 至 2026-03-01，共60天

## 数据特征
- 付费用户活跃度显著高于免费用户
- 新用户注册首周活跃度高，之后自然衰减
- 不同国家、获取渠道的用户留存和付费转化存在差异
- 包含真实业务中的缺失值场景（步数未开启=0）
