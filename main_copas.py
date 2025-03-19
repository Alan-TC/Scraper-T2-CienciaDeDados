import pandas as pd
from Copa import Competicoes
from Partida import PartidaCatch

comps = [('cbr', 'copabr'), ('la', 'liberta'), ('cl', 'champions')]

p_catch = PartidaCatch()
c = Competicoes()

for comp in comps:
    seasons = Competicoes().get_competicoes_temporadas()[comp[0]]

    for ano in range(seasons[0], max(2020, seasons[1] - 1), -1):
        partidas = []

        try:
            links = c.partidas_estatistica_links(comp[0], ano)
        except:
            print(ano, 'deu errado!')
            continue
        
        for fase in links:
            print(comp[0], fase, ' | Ano:', ano)
            for i, jogo in enumerate(links[fase]):
                print('Jogo:', i, jogo)
                try:
                    p_dict = p_catch.get_partida(jogo).get_partida_est()
                    p_dict['ano'], p_dict['fase'] = ano, fase
                    partidas.append(p_dict)
                except Exception as e:
                    print(e, '-> Partida sem estatísticas!?')
                    continue

        pd.DataFrame(partidas).to_csv(f'Dados/{comp[1]}_partidas/partidas_{ano}.csv', index=False)