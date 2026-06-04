# ─────────────────────────────────────────────────────────────────────
# data_utils.py  –  Shared data loading & cleaning
# ─────────────────────────────────────────────────────────────────────
import datetime
import numpy as np
import pandas as pd
import streamlit as st

try:
    import pytz
    _IST = pytz.timezone("Asia/Kolkata")
    def now_ist():
        return datetime.datetime.now(_IST)
except ImportError:
    def now_ist():
        return datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)


def in_window(start_h: int, end_h: int) -> tuple[bool, datetime.datetime]:
    """Return (is_in_window, now_ist_dt)."""
    n = now_ist()
    mins = n.hour * 60 + n.minute
    return (start_h * 60 <= mins < end_h * 60), n


def time_blocked_ui(start_h: int, end_h: int, task_label: str) -> bool:
    """
    Renders the blocked-page UI inside the current container if outside window.
    Returns True if BLOCKED — caller must do  `if time_blocked_ui(...): return`
    NEVER calls st.stop() so tabs stay fully functional.
    """
    ok, n = in_window(start_h, end_h)
    if ok:
        return False

    mins_now = n.hour * 60 + n.minute
    target   = start_h * 60
    wait     = (target - mins_now) if mins_now < target else (target + 24*60 - mins_now)

    st.markdown(f"""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;min-height:60vh;text-align:center;gap:18px;
                padding:40px 20px;">
      <div style="font-size:5rem;line-height:1;">🔒</div>
      <h2 style="color:#FF4C4C;margin:0;font-size:1.9rem;">{task_label}</h2>
      <h3 style="color:#FF4C4C;margin:0;font-size:1.3rem;font-weight:400;">Access Restricted</h3>
      <p style="color:#8B949E;font-size:0.98rem;max-width:440px;line-height:1.8;margin:0;">
        This visualization is only available between<br>
        <strong style="color:#E6EDF3;font-size:1.1rem;">
            {start_h:02d}:00 – {end_h:02d}:00 IST
        </strong>
      </p>
      <div style="background:#161B22;border:1px solid #30363D;border-radius:16px;
                  padding:24px 48px;margin-top:8px;">
        <p style="color:#8B949E;margin:0 0 6px;font-size:0.75rem;
                  text-transform:uppercase;letter-spacing:.08em;">Current Time (IST)</p>
        <p style="color:#58A6FF;font-size:2.4rem;font-weight:700;margin:0;
                  font-variant-numeric:tabular-nums;">
            {n.strftime("%I:%M %p")}
        </p>
        <p style="color:#8B949E;margin:10px 0 0;font-size:0.82rem;">
            Window opens in &nbsp;
            <strong style="color:#F0883E;font-size:1rem;">
                {wait//60}h {wait%60}m
            </strong>
        </p>
      </div>
      <p style="color:#30363D;font-size:0.76rem;margin-top:6px;">
          📅 {n.strftime("%A, %d %B %Y")}
      </p>
    </div>
    """, unsafe_allow_html=True)
    return True   # blocked — caller should `return` immediately


# ─────────────────────────────────────────────────────────────────────
# LOAD + CLEAN  (cached)
# ─────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv("Play Store Data.csv")
    rv = pd.read_csv("User Reviews.csv")

    df.drop_duplicates(subset=["App"], inplace=True)
    df = df[df["Category"] != "1.9"]          # remove junk row

    # Installs
    df["Installs_Clean"] = pd.to_numeric(
        df["Installs"].str.replace(",","",regex=False)
                      .str.replace("+","",regex=False).str.strip(),
        errors="coerce")

    # Size MB
    def _mb(s):
        s = str(s).strip()
        if s.endswith("M"):
            try: return float(s[:-1])
            except: pass
        elif s.endswith("k"):
            try: return float(s[:-1])/1024
            except: pass
        return np.nan
    df["Size_MB"] = df["Size"].apply(_mb)

    # Date
    df["Last_Updated_DT"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    df["Update_Month"]    = df["Last_Updated_DT"].dt.month
    df["Update_Year"]     = df["Last_Updated_DT"].dt.year
    df["YearMonth"]       = df["Last_Updated_DT"].dt.to_period("M")

    # Numeric
    df["Rating"]  = pd.to_numeric(df["Rating"],  errors="coerce")
    df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce")
    df["Price"]   = pd.to_numeric(
        df["Price"].str.replace("$","",regex=False), errors="coerce").fillna(0)

    # Revenue proxy  (installs × price; free = 0)
    df["Revenue"] = df["Installs_Clean"].fillna(0) * df["Price"]

    # Android version numeric
    df["Android_Ver_Num"] = pd.to_numeric(
        df["Android Ver"].str.extract(r"^(\d+\.\d+)")[0], errors="coerce")

    # Merge sentiment subjectivity (mean per app)
    subj = (rv.groupby("App")["Sentiment_Subjectivity"]
              .mean().reset_index()
              .rename(columns={"Sentiment_Subjectivity":"Avg_Subjectivity"}))
    df = df.merge(subj, on="App", how="left")

    return df, rv


def abbrev(n):
    n = float(n)
    if n >= 1e9:  return f"{n/1e9:.1f}B"
    if n >= 1e6:  return f"{n/1e6:.1f}M"
    if n >= 1e3:  return f"{n/1e3:.0f}K"
    return str(int(n))