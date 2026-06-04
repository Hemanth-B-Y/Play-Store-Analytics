# task4_timeseries.py
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from data_utils import load_data, time_blocked_ui, abbrev

# Translations
TRANSLATIONS = {
    "BEAUTY":   "सौंदर्य",        # Hindi
    "BUSINESS": "வணிகம்",         # Tamil
    "DATING":   "Dating",          # German (same word)
    "EDUCATION":"Education",
    "ENTERTAINMENT":"Entertainment",
    "EVENTS":   "Events",
    "COMICS":   "Comics",
    "COMMUNICATION":"Communication",
}

CAT_COLORS = {
    "BEAUTY":"#FF69B4","BUSINESS":"#58A6FF","DATING":"#F0883E",
    "EDUCATION":"#3FB950","ENTERTAINMENT":"#D4A017","EVENTS":"#C678DD",
    "COMICS":"#FF6B6B","COMMUNICATION":"#4ECDC4",
}

def render():
    st.markdown("## 📉 Task 4 — Time Series: Total Installs Over Time by Category")
    st.caption("Window: **6:00 PM – 9:00 PM IST**  |  Categories starting with E/C/B · Reviews>500 · App not starting X/Y/Z · No 'S' in app name · Shading where MoM growth >20%")

    if time_blocked_ui(18, 21, "Task 4 – Time Series"):
        return

    df, _ = load_data()

    # Category filter: starts with E, C, or B
    df_f = df[df["Category"].str.startswith(("E","C","B"))].copy()

    # App name: not starts with X/Y/Z, no letter 'S', reviews > 500
    df_f = df_f[
        (~df_f["App"].str.upper().str.startswith(("X","Y","Z"))) &
        (~df_f["App"].str.upper().str.contains("S", na=False)) &
        (df_f["Reviews"] > 500)
    ]

    # Need a valid date
    df_f = df_f.dropna(subset=["Last_Updated_DT","Installs_Clean"])
    df_f["YM"] = df_f["Last_Updated_DT"].dt.to_period("M").dt.to_timestamp()

    # Monthly totals per category
    monthly = (df_f.groupby(["Category","YM"])["Installs_Clean"]
                   .sum().reset_index())
    monthly.columns = ["Category","YM","Installs"]
    monthly = monthly.sort_values(["Category","YM"])

    # Compute MoM % change
    monthly["MoM_Pct"] = monthly.groupby("Category")["Installs"].pct_change() * 100

    cats = monthly["Category"].unique().tolist()
    if not cats:
        st.warning("No data after filters."); return

    fig = go.Figure()

    for cat in cats:
        sub = monthly[monthly["Category"]==cat].reset_index(drop=True)
        label = TRANSLATIONS.get(cat, cat.replace("_"," "))
        color = CAT_COLORS.get(cat,"#8B949E")

        fig.add_trace(go.Scatter(
            x=sub["YM"], y=sub["Installs"],
            name=label,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color,
                        line=dict(color="white",width=0.8)),
            hovertemplate=f"<b>{label}</b><br>%{{x|%b %Y}}<br>Installs: %{{y:,.0f}}<extra></extra>",
        ))

        # Shade areas with >20% MoM growth
        high_growth = sub[sub["MoM_Pct"] > 20]
        for _, row in high_growth.iterrows():
            fig.add_vrect(
                x0=row["YM"] - pd.DateOffset(days=10),
                x1=row["YM"] + pd.DateOffset(days=10),
                fillcolor=color, opacity=0.12,
                layer="below", line_width=0,
                annotation_text="▲20%+",
                annotation_position="top left",
                annotation_font_size=8,
                annotation_font_color=color,
            )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#1C2128",
        font_color="#E6EDF3",
        title=dict(text="Total Installs Over Time — E/C/B Categories (Shaded: MoM Growth >20%)",
                   font_size=17),
        height=540,
        xaxis=dict(title="Month",gridcolor="#30363D",tickformat="%b %Y",
                   tickangle=-30,title_font_color="#8B949E"),
        yaxis=dict(title="Total Installs",gridcolor="#30363D",
                   tickformat=".2s",title_font_color="#8B949E"),
        legend=dict(orientation="h",y=-0.22,bgcolor="rgba(0,0,0,0)",
                    font_color="#8B949E",font_size=10),
        hovermode="x unified",
        margin=dict(l=60,r=20,t=60,b=100),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🌐 Category Label Translations")
    trans_info = [
        ("BEAUTY","सौंदर्य (Hindi)","💅"),
        ("BUSINESS","வணிகம் (Tamil)","💼"),
        ("DATING","Dating (German — same word)","❤️"),
    ]
    c1,c2,c3 = st.columns(3)
    for col,(cat,tr,ic) in zip([c1,c2,c3],trans_info):
        col.metric(f"{ic} {cat}",tr)

    # Summary
    total_high = monthly[monthly["MoM_Pct"]>20]
    c1,c2,c3 = st.columns(3)
    c1.metric("📊 Categories",len(cats))
    c2.metric("🚀 High-Growth Months",len(total_high))
    c3.metric("📦 Apps (filtered)",f"{len(df_f):,}")