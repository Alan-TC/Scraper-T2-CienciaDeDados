import pandas as pd

ligas = [("brasileirao", list(range(2020, 2024))), ("premierleague", list(range(2020, 2024)))]

partidas_df = pd.read_csv('Dados/brasileirao_partidas/partidas_2024.csv')

for liga, anos in ligas:
    for ano in anos:
        df = pd.read_csv(f'Dados/{liga}_partidas/partidas_{ano}.csv')
        partidas_df = pd.concat([partidas_df, df], ignore_index=True)

partidas_df["publico_estadio"] = partidas_df["publico_estadio"].str.split(' ').str[0]
partidas_df["publico_estadio"] = partidas_df["publico_estadio"].str.replace('.', '')
partidas_df["publico_estadio"] = partidas_df["publico_estadio"].astype(str).apply(lambda x : x if x.isdigit() else '0').astype(int)
partidas_df["capacidade_estadio"] = partidas_df["capacidade_estadio"].fillna(0).multiply(1000).round(0).astype(int)

partidas_df.to_csv('Dados/partidas.csv', index=False)