# task2_choropleth.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data_utils import load_data, time_blocked_ui, abbrev

# ISO3 country mapping (proxy: spread installs across top countries per category)
COUNTRY_MAP = {
    "GAME":          {"USA":0.20,"IND":0.15,"BRA":0.10,"CHN":0.12,"DEU":0.08,
                      "GBR":0.07,"FRA":0.06,"RUS":0.05,"IDN":0.07,"MEX":0.10},
    "ENTERTAINMENT": {"USA":0.25,"IND":0.12,"BRA":0.10,"GBR":0.09,"DEU":0.07,
                      "AUS":0.06,"CAN":0.07,"FRA":0.05,"MEX":0.09,"ZAF":0.10},
    "TOOLS":         {"USA":0.18,"IND":0.18,"CHN":0.10,"BRA":0.09,"RUS":0.08,
                      "DEU":0.07,"GBR":0.06,"IDN":0.08,"TUR":0.07,"VNM":0.09},
    "PRODUCTIVITY":  {"USA":0.30,"GBR":0.10,"DEU":0.09,"AUS":0.08,"CAN":0.09,
                      "FRA":0.07,"JPN":0.07,"KOR":0.06,"SGP":0.07,"NLD":0.07},
    "FAMILY":        {"USA":0.22,"IND":0.14,"BRA":0.10,"CHN":0.08,"DEU":0.08,
                      "GBR":0.08,"AUS":0.06,"MEX":0.08,"IDN":0.08,"ZAF":0.08},
}
DEFAULT_DIST = {"USA":0.20,"IND":0.15,"BRA":0.10,"DEU":0.09,"GBR":0.08,
                "FRA":0.07,"AUS":0.06,"MEX":0.09,"IDN":0.08,"ZAF":0.08}


def render():
    st.markdown("## 🗺️ Task 2 — Choropleth: Global Installs by Category")
    st.caption("Window: **6:00 PM – 8:00 PM IST**  |  Top 5 categories · excludes A/C/G/S starts · highlights >1M installs")

    if time_blocked_ui(18, 20, "Task 2 – Choropleth Map"):
        return

    df, _ = load_data()

    # Filter: category must NOT start with A, C, G, S
    df = df[~df["Category"].str.startswith(("A","C","G","S"))].copy()

    # Top 5 categories by installs
    top5_cats = (
        df.groupby("Category")["Installs_Clean"].sum()
        .sort_values(ascending=False).head(5).index.tolist()
    )
    df5 = df[df["Category"].isin(top5_cats)].copy()

    # Aggregate installs per category
    cat_totals = df5.groupby("Category")["Installs_Clean"].sum().reset_index()
    cat_totals.columns = ["Category","Total_Installs"]

    # Expand to country rows
    rows = []
    for _, row in cat_totals.iterrows():
        cat = row["Category"]
        total = row["Total_Installs"]
        dist = COUNTRY_MAP.get(cat, DEFAULT_DIST)
        for iso, frac in dist.items():
            rows.append({"Category": cat, "ISO": iso,
                         "Installs": total * frac,
                         "Over1M": (total * frac) > 1_000_000})
    geo_df = pd.DataFrame(rows)

    # Selector
    selected_cat = st.selectbox("Select Category", ["All"] + top5_cats)
    if selected_cat != "All":
        plot_df = geo_df[geo_df["Category"] == selected_cat]
    else:
        plot_df = geo_df.groupby("ISO").agg(
            Installs=("Installs","sum")).reset_index()
        plot_df["Category"] = "All"
        plot_df["Over1M"] = plot_df["Installs"] > 1_000_000

    fig = px.choropleth(
        plot_df,
        locations="ISO",
        color="Installs",
        color_continuous_scale=[
            [0.0, "#1C2128"], [0.4, "#0D4F8C"],
            [0.7, "#1A7FD4"], [0.85, "#58A6FF"],
            [1.0, "#D4A017"]
        ],
        range_color=[0, plot_df["Installs"].max()],
        labels={"Installs":"Installs"},
        title=f"Global Install Distribution — {selected_cat}",
        template="plotly_dark",
    )

    # Highlight >1M with red border
    over1m = plot_df[plot_df["Over1M"]]
    if not over1m.empty:
        fig.add_trace(go.Choropleth(
            locations=over1m["ISO"],
            z=[1]*len(over1m),
            colorscale=[[0,"rgba(255,60,60,0.0)"],[1,"rgba(255,60,60,0.0)"]],
            showscale=False,
            marker_line_color="#FF4C4C",
            marker_line_width=2.5,
            name=">1M Installs",
        ))

    fig.update_layout(
        height=560,
        paper_bgcolor="#0D1117",
        plot_bgcolor="#0D1117",
        font_color="#E6EDF3",
        title_font_size=18,
        geo=dict(
            bgcolor="#0D1117",
            lakecolor="#0D1117",
            landcolor="#1C2128",
            showcoastlines=True,
            coastlinecolor="#30363D",
            showframe=False,
            projection_type="natural earth",
        ),
        margin=dict(l=0,r=0,t=50,b=0),
        coloraxis_colorbar=dict(
            title=dict(
                text="Installs",
                font=dict(color="#E6EDF3")
            ),
            tickvals=[0, 5e7, 1e8, 2e8, 3e8],
            ticktext=["0","50M","100M","200M","300M"],
            tickfont=dict(color="#8B949E"),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Summary table
    st.markdown("### 📋 Category Totals")
    tbl = cat_totals.copy()
    tbl["Total_Installs"] = tbl["Total_Installs"].apply(lambda x: abbrev(int(x)))
    tbl["Starts With"] = tbl["Category"].str[0]
    tbl["Category"] = tbl["Category"].str.replace("_"," ")
    st.dataframe(tbl, use_container_width=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("📊 Categories Shown", len(top5_cats))
    c2.metric("🌍 Countries", len(geo_df["ISO"].unique()))
    c3.metric("📥 Combined Installs", abbrev(int(cat_totals["Total_Installs"].sum())))