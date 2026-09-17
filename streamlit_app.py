import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Sparbuch vs. ETF: Das Finanz-Duell")
st.markdown("Finde heraus, was passiert, wenn du dein Geld für kurze oder lange Zeit anlegst. **Kurzfristig ein Risiko – langfristig eine Rakete?**")

# Eingaben über Regler
start_capital = st.slider("Startkapital in Euro", 100, 15000, 3000, step=100)
years = st.slider("Anlagedauer in Jahren", 1, 30, 15)

# Feste Sparbuch-Rendite (1.5%)
sparbuch_rate = 0.015
sparbuch_values = [start_capital * ((1 + sparbuch_rate) ** y) for y in range(years + 1)]

# Für den ultimativen Effekt: Wir geben dem ETF bei kurzen Laufzeiten eine höhere "Schock-Chance"
# und bei langen Laufzeiten greift der Zinseszinseffekt.
etf_mean = 0.075  # 7.5% Rendite im Schnitt
etf_std = 0.16    # 16% Schwankung (Volatilität)

etf_values = [start_capital]
current_etf = start_capital

# Wenn die Laufzeit super kurz ist (1-3 Jahre), "zwingen" wir im ersten Jahr fast immer einen kleinen Schock rein, 
# damit der Effekt sofort sichtbar wird, falls der Zufall es sonst zu glimpflich ausgehen lassen würde.
for i in range(years):
    if years <= 3 and i == 0:
        # Künstlicher Einbruch im 1. Jahr bei Kurzläufern, um das Risiko zu verdeutlichen
        random_return = np.random.choice([-0.08, -0.14, 0.02])
    else:
        random_return = np.random.normal(etf_mean, etf_std)
    
    current_etf *= (1 + random_return)
    etf_values.append(current_etf)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(years + 1), etf_values, label="ETF-Portfolio (Schwankend & Chancenreich)", color="#2ecc71", linewidth=2.5)
ax.plot(range(years + 1), sparbuch_values, label="Sparbuch (1.5% fest & sicher)", color="#3498db", linestyle="--", linewidth=2)

ax.set_xlabel("Jahre", fontsize=12)
ax.set_ylabel("Kapital in €", fontsize=12)
ax.set_title("Wertentwicklung im Zeitverlauf", fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Dynamische Erklärungen für Schüler (Der "Erleuchtungs-Text")
st.subheader("💡 Was bedeutet das für dich?")

if years <= 3:
    st.warning("⚠️ **Die Kurzfrist-Falle!** Schau dir das Diagramm an: Im ersten Jahr bricht der ETF oft ein. Wer sein Geld kurzfristig braucht (z.B. für den nächsten Urlaub in 2 Jahren), verliert mit Pech Geld. Das Sparbuch ist hier der sichere Hafen – aber ohne echten Gewinn.")
elif years >= 12:
    st.success("🚀 **Das exponentielle Wachstum (Zinseszins)!** Siehst du, wie die grüne Kurve nach ein paar Jahren steil nach oben wegschießt? Die Krisen am Anfang fallen gar nicht mehr ins Gewicht. Genau das ist der Grund, warum langfristiges Anlegen so mächtig ist!")
else:
    st.info("ℹ️ **Die Übergangsphase:** Der ETF schwankt erst hin und her, fängt aber an, dem Sparbuch langsam davonzulaufen. Teste mal den Regler ganz nach links (1–2 Jahre) und dann ganz nach rechts (25–30 Jahre)! Directer Vergleich ist krass.")

# Endergebnis anzeigen
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="ETF-Endkapital", value=f"{int(etf_values[-1]):,} €".replace(",", "."))
with col2:
    st.metric(label="Sparbuch-Endkapital", value=f"{int(sparbuch_values[-1]):,} €".replace(",", "."))
