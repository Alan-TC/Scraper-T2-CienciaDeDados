import requests
from Partida import PartidaCatch
from bs4 import BeautifulSoup
import pandas as pd

class Competicoes:
    _competicao = \
    {
        'cbr': (2024, 2020, 'https://www.transfermarkt.com.br/copa-do-brasil/startseite/pokalwettbewerb/BRC?saison_id='),
        'la': (2023, 2015, 'https://www.transfermarkt.com.br/copa-libertadores/startseite/pokalwettbewerb/CLI?saison_id='),
        'cl': (2024, 2000, 'https://www.transfermarkt.com.br/liga-dos-campeoes/startseite/pokalwettbewerb/CL?saison_id=')
    }

    def get_competicoes_desc(self):
        return {'cbr': 'Copa do Brasil', 'la': 'Libertadores da América', 'cl': 'Champions League'}
    
    def get_competicoes_temporadas(self):
        return {'cbr': (self._competicao['cbr'][0], self._competicao['cbr'][1]),
                'la': (self._competicao['la'][0], self._competicao['la'][1]),
                'cl': (self._competicao['cl'][0], self._competicao['cl'][1])}
    
    def partidas_estatistica_links(self, comp_tag, temporada):
        # Key = Fase, Value = links das partida na Fase
        links = {}

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

        season_url = self._competicao[comp_tag][2] + str(int(temporada) - 1)

        res = requests.get(url=season_url, headers=headers)

        if res.status_code != 200:
            raise Exception('Erro na página')
        
        pageSoup = BeautifulSoup(res.content, 'html.parser')

        tabela = pageSoup.find_all('tbody')[1]

        infos_partidas = tabela.find_all('tr', class_=['rundenzeile', 'begegnungZeile'])

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
    p_catch = PartidaCatch()
    
    c = Competicoes()
    comp_tag = 'cbr'

    seasons = Competicoes().get_competicoes_temporadas()[comp_tag]

    for ano in range(seasons[0], seasons[1] - 1, -1):
        partidas = []

        try:
            links = c.partidas_estatistica_links(comp_tag, ano)
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
                    print(e, '-> Partida sem estatísticas!?')
                    continue

        pd.DataFrame(partidas).to_csv(f'partidas_{ano}.csv', index=False)