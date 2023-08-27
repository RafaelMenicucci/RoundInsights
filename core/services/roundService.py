from core.classes.round import Round
from django.core.cache import cache
import requests

from round_insight.settings import LIVE_API_KEY_SOCCER
apiString = "https://v3.football.api-sports.io"

headersAuth = {
    'x-rapidapi-key': str(LIVE_API_KEY_SOCCER),
    'x-rapidapi-host': 'v3.football.api-sports.io',
}

# Campeonato Brasileiro
league = 71

# Temporada
season = 2023

class roundService():

    def getJsonRound():
        # Getting which round is next, or the one that is happening at the moment 
        if cache.get("championship") is None:
            response = requests.get(f'{apiString}/fixtures/rounds?league={league}&season={season}&current=true', headers=headersAuth)
            json = response.json()
            cache.add("championship", json, 86400)
        else:
            json = cache.get("championship")

        return json
    
    def getRound(roundNumber):
        round = roundNumber.split(" - ", 1)[1]
        # Getting informations from the current round
        if cache.get(f"round{round}") is None:
            response = requests.get(f'{apiString}/fixtures?league={league}&season={season}&round={roundNumber}&timezone=America/Sao_Paulo', headers=headersAuth)
            json = response.json()
            round = roundNumber.split(" - ", 1)[1]
            cache.add(f"round{round}", json, 86400)
        else:
            round = roundNumber.split(" - ", 1)[1]
            json = cache.get(f"round{round}")

        round = Round(roundNumber, json['response'])

        return round
    
    def clearCache(roundNumber):
        cache.delete(f"round{roundNumber}")