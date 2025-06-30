#python script
import os 
import shutil


#define the path to the directory(download) we are to manage
download_dir="D:/desktop/Desktop/downloads"

#define a path to the destination(target) folders for different file types
target_folders={
    'images':['.jpg','.jpeg','.png','.gif'],
    'archives':['.zip','.rar','.tar'],
    'documents': ['.pdf', '.docx', '.txt', '.xlsx','.csv'],
    'videos': ['.mp4', '.avi', '.mov'],
    'audio': ['.mp3', '.wav', '.flac'],
    'scripts': ['.py', '.sh', '.js'],
    'installers': ['.exe', '.msi'],
    'others': []
}

#create target folders if they dont exist

for folder in target_folders:
   folder_path=os.path.join(download_dir,folder)
   if not os.path.exists(folder_path):
       os.makedirs(folder_path)

# iterate through the files in the downloads
for filename in os.listdir(download_dir):
    file_path=os.path.join(download_dir,filename)
    
    #skip directories
    if os.path.isdir(file_path):
        continue
    
    #check file extension and move to it to the appropriate folder
    for folder , extensions in target_folders.items():
        if any(filename.lower().endswith(ext) for ext in extensions):
            target_folder=os.path.join(download_dir,folder)
            shutil.move(file_path,target_folder)
            print(f'moved {filename} to {target_folder}')

