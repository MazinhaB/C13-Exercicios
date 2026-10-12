import numpy as np

from scipy.io import loadmat
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_DATASET = RAIZ_PROJETO / "data" / "Forno_G7.mat"

def carregar_dados():
    """
    Carrega os dados experimentais do forno (grupo 7)

    Retorna:
        t: vetor de tempo
        degrau: sinal de entrada registrado no dataset
        saida: temperatura medida
    """
    if not CAMINHO_DATASET.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {CAMINHO_DATASET}")
    
    dados = loadmat(CAMINHO_DATASET)

    t = np.asarray(dados["t"]).flatten()
    degrau = np.asarray(dados["Degrau"]).flatten()
    saida = np.asarray(dados["Saida"]).flatten()

    if not (len(t) == len(degrau) == len(saida)):
        raise ValueError("Os vetores de tempo, entrada e saida devem ter o mesmo número de amostras")

    return t, degrau, saida