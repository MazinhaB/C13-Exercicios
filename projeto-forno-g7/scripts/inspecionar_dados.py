
import numpy as np

from src.dados import carregar_dados


t, degrau, saida = carregar_dados()

print("=== Dataset do Forno - Grupo 7 ===")
print(f"Número de amostras: {len(t)}")
print(f"Tempo inicial: {t[0]:.2f} s")
print(f"Tempo final: {t[-1]:.2f} s")
print(f"Intervalo de amostragem: {t[1] - t[0]:.2f} s")

print("\n=== Entrada ===")
print(f"Valor mínimo: {np.min(degrau):.2f}")
print(f"Valor máximo: {np.max(degrau):.2f}")
print(f"Valores distintos: {np.unique(degrau)}")

print("\n=== Temperatura ===")
print(f"Média inicial (primeiros 10 s): " f"{np.mean(saida[t < 10]):.2f} °C")
print(f"Média final (últimos 10 s): " f"{np.mean(saida[t >= t[-1] - 10]):.2f} °C")
