import streamlit as st
import pandas as pd


@st.cache_data
def carregar_dados():
    df = pd.read_csv(".\vendas.csv", parse_dates=["data"])
    return df


st.title("Dashboard de Vendas")

df = carregar_dados()

st.sidebar.title("Filtros")
lista_categorias = df["categoria"].unique().tolist()
categorias_sel = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_categorias,
    default=lista_categorias,
)

df_filtrado = df[df["categoria"].isin(categorias_sel)]

col1, col2 = st.columns([1, 1])

with col1:
    receita_total = df_filtrado["receita"].sum()
    st.metric(label="Receita Total", value=f"R$ {receita_total:,.2f}")

with col2:
    total_pedidos = len(df_filtrado)
    st.metric(label="Total de Pedidos", value=f"{total_pedidos:,}")

aba1, aba2 = st.tabs(["Evolução Mensal", "Tabela de Dados"])

with aba1:
    receita_mensal = (
        df_filtrado.set_index("data")["receita"]
        .resample("ME")
        .sum()
        .rename("receita")
    )
    st.area_chart(receita_mensal)

with aba2:
    st.dataframe(df_filtrado, use_container_width=True)

    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar recorte em CSV",
        data=csv_bytes,
        file_name="recorte_vendas.csv",
        mime="text/csv",
    )
