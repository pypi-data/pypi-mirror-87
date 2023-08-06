'''
Created on 10 mai 2020

@author: olivier
'''

import os, os.path

class File(object):
  '''
  Simple port of java.io.File
  '''

  def __init__(self, *args):
    '''
    Constructor
    '''
    self.__canonPath = args[0] if args[0] else ''
      
 
  
  def getName(self):
    lastSep = self.__canonPath.rfind(os.sep)
    return self.__canonPath[lastSep+1:] if lastSep>0 else self.__canonPath
  
  def getCanonicalPath(self):
    return self.__canonPath
  
  def exists(self):
    return os.path.exists(self.__canonPath)
    
  def isFile(self):
    return os.path.isfile(self.__canonPath)
