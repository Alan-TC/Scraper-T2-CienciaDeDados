import requests
from Partida import PartidaCatch
from bs4 import BeautifulSoup
import pandas as pd

class Competicoes:
    _competicao = \
    {
        'lbr': (2024, 1996, 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/gesamtspielplan/wettbewerb/BRA1?saison_id='),
        'pl': (2023, 1992, 'https://www.transfermarkt.com.br/premier-league/gesamtspielplan/wettbewerb/GB1?saison_id=')
    }

    def get_competicoes_desc(self):
        return {'lbr': 'Campeonato Brasileiro', 'pl': 'Premier League'}
    
    def get_competicoes_temporadas(self):
        return {'lbr': (self._competicao['lbr'][0], self._competicao['lbr'][1]),
                'pl': (self._competicao['pl'][0], self._competicao['pl'][1])}

    def partidas_estatistica_links(self, comp_tag, temporada):
        # Key = Rodada, Value = links das partida na rodada
        links = {}

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

        season_url = self._competicao[comp_tag][2] + str(int(temporada) - 1)

        res = requests.get(url=season_url, headers=headers)

        if res.status_code != 200:
            raise Exception('Erro na página')
        
        pageSoup = BeautifulSoup(res.content, 'html.parser')

        rodadas = pageSoup.find_all('div', {"class": "large-6 columns"})

        for rodada in rodadas:
            rodada_atual = rodada.find_all('div', {"class": "content-box-headline"})[0].text.strip()
            
            links[rodada_atual] = list(map(lambda x: x['href'].strip(), rodada.find_all('a', {"class": "ergebnis-link"})))

            links[rodada_atual] = [f'https://www.transfermarkt.com.br{x.replace("/index/", "/statistik/")}' for x in links[rodada_atual]]

        return links


if __name__ == "__main__":

    url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/gesamtspielplan/wettbewerb/BRA1?saison_id='

    p_catch = PartidaCatch()
    c = Competicoes()
    comp_tag = 'lbr'

    seasons = Competicoes().get_competicoes_temporadas()[comp_tag]

    for ano in range(seasons[0], max(2021, seasons[1] - 1), -1):
        partidas = []

        page_url = url + str(ano - 1)

        try:
            links = c.partidas_estatistica_links(comp_tag, ano)
        except:
            print(ano, 'deu errado!')
            continue
        
        for rodada in links:
            print(rodada, ' | Ano:', ano)
            for i, jogo in enumerate(links[rodada]):
                print('Jogo:', i, jogo)
                try:
                    p_dict = p_catch.get_partida(jogo).get_partida_est()
                    p_dict['ano'], p_dict['rodada'] = ano, rodada
                    partidas.append(p_dict)
                except Exception as e:
                    print(e, '-> Partida sem estatísticas!?')
                    continue

        pd.DataFrame(partidas).to_csv(f'partidas_{ano}.csv', index=False)