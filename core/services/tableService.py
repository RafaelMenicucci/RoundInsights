from core.classes.table import Table
from django.core.cache import cache
import requests

from round_insight.settings import LIVE_API_KEY_SOCCER

class tableService():

    def getTable():
        headersAuth = {
            'Authorization': 'Bearer '+ str(LIVE_API_KEY_SOCCER),
        }

        # Campeonato Brasileiro
        championship = 10

        # Getting informations from table
        if cache.get("table") is None:
            response = requests.get(f'https://api.api-futebol.com.br/v1/campeonatos/{championship}/tabela', headers=headersAuth)
            json = response.json()
            cache.add("table", json,86400)
        else:
            json = cache.get("table")
        
        table = []
        for teams in json:
            table.append(Table(teams['posicao'],teams['pontos'],teams['time']['nome_popular'],teams['jogos'],teams['vitorias'],teams['empates'],teams['derrotas'],teams['gols_pro'],
                    teams['gols_contra'],teams['saldo_gols'],teams['aproveitamento'],teams['ultimos_jogos']))
            
        return table