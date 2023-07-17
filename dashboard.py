# É necessário a instalação:
# !pip install dash
# !pip install plotly
# !pip install pandas

# Importar as bibliotecas necessárias
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Importando os dados
dados = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Criando uma lista com os anos únicos presentes no Dataset (Para o Dropdown)
opcoes_anos = list(dados['year'].sort_values(ascending=True).unique())

# Inicializando o aplicativo Dash
app = Dash(__name__)

# Declarando Variaveis (Axes)
fig = px.bar(dados, x='continent', y='pop', color='country')
fig1 = px.pie(dados, names='continent', values='pop')
fig2 = px.line(dados, x='year', y='pop')

# Dict colors para que possa ser mais fácil alterar a cor de fundo e de texto
colors = {
    'background': '#111111',
    'text': '#FFFFFF'
}


# Criando um layout, com background preto
app.layout = html.Div(style={'background': colors['background']}, children=[

    # Gera o título e imagem primeiro gráfico (px.line)
    html.H1(children='População de um país ao longo dos anos', style={'textAlign': 'center', 'color': colors['text']}),
    html.P('Seleione o país: ', style={'color': colors['text']}),
    dcc.Dropdown(dados.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-country'),

    # Gera o segundo gráfico (px.bar)
    html.H1(children='População dos continentes separada por ano', style={'textAlign': 'center',
                                                                          'color': colors['text']}),
    html.P('Seleione o ano: ', style={'color': colors['text']}),
    dcc.Dropdown(opcoes_anos, value=1952, id='lista_anos'),
    dcc.Graph(id='graph-populacao-ano', figure=fig),


    # Gera o terceiro gráfico (px.pie)
    html.H1(children='Porcentagem dos continentes na população', style={'textAlign': 'center',
                                                                        'color': colors['text']}),
    html.P('Seleione o ano: ', style={'color': colors['text']}),
    dcc.Dropdown(opcoes_anos, value=1952, id='lista_anos_pie'),
    dcc.Graph(id='graph_pie', figure=fig1)
])

# Callbacks para funcionar os dropdowns e ser possível interajir com os gráficos


@callback(
    Output('graph-country', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = dados[dados.country == value]
    fig2 = px.line(dff, x='year', y='pop')
    fig2.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig2


@callback(
    Output('graph-populacao-ano', 'figure'),
    Input('lista_anos', 'value')
)
def update_graph(value):
    tabela_filtrada = dados.loc[dados['year'] == value]
    fig = px.histogram(tabela_filtrada, x='continent', y='pop', color='country')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig


@callback(
    Output('graph_pie', 'figure'),
    Input('lista_anos_pie', 'value')
)
def update_graph(value):
    tabela_filtrada_pie = dados.loc[dados['year'] == value]
    fig1 = px.pie(tabela_filtrada_pie, names='continent', values='pop')
    fig1.update_layout(
        plot_bgcolor=colors['text'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig1

# Inicializa o Dash board


if __name__ == '__main__':
    app.run(debug=True)
