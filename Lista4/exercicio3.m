% Sistema massa-atrito - Caixa Cinza

M = 4;
F = 1;

v = 0.5;

B = F/v; 

num = 1;
den = [M B];

disp(B);
G1 = tf(num, den)

figure
step(G1)

grid on
xlabel("Tempo (s)")
ylabel("Velocidade (m/s)")
title("Sistema massa-atrito - Caixa Cinza")