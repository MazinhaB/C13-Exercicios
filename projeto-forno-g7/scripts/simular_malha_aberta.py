
import matplotlib.pyplot as plt

from src.dados import carregar_dados
from src.identificacao import smith
from src.modelo_forno import simular_fopdt, calcular_rmse


# 1. Carregar os dados experimentais
t, degrau, saida_real = carregar_dados()

# 2. Definir as condições usadas na identificação
delta_u = 50.0
y0 = saida_real[t < 10].mean()

# 3. Obter os parâmetros pelo método de Smith
modelo = smith(t, saida_real, delta_u)

k = modelo["k"]
tau = modelo["tau"]
theta = modelo["theta"]

# 4. Simular a resposta do forno em malha aberta
saida_modelo = simular_fopdt(t=t, k=k, tau=tau, theta=theta, delta_u=delta_u, y0=y0,)

# 5. Calcular o erro do modelo
rmse = calcular_rmse(saida_real, saida_modelo)

print("=== Modelo do forno - Método de Smith ===")
print(f"Ganho k: {k:.5f}")
print(f"Constante de tempo tau: {tau:.2f} s")
print(f"Atraso theta: {theta:.2f} s")
print(f"Temperatura inicial: {y0:.2f} °C")
print(f"RMSE: {rmse:.4f} °C")

# 6. Plotar a comparação
plt.figure(figsize=(12, 6))

plt.plot(t, saida_real, label="Temperatura experimental", color="black", linewidth=1, alpha=0.75,)

plt.plot(t, saida_modelo, label="Modelo FOPDT - Smith", linewidth=2,)

plt.xlabel("Tempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Resposta em malha aberta do forno - Grupo 7")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
