% Entrada de dados, condição e gráfico

a = input("Entre com o valor do coeficiente a: ");

x = -10:0.1:10;

y = a*x + 2;

if a < 0
    disp("Coeficiente negativo.");
elseif a == 0
    disp("Coeficiente igual a zero.");
else
    disp("Coeficiente positivo.");
end

figure
plot(x, y, 'LineWidth', 2);
xlabel('x');
ylabel('y');
axes('Position', [0.3, 0.6, 0.25, 0.25])
box on
plot(x, y, 'LineWidth', 1.5);
xlim([-2, 2]);
