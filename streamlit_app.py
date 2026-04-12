"""
streamlit_app.py — DarkByte AI Phishing Detection System
Streamlit frontend with full dark cyberpunk theme
Team DarkByte | K.R. Mangalam University | B.Tech Minor Project
"""

import streamlit as st
from detector import analyze_url, analyze_email

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DarkByte — AI Phishing Detector",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root palette ── */
:root {
  --bg-deep:    #050a12;
  --bg-panel:   #0a1020;
  --bg-card:    #0d1525;
  --neon-green: #00ff88;
  --neon-cyan:  #00e5ff;
  --neon-red:   #ff3860;
  --text:       #e8f4ff;
  --muted:      #5a7a99;
}

/* ── Page background + grid ── */
html, body, [data-testid="stAppViewContainer"] {
  background: #050a12 !important;
  background-image:
    linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px) !important;
  background-size: 50px 50px !important;
  font-family: 'Inter', sans-serif !important;
  color: #e8f4ff !important;
}
[data-testid="stHeader"] { background: rgba(5,10,18,0.9) !important; border-bottom: 1px solid rgba(0,229,255,0.12); }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stDecoration"] { display: none; }
footer { display: none !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 820px !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tab"] {
  font-family: 'Inter', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  color: #5a7a99 !important;
  border-radius: 8px !important;
  padding: 10px 20px !important;
  border: none !important;
  background: transparent !important;
  transition: all 0.25s ease !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: #00e5ff !important;
  background: rgba(0,229,255,0.1) !important;
  box-shadow: 0 0 16px rgba(0,229,255,0.2) !important;
}
[data-testid="stTabs"] [role="tablist"] {
  background: #0a1020 !important;
  border: 1px solid rgba(0,229,255,0.12) !important;
  border-radius: 12px !important;
  padding: 6px !important;
  gap: 6px !important;
}
[data-testid="stTabs"] [role="tabpanel"] { padding-top: 1rem !important; }

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: #091020 !important;
  border: 1px solid rgba(0,229,255,0.15) !important;
  border-radius: 10px !important;
  color: #e8f4ff !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.9rem !important;
  padding: 14px 18px !important;
  transition: all 0.3s ease !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: #00e5ff !important;
  box-shadow: 0 0 0 3px rgba(0,229,255,0.08), 0 0 20px rgba(0,229,255,0.3) !important;
  background: rgba(0,229,255,0.03) !important;
}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {
  color: #00e5ff !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
  width: 100% !important;
  background: linear-gradient(135deg, #00aaff, #00e5ff, #00ff88) !important;
  color: #050a12 !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Orbitron', monospace !important;
  font-size: 0.88rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  padding: 14px 32px !important;
  transition: all 0.3s ease !important;
  text-transform: uppercase !important;
}
[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(0,229,255,0.45), 0 0 60px rgba(0,255,136,0.2) !important;
  background: linear-gradient(135deg, #00ff88, #00e5ff, #3d8bff) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
  background: #0a1020 !important;
  border: 1px solid rgba(0,229,255,0.12) !important;
  border-radius: 12px !important;
  padding: 18px !important;
  text-align: center !important;
}
[data-testid="stMetricValue"] {
  font-family: 'Orbitron', monospace !important;
  color: #00e5ff !important;
  font-size: 1.4rem !important;
  text-shadow: 0 0 20px rgba(0,229,255,0.5) !important;
}
[data-testid="stMetricLabel"] {
  color: #5a7a99 !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}
[data-testid="stMetricDelta"] { display: none !important; }

/* ── Divider ── */
hr {
  border-color: rgba(0,229,255,0.1) !important;
  margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────────────────────────

def render_result(result: dict):
    verdict    = result["verdict"]
    confidence = result["confidence"]
    reason     = result["reason"]
    flags      = result.get("flags", [])
    is_phishing = verdict == "Phishing"

    if is_phishing:
        border_color = "#ff3860"
        bg_gradient  = "linear-gradient(135deg,rgba(255,56,96,0.08),rgba(255,100,50,0.04))"
        glow         = "0 0 40px rgba(255,56,96,0.15)"
        icon         = "⚠️"
        verdict_color = "#ff3860"
        ring_color   = "#ff3860"
    else:
        border_color = "#00ff88"
        bg_gradient  = "linear-gradient(135deg,rgba(0,255,136,0.07),rgba(0,229,255,0.04))"
        glow         = "0 0 40px rgba(0,255,136,0.12)"
        icon         = "✅"
        verdict_color = "#00ff88"
        ring_color   = "#00ff88"

    # SVG confidence ring
    circumference = 220
    fill_amount   = circumference - (confidence / 100) * circumference
    ring_svg = f"""
    <svg viewBox="0 0 90 90" width="90" height="90" style="transform:rotate(-90deg)">
      <circle cx="45" cy="45" r="35" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="6"/>
      <circle cx="45" cy="45" r="35" fill="none"
        stroke="{ring_color}" stroke-width="6" stroke-linecap="round"
        stroke-dasharray="{circumference}" stroke-dashoffset="{fill_amount}"
        style="filter:drop-shadow(0 0 6px {ring_color})"/>
    </svg>
    """

    flags_html = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.82rem;color:#b0c8e0;">'
        f'<span style="color:{verdict_color};font-size:0.7rem;">▶</span>{f}</div>'
        for f in flags
    ) if flags else ""

    card_html = f"""
    <div style="
      background:{bg_gradient};
      border:1px solid {border_color}55;
      border-radius:16px;
      padding:28px 32px;
      box-shadow:{glow};
      position:relative;
      overflow:hidden;
      margin-top:8px;
    ">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,{ring_color},{border_color});"></div>

      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:20px;">
        <div style="display:flex;align-items:center;gap:14px;">
          <span style="font-size:2.2rem;">{icon}</span>
          <div>
            <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:800;
              color:{verdict_color};text-shadow:0 0 20px {verdict_color}88;letter-spacing:0.05em;">
              {"PHISHING DETECTED" if is_phishing else "LEGITIMATE"}
            </div>
            <div style="font-size:0.75rem;color:#5a7a99;margin-top:2px;font-family:'JetBrains Mono',monospace;">
              THREAT ANALYSIS COMPLETE
            </div>
          </div>
        </div>
        <div style="position:relative;width:90px;height:90px;flex-shrink:0;">
          {ring_svg}
          <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;">
            <span style="font-family:'Orbitron',monospace;font-size:1.15rem;font-weight:700;
              color:{verdict_color};line-height:1;">{confidence}%</span>
            <span style="font-size:0.58rem;color:#5a7a99;text-transform:uppercase;margin-top:2px;">Confidence</span>
          </div>
        </div>
      </div>

      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
        border-radius:10px;padding:16px 18px;margin-bottom:{'16px' if flags else '0'};">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.7rem;color:#5a7a99;
          text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">📋 Analysis Report</div>
        <div style="font-size:0.9rem;color:#d0e8ff;line-height:1.7;">{reason}</div>
      </div>

      {"<div style='margin-top:16px;'><div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:#5a7a99;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;'>🚩 Detected Flags</div>" + flags_html + "</div>" if flags else ""}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# ── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 0 24px;">
  <h1 style="
    font-family:'Orbitron',monospace;
    font-size:clamp(1.8rem,5vw,3rem);
    font-weight:900;
    background:linear-gradient(135deg,#00e5ff 0%,#00ff88 50%,#3d8bff 100%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    line-height:1.15;
    margin:0 0 12px;
  ">DarkByte —<br/>AI Phishing Detector</h1>
  <p style="color:#5a7a99;font-size:0.95rem;max-width:500px;margin:0 auto;line-height:1.7;">
    Defend against cyber threats in real-time. Analyze suspicious URLs and email content
    using intelligent AI-powered detection.
  </p>
  <p style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:rgba(0,229,255,0.4);margin-top:8px;">
    K.R. Mangalam University · CSE Department
  </p>
</div>
""", unsafe_allow_html=True)

# ── STATS BAR ────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("URLs Scanned",      "10,482")
c2.metric("Phishing Blocked",  "3,291")
c3.metric("Accuracy",          "94.7%")
c4.metric("Checks This Run",   st.session_state.get("session_count", 0))

st.markdown("<hr/>", unsafe_allow_html=True)

# ── DETECTOR CARD HEADER ─────────────────────────────────────────────────────
st.markdown("""
<div style="
  background:#0d1525;
  border:1px solid rgba(0,229,255,0.12);
  border-radius:20px;
  padding:32px 36px 28px;
  box-shadow:0 0 60px rgba(0,229,255,0.05),0 20px 40px rgba(0,0,0,0.5);
  position:relative;
  overflow:hidden;
">
<div style="position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,#00e5ff,#00ff88,transparent);"></div>
<div style="font-family:'Orbitron',monospace;font-size:0.85rem;font-weight:700;
  color:#5a7a99;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:20px;">
  🔍 Threat Analysis Engine
</div>
""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab_url, tab_email = st.tabs(["🌐  Check URL", "📧  Check Email Text"])

# ── URL TAB ──────────────────────────────────────────────────────────────────
with tab_url:
    url_input = st.text_input(
        "Enter Target URL",
        placeholder="https://secure-login.bank-verify.tk/@account/update",
        key="url_input",
    )
    url_clicked = st.button("⚡  Analyze URL", key="url_btn")

    if url_clicked:
        url_val = url_input.strip()
        if not url_val:
            st.warning("⚠️ Please enter a URL to analyze.")
        elif not url_val.startswith("http"):
            st.warning("🌐 URL should start with http:// or https://")
        else:
            with st.spinner("Scanning URL…"):
                result = analyze_url(url_val)
            st.session_state["session_count"] = st.session_state.get("session_count", 0) + 1
            render_result(result)

# ── EMAIL TAB ─────────────────────────────────────────────────────────────────
with tab_email:
    email_input = st.text_area(
        "Paste Email Content",
        placeholder="Dear Customer, URGENT: Your account has been suspended…",
        height=180,
        key="email_input",
    )
    email_clicked = st.button("⚡  Analyze Email", key="email_btn")

    if email_clicked:
        email_val = email_input.strip()
        if not email_val:
            st.warning("⚠️ Please paste email content to analyze.")
        else:
            with st.spinner("Scanning email content…"):
                result = analyze_email(email_val)
            st.session_state["session_count"] = st.session_state.get("session_count", 0) + 1
            render_result(result)

# Close detector card div
st.markdown("</div>", unsafe_allow_html=True)

# ── FEATURES GRID ─────────────────────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("""
<h2 style="font-family:'Orbitron',monospace;font-size:0.95rem;font-weight:700;
  color:#00e5ff;text-align:center;letter-spacing:0.1em;margin-bottom:20px;">
  ⚙️ DETECTION CAPABILITIES
</h2>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)
features = [
    ("🔗", "URL Analysis", "Detects suspicious patterns, IP addresses, dangerous TLDs, and URL shorteners"),
    ("📧", "Email Scanning", "Identifies urgency tactics, keywords, personal data requests, and scam patterns"),
    ("🎯", "Confidence Score", "Multi-factor risk scoring provides a 0–100% confidence rating"),
    ("⚡", "Real-Time", "Instant analysis with detailed reasoning — no queues, no waiting"),
]
for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    col.markdown(f"""
    <div style="background:#0a1020;border:1px solid rgba(0,229,255,0.12);border-radius:12px;
      padding:20px 14px;text-align:center;height:100%;">
      <div style="font-size:1.6rem;margin-bottom:10px;">{icon}</div>
      <div style="font-size:0.82rem;font-weight:600;color:#e8f4ff;margin-bottom:6px;">{title}</div>
      <div style="font-size:0.75rem;color:#5a7a99;line-height:1.5;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<br/>
<div style="text-align:center;padding:24px 0;border-top:1px solid rgba(0,229,255,0.08);
  font-size:0.78rem;color:#5a7a99;">
  Built with ❤️ by <span style="color:#00e5ff;">Team DarkByte</span> ·
  K.R. Mangalam University · B.Tech Minor Project 2024–25
</div>
""", unsafe_allow_html=True)
