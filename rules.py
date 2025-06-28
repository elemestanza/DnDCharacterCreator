# rules.py

from enum import Enum
import reader
import numpy as np

class Type(Enum):
   ABILITY = "característica"
   CLASS = "clase"
   RACE = "raza"
   BACKGROUND = "trasfondo"

abilities = ["Fuerza", "Destreza", "Constitución",
           "Inteligencia", "Sabiduría", "Carisma"]

skills = ["Atletismo", "Acrobacias", "Juego de Manos", "Sigilo", "Arcano",
           "Historia", "Investigación", "Naturaleza", "Religión", "Medicina",
           "Percepción", "Perspicacia", "Supervivencia", "Trabajo con animales",
           "Engañar", "Intimidación", "Interpretación", "Persuasión"]

races = ["Enano (de las Colinas)", "Enano (de las Montañas)", "(Alto) Elfo",
           "Elfo (de los Bosques)", "Elfo (Oscuro)", "Mediano (Piesligeros)",
           "Mediano (Fornido)", "Humano", "Dracónido", "Gnomo (del Bosque)",
           "Gnomo (de la Roca)", "Semielfo", "Semiorco", "Tiefling"]

roles = ["Control", "Sanación", "Daño a objetivo",
           "Daño en área", "Defensa", "Utilidad", "Soporte",
           "Cara a cara", "Erudición", "Exploración"]

def getAbilities():
   return abilities

def getAllSkills():
   return skills

def isRace(iRace: str):
   res = False
   if iRace in races:
      res = True
   return res

def getRandomRace():
   return races[np.random.randint(0, len(races))]

def isRole(iRole: str):
   res = False
   if iRole in roles:
      res = True
   return res

def getRandomRole(iOtherRole = ''):
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

def getSkills(iParam: Type, iData: str):
   sheet = 'Habilidades por ' + iParam.value
   skillsList = reader.searchInTable('.\Rules.xlsx',
                        sheet, iData, iType=reader.TextType.TEXT)
   if (0 != skillsList[0]):
      setAbilities = set(skillsList[0].split(', '))
      return setAbilities
   else: return set()

def getNumClassProficiencies(iClase: str):
   sheet = 'Habilidades por clase'
   listAbilities = reader.searchInTable('.\Rules.xlsx',
                        sheet, iClase, iType=reader.TextType.TEXT)
   return listAbilities[1]
