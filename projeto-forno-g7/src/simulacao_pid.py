
import numpy as np


def simular_pid(k, tau, theta, y0, setpoint, kp, ti, td, tempo_total=600.0, dt=0.1, u_min=0.0, u_max=100.0,):
    """
    Simula o forno FOPDT em malha fechada com PID.
    """

    if tau <= 0 or ti <= 0 or dt <= 0:
        raise ValueError("tau, Ti e dt devem ser positivos.")

    if theta < 0 or u_min >= u_max:
        raise ValueError("Atraso ou limites do atuador inválidos.")

    n = int(tempo_total / dt) + 1
    t = np.arange(n) * dt

    temperatura = np.zeros(n)
    comando = np.zeros(n)
    historico_comando = np.zeros(n)

    temperatura[0] = y0
    atraso_amostras = int(round(theta / dt))
    integral = 0.0

    for i in range(1, n):
        erro = setpoint - temperatura[i - 1]

        derivada_medicao = ((temperatura[i - 1] - temperatura[i - 2]) / dt if i >= 2 else 0.0)

        integral_candidata = integral + erro * dt

        u_pid = (kp * erro + (kp / ti) * integral_candidata - kp * td * derivada_medicao)

        u_limitado = float(np.clip(u_pid, u_min, u_max))

        pode_integrar = (u_min < u_pid < u_max or (u_pid >= u_max and erro < 0) or (u_pid <= u_min and erro > 0))

        if pode_integrar:
            integral = integral_candidata

        comando[i] = u_limitado
        historico_comando[i] = u_limitado

        indice_atrasado = i - atraso_amostras

        entrada_atrasada = (historico_comando[indice_atrasado] if indice_atrasado >= 0 else 0.0)

        temperatura[i] = temperatura[i - 1] + dt * ((k * entrada_atrasada - (temperatura[i - 1] - y0)) / tau)

    return t, temperatura, comando
