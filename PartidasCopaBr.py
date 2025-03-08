import requests
from Partida import PartidaCatch
from bs4 import BeautifulSoup
import pandas as pd

def partidas_estatistica_links(season_url):
    # Key = Fase, Value = links das partida na Fase
    links = {}

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

    res = requests.get(url=season_url, headers=headers)

    if res.status_code != 200:
        raise Exception('Erro na página')
    
    pageSoup = BeautifulSoup(res.content, 'html.parser')

    tabela = pageSoup.find_all('tbody')[1]

    # Das oitavas até a final
    infos_partidas = tabela.find_all('tr')[0:38]

    fase = ''
    for item in infos_partidas:
        if item['class'][0] == 'rundenzeile':
            fase = item.find_all('a')[0].text.strip()
            links[fase] = []
        elif item['class'][0] == 'begegnungZeile':
            partida_link = item.find_all('a', {'title': 'Colocar informaçãoes online?'})[0]['href'].strip().replace("/index/", "/statistik/")
            links[fase].append(f'https://www.transfermarkt.com.br{partida_link}')

    return links

if __name__ == "__main__":
    url = 'https://www.transfermarkt.com.br/copa-do-brasil/startseite/pokalwettbewerb/BRC?saison_id='

    p_catch = PartidaCatch()

    for ano in range(2019, 1999, -1):
        partidas = []

        page_url = url + str(ano - 1)

        try:
            links = partidas_estatistica_links(page_url)
        except:
            print(ano, 'deu errado!')
            continue
        
        for fase in links:
            print(fase, ' | Ano:', ano)
            for i, jogo in enumerate(links[fase]):
                print('Jogo:', i, jogo)
                try:
                    p_dict = p_catch.get_partida(jogo).get_partida_est()
                    p_dict['ano'], p_dict['fase'] = ano, fase
                    partidas.append(p_dict)
                except Exception as e:
                    print(e)
                    continue

        pd.DataFrame(partidas).to_csv(f'Dados/copabr_partidas/partidas_{ano}.csv', index=False)