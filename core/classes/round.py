from core.classes.matches import Matches

class Round():

    def __init__(self, name, round, nextRound, previousRound, allMatches) -> None:
        self.name = name
        self.round = round
        self.nextRound = nextRound
        self.previousRound = previousRound
        self.matches = []
        for match in allMatches:
            self.matches.append(Matches(match['partida_id'], 
                                        match['time_mandante']['nome_popular'], 
                                        match['time_mandante']['escudo'],
                                        match['time_visitante']['nome_popular'],
                                        match['time_visitante']['escudo'],
                                        match['placar_mandante'],
                                        match['placar_visitante'],
                                        match['data_realizacao'],
                                        match['hora_realizacao'],
                                        match['estadio']['nome_popular'] if match['estadio'] is not None else ""))
