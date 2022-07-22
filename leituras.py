import csv
import pandas as pd
import datetime


# Conexão com base de dados, em modo leitura
file = open("database/COVID19 cases Toronto.csv", "r")
# Leitor em forma de Dicionário
reader = csv.DictReader(file)
# Transformar dicionário em DataFrame
df = pd.DataFrame(reader)

"""
df.columns:
Index(['_id', 'Outbreak Associated', 'Age Group', 'Neighbourhood Name', 'FSA',
       'Source of Infection', 'Classification', 'Episode Date',
       'Reported Date', 'Client Gender', 'Outcome', 'Currently Hospitalized',
       'Currently in ICU', 'Currently Intubated', 'Ever Hospitalized',
       'Ever in ICU', 'Ever Intubated'],
      dtype='object')

Número de registros: 14911
"""
total = len(df)

# Total de casos confirmados
confirmados = len(df[df['Classification'] == 'CONFIRMED'])

# Transformar datas(str) em datetime
df['Reported Date'] = pd.to_datetime(df['Reported Date'], format='%Y-%m-%d')
# Data inicial dos registros
inicio = (df['Reported Date'].min()).strftime("%d/%m/%Y")
# Data atual(final) dos registros
atual = (df['Reported Date'].max()).strftime("%d/%m/%Y")

sete_dias = datetime.timedelta(7)
catorze_dias = datetime.timedelta(14)

df_semana_atual = df[(df['Reported Date'] >= (df['Reported Date'].max() - sete_dias)) &
                     (df['Classification'] == 'CONFIRMED')].sort_values(by=['Reported Date'])

df_semana_anterior = df[(df['Reported Date'] < (df['Reported Date'].max() - sete_dias)) &
                        (df['Reported Date'] > (df['Reported Date'].max() - catorze_dias)) &
                        (df['Classification'] == 'CONFIRMED')].sort_values(by=['Reported Date'])


ncasos_semana_atual = len(df_semana_atual)
ncasos_semana_anterior = len(df_semana_anterior)

# Registros de pessoas hospitalizadas na semana atual
hospitalizados_atual = df_semana_atual[(df_semana_atual['Currently Hospitalized'] == 'Yes') &
                                 (df_semana_atual['Classification'] == 'CONFIRMED')]
total_hospitalizados_atual = len(hospitalizados_atual)

# Registros de pessoas entubadas na semana atual
entubados_atual = hospitalizados_atual[hospitalizados_atual['Currently Intubated'] == 'Yes']\
    .sort_values(by=['Age Group'])
total_entubados_atual = len(entubados_atual)


# Registros de pessoas hospitalizadas na semana anterior
hospitalizados_anterior = df_semana_anterior[(df_semana_anterior['Currently Hospitalized'] == 'Yes') &
                                 (df_semana_anterior['Classification'] == 'CONFIRMED')]
total_hospitalizados_anterior = len(hospitalizados_anterior)

# Registros de pessoas entubadas na semana anterior
entubados_anterior = hospitalizados_anterior[hospitalizados_anterior['Currently Intubated'] == 'Yes']\
    .sort_values(by=['Age Group'])
total_entubados_anterior = len(entubados_anterior)

# Óbitos totais
obitos = df[df['Outcome'] == 'FATAL'].sort_values(by=['Reported Date'])

# Óbitos na semana atual
obitos_semana_atual = df_semana_atual[df_semana_atual['Outcome'] == 'FATAL']
nobitos_atual = len(obitos_semana_atual)

# Óbitos na semana anterior
obitos_semana_anterior = df_semana_anterior[df_semana_anterior['Outcome'] == 'FATAL']
nobitos_anterior = len(obitos_semana_anterior)

# Óbitos por faixa etária
obitos_fe = {}
for data in obitos['Age Group']:
    if data in obitos_fe.keys():
        obitos_fe[data] += 1
    else:
        obitos_fe[data] = 1
# Ordenado por idade
obitos_fe = {k: v for k, v in sorted(obitos_fe.items(), key=lambda item: item[0], reverse=True)}
# Ordenado pelo maior numero
obitos_fe2 = {k: v for k, v in sorted(obitos_fe.items(), key=lambda item: item[1], reverse=True)}


# Dicionario com número de casos por mês
casos_por_mes = {'Janeiro': 0, 'Fevereiro': 0, 'Março': 0, 'Abril': 0, 'Maio': 0, 'Junho': 0, 'Julho': 0}
for data in df['Reported Date']:
    if data.strftime('%m') == '01':
        casos_por_mes['Janeiro'] += 1
    elif data.strftime('%m') == '02':
        casos_por_mes['Fevereiro'] += 1
    elif data.strftime('%m') == '03':
        casos_por_mes['Março'] += 1
    elif data.strftime('%m') == '04':
        casos_por_mes['Abril'] += 1
    elif data.strftime('%m') == '05':
        casos_por_mes['Maio'] += 1
    elif data.strftime('%m') == '06':
        casos_por_mes['Junho'] += 1
    elif data.strftime('%m') == '07':
        casos_por_mes['Julho'] += 1


bairros_qts = {}
for bairro in df['Neighbourhood Name'][(df['Classification'] == 'CONFIRMED')
                                       & (df['Neighbourhood Name'] != '')]:
    if bairro in bairros_qts.keys():
        bairros_qts[bairro] += 1
    else:
        bairros_qts[bairro] = 1
bairros_qts = {k: v for k, v in sorted(bairros_qts.items(), key=lambda item: item[1], reverse=True)}

# 10 bairros com maior índice de contaminação
dez_bairros = {}
for chave, valor in bairros_qts.items():
    if len(dez_bairros.keys()) <= 11:
        dez_bairros[chave] = valor



# Para gráfico 1: Casos, Mortes, Hospitalizados, Entubados
casos = [ncasos_semana_anterior, ncasos_semana_atual]
mortes = [nobitos_anterior, nobitos_atual]
hospitalizados = [total_hospitalizados_anterior, total_hospitalizados_atual]
entubados = [total_entubados_anterior, total_entubados_atual]
