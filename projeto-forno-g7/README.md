# Sistema de Controle PID de um Forno — Grupo 7

## 1. Descrição do projeto

Este projeto tem como objetivo identificar e modelar a dinâmica térmica de um forno e avaliar o desempenho de diferentes métodos de sintonia de controladores PID.

A partir de dados experimentais de temperatura, utiliza-se um modelo de primeira ordem com atraso (*First-Order Plus Dead Time* — FOPDT) para representar o comportamento do forno. Em seguida, são simulados controladores PID com diferentes parâmetros de sintonia, comparando suas respostas a uma referência de temperatura (*SetPoint*).

O critério principal de desempenho adotado para o Grupo 7 é o menor sobressinal.

## 2. Objetivos

- Analisar os dados experimentais de temperatura do forno.
- Estimar os parâmetros de um modelo FOPDT.
- Comparar os métodos de identificação de Smith e Sundaresan.
- Simular o modelo identificado em malha aberta.
- Implementar e comparar controladores PID sintonizados pelos métodos CHR sem sobressinal e Cohen–Coon.
- Avaliar o sobressinal, o tempo de subida, o tempo de assentamento e o erro final.
- Desenvolver uma interface gráfica para configurar o SetPoint e os parâmetros do controlador.

## 3. Métodos utilizados

### 3.1. Identificação do modelo

O comportamento térmico é aproximado por um modelo FOPDT, caracterizado por:

- **Ganho do processo (\(k\)):** relaciona a variação da entrada com a variação da saída em regime permanente.
- **Constante de tempo (\(\tau\)):** caracteriza a velocidade de resposta do processo.
- **Atraso (\(\theta\)):** representa o intervalo de tempo antes de a resposta modelada começar.

Foram comparados os métodos de identificação de Smith e Sundaresan utilizando a resposta experimental do forno. O método de Smith foi selecionado preliminarmente para as simulações seguintes por apresentar o menor RMSE entre os dois métodos avaliados.

### 3.2. Sintonia dos controladores PID

Foram implementadas duas regras de sintonia:

- **CHR sem sobressinal:** utilizada para favorecer uma resposta com menor sobressinal.
- **Cohen–Coon:** utilizada para comparação de desempenho.

Os controladores são comparados sob a mesma referência de temperatura e utilizando o mesmo modelo de processo.

## 4. Dados experimentais

O conjunto de dados está armazenado em `data/Forno_G7.mat` e contém as variáveis `t`, `Degrau` e `Saida`.

Características observadas:

- Número de amostras: 6.000.
- Intervalo de amostragem: 0,1 s.
- Intervalo temporal: 0 a 599,9 s.
- Temperatura média inicial: aproximadamente 21,22 °C.
- Temperatura média nos últimos 10 s: aproximadamente 86,66 °C.
- Entrada registrada: constante em 50 durante todo o arquivo.

**Limitação:** a entrada registrada não apresenta uma transição observável, e a temperatura continua aumentando no final do ensaio. Portanto, a interpretação física da entrada e a estimativa do regime permanente precisam ser confirmadas. Os parâmetros identificados são tratados como estimativas preliminares.

## 5. Resultados preliminares

### 5.1. Identificação do processo

| Parâmetro | Smith | Sundaresan |
|---|---:|---:|
| Ganho \(k\) | 1,30883 | 1,30883 |
| Constante de tempo \(\tau\) | 158,40 s | 148,74 s |
| Atraso \(\theta\) | 16,00 s | 22,48 s |
| RMSE | 0,9136 °C | 0,9680 °C |

O método de Smith apresentou o menor RMSE entre os métodos comparados, sendo escolhido preliminarmente para as simulações seguintes.

### 5.2. Simulação PID

A comparação inicial foi realizada com SetPoint de 40 °C e limites de comando do atuador entre 0% e 100%, assumindo provisoriamente que a entrada do modelo pode ser interpretada como potência em pontos percentuais.

| Métrica | CHR sem sobressinal | Cohen–Coon |
|---|---:|---:|
| Ganho proporcional \(K_p\) | 4,5384 | 10,2764 |
| Tempo integral \(T_i\) | 158,40 s | 37,782 s |
| Tempo derivativo \(T_d\) | 8,00 s | 5,7133 s |
| Sobressinal | 3,13% | 20,56% |
| Tempo de subida | 36,90 s | 19,60 s |
| Tempo de assentamento | 220,60 s | 109,20 s |
| Erro final | −0,03 °C | 0,00 °C |

Nesta simulação, o controlador Cohen–Coon apresentou resposta mais rápida, mas com maior sobressinal. O controlador CHR apresentou menor sobressinal, embora não tenha eliminado completamente a ultrapassagem do SetPoint.

Os resultados são preliminares e dependem da validade do modelo e da hipótese utilizada para relacionar a entrada experimental à potência do atuador. As métricas representam resultados de simulação, não de validação experimental em malha fechada.

## 6. Estrutura do projeto

```text
projeto-forno-g7/
├── data/
│   └── Forno_G7.mat
├── scripts/
│   ├── inspecionar_dados.py
│   ├── visualizar_dados.py
│   ├── validar_modelo.py
│   ├── ajustar_modelo.py
│   ├── comparar_identificacao.py
│   ├── simular_malha_aberta.py
│   ├── simular_pid.py
│   └── testar_controladores.py
├── src/
│   ├── __init__.py
│   ├── dados.py
│   ├── identificacao.py
│   ├── modelo_forno.py
│   ├── controladores.py
│   ├── metricas.py
│   └── simulacao_pid.py
├── app.py
├── requirements.txt
└── README.md
```

## 7. Instalação e execução

### 7.1. Clonar o repositório

Certifique-se de que o Git e o Python estejam instalados no computador.

Abra o terminal e execute o comando abaixo:

```bash
git clone https://github.com/MazinhaB/C13-Exercicios.git
```

Entre na pasta do projeto:

```bash
cd projeto-forno-g7
```

### 7.2. Instalar as dependências

É necessário ter Python instalado e as dependências listadas em `requirements.txt`.

Na raiz do projeto, execute:

```bash
python -m pip install -r requirements.txt
```

### 7.3. Inspecionar os dados

```bash
python -m scripts.inspecionar_dados
```

### 7.4. Comparar os métodos de identificação

```bash
python -m scripts.comparar_identificacao
```

### 7.5. Simular a resposta em malha aberta

```bash
python -m scripts.simular_malha_aberta
```

### 7.6. Simular os controladores PID

```bash
python -m scripts.simular_pid
```

### 7.7. Executar a interface gráfica

Para iniciar a interface de controle PID, execute:

```bash
python -m streamlit run app.py
```

A interface permite configurar o SetPoint, selecionar o método de sintonia ou ajustar manualmente os parâmetros PID e visualizar as respostas simuladas de temperatura e potência.
