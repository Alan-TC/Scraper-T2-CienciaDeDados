import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def converter_para_numero(valor):
    valor = valor.replace('.', '')
    try:
        if 'mil' in valor:
            valor = valor.split(sep=' ')[0].replace(',', '.').strip()
            return float(valor)
        elif 'mi' in valor:
            valor = valor.split(sep=' ')[0].replace(',', '.').strip()
            return float(valor) * 1000
        elif 'bilhões' in valor:
            valor = valor.split(sep=' ')[0].replace(',', '.').strip()
            return float(valor) * 1000000
        else:
            return float(valor) / 1000
    except:
        return 0.0

def para_float(valor):
    valor = valor.replace('.', '').strip()
    valor = valor.replace(',', '.').strip()
    try:
        return float(valor)
    except:
        return 0


class PartidaCatch:

    def __init__(self):
        options = Options()
        options.add_argument("--headless")

        self._driver = webdriver.Chrome(options=options)
    
    def get_partida(self, link_estatistica_partida):
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"}

        self._driver.get(link_estatistica_partida)
        self._driver.implicitly_wait(1)


        season_url = link_estatistica_partida.replace("/statistik/", "/vorbericht/")

        res = requests.get(url=season_url, headers=headers)

        if res.status_code != 200:
            raise Exception('Erro na página')
        
        return Partida(self._driver.page_source, res.content)

    def __del__(self):
        self._driver.quit()

class Partida:

    def __init__(self, page_html, page_html_teams):

        page_soup = BeautifulSoup(page_html, 'html.parser')
        page_soup_teams = BeautifulSoup(page_html_teams, 'html.parser')

        self._carrega_partida(page_soup, page_soup_teams)


    def _carrega_partida(self, page_soup, page_soup_teams):
        self._estatisticas = \
        {
            'capacidade_estadio': 0,
            'publico_estadio': 0,
            'time_casa': '',
            'valor_mercado_casa': 0,
            'valor_mercado_media_casa': 0,
            'media_idade_casa': 0,
            'jogadores_de_selecao_casa': 0,
            'jogadores_de_sub_selecao_casa': 0,
            'estrangeiros_casa': 0,
            'gols_casa': 0,
            'posse_casa': 0,
            'socios_torcedores_casa': 0,
            'tentativas_casa': 0,
            'chutes_fora_casa': 0,
            'defesa_casa': 0,
            'escanteios_casa': 0,
            'cobrancas_falta_casa': 0,
            'faltas_cometidas_casa': 0,
            'impedimentos_casa': 0,
            'time_fora': '',
            'valor_mercado_fora': 0,
            'valor_mercado_media_fora': 0,
            'media_idade_fora': 0,
            'jogadores_de_selecao_fora': 0,
            'jogadores_de_sub_selecao_fora': 0,
            'estrangeiros_fora': 0,
            'socios_torcedores_fora': 0,
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

        cap_table = page_soup.find_all('table', {"class":"profilheader"})[0]

        self._estatisticas['publico_estadio'], self._estatisticas['capacidade_estadio'] = list(map(lambda x: x.text.strip(), cap_table.find_all('td')[1:3]))

        casa = page_soup.find_all('div', {"class": "sb-team sb-heim"})[0]
        fora = page_soup.find_all('div', {"class": "sb-team sb-gast"})[0]

        self._estatisticas['time_casa'] = casa.find_all('a')[1].text.strip()
        self._estatisticas['time_fora'] =  fora.find_all('a')[1].text.strip()

        gols = page_soup.find_all('div', {"class": "sb-endstand"})
        self._estatisticas['gols_casa'], self._estatisticas['gols_fora'] = gols[0].text.strip().split(sep='(')[0].split(sep=':')

        posse = page_soup.find_all('tspan')

        self._estatisticas['posse_casa'], self._estatisticas['posse_fora'] = [posse[2].text, posse[1].text]

        todas__estatisticas = [x.text for x in page_soup.find_all('div', {"class": "sb-statistik-zahl"})]
        
        self._estatisticas['tentativas_casa'], self._estatisticas['tentativas_fora'] = todas__estatisticas[0:2]

        self._estatisticas['chutes_fora_casa'], self._estatisticas['chutes_fora_fora'] = todas__estatisticas[2:4]

        self._estatisticas['defesa_casa'], self._estatisticas['defesa_fora'] = todas__estatisticas[4:6]

        self._estatisticas['escanteios_casa'], self._estatisticas['escanteios_fora'] = todas__estatisticas[6:8]

        self._estatisticas['cobrancas_falta_casa'], self._estatisticas['cobrancas_falta_fora'] = todas__estatisticas[8:10]

        self._estatisticas['faltas_cometidas_casa'], self._estatisticas['faltas_cometidas_fora'] = todas__estatisticas[10:12]

        self._estatisticas['impedimentos_casa'], self._estatisticas['impedimentos_fora'] = todas__estatisticas[12:14]

        all_team_x_team_tds = page_soup_teams.find_all('td', class_=['daten-und-fakten-linker_balken', 'daten-und-fakten-rechter_balken'])
        tds_contents = [td.find_all('span')[0].text for td in all_team_x_team_tds]

        self._estatisticas['valor_mercado_casa'] = converter_para_numero(tds_contents[0])
        self._estatisticas['valor_mercado_fora'] = converter_para_numero(tds_contents[1])
        self._estatisticas['valor_mercado_media_casa'] = converter_para_numero(tds_contents[2])
        self._estatisticas['valor_mercado_media_fora'] = converter_para_numero(tds_contents[3])
        self._estatisticas['media_idade_casa'] = para_float(tds_contents[4])
        self._estatisticas['media_idade_fora'] = para_float(tds_contents[5])
        self._estatisticas['jogadores_de_selecao_casa'] = para_float(tds_contents[6])
        self._estatisticas['jogadores_de_selecao_fora'] = para_float(tds_contents[7])
        self._estatisticas['jogadores_de_sub_selecao_casa'] = para_float(tds_contents[8])
        self._estatisticas['jogadores_de_sub_selecao_fora'] = para_float(tds_contents[9])
        self._estatisticas['estrangeiros_casa'] = para_float(tds_contents[10])
        self._estatisticas['estrangeiros_fora'] = para_float(tds_contents[11])
        self._estatisticas['socios_torcedores_casa'] = para_float(tds_contents[12])
        self._estatisticas['socios_torcedores_fora'] = para_float(tds_contents[13])

    def get_partida_df(self):
        return pd.DataFrame({key: [self._estatisticas[key]] for key in self._estatisticas})
    
    def get_partida_est(self):
        return self._estatisticas

if __name__ == '__main__':

    links = [
        'https://www.transfermarkt.com.br/cr-vasco-da-gama_atletico-goianiense/statistik/spielbericht/4399304',
        'Link_Erro',
        'https://www.transfermarkt.com.br/sc-internacional_ec-bahia/statistik/spielbericht/4316187',
        'https://www.transfermarkt.com.br/gremio-fbpa_sc-corinthians/statistik/spielbericht/4399309',
        'https://www.transfermarkt.com.br/fc-burnley_manchester-city-fc/statistik/spielbericht/4087924'
    ]

    p_catch = PartidaCatch()

    all_matches = []

    for link in links:
        try:
            partida = p_catch.get_partida(link)
            all_matches.append(partida.get_partida_est())
        except:
            print("Erro:", link)
        
    
    # print(pd.DataFrame(all_matches))
    pd.DataFrame(all_matches).to_csv('partidas.csv', index=False)
