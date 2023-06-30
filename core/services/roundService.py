from core.classes.round import Round
from django.core.cache import cache
import requests

from round_insight.settings import LIVE_API_KEY_SOCCER

headersAuth = {
    'Authorization': 'Bearer '+ str(LIVE_API_KEY_SOCCER),
}

# Campeonato Brasileiro
championship = 10

class roundService():

    def getJsonRound():
        # Getting which round is next, or the one that is happening at the moment 
        if cache.get("championship") is None:
            response = requests.get(f'https://api.api-futebol.com.br/v1/campeonatos/{championship}/', headers=headersAuth)
            json = response.json()
            cache.add("championship", json,86400)
        else:
            json = cache.get("championship")

        return json
    
    def getRound(roundNumber):
        # Getting informations from the current round
        if cache.get(f"round{roundNumber}") is None:
            response = requests.get(f'https://api.api-futebol.com.br/v1/campeonatos/{championship}/rodadas/{roundNumber}', headers=headersAuth)
            json = response.json()
            cache.add(f"round{roundNumber}", json,86400)
        else:
            json = cache.get(f"round{roundNumber}")

        round = Round(json['nome'],json['rodada'],json['proxima_rodada']['rodada'],json['rodada_anterior']['rodada'],json['partidas'])

        return round