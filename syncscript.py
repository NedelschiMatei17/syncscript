import os
import shutil
import time
import hashlib
import sys


def get_hash(file_path):
    """Getting the MD5 hash of a file."""
    with open(file_path, 'rb') as f:
        hash = hashlib.md5()
        while 1>0:
            file_data = f.read(4096)
            if not file_data:
                break
            hash.update(file_data)
    return hash.hexdigest()

def sync_folders(src_folder_path, rep_folder_path, log_file):
    """Cloning the source folder as the replica folder."""

    if os.path.exists(rep_folder_path) == False:
        os.makedirs(rep_folder_path)

    print(f'Sync starting: {time.ctime()}')

    with open(log_file, 'a') as f:
        f.write(f'Sync starting: {time.ctime()}\n')

        for root, directories, files in os.walk(src_folder_path):
            rel_path = os.path.relpath(root, src_folder_path)
            rep_path = os.path.join(rep_folder_path, rel_path)

            # Create directories in replica folder if they don't exist
            for dir in directories:
                rep_dir = os.path.join(rep_path, dir)
                if not os.path.exists(rep_dir):
                    os.makedirs(rep_dir)
                    f.write(f'Created directory: {rep_dir}\n')
                    print(f'Created directory: {rep_dir}')

            # Replacing files in replica folder
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(rep_path, file)

                if os.path.exists(replica_file):
                    # Check if the file is the same as the one from the source folder
                    # Comparing the hash size
                    if get_hash(source_file) != get_hash(replica_file):
                        shutil.copy2(source_file, replica_file)
                        print(f'File replaced: {replica_file}')
                        f.write(f'File replaced: {replica_file}\n')
                        
                else:
                    shutil.copy2(source_file, replica_file)
                    print(f'Created file: {replica_file}')
                    f.write(f'Created file: {replica_file}\n')
                    

        # Remove extra files from replica folder in case those exist
        for root, files in os.walk(rep_folder_path):
            src_path = os.path.join(src_folder_path, relative_path)
            relative_path = os.path.relpath(root, rep_folder_path)
            
            for file in files:
                src_file = os.path.join(src_path, file)
                rep_file = os.path.join(root, file)
                
                if not os.path.exists(src_file):
                    os.remove(rep_file)
                    f.write(f'Removed file: {rep_file}\n')
                    print(f'Removed file: {rep_file}')

        f.write(f'Sync completed: {time.ctime()}\n\n')

    print(f'Sync completed: {time.ctime()}\n')

if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("Bad usage of the command(arguments < 5).")
        print("You should use the command like this:\n py syncscript.py src_folder_path rep_folder_path log_file_path interval")
        raise SystemExit()

    src_folder_path = sys.argv[1]
    rep_folder_path = sys.argv[2]
    log_file_path = sys.argv[3]
    time_interval = int(sys.argv[4])

    while 1 > 0:
        sync_folders(src_folder_path, rep_folder_path, log_file_path)
        time.sleep(time_interval)
