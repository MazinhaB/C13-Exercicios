% Sistema massa-mola-amortecedor - Caixa branca

M = 2;
B = 3;
K = 8;

num = [B K]; % numerador F.I.
den = [M B K]; % vetor representando o denominador

G1 = tf(num, den)

figure
step(G1, 15)
hold on
plot([0 0 15], [0 1 1], "r--", "LineWidth", 1.5)

grid on
xlabel("Tempo (s)")
ylabel("Deslocamento vertical y (m)")
title("Sistema massa-mola-amortecedor - Caixa Branca")