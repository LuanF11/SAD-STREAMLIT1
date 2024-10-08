import pandas as pd
import streamlit as st
import altair as alt

csv_file = 'vendas.csv'
data = pd.read_csv(csv_file, delimiter=';')

# Converte a coluna 'Date' para o formato de data
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')

# Converte a coluna 'Total' para numérico
data['Total'] = pd.to_numeric(data['Total'].str.replace(',', '.'), errors='coerce')

# Substitui vírgulas por pontos na coluna 'Rating' e converte para numérico
data['Rating'] = pd.to_numeric(data['Rating'].str.replace(',', '.'), errors='coerce')

# Adiciona colunas de ano e mês
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Agrupa os dados por dia, cidade e tipo de produto e calcula o faturamento total
faturamento_produto_cidade = data.groupby(['Date', 'City', 'Product line'])['Total'].sum().reset_index()

# Agrupa os dados por dia e cidade e calcula o faturamento total
faturamento_diario_cidade = data.groupby(['Date', 'City'])['Total'].sum().reset_index()

# Agrupa os dados por cidade e calcula o faturamento total
faturamento_total_cidade = data.groupby('City')['Total'].sum().reset_index()

# Agrupa os dados por tipo de pagamento e calcula o faturamento total
faturamento_pagamento = data.groupby('Payment')['Total'].sum().reset_index()

# Calcula a porcentagem de cada tipo de pagamento
faturamento_pagamento['Percentage'] = (faturamento_pagamento['Total'] / faturamento_pagamento['Total'].sum()) * 100

# Calcula a avaliação média por cidade
avaliacao_media_cidade = data.groupby('City')['Rating'].mean().reset_index()

# Título da aplicação
st.title('Análise de Vendas')

# Adiciona a barra lateral para filtro por mês e ano
st.sidebar.title('Filtros')
anos = data['Year'].unique()
ano_selecionado = st.sidebar.selectbox('Selecione o ano', anos)
meses = range(1, 13)
mes_selecionado = st.sidebar.selectbox('Selecione o mês', meses)

# Filtra os dados com base no mês e ano selecionados
filtered_data_produto_cidade = faturamento_produto_cidade[(faturamento_produto_cidade['Date'].dt.year == ano_selecionado) & 
                                                          (faturamento_produto_cidade['Date'].dt.month == mes_selecionado)]

filtered_data_diario_cidade = faturamento_diario_cidade[(faturamento_diario_cidade['Date'].dt.year == ano_selecionado) & 
                                                        (faturamento_diario_cidade['Date'].dt.month == mes_selecionado)]

# Criação do gráfico de barras horizontais com cores diferentes para cada cidade e tipo de produto
chart_produto_cidade = alt.Chart(filtered_data_produto_cidade).mark_bar().encode(
    y='Product line:N',
    x='Total:Q',
    color='City:N',
    tooltip=['Date:T', 'City:N', 'Product line:N', 'Total:Q']
).properties(
    width=800,
    height=400,
    title='Faturamento por Tipo de Produto e Cidade'
).interactive()

st.altair_chart(chart_produto_cidade)

# Criação do gráfico de barras verticais com cores diferentes para cada cidade
chart_diario_cidade = alt.Chart(filtered_data_diario_cidade).mark_bar().encode(
    x='Date:T',
    y='Total:Q',
    color='City:N',
    tooltip=['Date:T', 'City:N', 'Total:Q']
).properties(
    width=800,
    height=400,
    title='Faturamento Diário por Cidade'
).interactive()

st.altair_chart(chart_diario_cidade)

# Criação do gráfico de barras verticais para o faturamento total por cidade
chart_total_cidade = alt.Chart(faturamento_total_cidade).mark_bar().encode(
    x='City:N',
    y='Total:Q',
    color='City:N',
    tooltip=['City:N', 'Total:Q']
).properties(
    width=800,
    height=400,
    title='Faturamento Total por Cidade'
).interactive()

st.altair_chart(chart_total_cidade)

# Criação do gráfico de pizza para o faturamento por tipo de pagamento
chart_pagamento = alt.Chart(faturamento_pagamento).mark_arc().encode(
    theta=alt.Theta(field='Total', type='quantitative'),
    color=alt.Color(field='Payment', type='nominal'),
    tooltip=['Payment:N', 'Total:Q', alt.Tooltip('Percentage:Q', format='.2f', title='Percentage')]
).properties(
    width=800,
    height=400,
    title='Faturamento por Tipo de Pagamento'
).interactive()

# Adiciona rótulos de porcentagem dentro das fatias do gráfico de pizza
text = chart_pagamento.mark_text(radius=120, size=14).encode(
    text=alt.Text('Percentage:Q', format='.1f')
)

st.altair_chart(chart_pagamento + text)

# Criação do gráfico de barras verticais para a avaliação média por cidade
chart_avaliacao_cidade = alt.Chart(avaliacao_media_cidade).mark_bar().encode(
    x='City:N',
    y='Rating:Q',
    color='City:N',
    tooltip=['City:N', 'Rating:Q']
).properties(
    width=800,
    height=400,
    title='Avaliação Média por Cidade'
).interactive()

st.altair_chart(chart_avaliacao_cidade)