# fAfinidad.py

from character import Character
import numpy as np
import reader
import rules

from gekko import GEKKO

# OBTENER CLASE (S01)
def obtainClass(iPj: Character):
   # S01.1
   phiS1C = reader.searchInTable('.\Tablas.xlsx', 'phi(S,C)', iPj.roles[0])
   # S01.2
   phiS2C = reader.searchInTable('.\Tablas.xlsx', 'phi(S,C)', iPj.roles[1])
   # S01.3
   phiRC = reader.searchInTable('.\Tablas.xlsx', 'phi(R,C)', iPj.race)

   sumC = iPj.coefRoles * phiS1C + (1 - iPj.coefRoles) * phiS2C + phiRC
   maxC = sumC.max()
   indexC = np.where(sumC == maxC)[1][0]

   return reader.searchNameColumn('.\Tablas.xlsx', 'phi(R,C)', indexC)

# OBTENER PUNTUACIONES CARACTERISTICA (S02)
def obtainAbilityPoints(iPj: Character):
   # FAux.1
   kappaCA = reader.searchInTable('.\Tablas.xlsx', 'kappa(C,A)', iPj.job)
   # FAux.2
   rhoRA = reader.searchInTable('.\Tablas.xlsx', 'rho(R,A)', iPj.race)

   var = 27 - rhoRA.sum()
   phiRCA = var * kappaCA + rhoRA
   phiRCA = phiRCA.A[0]

   # Corrección de decimales
   if(sum(phiRCA) > 27):
      sobrante = sum(phiRCA) - 27
      for i in range(6):
         phiRCA[i] -= sobrante / 6

   # Solucionamos el problema de minimización
   # MILP (Mixed-Integer Linear Programming)
   m = GEKKO()
   m.options.SOLVER = 1

   phiGekko = m.Array(m.Const, 6)
   for i in range(6):
      phiGekko[i].value = phiRCA[i]
   
   x = m.Array(m.Var, 6, integer=True, lb=0, ub=9)
   for i in range(6):
      x[i] = m.sos1([0, 1, 2, 3, 4, 5, 7, 9])
      m.Minimize(m.abs((phiGekko[i] - x[i])))
   
   m.Equation(sum(x) == 27)
   m.solve(disp=False)

   costes = [int(x[i].value[0]) for i in range(6)]

   # Pasamos los costes a puntuaciones
   puntuaciones = []
   for coste in costes:
      if(9 == coste):
         puntuaciones.append(15)
      elif(7 == coste):
         puntuaciones.append(14)
      else:
         puntuaciones.append(coste + 8)

   # Caso especial con semielfos
   if("Semielfo" == iPj.race):
      puntRestante = 2
      auxPuntuaciones = puntuaciones.copy()
      auxPuntuaciones[5] = 100 # No puede escogerse carisma
      while(puntRestante != 0):
         puntElegido = min(auxPuntuaciones)
         indiceElegido = auxPuntuaciones.index(puntElegido)
         auxPuntuaciones[indiceElegido] = 100

         puntuaciones[indiceElegido] += 1
         puntRestante -= 1
   
   # Añadimos los puntos que otorga la raza
   for i in range(0, 6):
      puntuaciones[i] += int(round(rhoRA.A[0][i]))
   return puntuaciones

# OBTENER TRASFONDO (S03)
def obtainBackground(iPj: Character):
   # S03.1
   phiCT = reader.searchInTable('.\Tablas.xlsx', 'phi(C,T)', iPj.job)
   # S03.2
   phiRT = reader.searchInTable('.\Tablas.xlsx', 'phi(R,T)', iPj.race)
   
   sumT = phiCT + phiRT
   maxT = sumT.max()
   indexT = np.where(sumT == maxT)[1][0]

   return reader.searchNameColumn('.\Tablas.xlsx', 'phi(R,T)', indexT)

# OBTENER HABILIDADES (S11)
def obtainProficiencies(iPj: Character):
   # Un pj tiene las habilidades que da trasfondo y raza
   setAbilities = rules.getSkills(rules.Type.BACKGROUND, iPj.background).union(
                  rules.getSkills(rules.Type.RACE, iPj.race))
   
   # Obtenemos las habilidades que podemos escoger
   abilitiesToChoose = rules.getSkills(rules.Type.CLASS, iPj.job)
   abilitiesToChoose.difference_update(setAbilities)
   nAbilitiesToChoose = rules.getNumClassProficiencies(iPj.job)

   rolesForProficiencies = ["Cara a cara", "Erudición", "Exploración", "Utilidad"]
   etaSH = []
   for rol in iPj.roles:
      if (rol in rolesForProficiencies):
         etaSH.append(reader.searchInTable('.\Tablas.xlsx', 'eta(S,H)', rol))

   etaSH = reader.normalizeArray(etaSH).A[0]
   pointsAbilitesNorm = reader.normalizeArray(iPj.abilityPoints).A[0]

   caract = rules.getAbilities()
   phiNotZeroH = []
   for i in range(len(caract)):
      hab = rules.getSkills(rules.Type.ABILITY, caract[i])
      for h in hab:
         phiNotZeroH.append(pointsAbilitesNorm[i])

   if(1 == len(etaSH)):
      phiNotZeroH += etaSH[0]
   elif(2 == len(etaSH)):
      phiNotZeroH = phiNotZeroH + iPj.coefRoles * etaSH[0] + (1 - iPj.coefRoles) * etaSH[1]
   
   phiNotZeroH = reader.normalizeArray(phiNotZeroH).A[0]

   # Habilidad que no podemos seleccionar -> phiH(hablidad) = 0
   dictPhiH = {rules.getAllSkills()[i]: phiNotZeroH[i] for i in range(len(phiNotZeroH))}
   notAbilitiesToChoose = set(rules.getAllSkills()).difference(abilitiesToChoose)
   for hab in notAbilitiesToChoose:
      dictPhiH[hab] = 0
   phiH = list(dictPhiH.values())

   # Solucionamos el problema de maximización de elección de habilidades
   # MILP (Mixed-Integer Linear Programming)
   m = GEKKO()
   m.options.SOLVER = 1
   
   phiGekko = m.Array(m.Param, 18)
   for i in range(18):
      phiGekko[i].value = phiH[i]
   x = m.Array(m.Var, 18, integer=True, lb=0, ub=1)
   
   m.Maximize(m.sum(phiGekko * x))
   m.Equation(sum(x) == nAbilitiesToChoose)
   m.solve(disp=False)
   
   for i in range(18):
      if (1.0 == x[i].value[0]):
         setAbilities.add(rules.getAllSkills()[i])

   # Si la raza es semielfo, se escogen 2 hab adicionales de entre todas
   if ("Semielfo" == iPj.race):
      nAbilitiesToChoose = 2
      dictPhiH = {rules.getAllSkills()[i]: phiNotZeroH[i] for i in range(len(phiNotZeroH))}
      notAbilitiesToChoose = set(rules.getAllSkills()).difference(setAbilities)
      for hab in notAbilitiesToChoose:
         dictPhiH[hab] = 0
      phiH = list(dictPhiH.values())

      phiGekko = m.Array(m.Param, 18)
      for i in range(18):
         phiGekko[i].value = phiH[i]
      x = m.Array(m.Var, 18, integer=True, lb=0, ub=1)
      
      m.Maximize(m.sum(phiGekko * x))
      m.Equation(sum(x) == nAbilitiesToChoose)
      m.solve(disp=False)
      
      for i in range(18):
         if (1.0 == x[i].value[0]):
            setAbilities.add(rules.getAllSkills()[i])

   return setAbilities

# OBTENER ESCUELAS DE MAGIA (S12)
def obtainMagic(iPj: Character):
   magicClasses = ["Bardo", "Brujo", "Clérigo", "Druida",
                    "Explorador", "Hechicero", "Mago", "Paladín"]
   magicRoles = ["Control", "Sanación", "Daño a objetivo",
                 "Daño en área", "Defensa", "Utilidad", "Soporte"]
   
   if(not iPj.job in magicClasses):
      return []
   
   # S12.1
   phiCM = reader.searchInTable('.\Tablas.xlsx', 'phi(C,M)', iPj.job)

   # S12.2
   phiSM = []
   for rol in iPj.roles:
      if(rol in magicRoles):
         phiSM.append(reader.searchInTable('.\Tablas.xlsx', 'phi(S,M)', rol))
   
   sumM = phiCM
   if(1 == len(phiSM)):
      sumM += phiSM[0]
   elif(2 == len(phiSM)):
      sumM += iPj.coefRoles * phiSM[0] + (1 - iPj.coefRoles) * phiSM[1]
   
   sumM = sumM.A[0]

   maxM = sumM.max()
   indexM = np.where(sumM == maxM)[0]

   sumM[indexM] = -1
   max2ndM = sumM.max()
   index2ndM = np.where(sumM == max2ndM)[0]

   return [reader.searchNameColumn('.\Tablas.xlsx', 'phi(C,M)', indexM),
           reader.searchNameColumn('.\Tablas.xlsx', 'phi(C,M)', index2ndM)]
