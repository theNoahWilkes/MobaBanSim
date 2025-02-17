from itertools import cycle

import random
import json
import pprint

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
        with open("Overwatch_Heroes.json", "r") as f:
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
        bans = Overwatch.BanList()
        scored_bans = []
        for team in self.lobby.teams:
            team_bans = [pl.pick_bans() for pl in team]
            added = add_em_up(team_bans)
            added_and_sorted = sorted(added.items(), key=lambda x: x[1], reverse=True)
            scored_bans.append(added_and_sorted)

        pprint.pprint(scored_bans)

        # This isn't quite working how I'd like it.  If one team exhausts their list of bans in their "turn"
        # the break will stop the whole banning process.  For a small number of total bans (ie 4) this is probably fine
        # But it's possible this could result in too few bans being created.
        # TODO:  Make it so that if a team runs out of bans, the other team(s) can still use their bans.
        # Maybe instead a checker condition outside of the cycle call, that will break when both teams have exhausted their options

        for t in cycle(scored_bans):
            b, s = t.pop(0)
            print("Testing candidate {} with {} votes from team {}".format(b, s, t))
            try:
                while bans.ban(b) == False:  # this need a try/except
                    b, s = t.pop(0)
            except IndexError:
                continue
        return bans


def __main__():
    # Create a game of Overwatch
    game = Overwatch()

    # Create a lobby and initiate the ban phase
    print(game.ban_phase())


if __name__ == "__main__":
    __main__()