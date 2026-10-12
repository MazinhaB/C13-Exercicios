
import numpy as np


def _validar_dados(t, saida, delta_u):
    """
    Valida os dados necessários para identificar a planta.
    """
    t = np.asarray(t, dtype=float).flatten()
    saida = np.asarray(saida, dtype=float).flatten()

    if len(t) != len(saida):
        raise ValueError("Tempo e saída devem ter o mesmo tamanho.")

    if len(t) < 3:
        raise ValueError("São necessárias pelo menos três amostras.")

    if delta_u <= 0:
        raise ValueError("delta_u deve ser positivo.")

    if np.any(np.diff(t) <= 0):
        raise ValueError("O vetor de tempo deve ser crescente.")

    return t, saida


def _parametros_por_niveis(t, saida, delta_u, nivel1, nivel2):
    """
    Calcula os parâmetros FOPDT a partir de dois níveis
    percentuais da variação estimada da temperatura.
    """
    t, saida = _validar_dados(t, saida, delta_u)

    y0 = np.mean(saida[t < 10])
    yf = np.mean(saida[t >= t[-1] - 10])
    delta_y = yf - y0

    if delta_y <= 0:
        raise ValueError("A variação da saída deve ser positiva.")

    y1 = y0 + nivel1 * delta_y
    y2 = y0 + nivel2 * delta_y

    indices1 = np.where(saida >= y1)[0]
    indices2 = np.where(saida >= y2)[0]

    if len(indices1) == 0 or len(indices2) == 0:
        raise ValueError("A resposta não atingiu os níveis necessários.")

    t1 = t[indices1[0]]
    t2 = t[indices2[0]]

    if t2 <= t1:
        raise ValueError("Os tempos de cruzamento são inválidos.")

    return y0, yf, delta_y / delta_u, t1, t2


def smith(t, saida, delta_u):
    """
    Identifica o modelo FOPDT pelo método de Smith.
    """
    y0, yf, k, t28, t63 = _parametros_por_niveis(t, saida, delta_u, 0.283, 0.632)

    tau = 1.5 * (t63 - t28)
    theta = 1.5 * t28 - 0.5 * t63

    return {
        "metodo": "Smith",
        "k": k,
        "tau": tau,
        "theta": theta,
        "y0": y0,
        "yf_estimado": yf,
    }


def sundaresan(t, saida, delta_u):
    """
    Identifica o modelo FOPDT pelo método de Sundaresan.
    """
    y0, yf, k, t35, t85 = _parametros_por_niveis(t, saida, delta_u, 0.353, 0.853)

    tau = 0.67 * (t85 - t35)
    theta = 1.3 * t35 - 0.29 * t85

    return {
        "metodo": "Sundaresan",
        "k": k,
        "tau": tau,
        "theta": theta,
        "y0": y0,
        "yf_estimado": yf,
    }
