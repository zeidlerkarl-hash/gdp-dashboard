import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 ETF vs. Sparbuch")
st.markdown("**Kurzfristig riskant? Langfristig eine Rakete? Probier's aus!**")

# Eingaben über Regler
start_capital = st.slider("Startkapital in Euro", 100, 15000, 3000, step=100)
years = st.slider("Anlagedauer in Jahren", 1, 30, 15)

# Feste Sparbuch-Rendite (1.5%)
sparbuch_rate = 0.015
sparbuch_values = [start_capital * ((1 + sparbuch_rate) ** y) for y in range(years + 1)]

# Realistische, wellige ETF-Zacken mit gesunden Schwankungen
etf_mean = 0.075  
etf_std = 0.17    # Schöne Volatilität für Zacken im Chart

etf_values = [start_capital]
current_etf = start_capital
for _ in range(years):
    random_return = np.random.normal(etf_mean, etf_std)
    current_etf *= (1 + random_return)
    etf_values.append(current_etf)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(years + 1), etf_values, label="ETF (Zackig & Chancenreich)", color="#2ecc71", linewidth=2.5)
ax.plot(range(years + 1), sparbuch_values, label="Sparbuch (Konstant 1.5%)", color="#3498db", linestyle="--", linewidth=2)

ax.set_xlabel("Jahre")
ax.set_ylabel("Kapital in €")
ax.set_title("Wertentwicklung", fontsize=12, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Ultra-kurze Info für Schüler (Zero Blabla)
if years <= 3:
    st.warning("⚡ **Kurzfrist-Check:** Hier siehst du die Zacken. Auf kurze Sicht kann es auch mal ins Minus gehen – Risiko pur!")
elif years >= 12:
    st.fire("🔥 **Zinseszinseffekt:** Ab 10+ Jahren bügeln sich die Zacken weg und die Kurve schießt exponentiell nach oben!")
else:
    st.info("💡 **Der Verlauf:** Schieb den Regler mal ganz nach links (1 Jahr) und ganz nach rechts (30 Jahre) zum Vergleich.")

# Endergebnis kompakt
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="ETF-Ende", value=f"{int(etf_values[-1]):,} €".replace(",", "."))
with col2:
    st.metric(label="Sparbuch-Ende", value=f"{int(sparbuch_values[-1]):,} €".replace(",", "."))
