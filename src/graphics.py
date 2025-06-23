#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../data/yeardata.csv')
#%%
# remove colunas desnecessárias no código
df.drop(columns=['start_hour','ended_date','ended_hour','week_start_day_num'], inplace=True)

df.head()
#%%
# Ajuste o formato das colunas de data e hora
df['start_date'] = pd.to_datetime(df['start_date'], format='%Y-%m-%d')
df['trip_length'] = pd.to_timedelta(df['trip_length'])

# Ajuste o formato das colunas de string e categóricas
df = df.astype({
    'ride_id': 'string',
    'rideable_type': 'string',
    'start_station_name': 'string',
    'end_station_name': 'string',
    'member_casual': 'category',
    'week_start_day': 'category',
    })

# Ajusta a coluna do dia da semana
df['week_start_day'] = df['start_date'].dt.strftime('%A')

# Ordena os dias de forma categórica
df['week_start_day'] = pd.Categorical(
    df['week_start_day'],
    categories=[
        'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'
    ],
    ordered=True
)

# Cria a coluna do mês de inicio da viagem com o nome do mês
df['month'] = df['start_date'].dt.strftime('%B')

# Ordena os meses de forma categórica
df['month'] = pd.Categorical(
    df['month'],
    categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ],
    ordered=True
)

# %%
# Gráfico - Media de tempo das viagens

# Agrupa os dados por tipo de usuário e calcula a média de duração das viagens
avg_tripduration = (df.groupby('member_casual')['trip_length'].mean())

# Converte a média de duração para minutos
avg_tripduration_minutes = (avg_tripduration.dt.total_seconds() / 60).round(2)

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
avg_tripduration_minutes.plot(kind='bar', color=['blue', 'grey'], zorder=3)

# Adiciona os rótulos de duração acima das barras
for i, value in enumerate(avg_tripduration_minutes):
    plt.text(
        x=i,
        y=value + 0.2,
        s=f'{value} min',
        ha='center',
        fontsize=11
    )

# Configurações do gráfico
plt.ylim(0, 25)    
plt.title('Média de Duração das Viagens por Tipo de Usuário')
plt.xlabel('Tipo de Usuário')
plt.ylabel('Duração Média da Viagem (minutos)')
plt.xticks(rotation=0)
plt.yticks(range(0, 25, 3))
plt.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
plt.show()

# %%
# Gráfico - Bicicletas mais comuns

# Agrupa os dados por tipo de usuário e tipo de bicicleta, contando o número de ocorrências
common_bikes = (df.groupby('member_casual')['rideable_type'].value_counts()).reset_index()

# Altera o tipo do retorno para formato longo
pivot_df = common_bikes.pivot(index='rideable_type', columns='member_casual', values='count')

# Normaliza os dados para proporção das colunas
pivot_prop = pivot_df.div(pivot_df.sum(axis=0), axis=1)

# Sequencia de tipos de bicicleta para o eixo x
x = np.arange(len(pivot_prop.index))
# Largura das barras
bar_width = 0.35

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))
# Plota as barras para cada tipo de usuário
plt.bar(x - bar_width/2, pivot_prop['member'], width=bar_width, label='Member', color='orange')
plt.bar(x + bar_width/2, pivot_prop['casual'], width=bar_width, label='Casual', color='skyblue')

#Configurações do gráfico
plt.xticks(x, pivot_prop.index)
plt.ylabel('Proporção de uso (%)')
plt.title('Proporção de Tipos de Bicicleta por Tipo de Usuário')
plt.legend()

# Adiciona os rótulos de porcentagem acima das barras
for i, (casual_val, member_val) in enumerate(zip(pivot_prop['casual'], pivot_prop['member'])):
    plt.text(i + bar_width/2, casual_val + 0.01, f'{casual_val*100:.1f}%', ha='center', fontsize=10)
    plt.text(i - bar_width/2, member_val + 0.01, f'{member_val*100:.1f}%', ha='center', fontsize=10)

# Configurações do gráfico
plt.ylim(0, 0.60)
plt.tight_layout()
plt.show()


# %%
# Gráfico - Dias das semanas mais comuns por tipo de usuário

# Agrupa os dados por tipo de usuário e dia da semana, contando o número de viagens
week_day_counts = (df.groupby('member_casual')['week_start_day'].value_counts()).reset_index(name='count')

# Altera o tipo do retorno para formato longo
pivot_df = week_day_counts.pivot(index='week_start_day', columns='member_casual', values='count')

# Normaliza os dados para proporção das colunas
pivot_prop = pivot_df.div(pivot_df.sum(axis=0), axis=1)

# Sequencia de dias da semana para o eixo x
x = np.arange(len(pivot_prop.index))

# Largura das barras
bar_width = 0.35

# Cria o gráfico de barras
plt.figure(figsize=(10, 6))

# Plota as barras para cada tipo de usuário
bar_member = plt.bar(x - bar_width/2, pivot_prop['member'], width=bar_width, label='Member', color='orange', zorder = 3)
bar_casual = plt.bar(x + bar_width/2, pivot_prop['casual'], width=bar_width, label='Casual', color='skyblue', zorder = 3)

#Configurações do gráfico
plt.xticks(x, pivot_prop.index)
plt.ylabel('Proporção de uso (%)')
plt.xlabel('Dias da Semana')
plt.title('Proporção de uso por dia da semana e tipo de usuário')
plt.legend()

# Adiciona os rótulos de porcentagem acima das barras
for bar in bar_member:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.005, f'{height*100:.1f}%', ha='center', fontsize=8)
for bar in bar_casual:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.005, f'{height*100:.1f}%', ha='center', fontsize=8)

# Configurações do gráfico
plt.ylim(0, 0.23)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
plt.show()

# %%
# Gráfico - Meses com mais viagens

#Agrupa os dados por tipo de usuário e mês, contando o número de viagens
month_counts = (df.groupby('member_casual')['month'].value_counts()).reset_index(name='count')

# Altera o tipo do retorno para formato longo
pivot_df = month_counts.pivot(index='month', columns='member_casual', values='count')
# Normaliza os dados para proporção das colunas
pivot_prop = pivot_df.div(pivot_df.sum(axis=0), axis=1)

# Sequencia de meses para o eixo x
x = np.arange(len(pivot_prop.index))
# Largura das barras
bar_width = 0.40

# Cria o gráfico de barras
plt.figure(figsize=(12, 7))
# Plota as barras para cada tipo de usuário
bar_member = plt.bar(x - bar_width/2, pivot_prop['member'], width=bar_width, label='Member', color='orange', zorder = 3)
bar_casual = plt.bar(x + bar_width/2, pivot_prop['casual'], width=bar_width, label='Casual', color='skyblue', zorder = 3)

#Configurações do gráfico
plt.xticks(x, pivot_prop.index, rotation=45)
plt.ylabel('Proporção de uso (%)')
plt.xlabel('Meses do ano')
plt.title('Proporção de uso por mês e tipo de usuário')
plt.legend()

# Adiciona os rótulos de porcentagem acima das barras
for bar in bar_member:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.005, f'{height*100:.1f}%', ha='center', fontsize=8)

for bar in bar_casual:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.005, f'{height*100:.1f}%', ha='center', fontsize=8)

# Configurações do gráfico
plt.ylim(0, 0.20)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
plt.show()
