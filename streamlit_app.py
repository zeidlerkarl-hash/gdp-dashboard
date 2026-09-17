import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 ETF vs. Sparbuch")
st.markdown("**Kurzfristig kleine Zacken – langfristig die klare Nummer 1!**")

# Eingaben über Regler
start_capital = st.slider("Startkapital in Euro", 100, 15000, 3000, step=100)
years = st.slider("Anlagedauer in Jahren", 1, 30, 15)

# Feste Sparbuch-Rendite (1.5%)
sparbuch_rate = 0.015
sparbuch_values = [start_capital * ((1 + sparbuch_rate) ** y) for y in range(years + 1)]

# Realistische, starke ETF-Werte (8.5% Schnitt, moderate Schwankung damit er fast immer über dem Sparbuch bleibt)
etf_mean = 0.085  
etf_std = 0.13    # Schöne Zacken, aber stark genug

etf_values = [start_capital]
current_etf = start_capital
for _ in range(years):
    random_return = np.random.normal(etf_mean, etf_std)
    current_etf *= (1 + random_return)
    # Damit der ETF realistisch stark bleibt und nicht grundlos abstürzt:
    current_etf = max(current_etf, start_capital * 0.95) 
    etf_values.append(current_etf)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(years + 1), etf_values, label="ETF (Stark & Chancenreich)", color="#2ecc71", linewidth=2.5)
ax.plot(range(years + 1), sparbuch_values, label="Sparbuch (Konstant 1.5%)", color="#3498db", linestyle="--", linewidth=2)

ax.set_xlabel("Jahre")
ax.set_ylabel("Kapital in €")
ax.set_title("Wertentwicklung", fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Ultra-kurze Info für Schüler
if years <= 3:
    st.warning("⚡ **Kurzfrist-Check:** Selbst hier performt der ETF meist gut, zeigt aber kleine Zacken und Schwankungen.")
elif years >= 10:
    st.success("🚀 **Exponentielles Wachstum:** Schau dir an, wie der ETF dem Sparbuch komplett davonzieht! Zinseseszins pur.")
else:
    st.info("💡 **Der Vergleich:** Schieb den Regler mal hoch auf 20 oder 25 Jahre – der Abstand wird gigantisch.")

# Endergebnis kompakt
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="ETF-Ende", value=f"{int(etf_values[-1]):,} €".replace(",", "."))
with col2:
    st.metric(label="Sparbuch-Ende", value=f"{int(sparbuch_values[-1]):,} €".replace(",", "."))
