#----------------IMPORTS-----------------
from ast import While
import random
from os import system, name
from time import sleep

#-------------GAME CLASSSES--------------

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class Units:
    def __init__(self):
        self.head = None
        self.teil = None

    def iter(self):
        current = self.head
        while current:
            item_val = current
            current = current.next
            yield item_val

    def add(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

    def killhead(self):
        if self.head != None:
            temp = self.head
            self.head = self.head.next
            temp = None
            if self.head != None:
                self.head.prev = None


class Unit:
    def __init__(self, tile, name, health, damage):
        self.tile = tile
        self.name = name
        self.health = health
        self.damage = damage

#----------------GLOBALS-----------------

player = "Anonymous"
message_list = []
tiles = ["You","","","","","","","","","Enemy"]
player_gold = 15
enemy_gold = 10
player_health = 100
enemy_health = 100
message = ""
player_units = Units()
enemy_units = Units()

def zero_game():
    global message_list
    global tiles
    global player_gold
    global enemy_gold
    global player_health
    global enemy_health
    global message
    global player_units
    global enemy_units
    message_list.clear()
    tiles = ["You","","","","","","","","","Enemy"]
    player_gold = 10
    enemy_gold = 10
    player_health = 100
    enemy_health = 100
    message = ""
    player_units = False
    enemy_units = False
    player_units = Units()
    enemy_units = Units()

#-------------GAME FUNCTIONS--------------

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def new_game(player):
    clear()
    zero_game()
    print("Hello", player, ", please choose game difficulty.")
    print("(select difficulty by giving number between 20-100)")
    print("(you can give any number but anything under 20 is for practice purposes and anyting near 100 and over is unbeatable)")
    global difficulty
    global player_gold
    global enemy_gold
    difficulty = int(input("?"))
    player_gold = player_gold - difficulty//10
    enemy_gold = enemy_gold + difficulty//5


def draw_gameboard():
    print("Your gold ", player_gold, "                                                                                                                            Enemy gold", enemy_gold)
    print("Fortress",player_health,"         1               2             3              4              5              6              7              8       Enemy Castle",enemy_health)
    print("┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐")
    print("│", end="")
    current = player_units.head
    for i in range(10):
        string = "              "
        for current in player_units.iter():
            if current and current.value.tile == i:
                unit_name = current.value.name
                unit_health = str(current.value.health)
                current = current.next
                string = unit_name + " " * (6-len(unit_name)) + " " + unit_health + " " * (7-len(unit_health))
                break
        print(string, end="│")

    print("")
    print("│", end="")

    current = enemy_units.head
    for i in range(10):
        if current and current.value.tile == i:
            unit_name = current.value.name
            unit_health = str(current.value.health)
            current = current.next
            string = unit_name + " " * (7-len(unit_name)) + " " + unit_health + " " * (6-len(unit_health))
            print(string, end="│")
        else:
            string = "              "
            print(string, end="│")

    print("")
    print("├──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤")
    
    print("│", end="")
    for i in range(10):
        print(" " * 6 , str(i) + " " * 6, end="│" )
    print("")
    
    print("│", end="")
    for i in range(10):
        print(" " * 4 , tiles[i] + " " * (9-len(tiles[i])), end="│" )
    print("")
    print("└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘")

def welcome():
    print("Hello traveller. What art thou name ?")
    print(
        "(please give your name to start new game or type Q to exit")
    global player
    player = input("?").title()
    if player == "Q":
        exit()

    new_game(player)

def player_advance():
    # iter tru units to see if their current and next tile is empty then advance
    if player_units != None:  # first check if player has any units
        for current_unit in player_units.iter():  # iter tru all players units
            if enemy_units.head != None:  # check if enemy has any units
                for current_enemy_unit in enemy_units.iter():  # iter tru all enemys units
                    if current_enemy_unit.value.tile == current_unit.value.tile:  # check if enemys units is in the same tile
                        break
                    else:  # enemy has units but not in same tile this unit can advance
                        if current_unit.prev != None:  # check if player onw has other unit in front
                            # check if player own unit is bloclking the way
                            if current_unit.value.tile + 1 != current_unit.prev.value.tile and current_unit.value.tile != 9:
                                current_unit.value.tile += 1
                                add_message(
                                    "Your unit", current_unit.value.name, "advanced")
                                break
                        else:
                            current_unit.value.tile += 1
                            add_message(
                                "Your unit", current_unit.value.name, "advanced")
                            break
            else:  # enemy does not have any units so this unit can advance
                if current_unit.prev != None:  # check if player has onw  other unit in front
                    # check if player own unit is bloclking the way
                    if current_unit.value.tile + 1 != current_unit.prev.value.tile and current_unit.value.tile != 9:
                        current_unit.value.tile += 1
                        continue
                elif current_unit.value.tile != 9:
                    current_unit.value.tile += 1
                    add_message(
                        "Your unit", current_unit.value.name, "advanced")
                    continue


def enemy_advance():
    # iter tru units to see if their current and next tile is empty then advance
    if enemy_units != None:  # check if enemy has units
        for current_enemy_unit in enemy_units.iter():  # go tru enemy units one at the time
            if player_units.head != None:  # check if player has any units to block the way
                for current_unit in player_units.iter():  # go tru player units
                    if current_unit.value.tile == current_enemy_unit.value.tile:  # check if player unit in the same tile
                        break
                    else:
                        if current_enemy_unit.prev != None:  # check if enemys onw has other unit in front
                            # check if enemys onw unit blocking the way
                            if current_enemy_unit.value.tile - 1 != current_enemy_unit.prev.value.tile and current_enemy_unit.value.tile != 0:
                                current_enemy_unit.value.tile -= 1
                                add_message(
                                    "Enemy unit", current_enemy_unit.value.name, "advanced")
                                break
                        else:
                            current_enemy_unit.value.tile -= 1
                            add_message(
                                "Enemy unit", current_enemy_unit.value.name, "advanced")
                            break
                
            else:  # player does not have any units
                if current_enemy_unit.prev != None:  # check if enemys onw has other unit in front
                    # check if enemys onw unit blocking the way
                    if current_enemy_unit.value.tile - 1 != current_enemy_unit.prev.value.tile and current_enemy_unit.value.tile != 0:
                        current_enemy_unit.value.tile -= 1
                        add_message(
                            "Enemy unit", current_enemy_unit.value.name, "advanced")
                        continue
                elif current_enemy_unit.value.tile != 0: # player had no units plus enymys own unist aint blocking the way
                    current_enemy_unit.value.tile -= 1
                    add_message(
                        "Enemy unit", current_enemy_unit.value.name, "advanced")
                    continue

def player_attack():
    # check if players head unit currently in same tile as the emeny
    if player_units.head != None:
        current_unit = player_units.head
        for current_enemy_unit in enemy_units.iter():
            if current_enemy_unit.value.tile == current_unit.value.tile:
                add_message("Your unit", current_unit.value.name, "takes a swing at",
                            current_enemy_unit.value.name, "in the tile", current_unit.value.tile)
                current_enemy_unit.value.health -= current_unit.value.damage
                return
        if current_unit.value.tile == 9:
            add_message("Your unit", current_unit.value.name, "bombards the enemy's castle!")
            global enemy_health
            enemy_health -= current_unit.value.damage
        else: add_message("No player's attack this round")


def enemy_attack():
    # check if players head unit currently in same tile as the emeny
    if enemy_units.head != None:
        current_enemy_unit = enemy_units.head
        for current_unit in player_units.iter():
            if current_unit.value.tile == current_enemy_unit.value.tile:
                add_message("Enemy unit", current_enemy_unit.value.name, "takes a swing at",
                            current_unit.value.name, "in the tile", current_enemy_unit.value.tile)
                current_unit.value.health -= current_enemy_unit.value.damage
                return
        if current_enemy_unit.value.tile == 0:
            add_message("Enemy unit", current_enemy_unit.value.name, "bombards your castle!")
            global player_health
            player_health -= current_enemy_unit.value.damage
        else: add_message("No enemy's attack this round")


def check_health():
    if enemy_units.head != None:
        if int(enemy_units.head.value.health) <= 0:
            add_message(
                "Enemy unit", enemy_units.head.value.name, "was slain!")
            enemy_units.killhead()

    if player_units.head != None:
        if int(player_units.head.value.health) <= 0:
            add_message(
                "Your unit", player_units.head.value.name, "was slain!")
            player_units.killhead()

    if player_health <= 0:
        enemywins()
    
    if enemy_health <= 0:
        playerwins()


def check_tiles():
    if player_units != None:
        for current_unit in player_units.iter():
            if current_unit.value.tile != 9:
                global tiles
                tiles[current_unit.value.tile] = "You"

    if enemy_units != None:  # check if enemy has units
        for current_enemy_unit in enemy_units.iter():  # go tru player units
            if current_enemy_unit.value.tile != 0:
                tiles[current_enemy_unit.value.tile] = "Enemy"

def gather_gold():
    global tiles
    global player_gold
    global enemy_gold
    player_gold_temp = 0
    enemy_gold_temp = 0
    player_tiles_count = 0
    enemy_tiles_count = 0
    for i in range(10):
        if tiles[i] == "You":
            player_gold_temp += 1
            player_tiles_count += 1
        elif tiles[i] == "Enemy":
            enemy_gold_temp += 1
            enemy_tiles_count += 1
    add_message("You collected", player_gold_temp, "gold, form your", player_tiles_count, "tiles")
    player_gold += player_gold_temp
    add_message("Enemy collected", enemy_gold_temp, "gold, form ", enemy_tiles_count,"tiles")
    enemy_gold += enemy_gold_temp

def add_message(*arg):
    global message_list
    message_list.append("")
    for a in arg:
        message_list[len(message_list)-1] += " " + str(a)


def print_messages():
    global message_list
    print("----- JOURNAL -----")
    for item in message_list:
        print("*",item)
    message_list.clear()


def add_unit():
    global player_gold
    print("(1 - Troll for 20 gold)")
    print("(2 - Ogre for 10 gold)")
    print("(3 - Goblin for 5 gold)")
    print("(0 - Cancel)")
    user_input = input("Choise ? ")
    if user_input == "1" and player_gold >= 20:
        add_player_unit = Unit(0, "Troll", 30, 10)
        cost = 20
    elif user_input == "2" and player_gold >= 10:
        add_player_unit = Unit(0, "Ogre", 10, 5)
        cost = 10
    elif user_input == "3" and player_gold >= 5:
        add_player_unit = Unit(0, "Goblin", 5, 1)
        cost = 5
    elif user_input == "1" or user_input == "2" or user_input == "3":
        print("Not Enough Gold!")
        return
    else:
        print("Not a unit")
        return
    player_units.add(add_player_unit)
    player_gold -= cost
    add_message("Player puchased unit ",
                add_player_unit.name, "for", cost, "gold")
    clear()
    draw_gameboard()
    print_messages()

def playerwins():
    clear()
    print("Congratulations you have WON and the cruel enemy has been defeated!")
    user_input = input("Play Again? (Y)es for new game (N)o to quit").lower()
    if user_input == "y": new_game(player)
    else: 
        print("Farewell!",player)
        exit()

def enemywins():
    clear()
    print("You have been defeated and your hordes exiled to the wilderness!")
    user_input = input("Gather your toops and play again? (Y)es for new game (N)o to quit").lower()
    if user_input == "y": new_game(player)
    else: 
        print("Farewell!",player) 
        exit()

def enemy_move():
    global difficulty
    global enemy_gold
    if enemy_gold >= 5:
        probability = random.randint(0, 100)
        if probability<= difficulty:
            if enemy_units.head == None:
                while True:
                    choise = random.randint(1,3)
                    if enemy_gold >= 25:
                        add_enemy_unit = Unit(9, "Paladin", 30, 10)
                        cost = 20
                        break
                    elif enemy_gold >= 15:
                        add_enemy_unit = Unit(9, "Knight", 10, 5)
                        cost = 10
                        break
                    elif choise == 1 and enemy_gold >= 20:
                        add_enemy_unit = Unit(9, "Paladin", 30, 10)
                        cost = 20
                        break
                    elif choise == 2 and enemy_gold >= 10:
                        add_enemy_unit = Unit(9, "Knight", 10, 5)
                        cost = 10
                        break
                    elif choise == 3 and enemy_gold >= 5:
                        add_enemy_unit = Unit(9, "Footmen", 5, 1)
                        cost = 5
                        break
                enemy_units.add(add_enemy_unit)
                enemy_gold -= cost
                add_message("Enemy dispached unit", add_enemy_unit.name, "for", cost, "gold")

            elif enemy_units.head != None:
                if enemy_units.tail.value.tile != 9:
                    while True:
                        choise = random.randint(1,3)
                        if enemy_gold >= 25:
                            add_enemy_unit = Unit(9, "Paladin", 30, 10)
                            cost = 20
                            break
                        elif enemy_gold >= 15:
                            add_enemy_unit = Unit(9, "Knight", 10, 5)
                            cost = 10
                            break
                        if choise == 1 and enemy_gold >= 20:
                            add_enemy_unit = Unit(9, "Paladin", 30, 10)
                            cost = 20
                            break
                        elif choise == 2 and enemy_gold >= 10:
                            add_enemy_unit = Unit(9, "Knight", 10, 5)
                            cost = 10
                            break
                        elif choise == 3 and enemy_gold >= 5:
                            add_enemy_unit = Unit(9, "Footmen", 5, 1)
                            cost = 5
                            break
                    enemy_units.add(add_enemy_unit)
                    enemy_gold -= cost
                    add_message("Enemy dispached unit", add_enemy_unit.name, "for", cost, "gold")

#-----------------GAME STARTS HERE---------------

clear()
welcome()
clear()
draw_gameboard()

while True:
    print("(1 - Buy unit) | (Enter - Next turn) | (0 - Quit Game)",end=" | your choise = ")

    user_input = input("")
    if user_input == "0":
        break
    elif user_input == "1":
        if player_units.head == None:
            add_unit()
        elif player_units.head != None:
            if player_units.tail.value.tile != 0:
                add_unit()
            else:
                add_message("Cannot recruit unit, tile occupied")
                clear()
                draw_gameboard()
                print_messages()

    else:
        enemy_move()
        player_advance()
        enemy_advance()
        check_tiles()
        player_attack()
        enemy_attack()
        check_health()
        check_tiles()
        gather_gold()
        clear()
        draw_gameboard()
        print_messages()
