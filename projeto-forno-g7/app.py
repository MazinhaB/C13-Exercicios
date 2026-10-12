
import matplotlib.pyplot as plt
import streamlit as st

from src.dados import carregar_dados
from src.identificacao import smith
from src.controladores import sintonia_chr, sintonia_cohen_coon
from src.simulacao_pid import simular_pid
from src.metricas import calcular_metricas


st.set_page_config(page_title="Controle PID do Forno", page_icon="🌡️", layout="wide",)

st.title("Sistema de Controle PID do Forno")
st.caption("Grupo 7 | Identificação e controle de temperatura")

st.markdown("""Esta aplicação permite configurar e simular controladores PID para o modelo FOPDT identificado a partir dos dados experimentais.""")

# -------------------------------------------------- #
#       Carregar dados e identificar o modelo        #
# -------------------------------------------------- #

try:
    t_exp, _, saida_exp = carregar_dados()
    delta_u = 50.0

    modelo = smith(t_exp, saida_exp, delta_u)

    k = modelo["k"]
    tau = modelo["tau"]
    theta = modelo["theta"]
    y0 = float(saida_exp[t_exp < 10].mean())

except Exception as erro:
    st.error(f"Não foi possível carregar ou identificar o modelo: {erro}")
    st.stop()


# -------------------------------------------------- #
#       Mostrar os parâmetros identificados          #
# -------------------------------------------------- #

st.subheader("Modelo do forno")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Ganho (k)", f"{k:.5f}")
col2.metric("Constante de tempo (τ)", f"{tau:.2f} s")
col3.metric("Atraso (θ)", f"{theta:.2f} s")
col4.metric("Temperatura inicial", f"{y0:.2f} °C")

st.divider()


# -------------------------------------------------- #
#               Configurar a simulação               #
# -------------------------------------------------- #

st.subheader("Configuração do controlador")

modo_sintonia = st.radio("Modo de sintonia", ["Método clássico", "Manual"], horizontal=True,)

if modo_sintonia == "Método clássico":
    metodo = st.selectbox("Método de sintonia", ["CHR sem sobressinal", "Cohen-Coon"])

    if metodo == "CHR sem sobressinal":
        kp_inicial, ti_inicial, td_inicial = sintonia_chr(k, tau, theta)
    else:
        kp_inicial, ti_inicial, td_inicial = sintonia_cohen_coon(k, tau, theta)

    st.info("Os parâmetros PID são calculados pelo método selecionado e não podem ser editados no modo clássico")
else:
    metodo = "Sintonia manual"

    st.caption("Defina manualmente os parâmetros do controlador PID")

    kp_inicial = 4.5384
    ti_inicial = 158.4000
    td_inicial = 8.0000

with st.form("formulario_pid"):
    col1, col2 = st.columns(2)

    with col1:
        setpoint = st.number_input("SetPoint (°C)", min_value=0.0, max_value=100.0, value=40.0, step=1.0,)
        tempo_total = st.number_input("Tempo de simulação (s)", min_value=60, max_value=3600, value=600, step=60,)

    with col2:
        kp = st.number_input("Kp — Ganho proporcional", min_value=0.001, max_value=1000.0, value=float(kp_inicial), format="%.4f",disabled=(modo_sintonia=="Método clássico"),)
        ti = st.number_input("Ti — Tempo integral (s)", min_value=0.001, max_value=10000.0, value=float(ti_inicial), format="%.4f",disabled=(modo_sintonia=="Método clássico"),)
        td = st.number_input("Td — Tempo derivativo (s)", min_value=0.0, max_value=1000.0, value=float(td_inicial), format="%.4f",disabled=(modo_sintonia=="Método clássico"),)

    executar = st.form_submit_button("Executar simulação", type="primary",)


# -------------------------------------------------- #
#               Executar a simulação                 #
# -------------------------------------------------- #

if executar:
    try:
        t, temperatura, comando = simular_pid(k=k, tau=tau, theta=theta, y0=y0, setpoint=setpoint, kp=kp,
            ti=ti, td=td, tempo_total=float(tempo_total), dt=0.1, u_min=0.0, u_max=100.0,)

        metricas = calcular_metricas(t, temperatura, referencia=setpoint,)
        if abs(setpoint - y0) < 1e-9:
            st.warning("O SetPoint é igual à temperatura inicial. As métricas de resposta não são aplicáveis.")
            st.stop()
    except Exception as erro:
        st.error(f"Não foi possível executar a simulação: {erro}")
        st.stop()

    st.divider()
    st.subheader("Resultados da simulação")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Sobressinal", f"{metricas['overshoot_percentual']:.2f}%",)
    col2.metric("Tempo de subida", f"{metricas['tempo_subida']:.2f} s",)

    tempo_assentamento = metricas["tempo_acomodacao"]

    col3.metric("Tempo de assentamento", (f"{tempo_assentamento:.2f} s" if tempo_assentamento == tempo_assentamento else "Não atingido"),)
    col4.metric("Erro estacionário", f"{metricas['erro_estacionario']:.2f} °C",)

    
    # Gráficos lado a lado
    col_temp, col_cmd = st.columns(2)

    with col_temp:
        fig_temp, ax_temp = plt.subplots(figsize=(6, 4))

        ax_temp.plot(t, temperatura, label="Temperatura simulada", linewidth=1.8,)
        ax_temp.axhline(setpoint, linestyle="--", label=f"SetPoint = {setpoint:.1f} °C",)
        ax_temp.set_xlabel("Tempo (s)")
        ax_temp.set_ylabel("Temperatura (°C)")
        ax_temp.set_title("Resposta do forno")
        ax_temp.grid(True, alpha=0.3)
        ax_temp.legend(fontsize=8)
        fig_temp.tight_layout()

        st.pyplot(fig_temp, use_container_width=True)

        # Salvar o gráfico em alta resolução
        fig_temp.savefig("grafico_temperatura.png", dpi=300, bbox_inches="tight",)

        with open("grafico_temperatura.png", "rb") as arquivo:
            st.download_button("Baixar temperatura", data=arquivo.read(), file_name="grafico_temperatura.png",
                mime="image/png", key="download_temperatura",)

        plt.close(fig_temp)

    with col_cmd:
        fig_cmd, ax_cmd = plt.subplots(figsize=(6, 4))

        ax_cmd.plot(t, comando, label="Potência comandada", linewidth=1.5,)
        ax_cmd.set_xlabel("Tempo (s)")
        ax_cmd.set_ylabel("Potência (%)")
        ax_cmd.set_ylim(-5, 105)
        ax_cmd.set_title("Comando do atuador")
        ax_cmd.grid(True, alpha=0.3)
        ax_cmd.legend(fontsize=8)
        fig_cmd.tight_layout()

        st.pyplot(fig_cmd, use_container_width=True)

        # Salvar o gráfico em alta resolução
        fig_cmd.savefig("grafico_potencia.png", dpi=300, bbox_inches="tight",)

        with open("grafico_potencia.png", "rb") as arquivo:
            st.download_button("Baixar potência", data=arquivo.read(), file_name="grafico_potencia.png",
                mime="image/png", key="download_potencia",)

        plt.close(fig_cmd)

    st.caption(f"Potência mínima: {comando.min():.2f}% | " f"Potência máxima: {comando.max():.2f}%")

else:
    st.info("Configure o SetPoint e os parâmetros PID e clique em 'Executar simulação' para visualizar os resultados.")
