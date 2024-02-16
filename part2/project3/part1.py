import os
import shutil
import threading
from collections import defaultdict


def sort_files_by_extension(source_folder, destination_folder):
    file_extension_map = defaultdict(list)

    def process_file(file_path):
        _, extension = os.path.splitext(file_path)
        file_extension_map[extension].append(file_path)

    def traverse_folder(folder):
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path)

    traverse_folder(source_folder)

    def move_files(extension):
        destination_dir = os.path.join(destination_folder, extension[1:])
        os.makedirs(destination_dir, exist_ok=True)
        for file_path in file_extension_map[extension]:
            shutil.move(file_path, destination_dir)

    threads = []
    for extension in file_extension_map.keys():
        thread = threading.Thread(target=move_files, args=(extension,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    source_folder = "Хлам"
    destination_folder = "Сортовані_Файли"
    sort_files_by_extension(source_folder, destination_folder)
    print("Сортування файлів завершено.")
