import random

class Attack:
    def __init__(self, name, damage, stamina_cost):
        self.name = name
        self.damage = damage
        self.stamina_cost = stamina_cost

class Character:
    def __init__(self, name, hp, stamina, attacks):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_stamina = stamina
        self.stamina = stamina
        self.attacks = attacks

    def is_alive(self):
        return self.hp > 0

    def regen_stamina(self, amount=20):
        self.stamina = min(self.max_stamina, self.stamina + amount)

    def take_damage(self, amount):
        self.hp = max(self.hp - amount, 0)

    def perform_attack(self, target, attack):
        if self.stamina < attack.stamina_cost:
            print(f"{self.name} tried to use {attack.name}, but didn't have enough stamina!")
            return

        # Only miss if not skip or heal
        if attack.name.lower() not in ["skip", "heal"]:
            miss_roll = random.random()
            if miss_roll < 0.10:
                print(f"{self.name} tries to use {attack.name}, but misses!")
                self.stamina -= attack.stamina_cost  # Still costs stamina
                return

        self.stamina -= attack.stamina_cost

        if attack.name.lower() == "skip":
            regen_amount = 15
            self.regen_stamina(15)
            print(f"{self.name} skips the turn and regains {regen_amount} stamina.")
            return

        if attack.damage < 0:
            healed = min(-attack.damage, self.max_hp - self.hp)
            self.hp += healed
            print(f"{self.name} uses {attack.name} and heals for {healed} HP!")
        else:
            target.take_damage(attack.damage)
            print(f"{self.name} uses {attack.name} and deals {attack.damage} damage to {target.name}!")


    def get_available_attacks(self):
        return [atk for atk in self.attacks if self.stamina >= atk.stamina_cost]

# Define attacks
fireball = Attack("Fireball 🔥", 15, 20)
the_sun = Attack("The sun ☀️", 60, 45)
heal = Attack("Heal ❤️‍🩹", -25, 25)
skip = Attack("Skip 🚫", 0, 0)
bite = Attack("Bite", 8, 4)
claw = Attack("Claw", 14, 10)
roar = Attack("Roar", 0, 0)

# Create player
player = Character("Hero", 115, 75, [fireball, the_sun, heal, skip])

# Create enemies
enemies = [
    Character("Goblin", 45, 20, [bite, claw]),
    Character("Orc", 70, 25, [claw, bite, roar]),
    Character("Dragon", 135, 75, [Attack("Fire Breath", 20, 30), Attack("Tail Swipe", 15, 20), Attack("Skip", 0, 0)]),
    Character("Phobos", 210, 165, [Attack("Smite", 20, 40), Attack("Fall", 50, 100)]),
]
