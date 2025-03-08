import requests
import pandas as pd
from bs4 import BeautifulSoup

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

# url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/tabelle/wettbewerb/BRA1/saison_id/'

url = 'https://www.transfermarkt.com.br/premier-league/tabelle/wettbewerb/GB1?saison_id='

table_result = {
    'Ano': [],
    'Posicao': [],
    'Nome': [],
    'Jogos': [],
    'Vitorias': [],
    'Empates': [],
    'Derrotas': [],
    'Gols': [],
    'SG': [],
    'Pontos': []
}

for ano in range(2024, 1995, -1):
    print("Obtendo", ano, "...")

    page_url = url + str(ano - 1)

    res = requests.get(url=page_url, headers=headers)

    if res.status_code == 200:
        print(res.status_code)

    pageSoup = BeautifulSoup(res.content, 'html.parser')

    tables = pageSoup.find_all("table", {"class": "items"})

    table_rows = tables[0].find_all("tbody")[0].find_all("tr")

    for row in table_rows:
        line = row.find_all("td")

        table_result['Ano'].append(ano)
        table_result['Posicao'].append(line[0].text)
        table_result['Nome'].append(line[2].text.strip())
        table_result['Jogos'].append(line[3].text)
        table_result['Vitorias'].append(line[4].text)
        table_result['Empates'].append(line[5].text)
        table_result['Derrotas'].append(line[6].text)
        table_result['Gols'].append(line[7].text)
        table_result['SG'].append(line[8].text)
        table_result['Pontos'].append(line[9].text)


pd.DataFrame(table_result).to_csv('premierleague2.csv', index=False)