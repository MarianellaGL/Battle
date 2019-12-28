from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 100, "black")
quake = Spell("Quake", 10, 100, "black")

cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 99999)
hielixer = Item("MegaElixer", "elixer", "Fully restores HP/MP of one party member", 99999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_item = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
               {"item": superpotion, "quantity": 2},
               {"item": elixer, "quantity": 2}, {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 15}]

player = Person(460, 65, 60, 84, player_magic, player_item)
enemy = Person(1200, 65, 45, 64, [], [])

running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)

        print("You attacked for", dmg, "pts of damage. Enemy HP:", enemy.get_hp())
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
            print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == "black":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + "deals ," + str(magic_dmg), "points of damage" + bcolors.ENDC)
    elif index == 2:
        player.choose_item()
        item_choice = int(input("Choice Item")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]
        item_quantity = player_item[item_choice]["quantity"]
        item_quantity -= 1

        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\n" + "none left...." + bcolors.ENDC)
            continue

        player.items[item_choice]["quantity"] -= 1

        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + "heals for:", str(item.prop), "HP" + bcolors.ENDC)
        elif item.type == "elixer":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKGREEN + "\n" + item.name + "Fully restores HP/MP:" + bcolors.ENDC)
        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(bcolors.FAIL + "\n" + item.name + "deals for:", str(item.prop), "points of damage" + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("---------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)
    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC)
    print("Your MP:", bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False
