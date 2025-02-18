import os
import hashlib
import shutil
import time

def hash_file(file_path):
    hash_md5 = hashlib.md5()
    print(f"Обчислюється хеш для файлу: {file_path}")
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_md5.update(chunk)
    file_hash = hash_md5.hexdigest()
    print(f"Хеш файлу {file_path}: {file_hash}")
    return file_hash

def compare_folders(folder1, folder2, output_folder, fake=True, generate_both=False):
    folder1_files = {}
    folder2_files = {}

    print(f"Збираємо хеші для файлів у папці: {folder1}")
    for root, dirs, files in os.walk(folder1):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder1)
            file_hash = hash_file(file_path)
            folder1_files[file_hash] = rel_path

    print(f"Збираємо хеші для файлів у папці: {folder2}")
    for root, dirs, files in os.walk(folder2):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, folder2)
            file_hash = hash_file(file_path)
            folder2_files[file_hash] = rel_path

    both_folder = os.path.join(output_folder, 'BOTH')
    folder1_cutted = os.path.join(output_folder, f'{os.path.basename(folder1)}_cutted')
    folder2_cutted = os.path.join(output_folder, f'{os.path.basename(folder2)}_cutted')

    if not fake:
        print(f"Створюємо папки для результатів: {both_folder}, {folder1_cutted}, {folder2_cutted}")
        os.makedirs(both_folder, exist_ok=True)
        os.makedirs(folder1_cutted, exist_ok=True)
        os.makedirs(folder2_cutted, exist_ok=True)

    for file_hash, rel_path in folder1_files.items():
        src_path = os.path.join(folder1, rel_path)
        if file_hash in folder2_files:
            if generate_both:
                # Файл є в обох папках
                dest_path = os.path.join(both_folder, rel_path)
                if fake:
                    print(f"Показати: Копіювання {src_path} до {dest_path}")
                    time.sleep(1)
                else:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    print(f"Копіювання {src_path} до {dest_path}")
                    shutil.copy(src_path, dest_path)
        else:
            # Файл є тільки в папці 1
            dest_path = os.path.join(folder1_cutted, rel_path)
            if fake:
                print(f"Показати: Копіювання {src_path} до {dest_path}")
                time.sleep(1)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                print(f"Копіювання {src_path} до {dest_path}")
                shutil.copy(src_path, dest_path)

    for file_hash, rel_path in folder2_files.items():
        src_path = os.path.join(folder2, rel_path)
        if file_hash not in folder1_files:
            # Файл є тільки в папці 2
            dest_path = os.path.join(folder2_cutted, rel_path)
            if fake:
                print(f"Показати: Копіювання {src_path} до {dest_path}")
                time.sleep(1)
            else:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                print(f"Копіювання {src_path} до {dest_path}")
                shutil.copy(src_path, dest_path)

    if fake:
        print("Виведено назви операцій без виконання реальних операцій.")
    else:
        print("Порівняння завершено! Результати збережено в:", output_folder)

# Використання:
folder1 = '/storage/emulated/0/Download/folder1'
folder2 = '/storage/emulated/0/Download/folder2'
output_folder = '/storage/emulated/0/Download/out'
fake = False # Встановіть False для реального виконання операцій
generate_both = False

compare_folders(folder1, folder2, output_folder, fake, generate_both)
