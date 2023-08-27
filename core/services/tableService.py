from core.classes.table import Table
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

class tableService():

    def getTable():
    
        # Getting informations from table
        if cache.get("table") is None:
            response = requests.get(f'{apiString}/standings?league={league}&season={season}', headers=headersAuth)
            json = response.json()
            cache.add("table", json, 86400)
        else:
            json = cache.get("table")
        
        table = []
        json = json['response'][0]['league']['standings'][0]
        for teams in json:
            pointsPercentage = teams['points']/(teams['all']['played']*3)*100
            table.append(Table(teams['rank'], teams['points'], teams['team']['name'], teams['all']['played'], teams['all']['win'], teams['all']['draw'], teams['all']['lose'], teams['all']['goals']['for'],
                    teams['all']['goals']['against'], teams['goalsDiff'], f'{pointsPercentage:.2f}', teams['form']))
            
        return table