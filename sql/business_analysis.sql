-- ============================================================
-- 健身APP用户行为数据分析 - SQL业务查询脚本
-- Fitness App User Behavior Analytics - SQL Queries
-- ============================================================
-- 数据表:
--   user_info (user_id, country, gender, age, registration_date, acquisition_channel, is_premium)
--   user_daily_activity (user_id, activity_date, sessions, session_duration_min, 
--                        workouts_completed, ai_coach_used, training_plan_accessed,
--                        calories_burned, active_minutes, steps_recorded)
-- ============================================================

-- Q1: 整体核心指标概览 - 总用户数、平均DAU、付费率、平均会话时长
SELECT 
    (SELECT COUNT(*) FROM user_info) AS total_users,
    (SELECT ROUND(AVG(daily_users), 0) FROM (
        SELECT activity_date, COUNT(DISTINCT user_id) AS daily_users 
        FROM user_daily_activity GROUP BY activity_date
    ) t) AS avg_dau,
    (SELECT ROUND(AVG(is_premium) * 100, 1) FROM user_info) AS premium_rate_pct,
    (SELECT ROUND(AVG(session_duration_min), 1) FROM user_daily_activity) AS avg_session_min;

-- Q2: 各国活跃用户数排名及付费率
SELECT 
    u.country,
    COUNT(DISTINCT a.user_id) AS active_users,
    ROUND(AVG(u.is_premium) * 100, 1) AS premium_rate_pct,
    ROUND(AVG(a.session_duration_min), 1) AS avg_session_min
FROM user_info u
JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY u.country
ORDER BY active_users DESC;

-- Q3: 不同获取渠道的用户付费转化率对比
SELECT 
    acquisition_channel,
    COUNT(*) AS total_users,
    SUM(is_premium) AS premium_users,
    ROUND(SUM(is_premium) * 100.0 / COUNT(*), 1) AS conversion_rate_pct
FROM user_info
GROUP BY acquisition_channel
ORDER BY conversion_rate_pct DESC;

-- Q4: 付费用户 vs 免费用户的行为差异
SELECT 
    CASE WHEN u.is_premium = 1 THEN '付费用户' ELSE '免费用户' END AS user_type,
    COUNT(DISTINCT u.user_id) AS user_count,
    ROUND(AVG(a.sessions), 2) AS avg_sessions,
    ROUND(AVG(a.session_duration_min), 1) AS avg_session_min,
    ROUND(AVG(a.workouts_completed), 2) AS avg_workouts,
    ROUND(AVG(a.calories_burned), 0) AS avg_calories,
    ROUND(AVG(a.ai_coach_used) * 100, 1) AS ai_usage_pct,
    ROUND(AVG(a.training_plan_accessed) * 100, 1) AS plan_usage_pct
FROM user_info u
JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY u.is_premium;

-- Q5: AI教练功能使用与训练完成率的相关性
SELECT 
    ai_coach_used,
    COUNT(*) AS records,
    ROUND(AVG(workouts_completed), 2) AS avg_workouts,
    ROUND(AVG(session_duration_min), 1) AS avg_session_min,
    ROUND(AVG(calories_burned), 0) AS avg_calories
FROM user_daily_activity
GROUP BY ai_coach_used;

-- Q6: 周内活跃度分布 - 哪天用户最活跃
SELECT 
    STRFTIME('%w', activity_date) AS day_of_week,
    CASE STRFTIME('%w', activity_date)
        WHEN '0' THEN '周日' WHEN '1' THEN '周一' WHEN '2' THEN '周二'
        WHEN '3' THEN '周三' WHEN '4' THEN '周四' WHEN '5' THEN '周五'
        WHEN '6' THEN '周六'
    END AS day_name,
    COUNT(DISTINCT user_id) AS active_users,
    ROUND(AVG(session_duration_min), 1) AS avg_session_min
FROM user_daily_activity
GROUP BY day_of_week, day_name
ORDER BY day_of_week;

-- Q7: 用户注册后首周活跃度趋势（留存曲线）
SELECT 
    a.days_since_reg,
    COUNT(DISTINCT a.user_id) AS active_users,
    ROUND(AVG(a.session_duration_min), 1) AS avg_session_min
FROM (
    SELECT a.*, 
           CAST(JULIANDAY(a.activity_date) - JULIANDAY(u.registration_date) AS INTEGER) AS days_since_reg
    FROM user_daily_activity a
    JOIN user_info u ON a.user_id = u.user_id
) a
WHERE a.days_since_reg BETWEEN 0 AND 30
GROUP BY a.days_since_reg
ORDER BY a.days_since_reg;

-- Q8: 不同年龄段用户的行为差异
SELECT 
    CASE 
        WHEN age < 20 THEN '18-19岁'
        WHEN age < 25 THEN '20-24岁'
        WHEN age < 30 THEN '25-29岁'
        WHEN age < 35 THEN '30-34岁'
        WHEN age < 40 THEN '35-39岁'
        ELSE '40岁以上'
    END AS age_group,
    COUNT(DISTINCT u.user_id) AS user_count,
    ROUND(AVG(a.session_duration_min), 1) AS avg_session_min,
    ROUND(AVG(a.workouts_completed), 2) AS avg_workouts,
    ROUND(AVG(u.is_premium) * 100, 1) AS premium_rate_pct
FROM user_info u
JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY age_group
ORDER BY age_group;

-- Q9: 高价值用户识别 - 训练次数Top 10%的用户特征
WITH user_workout_totals AS (
    SELECT user_id, 
           SUM(workouts_completed) AS total_workouts,
           SUM(session_duration_min) AS total_minutes,
           COUNT(DISTINCT activity_date) AS active_days
    FROM user_daily_activity
    GROUP BY user_id
),
ranked_users AS (
    SELECT *, NTILE(10) OVER (ORDER BY total_workouts DESC) AS decile
    FROM user_workout_totals
)
SELECT 
    'Top 10%高活跃用户' AS user_segment,
    COUNT(*) AS user_count,
    ROUND(AVG(total_workouts), 1) AS avg_total_workouts,
    ROUND(AVG(total_minutes), 0) AS avg_total_minutes,
    ROUND(AVG(active_days), 1) AS avg_active_days
FROM ranked_users
WHERE decile = 1
UNION ALL
SELECT 
    '其他90%用户' AS user_segment,
    COUNT(*) AS user_count,
    ROUND(AVG(total_workouts), 1) AS avg_total_workouts,
    ROUND(AVG(total_minutes), 0) AS avg_total_minutes,
    ROUND(AVG(active_days), 1) AS avg_active_days
FROM ranked_users
WHERE decile > 1;

-- Q10: 训练计划访问与付费转化的关系
SELECT 
    u.acquisition_channel,
    COUNT(DISTINCT u.user_id) AS total_users,
    SUM(CASE WHEN a.training_plan_accessed = 1 THEN 1 ELSE 0 END) AS plan_users,
    ROUND(SUM(CASE WHEN a.training_plan_accessed = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT u.user_id), 1) AS plan_access_rate_pct,
    ROUND(AVG(u.is_premium) * 100, 1) AS premium_rate_pct
FROM user_info u
LEFT JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY u.acquisition_channel
ORDER BY plan_access_rate_pct DESC;

-- Q11: 每日新增注册用户数趋势
SELECT 
    registration_date,
    COUNT(*) AS new_users,
    SUM(is_premium) AS new_premium_users
FROM user_info
GROUP BY registration_date
ORDER BY registration_date;

-- Q12: 用户流失分析 - 注册后7天内未再活跃的用户占比
WITH user_first_last AS (
    SELECT 
        u.user_id,
        u.registration_date,
        MIN(a.activity_date) AS first_active,
        MAX(a.activity_date) AS last_active,
        COUNT(DISTINCT a.activity_date) AS active_days
    FROM user_info u
    LEFT JOIN user_daily_activity a ON u.user_id = a.user_id
    GROUP BY u.user_id
)
SELECT 
    CASE 
        WHEN active_days = 0 THEN '注册后从未活跃'
        WHEN active_days = 1 THEN '仅活跃1天'
        WHEN active_days <= 3 THEN '活跃2-3天'
        WHEN active_days <= 7 THEN '活跃4-7天'
        WHEN active_days <= 14 THEN '活跃8-14天'
        ELSE '活跃15天以上'
    END AS retention_segment,
    COUNT(*) AS user_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM user_first_last), 1) AS pct
FROM user_first_last
GROUP BY retention_segment
ORDER BY user_count DESC;

-- Q13: 卡路里消耗与会话时长的分群分析
SELECT 
    CASE 
        WHEN session_duration_min < 10 THEN '0-10分钟'
        WHEN session_duration_min < 20 THEN '10-20分钟'
        WHEN session_duration_min < 30 THEN '20-30分钟'
        WHEN session_duration_min < 45 THEN '30-45分钟'
        ELSE '45分钟以上'
    END AS duration_bucket,
    COUNT(*) AS sessions,
    ROUND(AVG(calories_burned), 0) AS avg_calories,
    ROUND(AVG(workouts_completed), 2) AS avg_workouts
FROM user_daily_activity
GROUP BY duration_bucket
ORDER BY duration_bucket;

-- Q14: 各国用户平均训练强度对比
SELECT 
    u.country,
    COUNT(DISTINCT u.user_id) AS users,
    ROUND(AVG(a.workouts_completed), 2) AS avg_workouts_per_day,
    ROUND(AVG(a.calories_burned), 0) AS avg_calories,
    ROUND(AVG(a.active_minutes), 1) AS avg_active_min,
    ROUND(AVG(a.ai_coach_used) * 100, 1) AS ai_usage_pct
FROM user_info u
JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY u.country
HAVING users > 50
ORDER BY avg_workouts_per_day DESC;

-- Q15: 付费用户月度价值(LTV估算) - 按获取渠道
SELECT 
    u.acquisition_channel,
    COUNT(DISTINCT u.user_id) AS users,
    SUM(CASE WHEN u.is_premium = 1 THEN 1 ELSE 0 END) AS premium_users,
    ROUND(SUM(CASE WHEN u.is_premium = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT u.user_id), 1) AS premium_conv_pct,
    ROUND(AVG(a.session_duration_min), 1) AS avg_session,
    ROUND(AVG(a.workouts_completed), 2) AS avg_workouts
FROM user_info u
JOIN user_daily_activity a ON u.user_id = a.user_id
GROUP BY u.acquisition_channel
ORDER BY premium_conv_pct DESC;

-- ============================================================
--  END OF SQL QUERIES
-- ============================================================
