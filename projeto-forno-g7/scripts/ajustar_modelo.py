
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

from src.dados import carregar_dados
from src.identificacao import smith, sundaresan
from src.modelo_forno import simular_fopdt, calcular_eqm, calcular_rmse


def calcular_residuos(parametros, t, saida, delta_u, y0):
    k, tau, theta = parametros

    saida_modelo = simular_fopdt(t=t, k=k, tau=tau, theta=theta, delta_u=delta_u, y0=y0,)

    return saida - saida_modelo


def main():
    # Carregar os dados
    t, _, saida = carregar_dados()

    delta_u = 50.0
    y0 = float(np.mean(saida[t < 10]))

    # Identificação de Smith
    modelo_smith = smith(t, saida, delta_u)

    k_smith = modelo_smith["k"]
    tau_smith = modelo_smith["tau"]
    theta_smith = modelo_smith["theta"]

    saida_smith = simular_fopdt(t, k_smith, tau_smith, theta_smith, delta_u, y0)

    rmse_smith = calcular_rmse(saida, saida_smith)
    eqm_smith = calcular_eqm(saida, saida_smith)

        # Identificação de Sundaresan
    modelo_sundaresan = sundaresan(t, saida, delta_u)

    k_sund = modelo_sundaresan["k"]
    tau_sund = modelo_sundaresan["tau"]
    theta_sund = modelo_sundaresan["theta"]

    saida_sund = simular_fopdt(t, k_sund, tau_sund, theta_sund, delta_u, y0)

    eqm_sund = calcular_eqm(saida, saida_sund)
    rmse_sund = calcular_rmse(saida, saida_sund)

    # Ajuste numérico a partir dos parâmetros de Smith
    resultado = least_squares(calcular_residuos, x0=[k_smith, tau_smith, theta_smith], bounds=([0.01, 1.0, 0.0], [10.0, 1000.0, 100.0],), args=(t, saida, delta_u, y0),)

    k_ajustado, tau_ajustado, theta_ajustado = resultado.x

    saida_ajustada = simular_fopdt(t, k_ajustado, tau_ajustado, theta_ajustado, delta_u, y0,)

    rmse_ajustado = calcular_rmse(saida, saida_ajustada)
    eqm_ajustado = calcular_eqm(saida, saida_ajustada)

    print("=== Comparação dos modelos do forno ===")
    print("\nMétodo de Smith")
    print(f"k = {k_smith:.5f}")
    print(f"tau = {tau_smith:.4f} s")
    print(f"theta = {theta_smith:.4f} s")
    print(f"RMSE = {rmse_smith:.4f} °C")
    print(f"EQM = {eqm_smith:.4f} °C²")
    print("\nMétodo de Sundaresan")
    print(f"k = {k_sund:.5f}")
    print(f"tau = {tau_sund:.4f} s")
    print(f"theta = {theta_sund:.4f} s")
    print(f"EQM = {eqm_sund:.4f} °C²")
    print(f"RMSE = {rmse_sund:.4f} °C")
    print("\nAjuste por mínimos quadrados")
    print(f"k = {k_ajustado:.5f}")
    print(f"tau = {tau_ajustado:.4f} s")
    print(f"theta = {theta_ajustado:.4f} s")
    print(f"RMSE = {rmse_ajustado:.4f} °C")
    print(f"EQM = {eqm_ajustado:.4f} °C²")
    print(f"Ajuste convergiu: {resultado.success}")
    print(f"Mensagem: {resultado.message}")

    # Gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(t, saida, label="Temperatura experimental", alpha=0.7)
    plt.plot(t, saida_smith, label="Modelo de Smith", linewidth=2)
    plt.plot(t, saida_sund, label="Modelo de Sundaresan", linewidth=2)
    plt.plot(t, saida_ajustada, label="Ajuste por mínimos quadrados", linewidth=2)

    plt.xlabel("Tempo (s)")
    plt.ylabel("Temperatura (°C)")
    plt.title("Comparação dos modelos do forno - Grupo 7")
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    caminho_grafico = "grafico_comparacao_modelos.png"
    plt.savefig(caminho_grafico, dpi=300, bbox_inches="tight")
    print(f"\nGráfico salvo em: {caminho_grafico}")
    plt.show()


if __name__ == "__main__":
    main()
