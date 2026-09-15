import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Sparbuch vs. ETF Simulation")
st.write("Vergleiche hier die historische und zufällige Wertentwicklung von einem sicheren Sparbuch und einem schwankenden ETF-Portfolio!")

# Eingaben über Regler
start_capital = st.slider("Startkapital in Euro", 100, 10000, 1000, step=100)
years = st.slider("Anlagedauer in Jahren", 5, 30, 15)

# Feste Sparbuch-Rendite (z.B. 1.5%)
sparbuch_rate = 0.015
sparbuch_values = [start_capital * ((1 + sparbuch_rate) ** y) for y in range(years + 1)]

# Zufällige ETF-Rendite mit Normalverteilung (Mittelwert 7%, Schwankung 15%)
etf_mean = 0.07
etf_std = 0.15

etf_values = [start_capital]
current_etf = start_capital
for _ in range(years):
    # Zufälliges Jahr via numpy normal distribution
    random_return = np.random.normal(etf_mean, etf_std)
    current_etf *= (1 + random_return)
    etf_values.append(current_etf)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(range(years + 1), etf_values, label="ETF-Portfolio (Zufallswert)", color="green", linewidth=2.5)
ax.plot(range(years + 1), sparbuch_values, label="Sparbuch (1.5% fest)", color="blue", linestyle="--", linewidth=2)

ax.set_xlabel("Jahre")
ax.set_ylabel("Kapital in €")
ax.set_title("Dein persönlicher Anlagevergleich")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Endergebnis anzeigen
st.subheader("Endergebnis nach Abschluss:")
st.markdown(f"📈 **ETF-Endkapital:** {int(etf_values[-1]):,} €".replace(",", "."))
st.markdown(f"🏦 **Sparbuch-Endkapital:** {int(sparbuch_values[-1]):,} €".replace(",", "."))
