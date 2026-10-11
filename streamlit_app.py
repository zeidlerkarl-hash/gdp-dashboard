import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------- Seite ----------
st.set_page_config(page_title="ETF vs. Sparbuch", page_icon="📈", layout="centered")

# Farben: Blau = ETF, Orange = Sparbuch, Grau = Preise
ETF_C = "#0071e3"
SPAR_C = "#ff9f0a"
PRICE_C = "#8e8e93"
INK = "#1d1d1f"
SOFT = "#6e6e73"


def html(s):
    """Entfernt Einrückungen und Leerzeilen. Sonst zeigt Markdown den HTML-Code
    als Code-Block an und die Seite wird zu breit (seitliches Wischen)."""
    return " ".join(line.strip() for line in s.splitlines() if line.strip())


def show(s):
    st.markdown(html(s), unsafe_allow_html=True)


show(
    f"""
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        overflow-x: hidden !important;
        max-width: 100vw;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Helvetica Neue", Arial, sans-serif;
        color: {INK};
    }}
    .stApp {{ background: #fbfbfd; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ max-width: 760px; padding: 4rem 1.5rem 5rem 1.5rem; }}
    img, svg {{ max-width: 100%; height: auto; }}

    .hero h1 {{
        font-size: 3.2rem; font-weight: 700; letter-spacing: -0.03em;
        line-height: 1.05; margin: 0 0 0.6rem 0;
    }}
    .hero p {{ font-size: 1.3rem; color: {SOFT}; margin: 0 0 3rem 0; line-height: 1.4; }}

    .section-title {{
        font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em;
        margin: 3.5rem 0 0.3rem 0;
    }}
    .section-sub {{ color: {SOFT}; font-size: 1rem; margin: 0 0 1.2rem 0; line-height: 1.5; }}

    .panel {{
        background: #ffffff; border-radius: 22px; padding: 1.5rem;
        margin-top: 14px; font-size: 1.05rem; line-height: 1.55;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }}
    .panel p {{ margin: 0 0 0.9rem 0; }}
    .panel p:last-child {{ margin-bottom: 0; }}

    .story-head {{ font-size: 1rem; color: {SOFT}; margin-bottom: 0.3rem; }}
    .dot {{
        display: inline-block; width: 10px; height: 10px; border-radius: 50%;
        margin-right: 8px;
    }}
    .story-big {{ font-size: 2.2rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 0.8rem; }}

    .bar {{
        position: relative; height: 14px; background: #ececf0;
        border-radius: 980px; margin: 1.6rem 0 2.2rem 0;
    }}
    .fill {{ height: 100%; border-radius: 980px; }}
    .marker {{
        position: absolute; top: -6px; width: 2px; height: 26px; background: {INK};
    }}
    .marker-label {{
        position: absolute; top: 24px; transform: translateX(-50%);
        font-size: 0.8rem; color: {SOFT}; white-space: nowrap;
    }}
    .result {{ font-size: 1.1rem; }}

    div[data-testid="stSlider"] label p {{ font-size: 1rem; color: {INK}; font-weight: 500; }}
    .stButton > button {{
        background: {ETF_C}; color: #fff; border: none; border-radius: 980px;
        padding: 0.55rem 1.4rem; font-weight: 500;
    }}
    .stButton > button:hover {{ background: #0077ed; color: #fff; border: none; }}

    @media (max-width: 640px) {{
        .block-container {{ padding: 2.5rem 1.1rem 4rem 1.1rem; }}
        .hero h1 {{ font-size: 2.3rem; }}
        .hero p {{ font-size: 1.1rem; margin-bottom: 2rem; }}
        .section-title {{ font-size: 1.3rem; margin-top: 2.5rem; }}
        .story-big {{ font-size: 1.9rem; }}
        .panel {{ padding: 1.2rem; font-size: 1rem; }}
    }}
    </style>
    """
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
    ax.tick_params(colors=SOFT, length=0, labelsize=10)
    ax.grid(axis="y", color="#e8e8ed", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(lambda v, _: f"{int(v):,}".replace(",", "."))


# ---------- Kopf ----------
show(
    """
    <div class="hero">
        <h1>ETF oder Sparbuch?</h1>
        <p>Sieh, was aus deinem Geld wird, wenn du ihm Zeit gibst.</p>
    </div>
    """
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
# So viel Geld brauchst du später, um dir dasselbe zu kaufen wie heute mit dem Startkapital
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

# ---------- Diagramm ----------
show('<div class="section-title">Dein Geld im Zeitverlauf</div>')
show(
    """
    <div class="section-sub">
        Die graue Linie zeigt, wie viel Geld du später bräuchtest, um dir dasselbe zu kaufen wie heute.
        Der orange Bereich ist das, was dem Sparbuch dazu fehlt.
    </div>
    """
)

fig, ax = plt.subplots(figsize=(8, 4.4))
fig.patch.set_alpha(0)
ax.fill_between(
    x, sparbuch_values, price_values,
    where=np.array(price_values) > np.array(sparbuch_values),
    color=SPAR_C, alpha=0.16, linewidth=0, label="Das fehlt dem Sparbuch",
)
ax.plot(x, price_values, color=PRICE_C, linewidth=2.2, linestyle=":", label="Preise steigen (3 %)")
ax.plot(x, sparbuch_values, color=SPAR_C, linewidth=2.6, label="Sparbuch (1 %)")
ax.plot(x, etf_values, color=ETF_C, linewidth=2.8, label="ETF")
ax.set_xlabel("Jahre", color=SOFT, fontsize=10)
style_axes(ax)
ax.legend(frameon=False, loc="upper left", fontsize=10, labelcolor=INK)
fig.tight_layout()
st.pyplot(fig, transparent=True)
plt.close(fig)

# ---------- Auswertung als Geschichte ----------
price_rise = (price_end / start_capital - 1) * 100
pct_etf = etf_end / price_end * 100
pct_sp = sparbuch_end / price_end * 100
scale = max(100, pct_etf, pct_sp)

show(f'<div class="section-title">Und was bleibt nach {years} Jahren wirklich?</div>')
show(
    f"""
    <div class="panel">
        <p>Stell dir einen Einkaufskorb vor, der heute <b>{euro(start_capital)}</b> kostet.</p>
        <p>In {years} Jahren sind die Preise um <b>{int(round(price_rise))} %</b> gestiegen.
        Derselbe Korb kostet dann <b>{euro(price_end)}</b>.</p>
        <p>Mit dieser Zahl vergleichen wir jetzt dein Geld:</p>
    </div>
    """
)


def story(color, subject, name, value, pct):
    gain = value - start_capital
    diff = value - price_end
    plus = gain >= 0
    big = f"{'+' if plus else '−'}{euro(abs(gain))}"
    top = (
        f"{subject} hat in der Simulation <b>{euro(abs(gain))} {'Plus' if plus else 'Minus'}</b> gemacht. "
        f"Auf dem Konto stehen jetzt <b>{euro(value)}</b>."
    )
    if diff < 0:
        but = (
            f"<b>Aber:</b> Der Korb kostet jetzt {euro(price_end)}. "
            f"Dir fehlen <b>{euro(-diff)}</b>."
        )
        result = (
            f"Du kannst dir nur noch <b>{int(round(pct))} %</b> vom Korb kaufen. "
            f"Das ist ein <b>echtes Minus von {max(1, int(round(100 - pct)))} %</b>."
        )
    else:
        but = (
            f"<b>Und:</b> Der Korb kostet jetzt {euro(price_end)}. "
            f"Dir bleiben <b>{euro(diff)}</b> übrig."
        )
        result = (
            f"Du kannst dir <b>{int(round(pct))} %</b> vom Korb kaufen. "
            f"Das ist ein <b>echtes Plus von {max(1, int(round(pct - 100)))} %</b>."
        )

    fill = min(pct / scale * 100, 100)
    marker = 100 / scale * 100

    show(
        f"""
        <div class="panel">
            <div class="story-head"><span class="dot" style="background:{color}"></span>{name}</div>
            <div class="story-big" style="color:{color}">{big}</div>
            <p>{top}</p>
            <p>{but}</p>
            <div class="bar">
                <div class="fill" style="width:{fill:.1f}%; background:{color}"></div>
                <div class="marker" style="left:{marker:.1f}%"></div>
                <div class="marker-label" style="left:clamp(16%, {marker:.1f}%, 84%)">so viel wie früher</div>
            </div>
            <p class="result">{result}</p>
        </div>
        """
    )


story(SPAR_C, "Das Sparbuch", "Sparbuch", sparbuch_end, pct_sp)
story(ETF_C, "Der ETF", "ETF", etf_end, pct_etf)

# ---------- Fazit ----------
if sparbuch_end < price_end:
    fazit_sp = (
        "Beim Sparbuch wird die Zahl auf dem Konto größer, aber die Preise wachsen schneller. "
        "Dein Geld ist am Ende <b>weniger wert</b>. Das nennt man <b>Inflation</b>."
    )
else:
    fazit_sp = "Das Sparbuch kommt hier mit den steigenden Preisen mit."

if etf_end >= price_end:
    fazit_etf = "Der ETF wächst schneller als die Preise, darum bleibt dein Geld wertvoll."
else:
    fazit_etf = "Der ETF hat die Preise hier noch nicht eingeholt. Mit mehr Zeit klappt das meist."

show(f'<div class="panel"><p>{fazit_sp}</p><p>{fazit_etf}</p></div>')

if years < SAFE_YEAR:
    st.caption("Bei weniger als 15 Jahren kann ein ETF auch im Minus landen. Ab 15 Jahren ist das praktisch ausgeschlossen.")
