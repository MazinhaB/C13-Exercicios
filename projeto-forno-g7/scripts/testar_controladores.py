
from src.controladores import sintonia_chr, sintonia_cohen_coon


def main():
    # Parâmetros de referência para testar as fórmulas.
    # Este teste não representa a identificação oficial do forno.
    k = 1.30883
    tau = 158.40
    theta = 16.00

    controladores = {
        "CHR sem sobressinal": sintonia_chr(k, tau, theta),
        "Cohen-Coon": sintonia_cohen_coon(k, tau, theta),
    }

    print("=== Teste das fórmulas de sintonia PID ===")

    for nome, (kp, ti, td) in controladores.items():
        assert kp > 0, f"{nome}: Kp deve ser positivo."
        assert ti > 0, f"{nome}: Ti deve ser positivo."
        assert td >= 0, f"{nome}: Td não pode ser negativo."

        print(f"\n{nome}")
        print(f"Kp = {kp:.4f}")
        print(f"Ti = {ti:.4f} s")
        print(f"Td = {td:.4f} s")

    print("\nTodas as verificações passaram.")


if __name__ == "__main__":
    main()
