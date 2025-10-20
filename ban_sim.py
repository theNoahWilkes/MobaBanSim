""" Ban Sim
    A simple module to simulate the banning phase of a MOBA game.
"""
import random

class Game:
    """Represents a generic game with characters, teams, and a banning phase.

    Attributes:
        characters (list): A list of Character objects available in the game.
        team_size (int): The number of players on each team.
        num_teams (int): The total number of teams in the game.
        lobby (Lobby): The game lobby where teams and players are managed.
    """
    def __init__(self, characters: list, team_size, num_teams = 2):
        """Initializes a new Game instance.

        Args:
            characters (list): A list of Character objects.
            team_size (int): The size of each team.
            num_teams (int, optional): The number of teams. Defaults to 2.
        """
        self._characters = characters
        self._team_size = team_size
        self._lobby = self.Lobby(self, team_size=team_size, num_teams=num_teams)

    class Lobby:
        """Manages the teams and players in the game lobby.

        Attributes:
            teams (list): A list of Team objects.
        """
        def __init__(self, game, team_size, num_teams):
            """Initializes a new Lobby instance.

            Args:
                game (Game): The parent Game object.
                team_size (int): The number of players per team.
                num_teams (int): The total number of teams.
            """
            self._teams = []
            for i in range(num_teams):
                self._teams.append(Team([Player(game)]*team_size))

        @property
        def teams(self):
            """list: Returns the list of teams in the lobby."""
            return self._teams

    def ban_phase(self) -> list:
        """Executes the character banning phase.

        This method should be implemented by a subclass.

        Returns:
            list: A list of banned characters.
        """
        pass

    @property
    def lobby(self):
        """Lobby: Returns the game lobby."""
        return self._lobby

    @property
    def characters(self):
        """list: Returns the list of available characters."""
        return self._characters


class Team(list):
    """Represents a team of players."""
    @property
    def players(self):
        """list: Returns the list of players on the team."""
        return self


class Player:
    """Represents a player in the game.

    Attributes:
        game (Game): The Game object the player belongs to.
        ban_strategy (function): The strategy used to vote for bans.
    """
    def __init__(self, game: Game):
        """Initializes a new Player instance.

        Args:
            game (Game): The parent Game object.
        """
        self._game = game
        self._ban_strategy = self.random_ban_vote

    @staticmethod
    def random_ban_vote(choices, number: int):
        """Randomly selects a specified number of ban votes from a list of choices.

        Args:
            choices (list): The list of characters to choose from.
            number (int): The number of votes to cast.

        Returns:
            list: A list of characters voted for banning.
        """
        ban_votes = []
        for i in range(number):
            ban_votes.append(random.choice(choices))
        return ban_votes

    def pick_bans(self, num_votes=3):
        """Picks character bans based on the assigned ban strategy.

        Args:
            num_votes (int, optional): The number of bans to pick. Defaults to 3.

        Returns:
            list: A list of characters to ban.
        """
        return self._ban_strategy(self._game.characters, num_votes)


class Character:
    """Represents a character in the game.

    Attributes:
        name (str): The name of the character.
        role (str): The role of the character (e.g., Tank, Damage, Support).
    """
    def __init__(self, name: str, role: str):
        """Initializes a new Character instance.

        Args:
            name (str): The name of the character.
            role (str): The role of the character.
        """
        self._role = role
        self._name = name

    def __repr__(self):
        """str: Returns the string representation of the character, which is its name."""
        return self._name

    @property
    def role(self):
        """str: Returns the role of the character."""
        return self._role

    @property
    def name(self):
        """str: Returns the name of the character."""
        return self._name