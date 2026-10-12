
import numpy as np


def calcular_metricas(t, y, referencia, tolerancia_percentual=2.0):
    """
    Calcula métricas de uma resposta em malha fechada.

    Tempo de subida: intervalo entre 10% e 90% da variação
    entre a temperatura inicial e a referência.

    Tempo de acomodação: instante a partir do qual a resposta
    permanece na faixa de tolerância em torno da referência.

    Erro estacionário: diferença entre a referência e a média
    dos últimos 5% das amostras.
    """

    t = np.asarray(t, dtype=float).flatten()
    y = np.asarray(y, dtype=float).flatten()

    if len(t) != len(y) or len(t) == 0:
        raise ValueError("Os vetores t e y devem ter o mesmo tamanho e não estar vazios.")

    if np.any(np.diff(t) <= 0):
        raise ValueError("O vetor de tempo deve ser estritamente crescente.")

    y0 = y[0]
    amplitude = referencia - y0

    if amplitude == 0:
        raise ValueError("A referência deve ser diferente da temperatura inicial.")

    # Sobressinal em relação à variação solicitada
    if amplitude > 0:
        overshoot = max(0.0, (np.max(y) - referencia) / amplitude * 100)
        nivel_10 = y0 + 0.1 * amplitude
        nivel_90 = y0 + 0.9 * amplitude
        indices_10 = np.where(y >= nivel_10)[0]
        indices_90 = np.where(y >= nivel_90)[0]
    else:
        overshoot = max(0.0, (referencia - np.min(y)) / abs(amplitude) * 100)
        nivel_10 = y0 + 0.1 * amplitude
        nivel_90 = y0 + 0.9 * amplitude
        indices_10 = np.where(y <= nivel_10)[0]
        indices_90 = np.where(y <= nivel_90)[0]

    if len(indices_10) and len(indices_90):
        tempo_subida = t[indices_90[0]] - t[indices_10[0]]
    else:
        tempo_subida = np.nan

    # Tempo de acomodação: tolerância relativa à variação desejada
    tolerancia = (tolerancia_percentual / 100) * abs(amplitude)
    fora_faixa = np.where(np.abs(y - referencia) > tolerancia)[0]

    if len(fora_faixa) == 0:
        tempo_acomodacao = 0.0
    elif fora_faixa[-1] == len(t) - 1:
        tempo_acomodacao = np.nan
    else:
        tempo_acomodacao = t[fora_faixa[-1] + 1]

    # Erro estacionário estimado pela média dos últimos 5%
    n_final = max(1, int(len(y) * 0.05))
    valor_final = float(np.mean(y[-n_final:]))
    erro_estacionario = float(referencia - valor_final)

    return {
        "overshoot_percentual": float(overshoot),
        "tempo_subida": float(tempo_subida),
        "tempo_acomodacao": float(tempo_acomodacao),
        "erro_estacionario": erro_estacionario,
        "valor_final_medio": valor_final,
    }
