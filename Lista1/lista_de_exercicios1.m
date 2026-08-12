% Lista de Exercicios 1

% 1. Operacoes Basicas
a = 12;
b = 5;
soma = a + b;
subtracao = a - b;
multiplicacao = a * b;
divisao = a / b;
potencia = a ^ b;

% 2. Raiz, arredondamento e resto
raiz = sqrt(144);
arredondamento = round(7.6);
arredondamento_cima = ceil(4.01);
resto = rem(405, 83);

% 3. MDC e MMC
max_div_comum = gcd(24, 36);
min_mult_comum = lcm(12, 18);

% 4. Exponencial e Trigonometria
exponencial = exp(2);
seno = sin(30*pi/180);
cosseno = cos(60*pi/180);
tangente = tan(45*pi/180);

% 5. Criando vetores
vet1 = 1:10;
vet2 = 10:-1:1;
vet_pares = 0:2:20;
vet3 = linspace(0,100,5);

% 6. Acessando posicoes de um vetor
vetor1 = [4 8 15 46 23 42];
primeiro = v(1);
ultimo = v(end);
v1 = v(2:4);
v2 = v([1,3,6]);

% 7. Informacoes sobre um vetor
vetor2 = [5 10 15 20 25];
qtd_elementos = length(vetor2);
dimensoes = size(vetor2);
soma_elementos = sum(vetor2);
media_elementos = mean(vetor2);
max_elementos = max(vetor2);
min_elelentos = min(vetor2);

% 8. Vetor linha e vetor coluna
vetor3 = [10 20 30 40];
coluna_vetor3 = vetor3';
dimensoes_antes = size(vetor3);
dimensoes_depois = size(coluna_vetor3);

% 9. Criando e acessando uma matriz
A = [3 6 9;
    2 4 8;
    1 5 7];
el = A(2,3);
linha1 = A(1,:);
coluna2 = A(:, 2);
dimensoes_matriz = size(A);

% 10. Operacoes com matrizes
A1 = [1 2;
    3 4];
B = [2 0;
    1 5];
soma_matrizes = A1 + B;
mult_matrizes = A1 * B;
transposta_A1 = A1';

Mzeros = zeros(3);
Muns = ones(2,4);
Mid = eye(4);
Maleatoria = rand(3);

