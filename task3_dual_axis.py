# task3_dual_axis.py
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from data_utils import load_data, time_blocked_ui, abbrev

def render():
    st.markdown("## 📈 Task 3 — Dual-Axis: Avg Installs & Revenue (Free vs Paid)")
    st.caption("Window: **1:00 PM – 2:00 PM IST**  |  Filters: Installs≥10K · Revenue≥$10K · Android>4.0 · Size>15MB · Content=Everyone · App name ≤30 chars")

    if time_blocked_ui(13, 14, "Task 3 – Dual-Axis Chart"):
        return

    df, _ = load_data()

    # Filters
    df_f = df[
        (df["Installs_Clean"]   >= 10_000) &
        (df["Revenue"]          >= 10_000) &
        (df["Android_Ver_Num"]  >  4.0) &
        (df["Size_MB"]          >  15.0) &
        (df["Content Rating"]   == "Everyone") &
        (df["App"].str.len()    <= 30) &
        (df["Type"].isin(["Free","Paid"]))
    ].copy()

    # Top 3 categories by installs
    top3 = (df_f.groupby("Category")["Installs_Clean"].sum()
               .sort_values(ascending=False).head(3).index.tolist())
    df_f = df_f[df_f["Category"].isin(top3)]

    agg = (df_f.groupby(["Category","Type"])
              .agg(Avg_Installs=("Installs_Clean","mean"),
                   Total_Revenue=("Revenue","sum"),
                   App_Count=("App","count"))
              .reset_index())

    COLORS = {"Free": {"installs":"#58A6FF","revenue":"#3FB950"},
              "Paid": {"installs":"#F0883E","revenue":"#D4A017"}}

    fig = go.Figure()
    cats = top3
    x_labels = [c.replace("_"," ") for c in cats]

    for app_type in ["Free","Paid"]:
        sub = agg[agg["Type"]==app_type]
        vals_inst = [sub[sub["Category"]==c]["Avg_Installs"].values[0]
                     if c in sub["Category"].values else 0 for c in cats]
        vals_rev  = [sub[sub["Category"]==c]["Total_Revenue"].values[0]
                     if c in sub["Category"].values else 0 for c in cats]

        fig.add_trace(go.Bar(
            name=f"{app_type} — Avg Installs",
            x=x_labels, y=vals_inst,
            marker_color=COLORS[app_type]["installs"],
            opacity=0.85,
            yaxis="y1",
            text=[abbrev(v) for v in vals_inst],
            textposition="outside",
            textfont_color="#E6EDF3",
        ))
        fig.add_trace(go.Scatter(
            name=f"{app_type} — Revenue",
            x=x_labels, y=vals_rev,
            mode="lines+markers",
            line=dict(color=COLORS[app_type]["revenue"],width=3,dash="dot" if app_type=="Paid" else "solid"),
            marker=dict(size=10,symbol="diamond" if app_type=="Paid" else "circle",
                        line=dict(color="white",width=1)),
            yaxis="y2",
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#1C2128",
        font_color="#E6EDF3",
        title=dict(text="Avg Installs & Revenue — Free vs Paid Apps · Top 3 Categories",
                   font_size=18),
        barmode="group",
        bargap=0.25,
        bargroupgap=0.05,
        height=520,
        legend=dict(orientation="h",y=-0.18,bgcolor="rgba(0,0,0,0)",
                    font_color="#8B949E"),
        yaxis=dict(title="Avg Installs",title_font_color="#58A6FF",
                   tickfont_color="#58A6FF",gridcolor="#30363D",
                   tickformat=".2s"),
        yaxis2=dict(title="Total Revenue ($)",title_font_color="#D4A017",
                    tickfont_color="#D4A017",overlaying="y",side="right",
                    gridcolor="rgba(0,0,0,0)",tickformat="$,.0f"),
        margin=dict(l=60,r=60,t=60,b=80),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Table
    st.markdown("### 📋 Filtered Summary")
    show = agg.copy()
    show["Avg_Installs"]   = show["Avg_Installs"].apply(lambda x: abbrev(int(x)))
    show["Total_Revenue"]  = show["Total_Revenue"].apply(lambda x: f"${x:,.0f}")
    show["Category"]       = show["Category"].str.replace("_"," ")
    st.dataframe(show, use_container_width=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("📊 Top Categories", len(top3))
    c2.metric("📦 Apps (filtered)", f"{len(df_f):,}")
    c3.metric("💰 Total Revenue", abbrev(int(df_f["Revenue"].sum())))