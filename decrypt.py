from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os
from rich.progress import Progress, track
from multiprocessing import Pool, cpu_count

def unpad(data):
    return data[:-data[-1]]

def decrypt_file(args):
    file_path, password = args
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        key = PBKDF2(password, salt, dkLen=32, count=1000000)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[32:]))

        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
    except (ValueError, IndexError, TypeError) as e:
        print(f"Error decrypting file {file_path}: {e}")
        return None
      
def list_files_only(directory):
    file_names = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                files_path = os.path.join(root, file)
                file_names.append(files_path)
        return file_names
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    path = "/storage/emulated/0/test"
    password = "mangjago"
    all_files = list_files_only(path)
    total_files = len(all_files)

    # Using multiprocessing to decrypt files
    pool = Pool(cpu_count())
    tasks = [(file, password) for file in all_files]

    with Progress() as progress:
        task = progress.add_task("Decrypting files...", total=total_files)
        for _ in progress.track(pool.imap_unordered(decrypt_file, tasks), total=total_files):
            progress.update(task, advance=1)

    pool.close()
    pool.join()
    print("Your files have been successfully decrypted")