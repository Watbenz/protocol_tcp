class Unit:
    def __init__(self, name, atk, max_hp):
        self.name = name
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

    def to_string(self):
        return '%s: %d/%d' % (self.name, self.hp, self.MAX_HP)


class GameObject:
    def __init__(self, item, typ):
        self.item = item
        self.typ = typ
