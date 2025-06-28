# reader.py

from enum import Enum
import pandas as pd
import numpy as np

class Mode(Enum):
   ROW    = 0
   COLUMN = 1

class TextType(Enum):
   NUM = 0
   TEXT = 1

def normalizeArray(oArray, iSearchMode = Mode.ROW):
   arraySum = np.sum(oArray)
   oArray = np.asmatrix(np.divide(oArray, arraySum))

   if(Mode.ROW == iSearchMode):
      return oArray
   else:
      return np.transpose(oArray)

def searchInTable(iFile: str, iSheet: str,
                  iParamToSearch, iMode = Mode.ROW, iType = TextType.NUM):
   with pd.ExcelFile(iFile) as xlsxFile:
      excelReader = pd.read_excel(xlsxFile, iSheet, index_col=0)
      if(Mode.ROW == iMode):
         arraySize = len(excelReader.columns)
      else:
         arraySize = len(excelReader[iParamToSearch])
      
      if(TextType.NUM == iType):
         array = np.zeros(arraySize)
      else:
         array = [""] * arraySize
      
      i = 0
      if(Mode.ROW == iMode):
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
   
   if(TextType.NUM == iType):
      return normalizeArray(array, iMode)
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
