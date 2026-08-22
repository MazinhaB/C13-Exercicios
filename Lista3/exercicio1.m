% Lista de Exercícios 3

% 1. Funções e Gráficos 2D

v_tempo = 0:0.1:10;

senoide = 2*sin(3*v_tempo);
cossenoide = 2*cos(3*v_tempo);

figure
plot(v_tempo, senoide);
xlabel('Tempo (s)')
ylabel('Amplitude')
hold on;
plot (v_tempo, cossenoide);
title('Senoide e Cossenoide')
legend('Senoide', 'Cossenoide')
grid on;

disp(length(v_tempo));