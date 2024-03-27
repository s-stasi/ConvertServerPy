import os
from pathlib import Path


class FilesQueue:
  synologyPath: str = 'Z:\\'
  stringPaths: list[str]
  filesQueue: list[Path] = []
  workingOn: list[Path] = []
  
  def __init__(self) -> None:
    self.__scanVideos__()
    for path in self.filesQueue:
      pass
      #print(path)
    
  def __scanVideos__(self) -> None:
    for root, _, files in os.walk(self.synologyPath):
      for file in files:
        if file.endswith('avi') or file.endswith('hecv'):
          self.filesQueue.append(Path(os.path.join(root, file)))
          
  def getElement(self, ip: str) -> str:
    if len(self.filesQueue) > 0:
      element: Path = self.filesQueue.pop(0)
      self.workingOn.append(element)
      print(ip + ' is processing file: ' + element.__str__().split('\\')[::-1][0])
      return element
    
    return 'done'
  
  def setFinished(self, file: str) -> None:
    print('removing:  ' + file + '\n\n')
    for file in self.workingOn: 
      if file.__str__() == file:
        self.workingOn.remove(file)