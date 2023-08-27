from core.classes.matches import Matches

class Round():

    def __init__(self, name, allMatches) -> None:
        self.name = name
        self.matches = []
        for match in allMatches:
            self.matches.append(Matches(match['fixture']['id'], 
                                        match['teams']['home']['name'], 
                                        match['teams']['home']['logo'],
                                        match['teams']['away']['name'], 
                                        match['teams']['away']['logo'],
                                        match['goals']['home'],
                                        match['goals']['away'],
                                        match['fixture']['date'].split("T",1)[0],
                                        match['fixture']['date'].split("T",1)[1].split("-",1)[0],
                                        match['fixture']['venue']['name'] ))
