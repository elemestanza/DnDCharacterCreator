#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from character import Character
import numpy as np
import rules
import sys

def isRace(iRace: str):
   res = False
   if iRace in rules.races():
      res = True
   return res

def getRandomRace():
   races = rules.races()
   return races[np.random.randint(0, len(races))]

def isRole(iRole: str):
   res = False
   if iRole in rules.roles():
      res = True
   return res

def getRandomRole(iOtherRole = ''):
   roles = rules.roles()
   oRole = roles[np.random.randint(0, len(roles))]
   while oRole.__eq__(iOtherRole):
      oRole = roles[np.random.randint(0, len(roles))]
   return oRole

def isValidCoef(iCoef: float):
   res = False
   if(0 <= iCoef <= 1):
      res = True
   return res

def getRandomCoef():
   return np.random.rand()

def printHelp():
   print('USO:')
   print('     py main.py [name | teamSize | name race | name race role1 role2 coef]\n')
   print('donde')
   print('     [name]                        Crea un personaje con valores aleatorios.')
   print('     [teamSize]                    Crea un equipo de personajes con nombre y valores aleatorios.')
   print('     [name race]                   Crea un personaje con valores aleatorios excepto la raza.')
   print('     [name race role1 role2 coef]  Crea un personaje con valores definidos.\n')
   print('Ejemplos:')
   print('     > py main.py Elena')
   print('     > py main.py 4')
   print('     > py main.py Elena Tiefling')
   print('     > py main.py Elena "(Alto) Elfo" "Daño en área" Soporte 0.3')

def printError(numErr: int):
   strErr = 'ERROR: '
   match numErr:
      case 0:
         strErr.join('Invalid number of arguments')
      case 1:
         strErr.join('Not a race')
      case 2:
         strErr.join('Not a role')
      case 3:
         strErr.join('Invalid value for coef, must be in [0,1]')
      case 4: 
         strErr.join('Invalid value for teamSize, must be greater than 1')

if (sys.argv[1].__eq__('/?')):
   printHelp()
else:
   numArgs = len(sys.argv) - 1
   match numArgs:
      case 0:
         printHelp()
      case 1:
         # Team with Random Values
         if(sys.argv[1].isnumeric()):
            teamSize = int(sys.argv[1])
            if(teamSize <= 1):
               printError(4)
            else:
               characters = []
               for i in range(teamSize):
                  chName = 'PJ ' + str(i+1)
                  role1 = getRandomRole()
                  characters.append(Character(chName,
                                              getRandomRace(),
                                              role1,
                                              getRandomRole(role1),
                                              getRandomCoef()))
               for c in characters:
                  print(str(c))
         # Character with Random Values
         else:
            role1 = getRandomRole()
            character = Character(sys.argv[1],
                                  getRandomRace(),
                                  role1,
                                  getRandomRole(role1),
                                  getRandomCoef())
            print(str(character))
      case 2:
         # Character with name and race
         if not isRace(sys.argv[2]):
            printError(1)
         else:
            role1 = getRandomRole()
            character = Character(sys.argv[1],
                                  sys.argv[2],
                                  role1,
                                  getRandomRole(role1),
                                  getRandomCoef())
            print(str(character))
      case 5:
         # Character with Defined Values
         coef = float(sys.argv[5])
         if not isRace(sys.argv[2]):
            printError(1)
         elif not (isRole(sys.argv[3]) and isRole(sys.argv[4])):
            printError(2)
         elif not isValidCoef(coef):
            printError(3)
         else:
            character = Character(sys.argv[1],
                                  sys.argv[2],
                                  sys.argv[3],
                                  sys.argv[4],
                                  coef)
            print(str(character))
      case _:
         printError(0)