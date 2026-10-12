
import numpy as np
import matplotlib.pyplot as plt

from src.dados import carregar_dados
from src.identificacao import smith
from src.controladores import sintonia_chr, sintonia_cohen_coon
from src.metricas import calcular_metricas
from src.simulacao_pid import simular_pid

# 1. Dados e modelo identificado
t_exp, degrau, saida_exp = carregar_dados()
y0 = float(np.mean(saida_exp[t_exp < 10]))

delta_u = 50.0
modelo = smith(t_exp, saida_exp, delta_u)

k = modelo["k"]
tau = modelo["tau"]
theta = modelo["theta"]

# 2. Condições da simulação
setpoint = 40.0
tempo_total = 600.0
dt = 0.1

# 3. Sintonia dos controladores
controladores = {
    "CHR sem sobressinal": sintonia_chr(k, tau, theta),
    "Cohen-Coon": sintonia_cohen_coon(k, tau, theta),
}

resultados = {}

for nome, (kp, ti, td) in controladores.items():
    t, temperatura, comando = simular_pid(
        k=k,
        tau=tau,
        theta=theta,
        y0=y0,
        setpoint=setpoint,
        kp=kp,
        ti=ti,
        td=td,
        tempo_total=tempo_total,
        dt=dt,
        u_min=0.0,
        u_max=100.0,
    )

    metricas = calcular_metricas(t, temperatura, referencia=setpoint)
    resultados[nome] = (t, temperatura, comando, metricas)

    print(f"\n=== {nome} ===")
    print(f"Kp = {kp:.4f}")
    print(f"Ti = {ti:.4f} s")
    print(f"Td = {td:.4f} s")
    print(f"Potência mínima = {comando.min():.2f}%")
    print(f"Potência máxima = {comando.max():.2f}%")
    print(f"Overshoot percentual = {metricas['overshoot_percentual']:.2f}%")
    print(f"Tempo de subida = {metricas['tempo_subida']:.2f} s")
    print(f"Tempo de acomodação = "f"{metricas['tempo_acomodacao']:.2f} s")
    print(f"Erro estacionario = {metricas['erro_estacionario']:.2f} °C")


# 4. Gráfico da temperatura
plt.figure(figsize=(12, 6))

for nome, (t, temperatura, comando, metricas) in resultados.items():
    plt.plot(t, temperatura, label=nome)

plt.axhline(setpoint, linestyle="--", label=f"SetPoint = {setpoint:.1f} °C",)

plt.xlabel("Tempo (s)")
plt.ylabel("Temperatura (°C)")
plt.title("Controle PID do forno - Grupo 7")
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()


# 5. Gráfico do comando do atuador
plt.figure(figsize=(12, 5))

for nome, (t, temperatura, comando, metricas) in resultados.items():
    plt.plot(t, comando, label=nome)

plt.xlabel("Tempo (s)")
plt.ylabel("Potência comandada (%)")
plt.title("Comando dos controladores PID")
plt.ylim(-5, 105)
plt.grid(True, alpha=0.4)
plt.legend()
plt.tight_layout()
plt.show()
