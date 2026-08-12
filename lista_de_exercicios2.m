% Lista de exercicios 2
%clc;
%clear all;
%close all;

% 1.Entrada e saida
%cidade = input('Entre com o nome de uma cidade: ', 's');
%disp(cidade);
%fprintf("Cidade escolhida: %s \n", cidade);

%2. if, elseif, else
%x = 7;
%x = 10;
x = 12;
if x > 10
    disp("Maior que 10");
elseif x == 10
    disp("Igual a 10");
else
    disp("Menor que 10");
end

%3. for
for i = 1:1:5
    aux = i*3;
    disp(aux);
end

% 4. while
x1 = 0;
i = 0;

while i < 5
    x1 = x1 + 1;
    i = i + 1;
    disp(x1);
end

% 5. switch e funcao
opcao = 2;

switch(opcao)
    case 1
        disp("Opcao A");
    case 2
        disp("Opcao B");
    case 3
        disp("Opcao C");
    otherwise
        disp("Opcao invalida");
end

retorno_funcao = funcao_triplo(5);