# Sistema de Controle PID de um Forno — Grupo 7

## 1. Descrição do projeto

Este projeto tem como objetivo identificar e modelar o comportamento térmico de um forno a partir de dados experimentais, permitindo analisar sua dinâmica e simular estratégias de controle em malha fechada.

Para isso, são utilizados modelos matemáticos de primeira ordem com atraso de transporte (FOPDT — *First Order Plus Dead Time*), métodos de identificação de parâmetros e simulações de controladores PID.

O principal critério de avaliação do projeto é a **minimização do sobressinal (*overshoot*)**, buscando uma resposta de temperatura estável e adequada ao valor de referência (*setpoint*).

## 2. Objetivos

Os principais objetivos são:

- Analisar os dados experimentais de temperatura do forno.
- Identificar os parâmetros de um modelo FOPDT.
- Comparar os métodos de identificação de Smith e Sundaresan.
- Ajustar um modelo aos dados experimentais por meio de mínimos quadrados.
- Simular a resposta do sistema em malha aberta.
- Implementar e comparar controladores PID utilizando os métodos CHR e Cohen–Coon.
- Avaliar o desempenho dos controladores por meio de métricas de resposta temporal.
- Disponibilizar uma interface interativa para visualização e simulação dos resultados utilizando Streamlit.

## 3. Fundamentação teórica e métodos utilizados

### 3.1. Modelo FOPDT

O comportamento térmico do forno é aproximado por um modelo de primeira ordem com atraso de transporte, representado pela função de transferência:

$$
G(s)=\frac{K e^{-\theta s}}{\tau s+1}
$$

Em que:

- **K:** ganho estático do processo.
- **τ:** constante de tempo do sistema.
- **θ:** tempo morto ou atraso de transporte.
- **s:** variável complexa da transformada de Laplace.

Esse modelo permite representar, de forma simplificada, a relação entre a entrada de controle e a resposta de temperatura do forno.

### 3.2. Identificação dos parâmetros

Foram considerados três métodos para estimar os parâmetros do modelo:

- **Smith:** estima os parâmetros a partir de pontos característicos da resposta ao degrau.
- **Sundaresan:** utiliza dois pontos específicos da curva de resposta, correspondentes a aproximadamente 35,3% e 85,3% da variação total.
- **Mínimos quadrados:** ajusta os parâmetros do modelo para minimizar o erro entre a resposta experimental e a resposta calculada.

Os métodos de Smith e Sundaresan–Krishnaswamy foram comparados por meio do erro quadrático médio (EQM) e da raiz do erro quadrático médio (RMSE).

Para as simulações PID apresentadas neste README, o método de Smith foi selecionado por apresentar um RMSE ligeiramente inferior ao de Sundaresan–Krishnaswamy nos dados analisados. Essa escolha é específica ao conjunto de dados utilizado e não implica superioridade universal do método.

### 3.3. Estratégias de controle PID

Foram implementadas duas estratégias para determinar os parâmetros do controlador PID:

- **CHR:** método de Chien–Hrones–Reswick, utilizando o critério de resposta sem sobressinal como referência de projeto.
- **Cohen–Coon:** método de sintonia baseado nos parâmetros de um modelo identificado do processo.

A comparação considera o sobressinal, o tempo de subida, o tempo de acomodação e o erro em regime permanente.

## 4. Dados experimentais

O conjunto de dados utilizado está armazenado em:

`data/Forno_G7.mat`

O arquivo contém as seguintes variáveis:

| Variável | Descrição |
|---|---|
| `t` | Vetor de tempo das medições |
| `Degrau` | Sinal de entrada registrado |
| `Saida` | Temperatura medida na saída do sistema |

### 4.1. Características do conjunto de dados

| Característica | Valor |
|---|---:|
| Número de amostras | 6.000 |
| Intervalo de amostragem | 0,1 s |
| Tempo inicial | 0 s |
| Tempo final | 599,9 s |
| Temperatura média inicial aproximada | 21,22 °C |
| Temperatura média dos últimos 10 segundos | 86,66 °C |
| Valor registrado da entrada | 50 |

### 4.2. Limitações dos dados

O sinal `Degrau` apresenta valor constante igual a 50 durante todo o intervalo registrado. Portanto, não é possível observar diretamente uma transição de entrada no conjunto de dados disponível.

Além disso, a temperatura ainda apresenta tendência de crescimento no final do intervalo analisado. Isso limita a confirmação do valor de regime permanente e afeta a interpretação física dos parâmetros identificados.

## 5. Resultados

### 5.1. Comparação dos métodos de identificação

Os métodos de Smith e Sundaresan apresentaram os seguintes resultados:

| Parâmetro ou métrica | Smith | Sundaresan |
|---|---:|---:|
| Ganho \(K\) | 1,30883 | 1,30883 |
| Constante de tempo (τ) (s) | 158,40 | 148,74 |
| Tempo morto (θ) (s) | 16,00 | 22,48 |
| RMSE (°C) | 0,9136 | 0,9680 |
| EQM (°C²) | 0,8348 | 0,9369 |

O método de Smith apresentou os menores valores de RMSE e EQM entre os dois métodos avaliados. Por essa razão, foi escolhido como referência para as simulações PID apresentadas a seguir.

O ajuste por mínimos quadrados também foi realizado, com os seguintes resultados:

| Parâmetro ou métrica | Mínimos quadrados |
|---|---:|
| Ganho \(K\) | 1,35733 |
| Constante de tempo (τ) (s) | 173,3246 |
| Tempo morto (θ) (s) | 14,2198 |
| RMSE (°C) | 0,2680 |
| EQM (°C²) | 0,0718 |
| Convergência do ajuste | Sim |

O ajuste por mínimos quadrados apresentou menor erro em relação aos dados experimentais.

### 5.2. Comparação dos controladores PID

As simulações foram realizadas considerando um *setpoint* de 40 °C.

| Métrica | CHR — sem sobressinal | Cohen–Coon |
|---|---:|---:|
| Kp | 4,5384 | 10,2764 |
| Ti (s) | 158,4 | 37,782 |
| Td (s) | 8,0 | 5,7133 |
| Sobressinal | 3,13% | 20,56% |
| Tempo de subida | 36,9 s | 19,6 s |
| Tempo de acomodação | 220,6 s | 109,2 s |
| Erro final aproximado | −0,03 °C | 0 °C |

### 5.3. Análise dos resultados

O controlador Cohen–Coon apresentou resposta mais rápida, com menor tempo de subida e menor tempo de acomodação. Entretanto, também apresentou sobressinal significativamente maior.

O controlador CHR apresentou sobressinal de 3,13%, consideravelmente inferior aos 20,56% obtidos com Cohen–Coon. Embora a resposta simulada não tenha sido completamente livre de sobressinal, o resultado está mais alinhado ao principal critério do projeto: minimizar a ultrapassagem da temperatura de referência.

Dessa forma, **o CHR é a estratégia mais alinhada ao critério de projeto nos resultados simulados**, enquanto Cohen–Coon oferece uma resposta mais rápida, porém com maior oscilação acima do *setpoint*.

### 5.4. Gráficos

Os gráficos gerados durante a análise estão organizados no diretório `images/`:

- `grafico_potencia.png`
- `grafico_temperatura.png`
- `grafico_comparacao_modelos.png`

O gráfico de comparação dos modelos permite analisar visualmente a resposta experimental e as respostas calculadas a partir dos modelos identificados.

As imagens devem ser mantidas atualizadas sempre que os resultados ou os parâmetros do projeto forem alterados.

## 6. Estrutura do projeto

A organização dos arquivos é apresentada a seguir:

```text
C13-Exercicios/
└── projeto-forno-g7/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── data/
    │   └── Forno_G7.mat
    ├── images/
    │   ├── grafico_potencia.png
    │   ├── grafico_temperatura.png
    │   └── grafico_comparacao_modelos.png
    ├── scripts/
    │   ├── visualizar_dados.py
    │   ├── ajustar_modelo.py
    │   ├── inspecionar_dados.py
    │   ├── comparar_identificacao.py
    │   ├── simular_malha_aberta.py
    │   └── simular_pid.py
    └── src/
        ├── dados.py
        ├── identificacao.py
        ├── modelo_forno.py
        └── simulacao_pid.py
```

O diretório `data/` armazena o conjunto de dados experimentais. O diretório `src/` reúne os módulos responsáveis pelo carregamento dos dados, pela identificação do processo, pela representação matemática do forno e pela simulação do controlador PID.

O diretório `scripts/` contém os scripts de análise e execução, enquanto `images/` armazena os gráficos gerados durante o desenvolvimento. O arquivo `app.py` disponibiliza a interface interativa.

## 7. Instalação e execução

### 7.1. Pré-requisitos

- Python instalado.
- Git instalado.
- Acesso ao repositório do projeto.
- Dependências Python listadas em `requirements.txt`.

### 7.2. Clonar o repositório

No terminal, execute:

```bash
git clone https://github.com/MazinhaB/C13-Exercicios.git
cd C13-Exercicios/projeto-forno-g7
```

### 7.3. Criar um ambiente virtual

No Windows, utilizando PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Caso o ambiente virtual já esteja ativo, não é necessário criá-lo novamente.

### 7.4. Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

### 7.5. Executar as análises

Os scripts de análise podem ser executados a partir do diretório `projeto-forno-g7`, utilizando os comandos correspondentes:

```bash
python -m scripts.visualizar_dados
python -m scripts.ajustar_modelo
python -m scripts.inspecionar_dados
python -m scripts.comparar_identificacao
python -m scripts.simular_malha_aberta
python -m scripts.simular_pid
```

A execução de cada comando depende da existência do respectivo arquivo e de suas dependências estarem instaladas corretamente.

### 7.6. Executar a interface interativa

Para iniciar a interface desenvolvida com Streamlit, execute:

```bash
python -m streamlit run app.py
```

O Streamlit disponibilizará o endereço local para abrir a aplicação no navegador.

## 8. Considerações finais

O projeto desenvolve uma metodologia para identificação e simulação do comportamento térmico de um forno, integrando modelagem FOPDT, comparação de métodos de identificação e avaliação de estratégias de controle PID.

Nos resultados simulados disponíveis, o método de Smith apresentou desempenho ligeiramente melhor que Sundaresan segundo o RMSE, enquanto o ajuste por mínimos quadrados apresentou menor erro em relação aos dados experimentais. Na comparação dos controladores, CHR apresentou menor sobressinal, enquanto Cohen–Coon apresentou resposta mais rápida.
