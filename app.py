"""
🎮 Google Play Store — ADVANCED Analytics Dashboard
Ultra-Modern UI · Glassmorphism · Smooth Animations
"""

import datetime
import streamlit as st

st.set_page_config(
    page_title="Play Store Analytics",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# 🎨 ADVANCED COLOUR PALETTE
# ──────────────────────────────────────────────────────────────────────────
BG      = "#0A0E27"      # Deep navy
CARD    = "#1A1F3A"      
PANEL   = "#242E4C"      
ACCENT1 = "#00D9FF"      # Cyan
ACCENT2 = "#FF006E"      # Magenta
ACCENT3 = "#00F5A0"      # Lime
ACCENT4 = "#FFB800"      # Gold
GRID    = "#2D3A5C"      
TEXT    = "#F0F4FF"      
TSUB    = "#A0A8C8"      
RED     = "#FF3B5C"

# ──────────────────────────────────────────────────────────────────────────
# 🎨 ADVANCED GLOBAL CSS + ANIMATIONS
# ──────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

  * {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}

  @keyframes float {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-8px); }} }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
  @keyframes slideInLeft {{ from {{ transform: translateX(-20px); opacity: 0; }} to {{ transform: translateX(0); opacity: 1; }} }}
  @keyframes slideInUp {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}

  [data-testid="stAppViewContainer"],
  [data-testid="stHeader"],
  .main .block-container {{ 
    background: linear-gradient(135deg, {BG} 0%, {PANEL} 100%) !important; 
    background-attachment: fixed; 
  }}

  section[data-testid="stSidebar"] > div {{
    background: rgba(26, 31, 58, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border-right: 1px solid rgba(45, 58, 92, 0.5) !important;
    box-shadow: 2px 0 20px rgba(0, 217, 255, 0.1) !important;
  }}

  html, body, [class*="css"], p, li, span, label {{ 
    color: {TEXT} !important; 
    font-weight: 400; 
    letter-spacing: 0.3px; 
  }}

  h1 {{ 
    color: {TEXT} !important; 
    font-weight: 700; 
    font-size: 2.2rem !important; 
    letter-spacing: -0.5px; 
    background: linear-gradient(135deg, {ACCENT1}, {ACCENT3}) !important; 
    -webkit-background-clip: text !important; 
    -webkit-text-fill-color: transparent !important; 
    background-clip: text !important; 
    animation: slideInLeft 0.8s ease-out; 
  }}
  h2 {{ color: {TEXT} !important; font-weight: 700; font-size: 1.45rem !important; }}
  h3 {{ color: {TSUB} !important; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}

  div[data-testid="metric-container"] {{
    background: linear-gradient(135deg, rgba(26, 31, 58, 0.8), rgba(36, 46, 76, 0.4)) !important;
    border: 1px solid rgba(45, 58, 92, 0.8) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1) !important;
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1) !important;
    animation: slideInUp 0.6s ease-out;
  }}

  div[data-testid="metric-container"]:hover {{
    transform: translateY(-8px) !important;
    box-shadow: 0 16px 48px rgba(0, 217, 255, 0.2) !important;
    border-color: {ACCENT1} !important;
  }}

  div[data-testid="metric-container"] label {{ 
    color: {TSUB} !important; 
    font-size: 0.7rem !important; 
    text-transform: uppercase; 
    letter-spacing: 1.2px; 
    font-weight: 600; 
  }}

  div[data-testid="metric-container"] [data-testid="stMetricValue"] {{ 
    color: {TEXT} !important; 
    font-size: 1.95rem !important; 
    font-weight: 700 !important; 
    font-variant-numeric: tabular-nums; 
  }}

  button[data-baseweb="tab"] {{ 
    background: transparent !important; 
    color: {TSUB} !important; 
    border-bottom: 2px solid transparent !important; 
    font-size: 0.95rem !important; 
    padding: 12px 18px !important; 
    font-weight: 600; 
    text-transform: uppercase; 
    letter-spacing: 0.8px; 
    transition: all 0.3s ease; 
  }}

  button[data-baseweb="tab"][aria-selected="true"] {{ 
    color: {TEXT} !important; 
    border-bottom: 2px solid {ACCENT1} !important; 
    background: rgba(0, 217, 255, 0.08) !important; 
  }}

  button[data-baseweb="tab"]:hover {{ 
    color: {ACCENT1} !important; 
    background: rgba(0, 217, 255, 0.05) !important; 
  }}

  [data-testid="stTabPanel"] {{ 
    background: transparent !important; 
    padding-top: 1.8rem !important; 
    animation: slideInUp 0.5s ease-out; 
  }}

  [data-testid="stDataFrame"] {{ 
    background: rgba(26, 31, 58, 0.5) !important; 
    border: 1px solid {GRID} !important; 
    border-radius: 12px !important; 
    backdrop-filter: blur(5px) !important; 
  }}

  hr {{ 
    border: 0 !important; 
    height: 1px !important; 
    background: linear-gradient(90deg, transparent, {GRID}, transparent) !important; 
    margin: 1.5rem 0 !important; 
  }}

  label[data-testid="stWidgetLabel"] {{ 
    color: {TSUB} !important; 
    font-size: 0.82rem !important; 
    font-weight: 600; 
    text-transform: uppercase; 
  }}

  .block-container {{ 
    padding-top: 2rem !important; 
    max-width: 1500px !important; 
    padding-left: 3% !important; 
    padding-right: 3% !important; 
  }}

  ::-webkit-scrollbar {{ width: 8px; }}
  ::-webkit-scrollbar-track {{ background: rgba(45, 58, 92, 0.3); }}
  ::-webkit-scrollbar-thumb {{ background: linear-gradient(180deg, {ACCENT1}, {ACCENT2}); border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)


def get_ist():
    try:
        import pytz
        return datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    except ImportError:
        return datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)


def window_badge(sh, eh):
    n = get_ist()
    mins = n.hour * 60 + n.minute
    ok = sh * 60 <= mins < eh * 60
    
    if ok:
        mins_left = (eh * 60) - mins
        return f'<span style="background:rgba(0,245,160,0.2);border:1px solid {ACCENT3};border-radius:20px;padding:4px 14px;font-size:0.76rem;color:{ACCENT3};font-weight:700;animation:pulse 2s infinite;">🟢 LIVE · Closes in {mins_left}m</span>'
    else:
        target = sh * 60
        wait = (target - mins) if mins < target else (target + 24*60 - mins)
        return f'<span style="background:rgba(255,59,92,0.2);border:1px solid {RED};border-radius:20px;padding:4px 14px;font-size:0.76rem;color:{RED};font-weight:700;">🔒 LOCKED · Opens in {wait}m</span>'


# ──────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────
now = get_ist()

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:20px 0 24px;animation:slideInLeft 0.8s ease-out;">
      <div style="font-size:3.5rem;animation:float 3s infinite;">🎮</div>
      <div style="font-size:1.15rem;font-weight:700;background:linear-gradient(135deg,{ACCENT1},{ACCENT3});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Play Store Analytics</div>
      <div style="font-size:0.75rem;color:{TSUB};text-transform:uppercase;letter-spacing:1px;font-weight:600;">Advanced Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(0,217,255,0.1),rgba(255,6,110,0.05));border:1px solid rgba(0,217,255,0.3);border-radius:14px;padding:16px;margin-bottom:20px;backdrop-filter:blur(10px);animation:slideInUp 0.8s ease-out;">
      <div style="font-size:0.68rem;color:{TSUB};text-transform:uppercase;font-weight:700;">⏰ Current IST Time</div>
      <div style="color:{ACCENT1};font-size:2rem;font-weight:700;font-family:monospace;margin:4px 0;">{now.strftime("%I:%M:%S %p")}</div>
      <div style="color:{TSUB};font-size:0.78rem;">📅 {now.strftime("%a, %d %b %Y")}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.73rem;color:{TSUB};font-weight:700;text-transform:uppercase;">⏱ Task Windows</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    mins_now = now.hour * 60 + now.minute
    
    TASKS = [
        ("1", "Grouped Bar", 15, 17, "📊"),
        ("2", "Choropleth", 18, 20, "🗺️"),
        ("3", "Dual-Axis", 13, 14, "📈"),
        ("4", "Time Series", 18, 21, "📉"),
        ("5", "Bubble", 17, 19, "🫧"),
        ("6", "Stacked", 16, 18, "📐"),
    ]
    
    for idx, (tid, tname, sh, eh, icon) in enumerate(TASKS):
        ok = sh * 60 <= mins_now < eh * 60
        col = cols[idx % 2]
        with col:
            bg = f"rgba(0,245,160,0.1)" if ok else f"rgba(255,59,92,0.05)"
            bc = ACCENT3 if ok else GRID
            tc = TEXT if ok else TSUB
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {bc};border-radius:10px;padding:10px;margin-bottom:6px;font-size:0.75rem;color:{tc};font-weight:600;">
              <span style="font-size:1rem;margin-right:4px;">{icon}</span>Task {tid}
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ──────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(0,217,255,0.15),rgba(255,6,110,0.1));border:1px solid rgba(0,217,255,0.3);border-radius:18px;padding:32px 40px;margin-bottom:28px;backdrop-filter:blur(20px);box-shadow:0 16px 64px rgba(0,217,255,0.15);animation:slideInUp 0.8s ease-out;position:relative;">
  <div style="display:flex;align-items:center;gap:20px;">
    <div style="font-size:3.2rem;animation:float 3s infinite;">🎮</div>
    <div>
      <h1 style="margin:0;">Play Store Analytics</h1>
      <p style="margin:8px 0 0;color:{TSUB};font-size:0.95rem;">✨ 6 Advanced Visualizations · Time-Gated Access · Ultra-Modern UI</p>
    </div>
    <div style="margin-left:auto;text-align:right;">
      <div style="font-size:0.8rem;color:{TSUB};">📅 {now.strftime("%I:%M %p IST")}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# OVERVIEW KPI ROW
# ──────────────────────────────────────────────────────────────────────────
from data_utils import load_data, abbrev

with st.spinner("🔄 Loading datasets..."):
    df, reviews_df = load_data()

c1, c2, c3, c4, c5, c6 = st.columns(6, gap="medium")

metrics = [
    (c1, "📦", "Total Apps", f"{len(df):,}", ACCENT1),
    (c2, "🗂️", "Categories", f"{df['Category'].nunique()}", ACCENT4),
    (c3, "📥", "Total Installs", abbrev(int(df['Installs_Clean'].sum())), ACCENT3),
    (c4, "⭐", "Avg Rating", f"{df['Rating'].mean():.2f}", ACCENT2),
    (c5, "🆓", "Free Apps", f"{(df['Type']=='Free').mean()*100:.0f}%", ACCENT1),
    (c6, "💬", "Reviews", abbrev(int(df['Reviews'].sum())), ACCENT4),
]

for col, emoji, label, value, color in metrics:
    with col:
        st.metric(label, value, help=emoji)

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Task 1", "🗺️ Task 2", "📈 Task 3", "📉 Task 4", "🫧 Task 5", "📐 Task 6", "🔍 Overview"
])

with tab1:
    st.markdown(window_badge(15, 17), unsafe_allow_html=True)
    st.markdown("<br>")
    import task1_grouped_bar as t1
    t1.render()

with tab2:
    st.markdown(window_badge(18, 20), unsafe_allow_html=True)
    st.markdown("<br>")
    import task2_choropleth as t2
    t2.render()

with tab3:
    st.markdown(window_badge(13, 14), unsafe_allow_html=True)
    st.markdown("<br>")
    import task3_dual_axis as t3
    t3.render()

with tab4:
    st.markdown(window_badge(18, 21), unsafe_allow_html=True)
    st.markdown("<br>")
    import task4_timeseries as t4
    t4.render()

with tab5:
    st.markdown(window_badge(17, 19), unsafe_allow_html=True)
    st.markdown("<br>")
    import task5_bubble as t5
    t5.render()

with tab6:
    st.markdown(window_badge(16, 18), unsafe_allow_html=True)
    st.markdown("<br>")
    import task6_stacked_area as t6
    t6.render()

with tab7:
    st.markdown("## 🔍 Dataset Overview")
    import plotly.express as px
    import plotly.graph_objects as go

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("### 📊 Top Categories by Installs")
        cat_inst = (df.groupby("Category")["Installs_Clean"].sum().sort_values(ascending=True).tail(15).reset_index())
        fig1 = px.bar(cat_inst, x="Installs_Clean", y="Category", orientation="h", color="Installs_Clean",
                      color_continuous_scale=[f"rgb(10,14,39)", f"rgb(0,217,255)"], template="plotly_dark")
        fig1.update_layout(paper_bgcolor=BG, plot_bgcolor=PANEL, height=480, showlegend=False,
                          coloraxis_showscale=False, margin=dict(l=10,r=20,t=20,b=20))
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("### 🆓 Free vs Paid")
        type_df = df[df["Type"].isin(["Free","Paid"])]["Type"].value_counts().reset_index()
        type_df.columns = ["Type","Count"]
        fig2 = px.pie(type_df, names="Type", values="Count",
                     color_discrete_sequence=[ACCENT1, ACCENT2], hole=0.48, template="plotly_dark")
        fig2.update_layout(paper_bgcolor=BG, height=480, margin=dict(t=20,b=20))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### ⭐ Rating Distribution")
    fig3 = go.Figure(go.Histogram(x=df["Rating"].dropna(), nbinsx=35,
                                  marker_color=ACCENT1, opacity=0.85))
    fig3.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=PANEL,
                      height=320, margin=dict(l=40,r=20,t=10,b=40),
                      xaxis=dict(gridcolor=GRID), yaxis=dict(gridcolor=GRID),
                      showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 📋 Dataset")
    st.dataframe(df[["App","Category","Rating","Reviews","Size","Installs",
                     "Type","Price","Content Rating"]].head(200),
                use_container_width=True, height=350)


# ──────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:48px;padding-top:24px;border-top:1px solid rgba(45,58,92,0.5);text-align:center;color:{TSUB};font-size:0.8rem;animation:pulse 3s infinite;">
  🎨 Advanced Analytics Dashboard · {now.strftime("%d %b %Y %H:%M IST")}
</div>
""", unsafe_allow_html=True)