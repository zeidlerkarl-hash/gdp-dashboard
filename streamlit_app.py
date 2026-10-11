import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- Seite & Design ----------
st.set_page_config(page_title="ETF vs. Sparbuch", page_icon="📈", layout="centered")

# Ruhige Farbwelt: ein Akzent (Apple-Blau) + Grautöne
ACCENT = "#0071e3"   # ETF
INK = "#1d1d1f"      # Sparbuch
MUTED = "#a1a1a6"    # Preise / Inflation
TEXT_SOFT = "#6e6e73"

st.markdown(
    f"""
    <style>
    html, body, [class*="css"], .stApp {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Helvetica Neue", Arial, sans-serif;
        color: {INK};
    }}
    .stApp {{ background: #fbfbfd; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ max-width: 760px; padding-top: 4.5rem; padding-bottom: 5rem; }}

    .hero h1 {{
        font-size: 3.2rem; font-weight: 700; letter-spacing: -0.03em;
        line-height: 1.05; margin: 0 0 0.6rem 0;
    }}
    .hero p {{ font-size: 1.3rem; color: {TEXT_SOFT}; margin: 0 0 3rem 0; line-height: 1.4; }}

    .section-title {{
        font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em;
        margin: 3.5rem 0 0.3rem 0;
    }}
    .section-sub {{ color: {TEXT_SOFT}; font-size: 1rem; margin: 0 0 1.2rem 0; line-height: 1.5; }}

    .cards {{ display: flex; gap: 14px; margin: 1.2rem 0 0.5rem 0; flex-wrap: wrap; }}
    .card {{
        flex: 1; min-width: 200px; background: #ffffff; border-radius: 22px;
        padding: 1.5rem 1.5rem 1.3rem 1.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    .card .dot {{
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        margin-right: 8px;
    }}
    .card .label {{ font-size: 0.95rem; color: {TEXT_SOFT}; margin-bottom: 0.4rem; }}
    .card .value {{ font-size: 2rem; font-weight: 700; letter-spacing: -0.02em; }}
    .card .line {{ font-size: 0.95rem; color: {TEXT_SOFT}; margin-top: 0.9rem; line-height: 1.45; }}
    .card .line b {{ color: {INK}; font-weight: 600; }}

    .summary {{
        background: #ffffff; border-radius: 22px; padding: 1.5rem;
        margin-top: 1.2rem; font-size: 1.05rem; line-height: 1.55;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}

    div[data-testid="stSlider"] label p {{ font-size: 1rem; color: {INK}; font-weight: 500; }}
    .stButton > button {{
        background: {ACCENT}; color: #fff; border: none; border-radius: 980px;
        padding: 0.55rem 1.4rem; font-weight: 500;
    }}
    .stButton > button:hover {{ background: #0077ed; color: #fff; border: none; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Konstanten ----------
SPARBUCH_RATE = 0.01   # 1 % pro Jahr
INFLATION = 0.03       # 3 % pro Jahr
SAFE_YEAR = 15         # ab hier kann der ETF nicht mehr im Minus sein


def euro(x):
    return f"{int(round(x)):,} €".replace(",", ".")


def style_axes(ax):
    ax.set_facecolor("none")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#d2d2d7")
    ax.tick_params(colors=TEXT_SOFT, length=0, labelsize=10)
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
# So viel Geld brauchst du, um dir später dasselbe zu kaufen wie heute mit dem Startkapital
price_values = [start_capital * (1 + INFLATION) ** y for y in range(years + 1)]

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
etf_end, sparbuch_end, price_end = etf_values[-1], sparbuch_values[-1], price_values[-1]

# ---------- Ein Diagramm für alles ----------
st.markdown('<div class="section-title">Dein Geld im Zeitverlauf</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Die graue Linie zeigt, wie teuer alles wird. '
    "Liegt deine Linie darüber, kannst du dir mehr leisten als am Anfang.</div>",
    unsafe_allow_html=True,
)

fig, ax = plt.subplots(figsize=(8, 4.4))
fig.patch.set_alpha(0)
ax.plot(x, price_values, color=MUTED, linewidth=2.2, linestyle=":", label="Preise steigen (3 %)")
ax.plot(x, sparbuch_values, color=INK, linewidth=2.2, linestyle="--", label="Sparbuch (1 %)")
ax.plot(x, etf_values, color=ACCENT, linewidth=2.8, label="ETF")
ax.set_xlabel("Jahre", color=TEXT_SOFT, fontsize=10)
style_axes(ax)
ax.legend(frameon=False, loc="upper left", fontsize=10, labelcolor=INK)
fig.tight_layout()
st.pyplot(fig, transparent=True)

# ---------- Auswertung in einfacher Sprache ----------
st.markdown(f'<div class="section-title">Das Ergebnis nach {years} Jahren</div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="summary">
        Alles wird mit der Zeit teurer. Was heute <b>{euro(start_capital)}</b> kostet,
        kostet dann <b>{euro(price_end)}</b>. Genau so viel brauchst du am Ende,
        um dir dasselbe zu kaufen wie heute.
    </div>
    """,
    unsafe_allow_html=True,
)


def card(color, name, value, own_text, real_diff):
    if real_diff >= 0:
        real = f"Du kannst dir <b>{euro(real_diff)} mehr</b> leisten als am Anfang."
    else:
        real = f"Du kannst dir <b>{euro(-real_diff)} weniger</b> leisten als am Anfang."
    return f"""
        <div class="card">
            <div class="label"><span class="dot" style="background:{color}"></span>{name}</div>
            <div class="value">{value}</div>
            <div class="line">{own_text}<br>{real}</div>
        </div>
    """


etf_gain = etf_end - start_capital
sp_gain = sparbuch_end - start_capital

st.markdown(
    '<div class="cards">'
    + card(ACCENT, "ETF", euro(etf_end), f"Du hast <b>{euro(etf_gain)} mehr</b> Euro als am Anfang.", etf_end - price_end)
    + card(INK, "Sparbuch", euro(sparbuch_end), f"Du hast <b>{euro(sp_gain)} mehr</b> Euro als am Anfang.", sparbuch_end - price_end)
    + "</div>",
    unsafe_allow_html=True,
)

# Fazit
if sparbuch_end < price_end:
    sparbuch_fazit = (
        f"Auf dem Sparbuch hast du zwar mehr Euro, aber du kannst dir damit "
        f"<b>weniger kaufen</b>. Dein Geld hat <b>{euro(price_end - sparbuch_end)}</b> an Wert verloren."
    )
else:
    sparbuch_fazit = "Das Sparbuch hält mit den steigenden Preisen mit."

if etf_end >= price_end:
    etf_fazit = "Der ETF wächst schneller als die Preise. Dein Geld wird wirklich mehr wert."
else:
    etf_fazit = "Der ETF schafft es hier noch nicht, die steigenden Preise zu schlagen."

st.markdown(
    f'<div class="summary">{sparbuch_fazit}<br><br>{etf_fazit}</div>',
    unsafe_allow_html=True,
)

if years < SAFE_YEAR:
    st.caption("Bei weniger als 15 Jahren kann ein ETF auch im Minus landen. Ab 15 Jahren ist das praktisch ausgeschlossen.")
