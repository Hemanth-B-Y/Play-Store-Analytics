# task5_bubble.py
import plotly.graph_objects as go
import streamlit as st
from data_utils import load_data, time_blocked_ui, abbrev

ALLOWED_CATS = [
    "GAME","BEAUTY","BUSINESS","COMICS","COMMUNICATION",
    "DATING","ENTERTAINMENT","SOCIAL","EVENTS"
]

TRANSLATIONS = {
    "BEAUTY":        "सौंदर्य (Beauty)",
    "BUSINESS":      "வணிகம் (Business)",
    "DATING":        "Dating (Ger.)",
}

CAT_COLORS = {
    "GAME":          "#FF69B4",   # Pink (highlighted)
    "BEAUTY":        "#FFB347",
    "BUSINESS":      "#58A6FF",
    "COMICS":        "#FF6B6B",
    "COMMUNICATION": "#4ECDC4",
    "DATING":        "#F0883E",
    "ENTERTAINMENT": "#D4A017",
    "SOCIAL":        "#3FB950",
    "EVENTS":        "#C678DD",
}

def render():
    st.markdown("## 🫧 Task 5 — Bubble Chart: App Size vs Avg Rating")
    st.caption("Window: **5:00 PM – 7:00 PM IST**  |  Rating>3.5 · Reviews>500 · Installs>50K · No 'S' in name · Sentiment Subjectivity>0.5 · GAME in pink")

    if time_blocked_ui(17, 19, "Task 5 – Bubble Chart"):
        return

    df, _ = load_data()

    df_f = df[
        (df["Category"].isin(ALLOWED_CATS)) &
        (df["Rating"]          >  3.5) &
        (df["Reviews"]         >  500) &
        (df["Installs_Clean"]  >  50_000) &
        (~df["App"].str.upper().str.contains("S", na=False)) &
        (df["Avg_Subjectivity"] > 0.5)
    ].dropna(subset=["Size_MB","Rating","Installs_Clean"]).copy()

    if df_f.empty:
        st.warning("No data after filters."); return

    # Aggregate per category-size bucket
    df_f["Size_Bin"] = (df_f["Size_MB"] // 5 * 5).astype(int)
    agg = (df_f.groupby(["Category","Size_Bin"])
              .agg(Avg_Rating=("Rating","mean"),
                   Total_Installs=("Installs_Clean","sum"),
                   App_Count=("App","count"))
              .reset_index())

    fig = go.Figure()
    for cat in ALLOWED_CATS:
        sub = agg[agg["Category"]==cat]
        if sub.empty: continue
        label = TRANSLATIONS.get(cat, cat.replace("_"," "))
        color = CAT_COLORS.get(cat,"#8B949E")
        is_game = (cat == "GAME")

        fig.add_trace(go.Scatter(
            x=sub["Size_Bin"],
            y=sub["Avg_Rating"],
            mode="markers",
            name=label,
            marker=dict(
                size=sub["Total_Installs"] / sub["Total_Installs"].max() * 60 + 8,
                color=color,
                opacity=0.80 if not is_game else 0.95,
                line=dict(
                    color="white" if not is_game else "#FF1493",
                    width=1.5 if not is_game else 3,
                ),
                symbol="circle" if not is_game else "star",
            ),
            text=sub.apply(
                lambda r: f"<b>{label}</b><br>Size: {r['Size_Bin']}–{r['Size_Bin']+5} MB"
                          f"<br>Rating: {r['Avg_Rating']:.2f}"
                          f"<br>Installs: {abbrev(r['Total_Installs'])}"
                          f"<br>Apps: {int(r['App_Count'])}", axis=1),
            hoverinfo="text",
        ))

    # GAME pink shading band
    game_data = agg[agg["Category"]=="GAME"]
    if not game_data.empty:
        fig.add_hrect(
            y0=game_data["Avg_Rating"].min()-0.05,
            y1=game_data["Avg_Rating"].max()+0.05,
            fillcolor="rgba(255,105,180,0.07)",
            line_width=0,
            layer="below",
            annotation_text="🎮 GAME zone",
            annotation_font_color="#FF69B4",
            annotation_font_size=10,
        )

    fig.add_hline(y=3.5,line_dash="dash",line_color="#FF4C4C",
                  annotation_text="Rating threshold = 3.5",
                  annotation_font_color="#FF4C4C",opacity=0.5)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1117",
        plot_bgcolor="#1C2128",
        font_color="#E6EDF3",
        title=dict(text="App Size vs Avg Rating (bubble size = installs) · GAME highlighted in pink",
                   font_size=17),
        height=560,
        xaxis=dict(title="App Size (MB)", gridcolor="#30363D",
                   title_font_color="#8B949E",ticksuffix=" MB"),
        yaxis=dict(title="Average Rating ⭐", gridcolor="#30363D",
                   title_font_color="#8B949E",range=[3.4,5.1]),
        legend=dict(orientation="h",y=-0.22,bgcolor="rgba(0,0,0,0)",
                    font_color="#8B949E",font_size=10),
        margin=dict(l=60,r=20,t=60,b=110),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🌐 Translations")
    c1,c2,c3 = st.columns(3)
    c1.metric("💅 BEAUTY","सौंदर्य (Hindi)")
    c2.metric("💼 BUSINESS","வணிகம் (Tamil)")
    c3.metric("❤️ DATING","Dating (German)")

    c1,c2,c3 = st.columns(3)
    c1.metric("🎮 GAME apps",f"{len(df_f[df_f['Category']=='GAME']):,}")
    c2.metric("📦 Total Apps",f"{len(df_f):,}")
    c3.metric("⭐ Avg Rating",f"{df_f['Rating'].mean():.2f}")