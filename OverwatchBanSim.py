from itertools import cycle, chain
from ban_sim import *

import json
import pprint
import logging

logging.basicConfig(level=logging.DEBUG)

def add_em_up(team_ban_votes: list):
    """Tallies player votes for character bans and assigns scores.

    This function takes a list of player votes, where each player submits a ranked
    list of characters to ban. It then calculates a score for each character based
    on their ranking, aggregates the scores, and returns a dictionary of
    characters and their total scores.

    Args:
        team_ban_votes (list): A list of lists, where each inner list represents a
                               player's ranked ban choices.

    Returns:
        dict: A dictionary where keys are the characters and values are their
              aggregated ban scores.
    """
    vote_tally = {}
    for player_vote in team_ban_votes:
        score = 3
        player_vote.reverse()
        for v in player_vote:  # I don't understand why this is saying NoneType isn't iterable...
            if v in vote_tally:
                vote_tally[v] += score
            else:
                vote_tally[v] = score
            score += 2
    return vote_tally


def snake_cycle(iterable) -> iter :
    """Cycles through an iterable in a 'snake' pattern (forward, then reverse).

    This generator function cycles through an iterable indefinitely, alternating
    between forward and reverse order for each cycle.

    Args:
        iterable: The iterable to cycle through.

    Yields:
        iter: The next item in the snake-cycled iterable.
    """
    r = reversed(iterable)
    for i in cycle(chain(iterable, r)):
        yield i

class Overwatch(Game):
    """Represents a game of Overwatch, including custom ban logic.

    This class extends the base `Game` class to implement the specific rules
    for character banning in Overwatch, such as role-based ban limits.

    Attributes:
        teams (list): A list of teams in the game.
    """
    def __init__(self):
        """Initializes a new Overwatch game instance.

        This constructor loads character data from a JSON file and sets up the
        game with the appropriate team size and characters.
        """
        characters = []
        # Read the characters and their roles
        with open("Overwatch_Heroes.json", "r", encoding="utf-8") as f:
            for char in json.load(f):
                characters.append(Character(char["name"], char["role"]))
                super().__init__(characters, 5)

    class BanList(list):
        """A custom list for managing banned characters with role limits.

        This class extends the built-in list to enforce a maximum number of
        bans per role.

        Attributes:
            MAX_ROLE_BANS (int): The maximum number of characters that can be
                                 banned from a single role.
        """
        MAX_ROLE_BANS = 2
        def __init__(self):
            """Initializes a new BanList instance."""
            super().__init__()
            self._role_count = {}

        def ban(self, character: Character) -> bool:
            """Attempts to ban a character, respecting role limits.

            This method checks if banning the given character would exceed the
            maximum number of bans for their role. If the ban is valid, the
            character is added to the ban list and the role count is updated.

            Args:
                character (Character): The character to be banned.

            Returns:
                bool: True if the character was successfully banned, False otherwise.
            """
            try:
                assert self._role_count.get(character.role) < self.MAX_ROLE_BANS
                assert character not in self
            except AssertionError:
                return False
            except TypeError:
                self._role_count[character.role] = 0
            self._role_count[character.role] += 1
            super().append(character)
            return True

    @property
    def teams(self):
        """list: Returns the list of teams in the game."""
        return self._teams

    def ban_phase(self):
        """Executes the Overwatch ban phase.

        This method guides players through the process of voting for their top
        three bans, tallies the votes, and then allows teams to take turns
        nominating characters to ban based on the vote results. Banning
        continues until each team has banned two characters or there are no
        more valid nominees.

        Returns:
            BanList: A list of the characters banned during the phase.
        """

        # Select and tally the votes
        scored_bans = []
        for team in self.lobby.teams:
            team_bans = [pl.pick_bans() for pl in team]
            added = add_em_up(team_bans)
            added_and_sorted = sorted(added.items(), key=lambda x: x[1], reverse=True)
            scored_bans.append(added_and_sorted)

        scored_bans.sort(key=lambda team: team[0][1], reverse=True)

        logging.debug(scored_bans)

        bans = Overwatch.BanList()
        team_ban_count = [0] * len(scored_bans)
        for i,t in snake_cycle(list(enumerate(scored_bans))):
            i = i % 2
            # Check if done banning, if yes break
            if len(set().union(*scored_bans)) == 0:
                break

            # if not, keep going
            try:
                b, s = t.pop(0)
                while bans.ban(b) == False:  # this need a try/except
                    logging.info("Candidate {} failed to be banned".format(b))
                    b, s = t.pop(0)
                team_ban_count[i] += 1
                logging.info("Team {} banned {} with {} votes".format(i +1, b, s))
            except IndexError:
                continue
            if team_ban_count[i] >= 2:
                t.clear()

        return bans


def __main__():
    """Main function to run the Overwatch ban simulation."""
    # Create a game of Overwatch
    game = Overwatch()

    # Create a lobby and initiate the ban phase
    final_bans = game.ban_phase()
    logging.debug(final_bans)
    print("Done!")


if __name__ == "__main__":
    __main__()