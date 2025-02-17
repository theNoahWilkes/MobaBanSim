""" Ban Sim
    A simple module to simulate the banning phase of a MOBA game.
"""
import random

class Game:
    def __init__(self, characters: list, team_size, num_teams = 2):
        self._characters = characters
        self._team_size = team_size
        self._lobby = self.Lobby(self, team_size=team_size, num_teams=num_teams)

    class Lobby:
        def __init__(self, game, team_size, num_teams):
            self._teams = []
            for i in range(num_teams):
                self._teams.append(Team([Player(game)]*team_size))

        @property
        def teams(self):
            return self._teams

    def ban_phase(self) -> list:
        pass

    @property
    def lobby(self):
        return self._lobby

    @property
    def characters(self):
        return self._characters


class Team(list):
    @property
    def players(self):
        return self


class Player:
    def __init__(self, game: Game):
        self._game = game
        self._ban_strategy = self.random_ban_vote

    @staticmethod
    def random_ban_vote(choices, number: int):
        ban_votes = []
        for i in range(number):
            ban_votes.append(random.choice(choices))
        return ban_votes

    def pick_bans(self, num_votes=3):
        return self._ban_strategy(self._game.characters, num_votes)


class Character:
    def __init__(self, name: str, role: str):
        self._role = role
        self._name = name

    def __repr__(self):
        return self._name

    @property
    def role(self):
        return self._role

    @property
    def name(self):
        return self._name