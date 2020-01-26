class Unit:
    def __init__(self, atk, max_hp):
        self.atk = atk
        self.MAX_HP = max_hp
        self.hp = max_hp
        self.status = 'alive'

    def lost_hp(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            self.status = 'died'

    def attack(self, unit):
        unit.lost_hp(self.atk)


class GameObject:
    def __init__(self, item, typ):
        self.item = item
        self.typ = typ
