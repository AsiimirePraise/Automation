import os
import shutil

backup_destination="D:/desktop/Desktop/Backups"
name="backup"

folders_backup=[
#    'D:/desktop/Desktop/downloads',
#    'D:/desktop/Desktop/desktop2',
   'D:/desktop/Desktop/my documents',
]
backup_folder_name=f'{name}'
full_backup_path=os.path.join(backup_destination,backup_folder_name)

#create the backup destination if it doesnt exist
if not os.path.exists(backup_destination):
   os.makedirs(backup_destination)

os.makedirs(full_backup_path)

folders_backed_up=0

for folder in folders_backup:
  if os.path.exists(folder):
      folder_name=os.path.basename(folder)
      destination_path=os.path.join(full_backup_path,folder_name)
      
      try:
          shutil.copytree(folder, destination_path)
          print(f'Successfully backed up {folder_name}')
          folders_backed_up += 1
      except Exception as e:
          print(f'Error backing up {folder_name}: {e}')
  else:
      print(f'Folder not found: {folder}')

print(f'\nBackup complete!')
print(f'Total folders backed up: {folders_backed_up}')
print(f'Backup saved to: {full_backup_path}')