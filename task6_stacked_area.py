import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from data_utils import load_data, time_blocked_ui, abbrev

# Translations for legend
TRANSLATIONS = {
    "TRAVEL_AND_LOCAL": "Voyage & Local (FR)",   # French
    "PRODUCTIVITY":     "Productividad (ES)",     # Spanish
    "PHOTOGRAPHY":      "写真撮影 (JA)",           # Japanese
}

CAT_COLORS = {
    "TRAVEL_AND_LOCAL": "#58A6FF",
    "PRODUCTIVITY":     "#3FB950",
    "PHOTOGRAPHY":      "#F0883E",
    "TOOLS":            "#D4A017",
    "PARENTING":        "#C678DD",
    "PERSONALIZATION":  "#FF69B4",
    "EDUCATION":        "#4ECDC4",
    "BUSINESS":         "#58A6FF",
}

def render():
    st.markdown("## 📐 Task 6 — Stacked Area: Cumulative Installs Over Time")
    st.caption(
        "Window: **4:00 PM – 6:00 PM IST**  |  "
        "Categories start with T/P · Rating≥4.2 · Reviews>1K · "
        "Size 20–80 MB · No numbers in app name · Highlight MoM >25%"
    )

    if time_blocked_ui(16, 18, "Task 6 – Stacked Area Chart"):
        return

    df, _ = load_data()

    # Filters
    df_f = df[
        (df["Category"].str.startswith(("T","P"))) &
        (df["Rating"]       >= 4.2) &
        (df["Reviews"]      >  1_000) &
        (df["Size_MB"]      >= 20.0) &
        (df["Size_MB"]      <= 80.0) &
        (~df["App"].str.contains(r"\d", regex=True, na=False))
    ].dropna(subset=["Last_Updated_DT","Installs_Clean"]).copy()

    df_f["YM"] = df_f["Last_Updated_DT"].dt.to_period("M").dt.to_timestamp()

    # Monthly installs per category
    monthly = (
        df_f.groupby(["Category","YM"])["Installs_Clean"]
        .sum().reset_index()
    )
    monthly.columns = ["Category","YM","Installs"]
    monthly = monthly.sort_values(["Category","YM"])

    # Cumulative installs per category
    monthly["Cumulative"] = monthly.groupby("Category")["Installs"].cumsum()

    # MoM % change (on raw monthly installs)
    monthly["MoM_Pct"] = monthly.groupby("Category")["Installs"].pct_change() * 100

    # Pivot for stacked area
    pivot = monthly.pivot_table(index="YM", columns="Category",
                                 values="Cumulative", aggfunc="sum").ffill().fillna(0)
    pivot_mom = monthly.pivot_table(index="YM", columns="Category",
                                     values="MoM_Pct", aggfunc="mean")

    cats = pivot.columns.tolist()
    if not cats:
        st.warning("No data after filters."); return

    fig = go.Figure()

    # Stacked area traces (bottom → top)
    for cat in cats:
        label = TRANSLATIONS.get(cat, cat.replace("_"," "))
        color = CAT_COLORS.get(cat,"#8B949E")

        fig.add_trace(go.Scatter(
            x=pivot.index,
            y=pivot[cat],
            name=label,
            mode="lines",
            stackgroup="one",
            line=dict(color=color, width=1.5),
            fillcolor=color,
            fill="tonexty",
            hovertemplate=(
                f"<b>{label}</b><br>"
                "%{x|%b %Y}<br>"
                "Cumulative Installs: %{y:,.0f}<extra></extra>"
            ),
        ))

    # Overlay high-growth month markers (MoM > 25%)
    for cat in cats:
        if cat not in pivot_mom.columns:
            continue
        high = pivot_mom[pivot_mom[cat] > 25]
        if high.empty:
            continue
        color = CAT_COLORS.get(cat,"#8B949E")
        label = TRANSLATIONS.get(cat, cat.replace("_"," "))
        y_vals = [pivot.loc[ts, cat] if ts in pivot.index else 0 for ts in high.index]
        fig.add_trace(go.Scatter(
            x=high.index,
            y=y_vals,
            mode="markers",
            name=f"▲25%+ ({label})",
            marker=dict(
                symbol="triangle-up",
                size=14,
                color=color,
                line=dict(color="white", width=1.5),
                opacity=1.0,
            ),
            hovertemplate=(
                f"<b>🚀 High Growth — {label}</b><br>"
                "%{x|%b %Y}<br>"
                "MoM > 25%<extra></extra>"
            ),
            showlegend=True,
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#1C2128",
        font_color="#E6EDF3",
        title=dict(
            text="Cumulative Installs Over Time — T/P Categories (▲ = MoM Growth >25%)",
            font_size=17,
        ),
        height=560,
        xaxis=dict(
            title="Month",
            gridcolor="#30363D",
            tickformat="%b %Y",
            tickangle=-30,
            title_font_color="#8B949E",
        ),
        yaxis=dict(
            title="Cumulative Installs",
            gridcolor="#30363D",
            tickformat=".2s",
            title_font_color="#8B949E",
        ),
        legend=dict(
            orientation="h",
            y=-0.28,
            bgcolor="rgba(0,0,0,0)",
            font_color="#8B949E",
            font_size=10,
        ),
        hovermode="x unified",
        margin=dict(l=60, r=20, t=60, b=120),
    )

    st.plotly_chart(fig, use_container_width=True)

    # Translation callouts
    st.markdown("#### 🌐 Legend Translations")
    c1, c2, c3 = st.columns(3)
    c1.metric("✈️ TRAVEL & LOCAL", "Voyage & Local (French)")
    c2.metric("⚙️ PRODUCTIVITY",   "Productividad (Spanish)")
    c3.metric("📷 PHOTOGRAPHY",    "写真撮影 (Japanese)")

    # Summary KPIs
    total_high_growth = sum(
        (pivot_mom[c] > 25).sum()
        for c in cats if c in pivot_mom.columns
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📊 Categories",         len(cats))
    c2.metric("🚀 High-Growth Months",  int(total_high_growth))
    c3.metric("📦 Apps (filtered)",     f"{len(df_f):,}")
    c4.metric("📥 Peak Month Installs",
              abbrev(int(monthly.groupby("YM")["Installs"].sum().max())))
