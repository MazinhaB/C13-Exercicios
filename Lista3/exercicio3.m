% Repetição e organização de gráficos

v_multiplos = zeros(1,5);
v_dobro = zeros(1,5);

for i = 1:1:5
    v_multiplos(i) = 3*i;
    v_dobro(i) = 2*v_multiplos(i);
end


figure

subplot(2,1,1)
plot(v_multiplos)
xlabel("Valor")
ylabel("Multiplo de 3")

subplot(2,1,2)
plot(v_dobro);
xlabel("Valor")
ylabel("Dobro do Multiplo de 3")


