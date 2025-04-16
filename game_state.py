import random

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.coins = 20
        self.has_completed_one_lap = False
        self.on_mountain = False
        self.eliminated = False

class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.turn_index = 0
        self.mountain_occupants = []
        self.king_of_mountain = None
        self.message = ""

    def current_player(self):
        return self.players[self.turn_index]

    def next_turn(self):
        self.turn_index = (self.turn_index + 1) % len(self.players)
        # Skip eliminated players
        while self.players[self.turn_index].eliminated:
            self.turn_index = (self.turn_index + 1) % len(self.players)

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player, steps):
        old_position = player.position
        player.position = (player.position + steps) % 32
        if player.position < old_position:
            player.has_completed_one_lap = True

    def climb_mountain(self, player):
        if player.has_completed_one_lap:
            player.on_mountain = True
            self.mountain_occupants.append(player)
            self.message = f"{player.name} climbs the mountain!"

    def handle_duels(self):
        # Mountain Duel
        if len(self.mountain_occupants) == 2:
            p1, p2 = self.mountain_occupants
            r1, r2 = self.roll_dice(), self.roll_dice()
            if r1 > r2:
                p1.coins += 10
                p2.coins -= 10
                self.king_of_mountain = p1
                p2.on_mountain = False
                self.mountain_occupants.remove(p2)
                p2.position = 0
                self.message = f"{p1.name} wins mountain duel ({r1} vs {r2})!"
            elif r2 > r1:
                p2.coins += 10
                p1.coins -= 10
                self.king_of_mountain = p2
                p1.on_mountain = False
                self.mountain_occupants.remove(p1)
                p1.position = 0
                self.message = f"{p2.name} wins mountain duel ({r2} vs {r1})!"
            else:
                self.message = f"Mountain duel tie ({r1} vs {r2}). Wait next round."

        # Regular duels
        positions = {}
        for p in self.players:
            if not p.eliminated and not p.on_mountain:
                positions.setdefault(p.position, []).append(p)
        for pos, players in positions.items():
            if len(players) > 1:
                p1, p2 = players[0], players[1]
                r1, r2 = self.roll_dice(), self.roll_dice()
                if r1 > r2:
                    p1.coins += 5
                    p2.coins -= 5
                    self.message = f"{p1.name} wins duel vs {p2.name} ({r1} vs {r2})"
                elif r2 > r1:
                    p2.coins += 5
                    p1.coins -= 5
                    self.message = f"{p2.name} wins duel vs {p1.name} ({r2} vs {r1})"
                else:
                    p1.coins -= 2
                    p2.coins -= 2
                    self.message = f"{p1.name} and {p2.name} tied ({r1}) — each lose 2 coins"

    def apply_king_tax(self):
        if self.king_of_mountain:
            for p in self.players:
                if not p.eliminated and not p.on_mountain:
                    p.coins -= 1
                    self.king_of_mountain.coins += 1

    def check_eliminations(self):
        for p in self.players:
            if not p.eliminated and p.coins <= 0:
                p.eliminated = True
                p.on_mountain = False
                if p in self.mountain_occupants:
                    self.mountain_occupants.remove(p)
                if p == self.king_of_mountain:
                    self.king_of_mountain = None
                self.message = f"{p.name} has been eliminated!"

    def check_winner(self):
        remaining = [p for p in self.players if not p.eliminated]
        if len(remaining) == 1:
            return remaining[0].name
        return None