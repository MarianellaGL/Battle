import random
from classes.game import Person, bcolors
from classes.inventory import Item
from classes.magic import Spell

fire = Spell("Fire", 100, 500, "black")
thunder = Spell("Thunder", 410, 1004, "black")
blizzard = Spell("Blizzard", 510, 10000, "black")
meteor = Spell("Meteor", 2000, 1004, "black")
quake = Spell("Quake", 1000, 3200, "black")

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 99999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of one party member", 99999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, blizzard, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 2},
                {"item": elixer, "quantity": 2}, {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 15}]

player1 = Person("Lilith   ", 46000, 850, 60, 84, player_magic, player_items)
player2 = Person("Christoph", 10060, 755, 60, 84, player_magic, player_items)
player3 = Person("Anabelle", 9000, 1000, 60, 84, player_magic, player_items)
enemy1 = Person("Vash    ", 12000, 755, 45, 64, enemy_spells, [])
enemy2 = Person("Lucile  ", 10200, 655, 45, 64, enemy_spells, [])
enemy3 = Person("Neulim  ", 11200, 6005, 45, 64, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("================")
    print("NAME:                        HP:                                      MP:")
    print("\n\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

        print("\n")
    for enemy in enemies:

        for player in players:
            player.get_stats()
            print("\n")
        for player in players:

            player.choose_action()
            choice = input("Choose action:")
            index = int(choice) - 1

            if index == 0:
                dmg = player.generate_damage()
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(dmg)

                print("You attacked " + enemies[enemy].name + "for " + str(dmg) + " pts of damage")

            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("Choice magic:")) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_dmg = spell.generate_damage()

                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if "white" == spell.type:
                    player.heal(magic_dmg)
                    print(bcolors.OKBLUE + "\n" + spell.name + "heals for ", str(magic_dmg), "HP." + bcolors.ENDC)
                elif spell.type == "black":

                    enemy = player.choose_target(enemies)

                    enemies[enemy].take_damage(magic_dmg)

                    print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg),
                          " points of damage to " + enemies[enemy].name + bcolors.ENDC)

            elif index == 2:
                player.choose_item()
                item_choice = int(input("Choice Item")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]
                item_quantity = player_items[item_choice]["quantity"]
                item_quantity -= 1

                if player.items[item_choice]["quantity"] == 0:
                    print(bcolors.FAIL + "\n" + "none left...." + bcolors.ENDC)
                    continue

                if item.type == "potion":
                    player.heal(item.prop)
                    print(bcolors.OKGREEN + "\n" + item.name + " heals for: ", str(item.prop), "HP" + bcolors.ENDC)
                elif item.type == "elixer":

                    if item.name == "MegaElixer":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + "Fully restores HP/MP:" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(item.prop)

                    print(bcolors.FAIL + "\n" + item.name + "deals for: ", str(item.prop),
                          " points of damage to " + enemies[enemy].name + bcolors.ENDC)
                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has died")
                        del enemies[enemy]

    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
    running = False

    for enemy in enemies:

        enemy_choice = 1
        target = random.randrange(0, 3)

        if enemy_choice == 0:

            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", " ") + "attacks " + player[target].name.replace(" ", "") + " for" + enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            print("Enemy choose: ", spell, "damage is ", magic_dmg)
