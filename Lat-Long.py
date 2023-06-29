import pandas as pd
from geopy.geocoders import Nominatim

### ESTE SCRIPT RETIRA A LATITUDE E LONGITUDE POR REFERENCIA DE MUNICIPIOS ###
# Lê o arquivo em Excel com os nomes dos municípios
df = pd.read_excel('Municipios_brasileiros_Mun_Falta1.xlsx')
df.columns = ['Municipio', 'UF']
# Cria uma instância do geocoder Nominatim
geolocator = Nominatim(user_agent="my_app")

# Define uma função para consultar a latitude e longitude de um município
def get_lat_lon(row):
    try:
        # Obtém o nome do município e a UF a partir do DataFrame
        municipio = row['Municipio']
        uf = row['UF']

        # Faz a consulta de geocodificação para o município e a UF
        location = geolocator.geocode(f'{municipio}, {uf}, Brasil')

        # Imprime as informações de latitude e longitude
        print(f'{municipio}, {uf}: {location.latitude}, {location.longitude}')

        # Retorna a latitude e longitude
        return (location.latitude, location.longitude)
    except:
        # Caso não seja possível fazer a consulta, retorna None
        return None

# Adiciona uma coluna para o UF e Municipio ao DataFrame
df['UF_Municipio'] = df['Municipio'] + ', ' + df['UF']

# Aplica a função para cada UF e Municipio e adiciona as colunas de latitude e longitude ao DataFrame
print('Coletando informações de latitude e longitude...')
df['latitude_longitude'] = df.apply(get_lat_lon, axis=1)
print('Informações de latitude e longitude coletadas.')

# Separa as colunas de UF e Municipio da coluna UF_Municipio
df[['Municipio', 'UF']] = pd.DataFrame(df['UF_Municipio'].str.split(', ', 1).tolist(), index=df.index)

# Divide a coluna de latitude e longitude em colunas separadas de latitude e longitude
df[['latitude', 'longitude']] = pd.DataFrame(df['latitude_longitude'].tolist(), index=df.index)

# Remove as colunas UF_Municipio e latitude_longitude
df.drop(['UF_Municipio', 'latitude_longitude'], axis=1, inplace=True)

# Salva o DataFrame com as informações de latitude e longitude em um novo arquivo em Excel
df.to_excel('municipios_lat-long_Falta1_restante.xlsx', index=False)

print('Arquivo salvo com sucesso!')
