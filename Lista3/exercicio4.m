% Comparação de escalas

t = 0.1:0.1:1000;
y = 50000 * exp(-0.05*t);

figure
subplot(2,1,1)
plot(t, y)
grid on
xlabel("Tempo(s)")
ylabel("Amplitude")
title("Escala normal")

subplot(2,1,2)
semilogy(t, y)
grid on
xlabel("Tempo(s)")
ylabel("Amplitude")
title("Escala log em Y")

