from pathlib import Path
import platform
import subprocess
import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor

toConvert:Path = Path('\\')

synoPath: str = sys.argv[1]

def get_file_names():
    response = requests.get('http://192.168.1.140:8080/getFile')
    data = response.json()
    if 'fileName' in data:
        return data['fileName']
    else:
        return None
      
def mark_file_finished(file_name):
    payload = {'fileName': file_name}
    response = requests.post('http://192.168.1.140:8080/setFinished', json=payload)
    if response.status_code == 200:
        print(f"File '{file_name}' marked as finished.")
    else:
        print(f"Failed to mark file '{file_name}' as finished.")

def process_file(file_name: str):
    isHecv: bool = False
    if "hecv" in file_name:
      isHecv = True
      
    fileNameParts: list[str] = file_name.split("\\film\\")
    
    if fileNameParts.__len__() == 1:
      fileNameParts = file_name.split("\\serie\\")
      fileNameParts[1] = "serie\\" + fileNameParts[1]
    else:
      
      fileNameParts[1] = "film\\" + fileNameParts[1]
      
    if platform.system() == "Windows":
        os_sep = "\\"
        if isHecv:
          command = 'ffmpeg -y -i "{}{}" -crf 23 -preset medium -c:v libx264 -c:a aac -b:a 128k "{}{}.mp4"'.format(synoPath.replace('/', os_sep), fileNameParts[1].replace('/', os_sep), synoPath.replace('/', os_sep), fileNameParts[1].split('.')[0].replace('/', os_sep))
        else:
          command = 'ffmpeg -y -i "{}{}" -c:v libx264 -c:a aac -strict experimental "{}{}.mp4"'.format(synoPath.replace('/', os_sep), fileNameParts[1].replace('/', os_sep), synoPath.replace('/', os_sep), fileNameParts[1].split('.')[0].replace('/', os_sep))
    else:
        os_sep = "/"
        if isHecv:
          command = 'ffmpeg -y -i "{}{}" -crf 23 -preset medium -c:v libx264 -c:a aac -b:a 128k "{}{}.mp4"'.format(synoPath.replace('\\', os_sep), fileNameParts[1].replace('\\', os_sep), synoPath.replace('\\', os_sep), fileNameParts[1].split('.')[0].replace('\\', os_sep))
        else: 
          command = 'ffmpeg -y -i "{}{}" -c:v libx264 -c:a aac -strict experimental "{}{}.mp4"'.format(synoPath.replace('\\', os_sep), fileNameParts[1].replace('\\', os_sep), synoPath.replace('\\', os_sep), fileNameParts[1].split('.')[0].replace('\\', os_sep))
     
     
    print(command)
    subprocess.run(command, shell=True)
    
    mark_file_finished(file_name)


def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        submitted_tasks = []
        
        done: bool = False

        while not done:
            while len(submitted_tasks) < 4:
                file_name = get_file_names()
                print(file_name)
                if file_name and file_name != 'done':
                    future = executor.submit(process_file, file_name)
                    submitted_tasks.append(future)
                
                if file_name == 'done':
                  done = True
                  break

            for task in submitted_tasks:
                if task.done():
                    submitted_tasks.remove(task)

            if not submitted_tasks:
                break
            
            time.sleep(1)

main()
