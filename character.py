# personaje.py

import math
import rules

class Character():

   name = ""
   abilityPoints = list() #P_A
   level = 1
   skillProficiencies = set() #H
   race = ""
   job = "" # Class
   background = ""
   roles = list()
   coefRoles = 0
   magic = list()
   modifiers = list()

   def obtainModifiers(self):
      intMod = []
      strMod = []
      for punt in self.abilityPoints:
         intMod.append(math.floor((punt / 2) - 5))
      for mod in intMod:
         if(mod < 0):
            strMod.append(str(mod))
         else:
            strMod.append('+' + str(mod))
      return strMod

   def __init__(self, iNombre, iRaza, iRol1, iRol2, iCoefRoles):
      self.name = iNombre
      self.race = iRaza
      self.roles = [iRol1, iRol2]
      if(iCoefRoles < 0):
         iCoefRoles = 0
      elif(iCoefRoles > 1):
         iCoefRoles = 1
      self.coefRoles = iCoefRoles

      import afinityFunctions as phi
      self.job = phi.obtainClass(self)
      self.abilityPoints = phi.obtainAbilityPoints(self)
      self.background = phi.obtainBackground(self)
      self.skillProficiencies = phi.obtainProficiencies(self)
      self.magic = phi.obtainMagic(self)

   def __str__(self):
      self.modifiers = self.obtainModifiers()
      abilityNames = rules.abilities()
      strReturn = "Nombre: " + self.name + "\n" +\
            "Raza: " + self.race + "\n" +\
            "Clase: " + self.job + "\n" +\
            "Trasfondo: " + self.background + "\n" +\
            "Nivel: " + str(self.level) + "\n" +\
            "Puntuaciones de característica: \n"
      for i in range(len(abilityNames)):
         strReturn += "- " + abilityNames[i] + ": " + \
            str(self.abilityPoints[i]) + " (" + self.modifiers[i] + ")\n"
      strReturn += "Habilidades competentes: \n"
      for hab in self.skillProficiencies:
         strReturn += "- " + hab + "\n"
      if(0 != len(self.magic)):
         strReturn += "Escuelas de magia: \n"
         for i in range(len(self.magic)):
            strReturn += "- " + self.magic[i] + "\n"

      return strReturn
               