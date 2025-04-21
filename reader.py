# reader.py

from enum import Enum
import pandas as pd
import numpy as np

class Modo(Enum):
   ROW    = 0
   COLUMN = 1

class Tipo(Enum):
   NUM = 0
   TEXT = 1

def obtainRawTable(iFile: str, iSheet: str, iType = Tipo.NUM):
   with pd.ExcelFile(iFile) as xlsxFile:
      excelReader = pd.read_excel(xlsxFile, iSheet, index_col=0)
      if(Tipo.NUM == iType):
         table = np.zeros(excelReader.shape)
      else:
         table = [[""] * excelReader.shape[1]]  * excelReader.shape[0]
      nCol = 0
      for col in excelReader:
         nRow = 0
         for cell in excelReader[col]:
            if(pd.isna(cell)):
               table[nRow][nCol] = 0
            else:
               table[nRow][nCol] = cell
            nRow += 1
         nCol += 1
   return table

def normalize(oArray, iSearchMode = Modo.ROW):
   arraySum = np.sum(oArray)
   oArray = np.asmatrix(np.divide(oArray, arraySum))

   if(Modo.ROW == iSearchMode):
      return oArray
   else:
      return np.transpose(oArray)

def searchInTable(iFile: str, iSheet: str,
                  iParamToSearch, iMode = Modo.ROW, iType = Tipo.NUM):
   with pd.ExcelFile(iFile) as xlsxFile:
      excelReader = pd.read_excel(xlsxFile, iSheet, index_col=0)
      if(Modo.ROW == iMode):
         arraySize = len(excelReader.columns)
      else:
         arraySize = len(excelReader[iParamToSearch])
      
      if(Tipo.NUM == iType):
         array = np.zeros(arraySize)
      else:
         array = [""] * arraySize
      
      i = 0
      if(Modo.ROW == iMode):
         for col in excelReader:
            if(pd.isna(excelReader[col][iParamToSearch])):
               array[i] = 0
            else:
               array[i] = excelReader[col][iParamToSearch]
            i += 1
      else:
         for i in range(array.size):
            if(pd.isna(excelReader[iParamToSearch][i])):
               array[i] = 0
            else:
               array[i] = excelReader[iParamToSearch][i]
            i += 1
   
   if(Tipo.NUM == iType):
      return normalize(array, iMode)
   else:
      return array

def searchNameColumn(iFile: str, iSheet: str, iIndex: int):
   with pd.ExcelFile(iFile) as xlsxFile:
      excelReader = pd.read_excel(xlsxFile, iSheet, index_col=0)
      count = 0
      for col in excelReader:
         if(iIndex == count):
            return col
         else:
            count += 1
