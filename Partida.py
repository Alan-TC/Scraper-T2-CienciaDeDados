from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup

class PartidaCatch:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=options)
    
    def get_partida(self, link_estatistica_partida):
        self._driver.get(link_estatistica_partida)

        self._driver.implicitly_wait(1)
        
        return Partida(self._driver.page_source)

    def __del__(self):
        self._driver.quit()

class Partida:

    def __init__(self, pageHtml):

        pageSoup = BeautifulSoup(pageHtml, 'html.parser')

        self._carrega_partida(pageSoup)


    def _carrega_partida(self, pageSoup):
        self._estatisticas = \
        {
            'capacidade_estadio': 0,
            'publico_estadio': 0,
            'time_casa': '',
            'gols_casa': 0,
            'posse_casa': 0,
            'tentativas_casa': 0,
            'chutes_fora_casa': 0,
            'defesa_casa': 0,
            'escanteios_casa': 0,
            'cobrancas_falta_casa': 0,
            'faltas_cometidas_casa': 0,
            'impedimentos_casa': 0,
            'time_fora': '',
            'gols_fora': 0,
            'posse_fora': 0,
            'tentativas_fora': 0,
            'chutes_fora_fora': 0,
            'defesa_fora': 0,
            'escanteios_fora': 0,
            'cobrancas_falta_fora': 0,
            'faltas_cometidas_fora': 0,
            'impedimentos_fora': 0,
        }

        cap_table = pageSoup.find_all('table', {"class":"profilheader"})[0]

        self._estatisticas['publico_estadio'], self._estatisticas['capacidade_estadio'] = list(map(lambda x: x.text.strip(), cap_table.find_all('td')[1:3]))

        casa = pageSoup.find_all('div', {"class": "sb-team sb-heim"})[0]
        fora = pageSoup.find_all('div', {"class": "sb-team sb-gast"})[0]

        self._estatisticas['time_casa'] = casa.find_all('a')[1].text.strip()
        self._estatisticas['time_fora'] =  fora.find_all('a')[1].text.strip()

        gols = pageSoup.find_all('div', {"class": "sb-endstand"})
        self._estatisticas['gols_casa'], self._estatisticas['gols_fora'] = gols[0].text.strip().split(sep='(')[0].split(sep=':')

        posse = pageSoup.find_all('tspan')

        self._estatisticas['posse_casa'], self._estatisticas['posse_fora'] = [posse[2].text, posse[1].text]

        todas__estatisticas = [x.text for x in pageSoup.find_all('div', {"class": "sb-statistik-zahl"})]
        
        self._estatisticas['tentativas_casa'], self._estatisticas['tentativas_fora'] = todas__estatisticas[0:2]

        self._estatisticas['chutes_fora_casa'], self._estatisticas['chutes_fora_fora'] = todas__estatisticas[2:4]

        self._estatisticas['defesa_casa'], self._estatisticas['defesa_fora'] = todas__estatisticas[4:6]

        self._estatisticas['escanteios_casa'], self._estatisticas['escanteios_fora'] = todas__estatisticas[6:8]

        self._estatisticas['cobrancas_falta_casa'], self._estatisticas['cobrancas_falta_fora'] = todas__estatisticas[8:10]

        self._estatisticas['faltas_cometidas_casa'], self._estatisticas['faltas_cometidas_fora'] = todas__estatisticas[10:12]

        self._estatisticas['impedimentos_casa'], self._estatisticas['impedimentos_fora'] = todas__estatisticas[12:14]

    def get_partida_df(self):
        return pd.DataFrame({key: [self._estatisticas[key]] for key in self._estatisticas})
    
    def get_partida_est(self):
        return self._estatisticas

if __name__ == '__main__':

    links = [
        'https://www.transfermarkt.com.br/cr-vasco-da-gama_atletico-goianiense/statistik/spielbericht/4399304',
        'Link_Erro',
        'https://www.transfermarkt.com.br/sc-internacional_ec-bahia/statistik/spielbericht/4316187',
        'https://www.transfermarkt.com.br/gremio-fbpa_sc-corinthians/statistik/spielbericht/4399309'
    ]

    p_catch = PartidaCatch()

    all_matches = []

    for link in links:
        try:
            partida = p_catch.get_partida(link)
            all_matches.append(partida.get_partida_est())
        except:
            print("Erro:", link)
        
    
    print(pd.DataFrame(all_matches))
