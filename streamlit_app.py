import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("ETF vs. Sparbuch")
st.markdown("**Die magische Reise des Geldes, wie schlägt sich ein Etf gegenüber dem Sparbuch?**")

# Eingaben über Regler
start_capital = st.slider("Startkapital in Euro", 100, 15000, 3000, step=100)
years = st.slider("Anlagedauer in Jahren", 1, 30, 15)

# Feste Sparbuch-Rendite (1.5%)
sparbuch_rate = 0.015
sparbuch_values = [start_capital * ((1 + sparbuch_rate) ** y) for y in range(years + 1)]

# Realistische ETF-Modellierung mit perfektem zeitlichen Verlauf
np.random.seed() # Frischer Zufall bei jedem Laden
etf_values = [start_capital]
current_etf = start_capital

for i in range(1, years + 1):
    if i <= 5:
        # Phase 1: Ganz nah am Sparbuch (knapp drüber oder drunter, leichte Zacken)
        return_rate = np.random.normal(0.02, 0.08)
    elif i <= 15:
        # Phase 2: Solides Wachstum, erkennbar über dem Sparbuch
        return_rate = np.random.normal(0.065, 0.11)
    else:
        # Phase 3: Der Turbo-Modus / exponentielles Wachstum
        return_rate = np.random.normal(0.10, 0.14)
        
    current_etf *= (1 + return_rate)
    # Kleiner Sicherheitsanker, damit es in den ersten Jahren nah am Sparbuch bleibt
    if i <= 5 and current_etf < start_capital * 0.92:
        current_etf = start_capital * 0.95
        
    etf_values.append(current_etf)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(years + 1), etf_values, label="ETF (Chancenreich & Dynamisch)", color="#2ecc71", linewidth=2.5)
ax.plot(range(years + 1), sparbuch_values, label="Sparbuch (Konstant 1.5%)", color="#3498db", linestyle="--", linewidth=2)

ax.set_xlabel("Jahre")
ax.set_ylabel("Kapital in €")
ax.set_title("Wertentwicklung im Zeitverlauf", fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Ultra-kurze Info für Mitschüler
if years <= 5:
    st.warning("⚖️ **1–5 Jahre:** Kopf-an-Kopf-Rennen! Hier merkst du kaum einen Unterschied zum Sparbuch – manchmal bist du sogar kurz im Minus. Kurzfristig lohnt sich das Risiko kaum.")
elif years <= 15:
    st.info("📈 **5–15 Jahre:** Der ETF steigt schneller an. Der Abstand zum Sparbuch wird Monat für Monat deutlicher.")
else:
    st.success("🚀 **15+ Jahre (Die Rakete):** Schau dir diesen Anstieg an! Hier greift der Zinseszinseffekt voll – der ETF explodiert förmlich nach oben.")

# Endergebnis kompakt
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="ETF-Ende", value=f"{int(etf_values[-1]):,} €".replace(",", "."))
with col2:
    st.metric(label="Sparbuch-Ende", value=f"{int(sparbuch_values[-1]):,} €".replace(",", "."))
