
import numpy as np
import matplotlib.pyplot as plt

from src.dados import carregar_dados
from src.identificacao import smith
from src.modelo_forno import simular_fopdt, calcular_rmse


# 1. Carregar os dados experimentais
t, _, saida = carregar_dados()

# 2. Identificar o modelo pelo método de Smith
delta_u = 50.0
modelo = smith(t, saida, delta_u)

k = modelo["k"]
tau = modelo["tau"]
theta = modelo["theta"]
y0 = modelo["y0"]

# 3. Simular o modelo FOPDT
saida_modelo = simular_fopdt(t=t, k=k, tau=tau, theta=theta, delta_u=delta_u, y0=y0,)

# 4. Calcular o RMSE
rmse = calcular_rmse(saida, saida_modelo)

# 5. Analisar o erro nos últimos 10 segundos
mascara_final = t >= t[-1] - 10
erro_final = saida[mascara_final] - saida_modelo[mascara_final]

print("=== Validação do modelo de Smith ===")
print(f"k = {k:.5f}")
print(f"tau = {tau:.2f} s")
print(f"theta = {theta:.2f} s")
print(f"RMSE = {rmse:.4f} °C")

print("\n=== Análise do erro nos últimos 10 segundos ===")
print(f"Erro médio: {np.mean(erro_final):.4f} °C")
print(f"Erro máximo absoluto: {np.max(np.abs(erro_final)):.4f} °C")

# 6. Temperatura média por janela de 10 segundos
print("\n=== Temperatura média por janela de 10 segundos ===")

for inicio in range(0, int(t[-1]) + 1, 10):
    mascara = (t >= inicio) & (t < inicio + 10)

    if np.any(mascara):
        media = np.mean(saida[mascara])
        print(f"{inicio:3d}-{inicio + 10:3d} s: {media:.3f} °C")

# 7. Gráfico de comparação
plt.figure(figsize=(11, 6))

plt.plot(t, saida, label="Temperatura experimental", alpha=0.7,)

plt.plot(t, saida_modelo, label="Modelo FOPDT - Smith", linewidth=2,)

plt.xlabel("Tempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Validação do modelo do forno - Grupo 7")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()