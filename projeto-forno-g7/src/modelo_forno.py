import numpy as np

def simular_fopdt(t, k, tau, theta, delta_u, y0):
    """
    Simula a resposta de um modelo FOPDT a um degrau

    Parâmetros:
        t: vetor de tempo
        k: ganho estático
        tau: constante de tempo
        theta: atraso de transporte
        delta_u: amplitude de variação da entrada
        y0: saída inicial
    
    Retorna:
        Vetor da saída estimada pelo modelo
    """

    t = np.asarray(t, dtype=float).flatten()

    if tau <= 0:
        raise ValueError("tau deve ser positivo")
    
    if theta < 0:
        raise ValueError("theta não pode ser negativo")

    saida = np.full_like(t, y0, dtype=float)
    apos_atraso = t >= theta

    tempo_efetivo = t[apos_atraso] - theta
    saida[apos_atraso] = (y0 + k * delta_u * (1 - np.exp(-tempo_efetivo/tau)))

    return saida

def calcular_eqm(saida_real, saida_modelo):
    """
    Calcula o erro quadrático médio entre a saída experimental e a saída estimada.
    """
    saida_real = np.asarray(saida_real, dtype=float).flatten()
    saida_modelo = np.asarray(saida_modelo, dtype=float).flatten()

    if len(saida_real) != len(saida_modelo):
        raise ValueError("As saídas real e estimada devem ter o mesmo tamanho.")

    if len(saida_real) == 0:
        raise ValueError("As saídas não podem estar vazias.")

    return float(np.mean((saida_real - saida_modelo) ** 2))

def calcular_rmse(saida_real, saida_modelo):
    """
    Calcula a raiz do erro quadrático médio entre
    a saída experimental e a saída estimada.
    """
    saida_real = np.asarray(saida_real, dtype=float).flatten()
    saida_modelo = np.asarray(saida_modelo, dtype=float).flatten()

    if len(saida_real) != len(saida_modelo):
        raise ValueError("As saídas real e estimada devem ter o mesmo tamanho.")

    if len(saida_real) == 0:
        raise ValueError("As saídas não podem estar vazias.")

    return float(np.sqrt(np.mean((saida_real - saida_modelo) ** 2)))
