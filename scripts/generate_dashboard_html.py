"""
生成交互式数据看板HTML（数据内嵌，离线可用）
"""
import json
import os

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析"
json_path = os.path.join(base_dir, 'dashboard', 'dashboard_data.json')
html_path = os.path.join(base_dir, 'dashboard', 'index.html')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>健身APP用户行为数据分析看板</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: #f0f2f5;
            color: #333;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 24px 32px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
        .header p {{ font-size: 14px; opacity: 0.85; }}
        .controls {{
            background: white;
            padding: 16px 24px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        .controls label {{ font-size: 14px; font-weight: 500; color: #555; }}
        .controls select {{
            padding: 8px 16px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            background: white;
            min-width: 160px;
        }}
        .controls select:focus {{ outline: none; border-color: #2c5282; }}
        .reset-btn {{
            padding: 8px 20px;
            background: #2c5282;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }}
        .reset-btn:hover {{ background: #1a365d; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 20px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid #2c5282;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .metric-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
        .metric-card .label {{ font-size: 13px; color: #888; margin-bottom: 8px; }}
        .metric-card .value {{ font-size: 28px; font-weight: 700; color: #1a365d; }}
        .metric-card .unit {{ font-size: 14px; color: #888; font-weight: 400; margin-left: 4px; }}
        .metric-card.green {{ border-left-color: #38a169; }}
        .metric-card.green .value {{ color: #2f855a; }}
        .metric-card.orange {{ border-left-color: #dd6b20; }}
        .metric-card.orange .value {{ color: #c05621; }}
        .metric-card.purple {{ border-left-color: #805ad5; }}
        .metric-card.purple .value {{ color: #6b46c1; }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}
        .chart-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        .chart-card.full-width {{ grid-column: 1 / -1; }}
        .chart-card h3 {{ font-size: 16px; color: #1a365d; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #eee; }}
        .chart-container {{ width: 100%; height: 320px; }}
        .footer {{
            text-align: center;
            padding: 16px;
            color: #999;
            font-size: 12px;
        }}
        @media (max-width: 768px) {{
            .charts-grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 18px; }}
            .metric-card .value {{ font-size: 22px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 健身APP用户行为数据分析看板</h1>
        <p>Fitness App User Behavior Analytics | 3000用户 · 48754条行为记录 · 2026.01-2026.03</p>
    </div>

    <div class="controls">
        <label for="countrySelect">🌍 筛选国家：</label>
        <select id="countrySelect">
            <option value="all">全部国家</option>
        </select>
        <button class="reset-btn" onclick="resetFilter()">重置筛选</button>
        <span id="filterInfo" style="font-size:13px;color:#666;margin-left:auto;"></span>
    </div>

    <div class="metrics-grid" id="metricsGrid"></div>

    <div class="charts-grid">
        <div class="chart-card full-width">
            <h3>📈 日活跃用户(DAU)趋势</h3>
            <div id="dauChart" class="chart-container"></div>
        </div>
        <div class="chart-card">
            <h3>💰 付费用户 vs 免费用户行为对比</h3>
            <div id="premiumChart" class="chart-container"></div>
        </div>
        <div class="chart-card">
            <h3>🌍 各国活跃用户分布</h3>
            <div id="countryChart" class="chart-container"></div>
        </div>
        <div class="chart-card">
            <h3>⚡ 核心功能使用率</h3>
            <div id="featureChart" class="chart-container"></div>
        </div>
        <div class="chart-card">
            <h3>📅 周内活跃度分布</h3>
            <div id="weekdayChart" class="chart-container"></div>
        </div>
    </div>

    <div class="footer">
        数据基于健身APP真实业务逻辑生成 | 个人数据分析项目 | Python + SQL + ECharts
    </div>

    <script>
    (function() {{
        const DATA = {data_json};
        let currentCountry = 'all';
        let charts = {{}};

        // 初始化国家下拉框
        const countrySelect = document.getElementById('countrySelect');
        DATA.countries.forEach(c => {{
            const opt = document.createElement('option');
            opt.value = c.country;
            opt.textContent = c.country + ' (' + c.users + '用户)';
            countrySelect.appendChild(opt);
        }});

        countrySelect.addEventListener('change', function() {{
            currentCountry = this.value;
            updateDashboard();
        }});

        function resetFilter() {{
            currentCountry = 'all';
            countrySelect.value = 'all';
            updateDashboard();
        }}

        function getFilteredData() {{
            if (currentCountry === 'all') {{
                return {{
                    metrics: DATA.metrics,
                    dau: DATA.dau_trend,
                    countries: DATA.countries,
                    premium: DATA.premium_compare,
                    features: DATA.feature_usage,
                    weekday: DATA.weekday_activity
                }};
            }}
            const cd = DATA.country_detail.find(c => c.country === currentCountry);
            if (!cd) return null;
            return {{
                metrics: {{
                    total_users: cd.users,
                    total_records: DATA.metrics.total_records,
                    avg_dau: Math.round(cd.dau_series.reduce((s,d) => s + d.dau, 0) / cd.dau_series.length),
                    max_dau: Math.max(...cd.dau_series.map(d => d.dau)),
                    premium_rate: cd.premium_rate,
                    avg_session: cd.avg_session,
                    avg_workouts: cd.avg_workouts,
                    ai_usage: cd.ai_usage,
                    plan_usage: DATA.metrics.plan_usage
                }},
                dau: cd.dau_series,
                countries: DATA.countries,
                premium: DATA.premium_compare,
                features: DATA.feature_usage,
                weekday: DATA.weekday_activity
            }};
        }}

        function renderMetrics(m) {{
            const grid = document.getElementById('metricsGrid');
            const cards = [
                {{ label: '总用户数', value: m.total_users.toLocaleString(), unit: '人', cls: '' }},
                {{ label: '平均DAU', value: m.avg_dau.toLocaleString(), unit: '人', cls: 'green' }},
                {{ label: '最高DAU', value: m.max_dau.toLocaleString(), unit: '人', cls: 'green' }},
                {{ label: '付费率', value: m.premium_rate, unit: '%', cls: 'orange' }},
                {{ label: '平均会话时长', value: m.avg_session, unit: '分钟', cls: 'purple' }},
                {{ label: 'AI教练使用率', value: m.ai_usage, unit: '%', cls: 'purple' }}
            ];
            grid.innerHTML = cards.map(c => 
                '<div class="metric-card ' + c.cls + '"><div class="label">' + c.label + '</div><div class="value">' + c.value + '<span class="unit">' + c.unit + '</span></div></div>'
            ).join('');
        }}

        function initCharts() {{
            charts.dau = echarts.init(document.getElementById('dauChart'));
            charts.premium = echarts.init(document.getElementById('premiumChart'));
            charts.country = echarts.init(document.getElementById('countryChart'));
            charts.feature = echarts.init(document.getElementById('featureChart'));
            charts.weekday = echarts.init(document.getElementById('weekdayChart'));
        }}

        function updateCharts(d) {{
            // DAU趋势
            charts.dau.setOption({{
                backgroundColor: 'transparent',
                tooltip: {{ trigger: 'axis', triggerOn: 'click', renderMode: 'richText', confine: true }},
                grid: {{ left: 50, right: 20, top: 20, bottom: 40, containLabel: true }},
                xAxis: {{ type: 'category', data: d.dau.map(x => x.date), axisLabel: {{ fontSize: 10, rotate: 45 }} }},
                yAxis: {{ type: 'value', name: '活跃用户', axisLabel: {{ fontSize: 11 }} }},
                series: [{{
                    type: 'line', data: d.dau.map(x => x.dau), smooth: true,
                    lineStyle: {{ color: '#2c5282', width: 2 }},
                    areaStyle: {{ color: {{ type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{{ offset: 0, color: 'rgba(44,82,130,0.3)' }}, {{ offset: 1, color: 'rgba(44,82,130,0.02)' }}] }} }},
                    itemStyle: {{ color: '#2c5282' }}
                }}]
            }});

            // 付费vs免费
            const premiumData = d.premium;
            const freeUser = premiumData.find(function(x){{ return x.type === '免费用户'; }});
            const premUser = premiumData.find(function(x){{ return x.type === '付费用户'; }});
            const freeArr = freeUser ? [freeUser.session_duration, freeUser.workouts, freeUser.calories, freeUser.ai_usage*100, freeUser.plan_usage*100] : [];
            const premArr = premUser ? [premUser.session_duration, premUser.workouts, premUser.calories, premUser.ai_usage*100, premUser.plan_usage*100] : [];
            charts.premium.setOption({{
                backgroundColor: 'transparent',
                tooltip: {{ trigger: 'axis', triggerOn: 'click', renderMode: 'richText', confine: true }},
                legend: {{ data: ['免费用户', '付费用户'], bottom: 0, textStyle: {{ fontSize: 11 }} }},
                grid: {{ left: 50, right: 20, top: 20, bottom: 40, containLabel: true }},
                xAxis: {{ type: 'category', data: ['会话时长(分)', '训练次数', '消耗卡路里', 'AI使用率(%)', '计划访问率(%)'], axisLabel: {{ fontSize: 10 }} }},
                yAxis: {{ type: 'value', axisLabel: {{ fontSize: 11 }} }},
                series: [
                    {{ name: '免费用户', type: 'bar', data: freeArr, itemStyle: {{ color: '#85CDCA' }} }},
                    {{ name: '付费用户', type: 'bar', data: premArr, itemStyle: {{ color: '#2c5282' }} }}
                ]
            }});

            // 国家分布
            charts.country.setOption({{
                backgroundColor: 'transparent',
                tooltip: {{ trigger: 'axis', triggerOn: 'click', renderMode: 'richText', confine: true, axisPointer: {{ type: 'shadow' }} }},
                grid: {{ left: 80, right: 30, top: 10, bottom: 20, containLabel: true }},
                xAxis: {{ type: 'value', axisLabel: {{ fontSize: 11 }} }},
                yAxis: {{ type: 'category', data: d.countries.map(c => c.country).reverse(), axisLabel: {{ fontSize: 11 }} }},
                series: [{{
                    type: 'bar', data: d.countries.map(c => c.users).reverse(),
                    itemStyle: {{ color: {{ type: 'linear', x: 0, y: 0, x2: 1, y2: 0, colorStops: [{{ offset: 0, color: '#2c5282' }}, {{ offset: 1, color: '#63b3ed' }}] }}, borderRadius: [0, 4, 4, 0] }},
                    label: {{ show: true, position: 'right', fontSize: 10 }}
                }}]
            }});

            // 功能使用率
            charts.feature.setOption({{
                backgroundColor: 'transparent',
                tooltip: {{ trigger: 'item', triggerOn: 'click', renderMode: 'richText', confine: true, formatter: '{{b}}: {{c}}%' }},
                series: [{{
                    type: 'pie', radius: ['45%', '70%'], center: ['50%', '50%'],
                    data: d.features.map(f => ({{ value: f.usage, name: f.feature }})),
                    itemStyle: {{ borderRadius: 6, borderColor: '#fff', borderWidth: 2 }},
                    label: {{ fontSize: 12, formatter: '{{b}}\\n{{c}}%' }},
                    color: ['#2c5282', '#dd6b20', '#38a169']
                }}]
            }});

            // 周内活跃度
            charts.weekday.setOption({{
                backgroundColor: 'transparent',
                tooltip: {{ trigger: 'axis', triggerOn: 'click', renderMode: 'richText', confine: true }},
                grid: {{ left: 50, right: 20, top: 20, bottom: 30, containLabel: true }},
                xAxis: {{ type: 'category', data: d.weekday.map(w => w.day), axisLabel: {{ fontSize: 11 }} }},
                yAxis: {{ type: 'value', name: '活跃记录', axisLabel: {{ fontSize: 11 }} }},
                series: [{{
                    type: 'line', data: d.weekday.map(w => w.count), smooth: true,
                    lineStyle: {{ color: '#805ad5', width: 2 }},
                    areaStyle: {{ color: 'rgba(128,90,213,0.15)' }},
                    itemStyle: {{ color: '#805ad5' }},
                    symbol: 'circle', symbolSize: 8
                }}]
            }});
        }}

        function updateDashboard() {{
            const d = getFilteredData();
            if (!d) return;
            renderMetrics(d.metrics);
            updateCharts(d);
            document.getElementById('filterInfo').textContent = 
                currentCountry === 'all' ? '当前显示：全部国家数据' : '当前筛选：' + currentCountry;
            Object.values(charts).forEach(c => c.resize());
        }}

        // 初始化
        if (typeof echarts === 'undefined') {{
            document.body.innerHTML = '<div style="padding:40px;text-align:center;color:#666;">图表库加载失败，请检查网络连接后刷新页面。</div>';
            return;
        }}
        initCharts();
        updateDashboard();
        window.addEventListener('resize', function() {{
            Object.values(charts).forEach(c => c.resize());
        }});
    }})();
    </script>
</body>
</html>'''

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"交互式看板已生成: {html_path}")
print(f"文件大小: {os.path.getsize(html_path) / 1024:.1f} KB")
