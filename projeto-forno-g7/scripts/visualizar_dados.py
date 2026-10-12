import numpy as np
import matplotlib.pyplot as plt

from src.dados import carregar_dados

def main():
    t, degrau, saida = carregar_dados()

    print("Numero de amostras: ", len(t))
    print("Tempo inicial: ", t[0], "s")
    print("Tempo final: ", t[-1], "s")
    print("Intervalo de amostragem: ", t[1] - t[0], "s")

    print("\nValores distintos da entrada: ")
    print(np.unique(degrau))

    print("\nSaída nos primeiros 10 segundos")
    print("Média: ", np.mean(saida[t < 10]))

    print("\nSaída nos últimos 10 segundos")
    print("Média: ", np.mean(saida[t >= t[-1] - 10]))

    # Gráficos
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

    ax[0].plot(t, degrau)
    ax[0].set_ylabel("Entrada (Degrau)")
    ax[0].set_title("Sinal de entrada aplicado ao forno")
    ax[0].grid(True)

    ax[1].plot(t, saida)
    ax[1].set_xlabel("Tempo (s)")
    ax[1].set_ylabel("Temperatura (ºC)")
    ax[1].set_title("Resposta experimental do forno")
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()

    print("\nPrimeiros valores da entrada:")
    print(degrau[:10])

    print("\nÚltimos valores da entrada:")
    print(degrau[-10:])

    print("\nVariação total da entrada:")
    print("Mínimo:", np.min(degrau))
    print("Máximo:", np.max(degrau))
    print("Amplitude:", np.max(degrau) - np.min(degrau))

if __name__ == "__main__":
    main()