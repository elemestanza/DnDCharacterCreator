# rules.py

from enum import Enum
import reader

class Tipo(Enum):
   ABILITY = "característica"
   CLASS = "clase"
   RACE = "raza"
   BACKGROUND = "trasfondo"

def obtainSkills(iParam: Tipo, iData: str):
   sheet = 'Habilidades por ' + iParam.value
   skillsList = reader.searchInTable('.\Rules.xlsx',
                        sheet, iData, iType=reader.Tipo.TEXT)
   if (0 != skillsList[0]):
      setAbilities = set(skillsList[0].split(', '))
      return setAbilities
   else: return set()

def obtainNumClassProficiencies(iClase: str):
   sheet = 'Habilidades por clase'
   listAbilities = reader.searchInTable('.\Rules.xlsx',
                        sheet, iClase, iType=reader.Tipo.TEXT)
   return listAbilities[1]

def abilities():
   return ["Fuerza", "Destreza", "Constitución",
           "Inteligencia", "Sabiduría", "Carisma"]

def skills():
   return ["Atletismo", "Acrobacias", "Juego de Manos", "Sigilo", "Arcano",
           "Historia", "Investigación", "Naturaleza", "Religión", "Medicina",
           "Percepción", "Perspicacia", "Supervivencia", "Trabajo con animales",
           "Engañar", "Intimidación", "Interpretación", "Persuasión"]

def races():
   return ["Enano (de las Colinas)", "Enano (de las Montañas)", "(Alto) Elfo",
           "Elfo (de los Bosques)", "Elfo (Oscuro)", "Mediano (Piesligeros)",
           "Mediano (Fornido)", "Humano", "Dracónido", "Gnomo (del Bosque)",
           "Gnomo (de la Roca)", "Semielfo", "Semiorco", "Tiefling"]

def roles():
   return ["Control", "Sanación", "Daño a objetivo",
           "Daño en área", "Defensa", "Utilidad", "Soporte",
           "Cara a cara", "Erudición", "Exploración"]