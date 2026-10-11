import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- Seite & Design ----------
st.set_page_config(page_title="ETF vs. Sparbuch", page_icon="📈", layout="centered")

st.markdown(
    """
    <style>
    html, body, [class*="css"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Helvetica Neue", Arial, sans-serif;
        color: #1d1d1f;
    }
    .stApp { background: #fbfbfd; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { max-width: 760px; padding-top: 4.5rem; padding-bottom: 5rem; }

    .hero h1 {
        font-size: 3.2rem; font-weight: 700; letter-spacing: -0.03em;
        line-height: 1.05; margin: 0 0 0.6rem 0; color: #1d1d1f;
    }
    .hero p { font-size: 1.3rem; color: #6e6e73; margin: 0 0 3rem 0; line-height: 1.4; }

    .section-title {
        font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em;
        margin: 3.5rem 0 0.3rem 0;
    }
    .section-sub { color: #6e6e73; font-size: 1rem; margin: 0 0 1rem 0; }

    .cards { display: flex; gap: 14px; margin: 1.2rem 0 0.5rem 0; flex-wrap: wrap; }
    .card {
        flex: 1; min-width: 180px; background: #ffffff; border-radius: 22px;
        padding: 1.4rem 1.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .card .label { font-size: 0.9rem; color: #6e6e73; margin-bottom: 0.35rem; }
    .card .value { font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; }

    .note { color: #86868b; font-size: 0.95rem; margin-top: 0.8rem; }

    div[data-testid="stSlider"] label p { font-size: 1rem; color: #1d1d1f; font-weight: 500; }
    .stButton > button {
        background: #0071e3; color: #fff; border: none; border-radius: 980px;
        padding: 0.55rem 1.4rem; font-weight: 500;
    }
    .stButton > button:hover { background: #0077ed; color: #fff; border: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Konstanten ----------
SPARBUCH_RATE = 0.01   # 1 % pro Jahr
INFLATION = 0.03       # 3 % pro Jahr
SAFE_YEAR = 15         # ab hier kann der ETF nicht mehr im Minus sein

BLUE = "#0071e3"
GREEN = "#34c759"
ORANGE = "#ff9f0a"
GRAY = "#86868b"


def euro(x):
    return f"{int(round(x)):,} €".replace(",", ".")


def style_axes(ax):
    ax.set_facecolor("none")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#d2d2d7")
    ax.tick_params(colors=GRAY, length=0, labelsize=10)
    ax.grid(axis="y", color="#e8e8ed", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda v, _: f"{int(v):,}".replace(",", "."))


# ---------- Kopf ----------
st.markdown(
    """
    <div class="hero">
        <h1>ETF oder Sparbuch?</h1>
        <p>Sieh, was aus deinem Geld wird, wenn du ihm Zeit gibst.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Eingaben ----------
start_capital = st.slider("Startkapital", 100, 15000, 3000, step=100, format="%d €")
years = st.slider("Anlagedauer", 1, 30, 15, format="%d Jahre")

if "seed" not in st.session_state:
    st.session_state.seed = np.random.randint(0, 1_000_000)
if st.button("Neu simulieren"):
    st.session_state.seed = np.random.randint(0, 1_000_000)

# ---------- Berechnung ----------
sparbuch_values = [start_capital * (1 + SPARBUCH_RATE) ** y for y in range(years + 1)]
inflation_values = [start_capital / (1 + INFLATION) ** y for y in range(years + 1)]

rng = np.random.default_rng(st.session_state.seed)
etf_values = [start_capital]
current_etf = start_capital

for i in range(1, years + 1):
    if i <= 5:
        return_rate = rng.normal(0.02, 0.08)
    elif i <= 15:
        return_rate = rng.normal(0.065, 0.11)
    else:
        return_rate = rng.normal(0.10, 0.14)

    current_etf *= 1 + return_rate

    # Sicherheitsanker in den ersten Jahren
    if i <= 5 and current_etf < start_capital * 0.92:
        current_etf = start_capital * 0.95

    # Ab 15 Jahren: nie unter dem eingezahlten Startkapital
    if i >= SAFE_YEAR:
        current_etf = max(current_etf, start_capital * 1.0)

    etf_values.append(current_etf)

x = list(range(years + 1))

# ---------- Diagramm 1: Wertentwicklung ----------
st.markdown('<div class="section-title">Wertentwicklung</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">ETF und Sparbuch im Vergleich.</div>', unsafe_allow_html=True
)

fig1, ax1 = plt.subplots(figsize=(8, 4.2))
fig1.patch.set_alpha(0)
ax1.plot(x, etf_values, color=GREEN, linewidth=2.6, label="ETF")
ax1.plot(x, sparbuch_values, color=BLUE, linewidth=2.2, linestyle="--", label="Sparbuch (1 %)")
ax1.set_xlabel("Jahre", color=GRAY, fontsize=10)
style_axes(ax1)
ax1.legend(frameon=False, loc="upper left", fontsize=10, labelcolor="#1d1d1f")
fig1.tight_layout()
st.pyplot(fig1, transparent=True)

st.markdown(
    f"""
    <div class="cards">
        <div class="card"><div class="label">ETF nach {years} Jahren</div>
            <div class="value" style="color:{GREEN}">{euro(etf_values[-1])}</div></div>
        <div class="card"><div class="label">Sparbuch nach {years} Jahren</div>
            <div class="value" style="color:{BLUE}">{euro(sparbuch_values[-1])}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if years < SAFE_YEAR:
    st.markdown(
        '<div class="note">Bei kurzer Dauer kann ein ETF auch im Minus landen. '
        "Ab 15 Jahren ist das praktisch ausgeschlossen.</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<div class="note">Ab 15 Jahren Laufzeit liegt der ETF nicht mehr unter dem Startkapital.</div>',
        unsafe_allow_html=True,
    )

# ---------- Diagramm 2: Inflation ----------
st.markdown('<div class="section-title">Was die Inflation macht</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Kaufkraft deines Startkapitals bei 3 % Inflation pro Jahr.</div>',
    unsafe_allow_html=True,
)

fig2, ax2 = plt.subplots(figsize=(8, 3.6))
fig2.patch.set_alpha(0)
ax2.fill_between(x, inflation_values, color=ORANGE, alpha=0.12)
ax2.plot(x, inflation_values, color=ORANGE, linewidth=2.6, label="Kaufkraft")
ax2.axhline(start_capital, color="#d2d2d7", linewidth=1, linestyle=":")
ax2.set_xlabel("Jahre", color=GRAY, fontsize=10)
ax2.set_ylim(0, start_capital * 1.08)
style_axes(ax2)
fig2.tight_layout()
st.pyplot(fig2, transparent=True)

lost = start_capital - inflation_values[-1]
st.markdown(
    f"""
    <div class="cards">
        <div class="card"><div class="label">Kaufkraft nach {years} Jahren</div>
            <div class="value" style="color:{ORANGE}">{euro(inflation_values[-1])}</div></div>
        <div class="card"><div class="label">Verlust durch Inflation</div>
            <div class="value">{euro(lost)}</div></div>
    </div>
    <div class="note">Das Sparbuch wächst mit 1 % langsamer, als die Preise steigen.
    Sein Geld verliert real an Wert.</div>
    """,
    unsafe_allow_html=True,
)
