# task1_grouped_bar.py
import textwrap
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.ticker import FuncFormatter
from data_utils import load_data, time_blocked_ui, now_ist, abbrev

BG_DARK="#0D1117"; BG_CARD="#161B22"; BG_PANEL="#1C2128"
ACCENT1="#58A6FF"; ACCENT2="#3FB950"; GRID="#30363D"
TEXT="#E6EDF3"; TSUB="#8B949E"; GOLD="#D4A017"; ORANGE="#F0883E"

def render():
    st.markdown("## 📊 Task 1 — Top 10 Categories: Avg Rating & Total Reviews")
    st.caption("Window: **3:00 PM – 5:00 PM IST**  |  Filters: Rating ≥ 4.0 · Size ≥ 10 MB · Updated in January")

    if time_blocked_ui(15, 17, "Task 1 – Grouped Bar Chart"):
        return

    df, _ = load_data()

    df_f = df[
        (df["Rating"]       >= 4.0) &
        (df["Size_MB"]      >= 10.0) &
        (df["Update_Month"] == 1)
    ].copy()

    top10 = (
        df_f.groupby("Category")
        .agg(Total_Installs=("Installs_Clean","sum"),
             Avg_Rating=("Rating","mean"),
             Total_Reviews=("Reviews","sum"),
             App_Count=("App","count"))
        .reset_index()
        .sort_values("Total_Installs", ascending=False)
        .head(10).reset_index(drop=True)
    )

    if top10.empty:
        st.warning("No data matches filters."); return

    n=len(top10); x=np.arange(n); bw=0.32; gap=0.06
    xr=x-(bw/2+gap/2); xv=x+(bw/2+gap/2)
    rv=top10["Avg_Rating"].values; vv=top10["Total_Reviews"].values
    max_rev=vv.max()

    sns.set_theme(style="darkgrid")
    fig=plt.figure(figsize=(20,11),facecolor=BG_DARK)
    gs=gridspec.GridSpec(2,1,figure=fig,height_ratios=[0.88,0.12],hspace=0.04)
    ax_m=fig.add_subplot(gs[0]); ax_f=fig.add_subplot(gs[1])
    ax_m.set_facecolor(BG_PANEL); ax_f.axis("off"); ax_f.set_facecolor(BG_DARK)
    ax2=ax_m.twinx(); ax2.set_facecolor("none")

    br=ax_m.bar(xr,rv,width=bw,color=ACCENT1,alpha=0.88,zorder=3,linewidth=0)
    bv=ax2.bar(xv,vv,width=bw,color=ACCENT2,alpha=0.80,zorder=3,linewidth=0)

    for bar in br:
        h=bar.get_height()
        ax_m.bar(bar.get_x()+bar.get_width()/2,h*0.12,width=bar.get_width()*0.6,
                 bottom=h*0.82,color="white",alpha=0.10,zorder=4,linewidth=0)

    for bar,val in zip(br,rv):
        ax_m.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.04,f"{val:.2f}",
                  ha="center",va="bottom",fontsize=9,fontweight="bold",color=ACCENT1,zorder=5)
    for bar,val in zip(bv,vv):
        ax2.text(bar.get_x()+bar.get_width()/2,bar.get_height()+max_rev*0.01,abbrev(val),
                 ha="center",va="bottom",fontsize=9,fontweight="bold",color=ACCENT2,zorder=5)

    for i,row in top10.iterrows():
        ax_m.scatter(x[i],5.06,s=max(row["App_Count"]*6,30),color=ORANGE,alpha=0.75,
                     zorder=6,edgecolors="white",linewidths=0.5)
        ax_m.text(x[i],5.13,f"n={int(row['App_Count'])}",ha="center",va="bottom",
                  fontsize=8,color=ORANGE)

    rc=[GOLD,"#C0C0C0","#CD7F32"]+[TSUB]*(n-3)
    for i in range(n):
        ax_m.text(x[i],-0.20,f"#{i+1}",ha="center",va="top",fontsize=9,
                  fontweight="bold",color=rc[i],transform=ax_m.get_xaxis_transform())

    ax_m.set_ylim(0,5.65); ax_m.set_yticks([0,1,2,3,4,5])
    ax_m.set_yticklabels(["0","1","2","3","4","5"],color=ACCENT1,fontsize=10)
    ax_m.set_ylabel("Average Rating ⭐",color=ACCENT1,fontsize=12,labelpad=10)
    ax_m.tick_params(axis="y",colors=ACCENT1)
    ax2.set_ylim(0,max_rev*1.30)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda v,_: abbrev(v)))
    ax2.set_ylabel("Total Reviews 💬",color=ACCENT2,fontsize=12,labelpad=10)
    ax2.tick_params(axis="y",colors=ACCENT2)
    ax2.spines["right"].set_color(ACCENT2); ax2.spines["right"].set_alpha(0.5)

    wrapped=[textwrap.fill(c.replace("_"," "),11) for c in top10["Category"]]
    ax_m.set_xticks(x); ax_m.set_xticklabels(wrapped,color=TEXT,fontsize=9.5,
                                               rotation=0,ha="center",multialignment="center")
    ax_m.tick_params(axis="x",length=0)
    for sp in ["top","left","bottom","right"]: ax_m.spines[sp].set_visible(False)
    for sp in ["top","left","bottom"]: ax2.spines[sp].set_visible(False)
    ax_m.yaxis.grid(True,color=GRID,linewidth=0.6,alpha=0.5,zorder=0); ax_m.set_axisbelow(True)
    ax_m.axhline(4.0,color=ACCENT1,linestyle="--",linewidth=0.9,alpha=0.4,zorder=2)
    ax_m.text(n-0.35,4.06,"Threshold=4.0",color=ACCENT1,fontsize=8,alpha=0.65)
    ax_m.set_xlim(-0.6,n-0.4)

    lp=[mpatches.Patch(color=ACCENT1,label="Avg Rating"),
        mpatches.Patch(color=ACCENT2,label="Total Reviews"),
        mpatches.Patch(color=ORANGE, label="App Count"),
        mpatches.Patch(color=GOLD,   label="#1 Gold"),
        mpatches.Patch(color="#C0C0C0",label="#2 Silver"),
        mpatches.Patch(color="#CD7F32",label="#3 Bronze")]
    ax_m.legend(handles=lp,loc="upper right",framealpha=0.18,facecolor=BG_CARD,
                edgecolor=GRID,fontsize=9,ncol=3,labelcolor=TEXT)

    n_ist=now_ist()
    stats=[("🏆 #1",top10.iloc[0]["Category"].replace("_"," ")),
           ("⭐ Best Rating",f"{top10['Avg_Rating'].max():.2f}"),
           ("📥 Installs",abbrev(top10['Total_Installs'].sum())),
           ("💬 Reviews",abbrev(top10['Total_Reviews'].sum())),
           ("📅 Filter","January"),("🕒 IST",n_ist.strftime("%H:%M"))]
    for idx,(lbl,val) in enumerate(stats):
        rx=(idx+0.5)/len(stats)
        ax_f.text(rx,0.68,lbl,ha="center",va="center",fontsize=8,color=TSUB,transform=ax_f.transAxes)
        ax_f.text(rx,0.20,val,ha="center",va="center",fontsize=10,fontweight="bold",
                  color=TEXT,transform=ax_f.transAxes)
    ax_f.plot([0,1],[0.94,0.94],color=GRID,linewidth=0.8,transform=ax_f.transAxes,clip_on=False)
    plt.tight_layout(pad=1.2)
    st.pyplot(fig,use_container_width=True); plt.close(fig)

    # KPIs
    c1,c2,c3,c4=st.columns(4)
    c1.metric("🏆 #1 Category",top10.iloc[0]["Category"].replace("_"," "))
    c2.metric("📥 Total Installs",abbrev(int(top10["Total_Installs"].sum())))
    c3.metric("⭐ Avg Rating",f"{top10['Avg_Rating'].mean():.2f}")
    c4.metric("📦 Apps",f"{int(top10['App_Count'].sum()):,}")