from itertools import cycle
from ban_sim import *

import json
import pprint
import logging

# testing branch protection

logging.basicConfig(level=logging.DEBUG)

def add_em_up(team_ban_votes: list):
    vote_tally = {}
    for player_vote in team_ban_votes:
        score = 1
        player_vote.reverse()
        for v in player_vote:  # I don't understand why this is saying NoneType isn't iterable...
            if v in vote_tally:
                vote_tally[v] += score
            else:
                vote_tally[v] = score
            score += 1
    return vote_tally


class Overwatch(Game):
    def __init__(self):
        characters = []
        # Read the characters and their roles
        with open("Overwatch_Heroes.json", "r", encoding="utf-8") as f:
            for char in json.load(f):
                characters.append(Character(char["name"], char["role"]))
                super().__init__(characters, 5)

    class BanList(list):
        MAX_ROLE_BANS = 2
        def __init__(self):
            super().__init__()
            self._role_count = {}

        def ban(self, character: Character) -> bool:
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
        return self._teams

    def ban_phase(self):
        """
        Ask players to vote for their top 3 bans, and tally the votes
        Taking turns, each team nominates one character to ban from the tallied votes
        Banning continues until each team has banned 2 characters, or until there are no more valid nominees
        :return:
        """

        # Select and tally the votes
        scored_bans = []
        for team in self.lobby.teams:
            team_bans = [pl.pick_bans() for pl in team]
            added = add_em_up(team_bans)
            added_and_sorted = sorted(added.items(), key=lambda x: x[1], reverse=True)
            scored_bans.append(added_and_sorted)

        logging.debug(scored_bans)

        bans = Overwatch.BanList()
        team_ban_count = [0] * len(scored_bans)
        for i,t in cycle(enumerate(scored_bans)):
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
    # Create a game of Overwatch
    game = Overwatch()

    # Create a lobby and initiate the ban phase
    final_bans = game.ban_phase()
    logging.debug(final_bans)
    print("Done!")


if __name__ == "__main__":
    __main__()