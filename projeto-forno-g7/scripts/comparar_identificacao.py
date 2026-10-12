import matplotlib.pyplot as plt

from src.dados import carregar_dados
from src.identificacao import smith, sundaresan
from src.modelo_forno import simular_fopdt, calcular_rmse


# Carrega o dataset
t, degrau, saida = carregar_dados()

# Hipótese de trabalho: degrau de amplitude 50
delta_u = 50.0

# Temperatura inicial estimada
y0 = saida[t < 10].mean()

# Executa os métodos de identificação
modelos = [
    smith(t, saida, delta_u),
    sundaresan(t, saida, delta_u),
]

resultados = {}

for modelo in modelos:
    nome = modelo["metodo"]

    saida_modelo = simular_fopdt(t=t, k=modelo["k"], tau=modelo["tau"], theta=modelo["theta"], delta_u=delta_u, y0=y0,)

    rmse = calcular_rmse(saida, saida_modelo)

    resultados[nome] = {
        "parametros": modelo,
        "saida": saida_modelo,
        "rmse": rmse,
    }

    print(f"\n=== Método: {nome} ===")
    print(f"k = {modelo['k']:.5f}")
    print(f"tau = {modelo['tau']:.4f} s")
    print(f"theta = {modelo['theta']:.4f} s")
    print(f"RMSE = {rmse:.4f} °C")

# Gráfico comparativo
plt.figure(figsize=(12, 6))

plt.plot(t, saida, label="Temperatura experimental", color="black", alpha=0.7,)

for nome, resultado in resultados.items():
    plt.plot(t, resultado["saida"], label=f"Modelo {nome}",)

plt.xlabel("Tempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Comparação da identificação do forno - Grupo 7")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
