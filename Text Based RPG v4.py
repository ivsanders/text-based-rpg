#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Current version v3:
v1) player HP resets after combat. Enemy is not eliminated from the room after combat. Items do not have actual "usage"
v2) player HP does no reset after combat (thanks to Bapak Fananda)
v3) Enemy "eliminated" from room after each combat
v4) Keys can unlock doors, gone after one usage


Target for next version:
1. Enemy appearance is a random encounter with a predetermined chance
2. Item has actual usage such as increasing damage dealt, or healing player HP


"""


def showInstructions():
  #print a main menu and the commands
  print('''
Dark Labyrinth
========
You woke up in a prison cell and now must escape the labyrinth. Get to the Garden!
Beware of the Monsters!

Commands:
  go [direction] (e.g. south, west, north, east)
  get [item]
''')

def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Inventory : ' + str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  print("---------------------------")

#an inventory, which is initially empty
inventory = []

#a dictionary to list down the rooms, and what is in each room
rooms = {

            'Prison Cell'      : { 
                  'east'      : {'destination' : 'Prison Hallway',
                                 'requirement' : 'none'}
                },

            'Prison Hallway'  : {
                  'west'      : {'destination' : 'Prison Cell',
                                 'requirement' : 'none'},
                  'south'     : {'destination' : 'Torture Chamber',
                                 'requirement' : 'none'},
                  'east'      : {'destination' : 'Hallway',
                                 'requirement' : 'key'},
                  'north'     : {'destination' : 'Guard Room',
                                 'requirement' : 'none'}
                },
    
            'Torture Chamber' : {
                  'north'     : {'destination' : 'Prison Hallway',
                                 'requirement' : 'none'},
                  'item'      : 'key',
                  'encounter' : 'Monster'
                },
    
            'Guard Room'      : {
                  'south'     : {'destination' : 'Prison Hallway',
                                 'requirement' : 'none'},
                  'item'      : 'sword'
                },
    
            'Hallway'         : {
                'west'        : {'destination' : 'Prison Hallway',
                                 'requirement' : 'none'},
                'south'       : {'destination' : 'Reception Hall',
                                 'requirement' : 'none'},
                'east'        : {'destination' : 'Dining Room',
                                 'requirement' : 'none'}
                },
    
            'Dining Room'     : {
                'west'        : {'destination' : 'Hallway',
                                 'requirement' : 'none'},
                'south'       : {'destination' : 'Garden',
                                 'requirement' : 'key'},
                'encounter'   : 'Monster'
                },
    
            'Reception Hall'  : {
                'north'       : {'destination' : 'Hallway',
                                 'requirement' : 'none'},
                'east'        : {'destination' : 'Garden',
                                 'requirement' : 'key'},
                'item'        : 'key'
                },
    
            'Garden'          : {
                'north'       : {'destination' : 'Dining Room',
                                 'requirement' : 'none'},
                'west'        : {'destination' : 'Reception Hall',
                                 'requirement' : 'none'},
                'south'       : {'destination' : 'Exit',
                                 'requirement' : 'none'},
                'encounter'   : 'Monster'
                },
    
            'Exit'            : {
                'north'       : {'destination' : 'Garden',
                                 'requirement' : 'none'}
            }
            

         }


#combat encounter

def combat(player_hp=100):
    from random import randint
    
    cpu_hp = 10
    while player_hp > 0 or cpu_hp > 0:
        player = input("rock (r), paper (p), scissors (s)?")
        cpu_choice = randint(1,3)
        if   cpu_choice == 1:
             cpu = "r"
        elif cpu_choice == 2:
             cpu = "p"
        else:
             cpu = "s"
        print("player", player, "vs", cpu, "cpu")
        if player == cpu:
            result = "draw"
            print("it's a draw")
        elif player == "r" and cpu == "p":
            result = "defeat"
        elif player == "r" and cpu == "s":
            result = "victory"
        elif player == "p" and cpu == "r":
            result = "victory"
        elif player == "p" and cpu == "s":
            result = "defeat"
        elif player == "s" and cpu == "p":
            result = "victory"
        elif player == "s" and cpu == "r":
            result = "defeat"
        if result == "defeat":
            damage = randint(15,30)
            player_hp = player_hp - damage
            print("you take", damage, "points of damage")
            print("player hp", player_hp)
            print("cpu hp", cpu_hp)
        elif result == "victory":
            damage = randint(15,30)
            cpu_hp = cpu_hp - randint(15,30)
            print("you dealt", damage, "points of damage")
            print("player hp", player_hp)
            print("cpu hp", cpu_hp)
        if player_hp < 1:
            print("You are dead and shall be forgotten")
            global player_status
            player_status ='dead'
            break
        if cpu_hp <1:
            print("You won!")
            break
    return player_hp

#start the player in the Prison Cell
currentRoom = 'Prison Cell'
player_status = ''
player_hp=100 #initial hp

showInstructions()



#loop forever
while True:
     
      showStatus()
    
      #get the player's next 'move'
      #.split() breaks it up into an list array
      #eg typing 'go east' would give the list:
      #['go','east']

      move = ''
      while move == '':  
        move = input('>')
        
      move = move.lower().split()
    
      #if they type 'go' first
      if move[0] == 'go':
        #check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            if rooms[currentRoom][move[1]]['requirement'] == 'none':
                #set the current room to the new room
                currentRoom = rooms[currentRoom][move[1]]['destination']
                #there is no door (link) to the new room
            else:
                if 'key' in inventory:
                    if move[1] in rooms[currentRoom]:
                        #set the current room to the new room
                        currentRoom = rooms[currentRoom][move[1]]['destination']
                        #there is no door (link) to the new room
                        inventory.remove('key')
                    else:
                        print('You need a key for that')
        else:
            print('You  can\'t go that way!')
            
    
      #if they type 'get' first
      if move[0] == 'get' :
        #if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
          #add the item to their inventory
          inventory += [move[1]]
          #display a helpful message
          print(move[1] + ' got!')
          #delete the item from the room
          del rooms[currentRoom]['item']
        #otherwise, if the item isn't there to get
        else:
          #tell them they can't get it
          print('Can\'t get ' + move[1] + '!')
      
      #if there is an enemy in the room
      if 'encounter' in rooms[currentRoom] and 'Monster' in rooms[currentRoom]['encounter']:
        print('A wild monster appears! It attacks you!')
        player_hp = combat(player_hp) #update initial hp by return function
        #delete the monster from the after combat
        del rooms[currentRoom]['encounter']
            
    
      #if player reaches exit
      if currentRoom == 'Exit':
        print('You escaped the house... YOU WIN!')
        break
        
      #if you are dead
      if player_status == 'dead':
        print('You have been slain.')
        break


# In[ ]:





# In[ ]:




