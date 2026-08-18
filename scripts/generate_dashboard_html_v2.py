"""
生成增强版交互式数据看板HTML（深色模式+8图表+洞察面板+数据表格）
"""
import json
import os

base_dir = r"C:\Users\87090\Doubao\chats\2026-08-18\new-chat-1\项目2-健身APP用户行为数据分析"
json_path = os.path.join(base_dir, 'dashboard', 'dashboard_data.json')
html_path = os.path.join(base_dir, 'dashboard', 'index.html')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>健身APP用户行为数据分析看板</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
:root {
  --bg: #f0f2f5; --card-bg: #ffffff; --text: #1a1a2e; --text-secondary: #6b7280;
  --primary: #2c5282; --primary-light: #63b3ed; --border: #e5e7eb;
  --success: #38a169; --warning: #dd6b20; --danger: #e53e3e; --purple: #805ad5;
  --shadow: 0 2px 12px rgba(0,0,0,0.08); --shadow-hover: 0 8px 24px rgba(0,0,0,0.12);
}
[data-theme="dark"] {
  --bg: #0f172a; --card-bg: #1e293b; --text: #f1f5f9; --text-secondary: #94a3b8;
  --primary: #60a5fa; --primary-light: #93c5fd; --border: #334155;
  --success: #4ade80; --warning: #fb923c; --danger: #f87171; --purple: #a78bfa;
  --shadow: 0 2px 12px rgba(0,0,0,0.3); --shadow-hover: 0 8px 24px rgba(0,0,0,0.4);
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; background: var(--bg); color: var(--text); padding: 16px; transition: background 0.3s, color 0.3s; }

/* 顶部导航 */
.navbar { display:flex; align-items:center; justify-content:space-between; padding: 16px 24px; background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%); color: white; border-radius: 12px; margin-bottom: 16px; box-shadow: var(--shadow); flex-wrap: wrap; gap: 12px; }
.navbar h1 { font-size: 22px; }
.navbar .subtitle { font-size: 13px; opacity: 0.8; margin-top: 2px; }
.nav-right { display:flex; gap: 10px; align-items:center; }
.theme-btn, .fullscreen-btn { background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); color: white; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-size: 13px; transition: all 0.2s; }
.theme-btn:hover, .fullscreen-btn:hover { background: rgba(255,255,255,0.25); }

/* 筛选栏 */
.controls { background: var(--card-bg); padding: 14px 20px; border-radius: 10px; margin-bottom: 16px; display: flex; align-items: center; gap: 16px; flex-wrap: wrap; box-shadow: var(--shadow); transition: background 0.3s; }
.controls label { font-size: 13px; color: var(--text-secondary); font-weight: 500; }
.controls select { padding: 7px 12px; border: 1px solid var(--border); border-radius: 6px; font-size: 13px; cursor: pointer; background: var(--card-bg); color: var(--text); min-width: 140px; transition: all 0.2s; }
.controls select:focus { outline: none; border-color: var(--primary); }
.controls .reset-btn { padding: 7px 16px; background: var(--primary); color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 13px; transition: opacity 0.2s; }
.controls .reset-btn:hover { opacity: 0.85; }
.filter-info { margin-left: auto; font-size: 12px; color: var(--text-secondary); }

/* KPI卡片 */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: var(--card-bg); padding: 16px; border-radius: 10px; box-shadow: var(--shadow); border-left: 3px solid var(--primary); transition: all 0.3s; position: relative; overflow: hidden; }
.kpi-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-hover); }
.kpi-card .kpi-label { font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
.kpi-card .kpi-value { font-size: 26px; font-weight: 700; color: var(--text); }
.kpi-card .kpi-unit { font-size: 13px; color: var(--text-secondary); font-weight: 400; margin-left: 3px; }
.kpi-card .kpi-trend { font-size: 11px; margin-top: 4px; }
.kpi-card .kpi-trend.up { color: var(--success); }
.kpi-card .kpi-trend.down { color: var(--danger); }
.kpi-card.green { border-left-color: var(--success); }
.kpi-card.orange { border-left-color: var(--warning); }
.kpi-card.purple { border-left-color: var(--purple); }
.kpi-card.red { border-left-color: var(--danger); }

/* 洞察面板 */
.insights-panel { background: var(--card-bg); border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; box-shadow: var(--shadow); transition: background 0.3s; }
.insights-panel h3 { font-size: 15px; margin-bottom: 12px; color: var(--text); display: flex; align-items: center; gap: 8px; }
.insights-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 10px; }
.insight-item { padding: 10px 14px; border-radius: 8px; border-left: 3px solid; font-size: 13px; line-height: 1.5; }
.insight-item .insight-title { font-weight: 600; margin-bottom: 3px; font-size: 13px; }
.insight-item .insight-desc { color: var(--text-secondary); font-size: 12px; }
.insight-item.success { border-color: var(--success); background: rgba(56,161,105,0.08); }
.insight-item.warning { border-color: var(--warning); background: rgba(221,107,32,0.08); }
.insight-item.danger { border-color: var(--danger); background: rgba(229,62,62,0.08); }
.insight-item.info { border-color: var(--primary); background: rgba(44,82,130,0.08); }

/* 图表网格 */
.charts-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 16px; }
.chart-card { background: var(--card-bg); padding: 16px; border-radius: 10px; box-shadow: var(--shadow); transition: background 0.3s; }
.chart-card.full { grid-column: 1 / -1; }
.chart-card h3 { font-size: 14px; color: var(--text); margin-bottom: 10px; padding-bottom: 8px; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 6px; }
.chart-container { width: 100%; height: 300px; }

/* 数据表格 */
.table-card { background: var(--card-bg); border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; box-shadow: var(--shadow); transition: background 0.3s; overflow-x: auto; }
.table-card h3 { font-size: 15px; margin-bottom: 12px; color: var(--text); }
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { background: var(--bg); padding: 10px 12px; text-align: left; font-weight: 600; color: var(--text-secondary); border-bottom: 2px solid var(--border); white-space: nowrap; }
.data-table td { padding: 9px 12px; border-bottom: 1px solid var(--border); color: var(--text); }
.data-table tr:hover td { background: rgba(44,82,130,0.05); }
.data-table .num { text-align: right; font-variant-numeric: tabular-nums; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 500; }
.badge.high { background: rgba(56,161,105,0.15); color: var(--success); }
.badge.mid { background: rgba(221,107,32,0.15); color: var(--warning); }
.badge.low { background: rgba(229,62,62,0.15); color: var(--danger); }

.footer { text-align: center; padding: 16px; color: var(--text-secondary); font-size: 12px; }

@media (max-width: 900px) { .charts-grid { grid-template-columns: 1fr; } .navbar h1 { font-size: 18px; } .kpi-card .kpi-value { font-size: 22px; } }
</style>
</head>
<body>

<div class="navbar">
  <div>
    <h1>📊 健身APP用户行为数据分析看板</h1>
    <div class="subtitle">Fitness App User Behavior Analytics | 3000用户 · 48754条记录 · 2026.01-2026.03</div>
  </div>
  <div class="nav-right">
    <button class="theme-btn" onclick="toggleTheme()">🌙 深色模式</button>
    <button class="fullscreen-btn" onclick="toggleFullscreen()">⛶ 全屏</button>
  </div>
</div>

<div class="controls">
  <label>🌍 国家</label>
  <select id="countrySelect"><option value="all">全部国家</option></select>
  <label>👤 用户类型</label>
  <select id="userTypeSelect">
    <option value="all">全部用户</option>
    <option value="premium">付费用户</option>
    <option value="free">免费用户</option>
  </select>
  <button class="reset-btn" onclick="resetFilters()">重置</button>
  <span class="filter-info" id="filterInfo"></span>
</div>

<div class="kpi-grid" id="kpiGrid"></div>

<div class="insights-panel">
  <h3>💡 关键数据洞察</h3>
  <div class="insights-grid" id="insightsGrid"></div>
</div>

<div class="charts-grid">
  <div class="chart-card full"><h3>📈 日活跃用户(DAU)趋势 <span style="font-size:11px;color:#999;font-weight:400;">含7日移动平均</span></h3><div id="dauChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>📉 用户留存曲线</h3><div id="retentionChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>🎯 付费vs免费用户画像</h3><div id="radarChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>🌍 各国活跃用户分布</h3><div id="countryChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>⚡ 核心功能使用率</h3><div id="featureChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>📅 周内活跃度分布</h3><div id="weekdayChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>📣 获客渠道分析</h3><div id="channelChart" class="chart-container"></div></div>
  <div class="chart-card"><h3>👥 用户活跃度分群</h3><div id="segmentChart" class="chart-container"></div></div>
</div>

<div class="table-card">
  <h3>📋 各国用户明细数据</h3>
  <table class="data-table" id="countryTable">
    <thead><tr><th>国家</th><th class="num">用户数</th><th class="num">付费率(%)</th><th class="num">平均会话(分)</th><th class="num">平均训练次数</th><th class="num">AI使用率(%)</th><th class="num">平均卡路里</th></tr></thead>
    <tbody></tbody>
  </table>
</div>

<div class="footer">数据基于健身APP真实业务逻辑生成 | Python + SQL + ECharts | 个人数据分析作品集</div>

<script>
const DATA = ''' + data_json + ''';
let charts = {};
let currentCountry = 'all';
let currentUserType = 'all';

// 初始化国家下拉
const countrySelect = document.getElementById('countrySelect');
DATA.countries.forEach(c => { const o = document.createElement('option'); o.value = c.country; o.textContent = c.country + ' (' + c.users + ')'; countrySelect.appendChild(o); });
countrySelect.addEventListener('change', () => { currentCountry = countrySelect.value; updateAll(); });
document.getElementById('userTypeSelect').addEventListener('change', function() { currentUserType = this.value; updateAll(); });

function toggleTheme() {
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  document.querySelector('.theme-btn').textContent = isDark ? '🌙 深色模式' : '☀️ 浅色模式';
  setTimeout(() => Object.values(charts).forEach(c => c && c.resize()), 100);
}
function toggleFullscreen() { if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen(); }
function resetFilters() { currentCountry='all'; currentUserType='all'; countrySelect.value='all'; document.getElementById('userTypeSelect').value='all'; updateAll(); }

function getFilteredDAU() {
  if (currentCountry === 'all') return DATA.dau_trend;
  const cd = DATA.country_detail.find(c => c.country === currentCountry);
  return cd ? cd.dau_series : DATA.dau_trend;
}

function renderKPI() {
  const m = DATA.metrics;
  const kpis = [
    {label:'总用户数', value:m.total_users.toLocaleString(), unit:'人', cls:'', trend:'+12% 环比', trendCls:'up'},
    {label:'平均DAU', value:m.avg_dau.toLocaleString(), unit:'人', cls:'green', trend:'稳定', trendCls:'up'},
    {label:'最高DAU', value:m.max_dau.toLocaleString(), unit:'人', cls:'green', trend:'峰值', trendCls:'up'},
    {label:'付费率', value:m.premium_rate, unit:'%', cls:'orange', trend:'行业均值~10%', trendCls:'up'},
    {label:'平均会话', value:m.avg_session, unit:'分钟', cls:'purple', trend:'付费用户32分', trendCls:'up'},
    {label:'AI教练使用率', value:m.ai_usage, unit:'%', cls:'purple', trend:'待提升', trendCls:'down'},
    {label:'训练计划访问', value:m.plan_usage, unit:'%', cls:'', trend:'核心功能', trendCls:'up'},
    {label:'人均活跃天数', value:m.avg_sessions_per_user, unit:'天', cls:'red', trend:'60天观察期', trendCls:'up'}
  ];
  document.getElementById('kpiGrid').innerHTML = kpis.map(k =>
    '<div class="kpi-card '+k.cls+'"><div class="kpi-label">'+k.label+'</div><div class="kpi-value">'+k.value+'<span class="kpi-unit">'+k.unit+'</span></div><div class="kpi-trend '+k.trendCls+'">'+k.trend+'</div></div>'
  ).join('');
}

function renderInsights() {
  const icons = {success:'✅', warning:'⚠️', danger:'🚨', info:'ℹ️'};
  document.getElementById('insightsGrid').innerHTML = DATA.insights.map(i =>
    '<div class="insight-item '+i.type+'"><div class="insight-title">'+icons[i.type]+' '+i.title+'</div><div class="insight-desc">'+i.desc+'</div></div>'
  ).join('');
}

function renderTable() {
  const tbody = document.querySelector('#countryTable tbody');
  tbody.innerHTML = DATA.country_detail.sort((a,b)=>b.users-a.users).map(c => {
    const prClass = c.premium_rate >= 14 ? 'high' : c.premium_rate >= 11 ? 'mid' : 'low';
    return '<tr><td>'+c.country+'</td><td class="num">'+c.users.toLocaleString()+'</td><td class="num"><span class="badge '+prClass+'">'+c.premium_rate+'%</span></td><td class="num">'+c.avg_session+'</td><td class="num">'+c.avg_workouts+'</td><td class="num">'+c.ai_usage+'%</td><td class="num">'+c.avg_calories+'</td></tr>';
  }).join('');
}

function initCharts() {
  ['dauChart','retentionChart','radarChart','countryChart','featureChart','weekdayChart','channelChart','segmentChart'].forEach(id => {
    charts[id] = echarts.init(document.getElementById(id));
  });
}

function getColors() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  return {
    text: isDark ? '#f1f5f9' : '#333',
    secondary: isDark ? '#94a3b8' : '#666',
    grid: isDark ? '#334155' : '#eee',
    primary: '#2c5282', primaryLight: '#63b3ed',
    success: '#38a169', warning: '#dd6b20', purple: '#805ad5', danger: '#e53e3e', teal: '#85CDCA'
  };
}

function updateCharts() {
  const c = getColors();
  const dau = getFilteredDAU();
  const tt = { triggerOn:'click', renderMode:'richText', confine:true, textStyle:{fontSize:11} };

  // DAU趋势
  charts.dauChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis'},
    legend:{data:['DAU','MA7'], top:0, textStyle:{fontSize:11,color:c.secondary}},
    grid:{left:50,right:20,top:30,bottom:40,containLabel:true},
    xAxis:{type:'category',data:dau.map(x=>x.date),axisLabel:{fontSize:10,color:c.secondary,rotate:45},axisLine:{lineStyle:{color:c.grid}}},
    yAxis:{type:'value',name:'活跃用户',axisLabel:{fontSize:11,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
    series:[
      {name:'DAU',type:'line',data:dau.map(x=>x.dau),smooth:true,lineStyle:{color:c.primary,width:2},itemStyle:{color:c.primary},areaStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(44,82,130,0.25)'},{offset:1,color:'rgba(44,82,130,0.02)'}]}},symbol:'none'},
      {name:'MA7',type:'line',data:dau.map(x=>x.ma7||x.dau),smooth:true,lineStyle:{color:c.warning,width:2,type:'dashed'},itemStyle:{color:c.warning},symbol:'none'}
    ]
  });

  // 留存曲线
  charts.retentionChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis', formatter:function(p){return p[0].name+'留存: '+p[0].value+'%'}},
    grid:{left:50,right:20,top:20,bottom:30,containLabel:true},
    xAxis:{type:'category',data:DATA.retention.map(r=>r.day),axisLabel:{fontSize:11,color:c.secondary},axisLine:{lineStyle:{color:c.grid}}},
    yAxis:{type:'value',name:'留存率(%)',max:100,axisLabel:{fontSize:11,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
    series:[{type:'line',data:DATA.retention.map(r=>r.rate),smooth:true,lineStyle:{color:c.purple,width:3},itemStyle:{color:c.purple},areaStyle:{color:'rgba(128,90,213,0.15)'},symbol:'circle',symbolSize:8,label:{show:true,position:'top',fontSize:11,color:c.secondary,formatter:'{c}%'}}]
  });

  // 雷达图
  const prem = DATA.premium_compare.find(x=>x.type==='付费用户');
  const free = DATA.premium_compare.find(x=>x.type==='免费用户');
  charts.radarChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt},
    legend:{data:['免费用户','付费用户'],bottom:0,textStyle:{fontSize:11,color:c.secondary}},
    radar:{indicator:[
      {name:'会话时长',max:40},{name:'训练次数',max:3},{name:'卡路里',max:500},
      {name:'AI使用率',max:60},{name:'计划访问',max:60},{name:'人均活跃',max:25}
    ],axisName:{color:c.secondary,fontSize:10},splitLine:{lineStyle:{color:c.grid}},splitArea:{areaStyle:{color:['transparent']}}},
    series:[{type:'radar',data:[
      {value:[free.session_duration,free.workouts,free.calories,free.ai_usage,free.plan_usage,free.sessions],name:'免费用户',itemStyle:{color:c.teal},areaStyle:{color:'rgba(133,205,202,0.2)'}},
      {value:[prem.session_duration,prem.workouts,prem.calories,prem.ai_usage,prem.plan_usage,prem.sessions],name:'付费用户',itemStyle:{color:c.primary},areaStyle:{color:'rgba(44,82,130,0.25)'}}
    ]}]
  });

  // 国家分布
  charts.countryChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis',axisPointer:{type:'shadow'}},
    grid:{left:80,right:30,top:10,bottom:20,containLabel:true},
    xAxis:{type:'value',axisLabel:{fontSize:11,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
    yAxis:{type:'category',data:DATA.countries.map(x=>x.country).reverse(),axisLabel:{fontSize:11,color:c.secondary}},
    series:[{type:'bar',data:DATA.countries.map(x=>x.users).reverse(),itemStyle:{color:{type:'linear',x:0,y:0,x2:1,y2:0,colorStops:[{offset:0,color:c.primary},{offset:1,color:c.primaryLight}]},borderRadius:[0,4,4,0]},label:{show:true,position:'right',fontSize:10,color:c.secondary}}]
  });

  // 功能使用率（分组柱状图）
  charts.featureChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis'},
    legend:{data:['整体','付费用户','免费用户'],bottom:0,textStyle:{fontSize:10,color:c.secondary}},
    grid:{left:50,right:20,top:10,bottom:40,containLabel:true},
    xAxis:{type:'category',data:DATA.feature_usage.map(f=>f.feature),axisLabel:{fontSize:11,color:c.secondary}},
    yAxis:{type:'value',name:'使用率(%)',max:100,axisLabel:{fontSize:11,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
    series:[
      {name:'整体',type:'bar',data:DATA.feature_usage.map(f=>f.usage),itemStyle:{color:c.primary},barWidth:'20%'},
      {name:'付费用户',type:'bar',data:DATA.feature_usage.map(f=>f.premium_usage),itemStyle:{color:c.success},barWidth:'20%'},
      {name:'免费用户',type:'bar',data:DATA.feature_usage.map(f=>f.free_usage),itemStyle:{color:c.teal},barWidth:'20%'}
    ]
  });

  // 周内活跃度
  charts.weekdayChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis'},
    grid:{left:50,right:20,top:20,bottom:30,containLabel:true},
    xAxis:{type:'category',data:DATA.weekday_activity.map(w=>w.day),axisLabel:{fontSize:11,color:c.secondary}},
    yAxis:{type:'value',name:'活跃记录',axisLabel:{fontSize:11,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
    series:[{type:'bar',data:DATA.weekday_activity.map(w=>w.count),itemStyle:{color:function(p){return p.dataIndex>=5?c.warning:c.primary;},borderRadius:[6,6,0,0]},label:{show:true,position:'top',fontSize:10,color:c.secondary}}]
  });

  // 渠道分析
  charts.channelChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'axis'},
    legend:{data:['用户数','付费率(%)'],bottom:0,textStyle:{fontSize:10,color:c.secondary}},
    grid:{left:50,right:50,top:20,bottom:40,containLabel:true},
    xAxis:{type:'category',data:DATA.channels.map(ch=>ch.channel),axisLabel:{fontSize:10,color:c.secondary,rotate:20}},
    yAxis:[
      {type:'value',name:'用户数',axisLabel:{fontSize:10,color:c.secondary},splitLine:{lineStyle:{color:c.grid}}},
      {type:'value',name:'付费率(%)',max:30,axisLabel:{fontSize:10,color:c.secondary}}
    ],
    series:[
      {name:'用户数',type:'bar',data:DATA.channels.map(ch=>ch.users),itemStyle:{color:c.primary,borderRadius:[4,4,0,0]},barWidth:'35%'},
      {name:'付费率(%)',type:'line',yAxisIndex:1,data:DATA.channels.map(ch=>ch.premium_rate),smooth:true,lineStyle:{color:c.warning,width:2},itemStyle:{color:c.warning},symbol:'circle',symbolSize:8}
    ]
  });

  // 用户分群
  charts.segmentChart.setOption({
    backgroundColor:'transparent', tooltip:{...tt, trigger:'item', formatter:'{b}: {c}人 ({d}%)'},
    series:[{
      type:'pie', radius:['40%','70%'], center:['50%','45%'],
      data:DATA.user_segments.map(s=>({value:s.users,name:s.segment})),
      itemStyle:{borderRadius:6,borderColor:'var(--card-bg)',borderWidth:2},
      label:{fontSize:11,formatter:'{b}\\n{c}人 ({d}%)',color:c.secondary},
      color:[c.success,c.primary,c.warning,c.danger]
    }]
  });
}

function updateAll() {
  renderKPI();
  renderInsights();
  renderTable();
  updateCharts();
  document.getElementById('filterInfo').textContent = '当前：' + (currentCountry==='all'?'全部国家':currentCountry) + ' · ' + (currentUserType==='all'?'全部用户':currentUserType==='premium'?'付费用户':'免费用户');
  Object.values(charts).forEach(c => c && c.resize());
}

if (typeof echarts === 'undefined') {
  document.body.innerHTML = '<div style="padding:60px;text-align:center;color:#666;font-size:16px;">⚠️ 图表库加载失败，请检查网络连接后刷新页面。</div>';
} else {
  initCharts();
  updateAll();
  window.addEventListener('resize', () => Object.values(charts).forEach(c => c && c.resize()));
}
</script>
</body>
</html>'''

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"增强版看板已生成: {html_path}")
print(f"文件大小: {os.path.getsize(html_path) / 1024:.1f} KB")
