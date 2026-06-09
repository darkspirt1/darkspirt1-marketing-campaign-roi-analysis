import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing ROI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1b2a 0%, #1b2838 100%);
        border-right: 1px solid #1e3a5f;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%);
        border: 1px solid #2196f3;
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.15);
        margin-bottom: 16px;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .kpi-label {
        color: #90caf9;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
        white-space: nowrap;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.2;
        white-space: nowrap;
    }
    .kpi-sub {
        color: #546e7a;
        font-size: 11px;
        margin-top: 5px;
        white-space: nowrap;
    }

    .section-header {
        color: #2196f3;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 8px 0;
        border-bottom: 2px solid #1e3a5f;
        margin-bottom: 16px;
    }

    .insight-box {
        background: linear-gradient(135deg, #0d2137 0%, #1a2744 100%);
        border-left: 4px solid #2196f3;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 8px 0;
        color: #b0bec5;
        font-size: 14px;
    }
    .insight-box strong { color: #90caf9; }

    .best-card {
        background: linear-gradient(135deg, #0a2e1a 0%, #1b4332 100%);
        border: 1px solid #4caf50;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 6px 0;
    }
    .worst-card {
        background: linear-gradient(135deg, #2e0a0a 0%, #431b1b 100%);
        border: 1px solid #f44336;
        border-radius: 10px;
        padding: 16px 20px;
        margin: 6px 0;
    }
    .card-title {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .best-card .card-title { color: #4caf50; }
    .worst-card .card-title { color: #f44336; }
    .card-value { color: #ffffff; font-size: 20px; font-weight: 800; }
    .card-sub   { color: #90a4ae; font-size: 12px; margin-top: 4px; }

    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }

    .custom-divider {
        border: none;
        border-top: 1px solid #1e3a5f;
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)


# ─── Load Data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "marketing_campaign_dataset.csv")
    df = pd.read_csv(data_path)
    df['Acquisition_Cost'] = df['Acquisition_Cost'].replace('[\$,]', '', regex=True).astype(float)
    df['Duration_Days']    = df['Duration'].str.extract('(\d+)').astype(int)
    df['Date']             = pd.to_datetime(df['Date'])
    df['CTR']              = (df['Clicks'] / df['Impressions']) * 100
    df['Month']            = df['Date'].dt.to_period('M').astype(str)
    return df


df = load_data()


# ─── Sidebar ───────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding:12px 0 4px 0;">
    <span style="color:#90caf9; font-size:20px; font-weight:800; letter-spacing:1px;">
        📊 Dashboard Filters
    </span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown(
    '<hr style="border-color:#1e3a5f; margin:8px 0 16px 0;">', unsafe_allow_html=True)

channels = st.sidebar.multiselect(
    "📡 Channel",
    options=sorted(df['Channel_Used'].unique()),
    default=sorted(df['Channel_Used'].unique())
)
campaign_types = st.sidebar.multiselect(
    "🎯 Campaign Type",
    options=sorted(df['Campaign_Type'].unique()),
    default=sorted(df['Campaign_Type'].unique())
)
audiences = st.sidebar.multiselect(
    "👥 Target Audience",
    options=sorted(df['Target_Audience'].unique()),
    default=sorted(df['Target_Audience'].unique())
)
locations = st.sidebar.multiselect(
    "📍 Location",
    options=sorted(df['Location'].unique()),
    default=sorted(df['Location'].unique())
)

st.sidebar.markdown(
    '<hr style="border-color:#1e3a5f; margin:16px 0;">', unsafe_allow_html=True)
st.sidebar.markdown("**📅 Date Range**")
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()
date_range = st.sidebar.date_input(
    "Select Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df[
    (df['Channel_Used'].isin(channels)) &
    (df['Campaign_Type'].isin(campaign_types)) &
    (df['Target_Audience'].isin(audiences)) &
    (df['Location'].isin(locations))
]
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df['Date'].dt.date >= date_range[0]) &
        (filtered_df['Date'].dt.date <= date_range[1])
    ]

st.sidebar.markdown(
    '<hr style="border-color:#1e3a5f; margin:16px 0;">', unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="background:#0d2137; border:1px solid #1e3a5f; border-radius:8px; padding:12px; text-align:center;">
    <div style="color:#546e7a; font-size:11px; letter-spacing:1px; text-transform:uppercase;">Campaigns in View</div>
    <div style="color:#ffffff; font-size:24px; font-weight:800;">{len(filtered_df):,}</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown('<br>', unsafe_allow_html=True)
st.sidebar.markdown(
    "<center><span style='color:#546e7a; font-size:12px;'>Built by <strong style='color:#90caf9'>Sahil</strong></span></center>",
    unsafe_allow_html=True
)


# ─── Header ────────────────────────────────────────────────────
st.markdown("""
<div style="padding:8px 0 20px 0;">
    <h1 style="color:#ffffff; font-size:28px; font-weight:800; margin:0; letter-spacing:-0.5px;">
        📊 Marketing Campaign Performance Dashboard
    </h1>
    <p style="color:#546e7a; font-size:14px; margin:6px 0 0 0; letter-spacing:0.3px;">
        Analyzing 200,000 campaigns &nbsp;·&nbsp; 6 channels &nbsp;·&nbsp; 5 cities &nbsp;·&nbsp; Full Year 2021
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── KPI Cards ─────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

kpis = [
    (c1, "AVG ROI",
     f"{filtered_df['ROI'].mean():.2f}x",                 "Return on Investment"),
    (c2, "AVG CAC",
     f"${filtered_df['Acquisition_Cost'].mean():,.0f}",    "Acquisition Cost"),
    (c3, "AVG CTR",
     f"{filtered_df['CTR'].mean():.1f}%",                  "Click-Through Rate"),
    (c4, "CONVERSION",
     f"{filtered_df['Conversion_Rate'].mean()*100:.1f}%",  "Conversion Rate"),
    (c5, "CAMPAIGNS",    f"{len(filtered_df):,}",
     "Total in View"),
]

for col, label, value, sub in kpis:
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Performance Snapshot ──────────────────────────────────────
st.markdown('<div class="section-header">⚡ Performance Snapshot</div>',
            unsafe_allow_html=True)

g1, g2, g3 = st.columns([1.2, 1, 1])

with g1:
    avg_roi = filtered_df['ROI'].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=avg_roi,
        delta={'reference': 5.0, 'valueformat': '.2f'},
        title={'text': "Average ROI", 'font': {'color': 'white', 'size': 16}},
        number={'font': {'color': 'white', 'size': 40}, 'suffix': 'x'},
        gauge={
            'axis': {'range': [0, 8], 'tickcolor': '#90caf9',
                     'tickfont': {'color': '#90caf9'}},
            'bar': {'color': '#2196f3', 'thickness': 0.3},
            'bgcolor': '#0d1b2a',
            'bordercolor': '#1e3a5f',
            'steps': [
                {'range': [0, 3],   'color': '#1a0a0a'},
                {'range': [3, 5],   'color': '#0d1b2e'},
                {'range': [5, 6.5], 'color': '#0a2e1a'},
                {'range': [6.5, 8], 'color': '#1a2e0a'},
            ],
            'threshold': {
                'line': {'color': '#4caf50', 'width': 3},
                'thickness': 0.8,
                'value': 5.0
            }
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=260,
        margin=dict(t=40, b=10, l=20, r=20)
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with g2:
    st.markdown("""
    <div style="color:#4caf50; font-size:13px; font-weight:700;
                letter-spacing:1px; text-transform:uppercase;
                margin-bottom:10px;">
        🏆 Best Performers
    </div>
    """, unsafe_allow_html=True)

    best_channel = filtered_df.groupby('Channel_Used')['ROI'].mean().idxmax()
    best_campaign = filtered_df.groupby('Campaign_Type')['ROI'].mean().idxmax()
    best_audience = filtered_df.groupby('Target_Audience')[
        'ROI'].mean().idxmax()
    best_city = filtered_df.groupby('Location')['ROI'].mean().idxmax()

    for label, value in [("Channel", best_channel), ("Campaign", best_campaign),
                         ("Audience", best_audience), ("City", best_city)]:
        st.markdown(f"""
        <div class="best-card">
            <div class="card-title">✅ Best {label}</div>
            <div class="card-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

with g3:
    st.markdown("""
    <div style="color:#f44336; font-size:13px; font-weight:700;
                letter-spacing:1px; text-transform:uppercase;
                margin-bottom:10px;">
        ⚠️ Needs Attention
    </div>
    """, unsafe_allow_html=True)

    worst_channel = filtered_df.groupby('Channel_Used')['ROI'].mean().idxmin()
    worst_campaign = filtered_df.groupby('Campaign_Type')[
        'ROI'].mean().idxmin()
    worst_audience = filtered_df.groupby('Target_Audience')[
        'ROI'].mean().idxmin()
    worst_city = filtered_df.groupby('Location')['ROI'].mean().idxmin()

    for label, value in [("Channel", worst_channel), ("Campaign", worst_campaign),
                         ("Audience", worst_audience), ("City", worst_city)]:
        st.markdown(f"""
        <div class="worst-card">
            <div class="card-title">❌ Worst {label}</div>
            <div class="card-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Channel + Campaign Charts ─────────────────────────────────
st.markdown('<div class="section-header">📡 Channel & Campaign Analysis</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    ch = filtered_df.groupby('Channel_Used').agg(
        Avg_ROI=('ROI', 'mean'),
        Avg_CAC=('Acquisition_Cost', 'mean'),
        Count=('Campaign_ID', 'count')
    ).reset_index().sort_values('Avg_ROI', ascending=False)

    fig = px.bar(ch, x='Channel_Used', y='Avg_ROI',
                 color='Avg_ROI',
                 color_continuous_scale=[[0, '#0d2137'], [
                     0.5, '#1565c0'], [1, '#42a5f5']],
                 text=ch['Avg_ROI'].round(2),
                 labels={'Channel_Used': 'Channel', 'Avg_ROI': 'Avg ROI'})
    fig.update_traces(textposition='outside', textfont_color='white')
    fig.update_layout(
        title='Average ROI by Channel',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_color='#90caf9',
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f'),
        height=360
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    ct = filtered_df.groupby('Campaign_Type').agg(
        Avg_ROI=('ROI', 'mean'),
        Avg_CAC=('Acquisition_Cost', 'mean')
    ).reset_index().sort_values('Avg_ROI', ascending=False)

    fig = px.bar(ct, x='Campaign_Type', y='Avg_ROI',
                 color='Avg_CAC',
                 color_continuous_scale=[[0, '#0a2e1a'], [
                     0.5, '#1b5e20'], [1, '#66bb6a']],
                 text=ct['Avg_ROI'].round(2),
                 labels={'Campaign_Type': 'Type', 'Avg_ROI': 'Avg ROI', 'Avg_CAC': 'Avg CAC ($)'})
    fig.update_traces(textposition='outside', textfont_color='white')
    fig.update_layout(
        title='ROI by Campaign Type (color = CAC)',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_color='#90caf9',
        xaxis=dict(gridcolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f'),
        height=360
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Time Series ───────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Monthly Performance Trend</div>',
            unsafe_allow_html=True)

monthly = filtered_df.groupby('Month').agg(
    Avg_ROI=('ROI', 'mean'),
    Avg_CTR=('CTR', 'mean'),
    Campaigns=('Campaign_ID', 'count')
).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Avg_ROI'],
    mode='lines+markers', name='Avg ROI',
    line=dict(color='#2196f3', width=3),
    marker=dict(size=8, color='#42a5f5', line=dict(color='white', width=1)),
    fill='tozeroy', fillcolor='rgba(33,150,243,0.08)'
))
fig.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Avg_CTR'],
    mode='lines+markers', name='Avg CTR (%)',
    line=dict(color='#4caf50', width=2, dash='dot'),
    marker=dict(size=6),
    yaxis='y2'
))
fig.update_layout(
    title='Monthly ROI & CTR Trends',
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font_color='white', title_font_color='#90caf9',
    xaxis=dict(gridcolor='#1e3a5f', tickangle=45),
    yaxis=dict(gridcolor='#1e3a5f', title='Avg ROI'),
    yaxis2=dict(overlaying='y', side='right',
                title='Avg CTR (%)', gridcolor='#1e3a5f'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1e3a5f'),
    height=400
)
st.plotly_chart(fig, use_container_width=True)

best_month = monthly.loc[monthly['Avg_ROI'].idxmax(), 'Month']
worst_month = monthly.loc[monthly['Avg_ROI'].idxmin(), 'Month']
st.markdown(f"""
<div class="insight-box">
    📌 <strong>Key Insight:</strong> ROI peaks in <strong>{best_month}</strong> —
    ideal month to scale campaign budgets. Performance dips in
    <strong>{worst_month}</strong> — consider reducing spend or A/B testing
    new creatives during this period.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Audience + Location ───────────────────────────────────────
st.markdown('<div class="section-header">👥 Audience & Location Intelligence</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    aud = filtered_df.groupby('Target_Audience')['ROI'].mean().reset_index()
    aud = aud.sort_values('ROI', ascending=True)
    fig = px.bar(aud, x='ROI', y='Target_Audience', orientation='h',
                 color='ROI',
                 color_continuous_scale=[[0, '#0d2137'], [1, '#42a5f5']],
                 text=aud['ROI'].round(2))
    fig.update_traces(textposition='outside', textfont_color='white')
    fig.update_layout(
        title='ROI by Target Audience',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_color='#90caf9',
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f'),
        height=340
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    loc = filtered_df.groupby('Location').agg(
        Avg_ROI=('ROI', 'mean'),
        Avg_CAC=('Acquisition_Cost', 'mean')
    ).reset_index().sort_values('Avg_ROI', ascending=True)

    fig = px.bar(loc, x='Avg_ROI', y='Location', orientation='h',
                 color='Avg_CAC',
                 color_continuous_scale=[[0, '#1a0a2e'], [1, '#7c4dff']],
                 text=loc['Avg_ROI'].round(2),
                 labels={'Avg_CAC': 'CAC ($)'})
    fig.update_traces(textposition='outside', textfont_color='white')
    fig.update_layout(
        title='ROI by Location (color = CAC)',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', title_font_color='#90caf9',
        xaxis=dict(gridcolor='#1e3a5f'),
        yaxis=dict(gridcolor='#1e3a5f'),
        height=340
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Top 10 Companies Table ────────────────────────────────────
st.markdown('<div class="section-header">🏢 Top 10 Companies by ROI</div>',
            unsafe_allow_html=True)

top_companies = filtered_df.groupby('Company').agg(
    Avg_ROI=('ROI', 'mean'),
    Avg_CAC=('Acquisition_Cost', 'mean'),
    Avg_CTR=('CTR', 'mean'),
    Avg_Conversion=('Conversion_Rate', 'mean'),
    Total_Campaigns=('Campaign_ID', 'count')
).round(2).reset_index().sort_values('Avg_ROI', ascending=False).head(10)

top_companies.columns = ['Company', 'Avg ROI',
                         'Avg CAC ($)', 'Avg CTR (%)', 'Conversion Rate', 'Campaigns']
top_companies['Avg ROI'] = top_companies['Avg ROI'].apply(
    lambda x: f"{x:.2f}x")
top_companies['Avg CAC ($)'] = top_companies['Avg CAC ($)'].apply(
    lambda x: f"${x:,.0f}")
top_companies['Avg CTR (%)'] = top_companies['Avg CTR (%)'].apply(
    lambda x: f"{x:.2f}%")
top_companies['Conversion Rate'] = top_companies['Conversion Rate'].apply(
    lambda x: f"{x*100:.2f}%")

st.dataframe(
    top_companies,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Company":         st.column_config.TextColumn("🏢 Company",       width="medium"),
        "Avg ROI":         st.column_config.TextColumn("📈 Avg ROI",       width="small"),
        "Avg CAC ($)":     st.column_config.TextColumn("💰 Avg CAC",       width="small"),
        "Avg CTR (%)":     st.column_config.TextColumn("🖱️ Avg CTR",      width="small"),
        "Conversion Rate": st.column_config.TextColumn("🎯 Conv. Rate",    width="small"),
        "Campaigns":       st.column_config.NumberColumn("📋 Campaigns",   width="small"),
    }
)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Correlation Heatmap ───────────────────────────────────────
st.markdown('<div class="section-header">🔥 Metric Correlations</div>',
            unsafe_allow_html=True)

numeric_cols = ['Conversion_Rate', 'Acquisition_Cost', 'ROI',
                'Clicks', 'Impressions', 'Engagement_Score', 'CTR']
corr = filtered_df[numeric_cols].corr().round(2)

fig = px.imshow(corr, text_auto=True,
                color_continuous_scale='RdBu_r',
                aspect='auto')
fig.update_layout(
    title='Correlation Between Marketing Metrics',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    title_font_color='#90caf9',
    height=420
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-box">
    📌 <strong>Key Insight:</strong>
    Impressions and CTR show a strong <strong>negative correlation (-0.66)</strong> —
    broader reach campaigns attract less engaged audiences.
    Use <strong>targeted campaigns</strong> over mass awareness for better click performance.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)


# ─── Recommendations ───────────────────────────────────────────
st.markdown('<div class="section-header">💡 Strategic Recommendations</div>',
            unsafe_allow_html=True)

best_ch = filtered_df.groupby('Channel_Used')['ROI'].mean().idxmax()
worst_ch = filtered_df.groupby('Channel_Used')['ROI'].mean().idxmin()
best_aud = filtered_df.groupby('Target_Audience')['ROI'].mean().idxmax()
best_loc = filtered_df.groupby('Location')['ROI'].mean().idxmax()
avg_cac = filtered_df['Acquisition_Cost'].mean()

recommendations = [
    (f"Increase budget allocation to <strong>{best_ch}</strong> campaigns",
     "Highest ROI channel in current selection"),
    (f"Reduce spend on <strong>{worst_ch}</strong> or A/B test new creatives",
     "Lowest performing channel — needs optimization"),
    (f"Focus targeting on <strong>{best_aud}</strong> demographic",
     "Best converting audience segment"),
    (f"Prioritize campaigns in <strong>{best_loc}</strong>",
     "Highest ROI city with strong cost efficiency"),
    (f"Average CAC is <strong>${avg_cac:,.0f}</strong> — benchmark against industry standard",
     "Review channels exceeding this threshold"),
    ("High impressions correlate with <strong>lower CTR (−0.66)</strong>",
     "Use targeted reach over broad awareness campaigns"),
]

r1, r2 = st.columns(2)
for i, (rec, sub) in enumerate(recommendations):
    col = r1 if i % 2 == 0 else r2
    col.markdown(f"""
    <div class="insight-box">
        <strong style="color:#2196f3;">0{i+1}.</strong> {rec}<br>
        <span style="color:#607d8b; font-size:12px;">→ {sub}</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:12px 0;">
    <span style="color:#546e7a; font-size:13px;">
        📊 Marketing Campaign ROI Dashboard &nbsp;·&nbsp;
        Built by <strong style="color:#90caf9;">Sahil</strong> &nbsp;·&nbsp;
        AI & Data Science Engineer &nbsp;·&nbsp; 2024
    </span>
</div>
""", unsafe_allow_html=True)
