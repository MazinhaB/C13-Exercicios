% Circuito RC - Caixa Cinza

R = 1000;
tau = 2; % tau = R * C
C = tau/R;

num = 1;
den = [R*C 1];

disp(C);
G1 = tf(num, den)

figure
step(G1, 10)

grid on
xlabel("Tempo (s)")
ylabel("Tensão (V)")
title("Sistema Circuito RC - Caixa Cinza")