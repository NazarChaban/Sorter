import sys
import os
import shutil

# Відомі розширення файлів для програми (Можна додавати нові категорії та розширення)
KNOWN_EXT = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'archives': ['.zip', '.gz', '.tar']
}


# Функція для транслітерації імені файлу
def normalize(raw: str) -> str:
    mapping = {
        ord('а'): 'a', ord('б'): 'b', ord('в'): 'v', ord('г'): 'h',
        ord('ґ'): 'g', ord('д'): 'd', ord('е'): 'e', ord('є'): 'ie',
        ord('ж'): 'zh', ord('з'): 'z', ord('и'): 'y', ord('і'): 'i',
        ord('ї'): 'i', ord('й'): 'i', ord('к'): 'k', ord('л'): 'l',
        ord('м'): 'm', ord('н'): 'n', ord('о'): 'o', ord('п'): 'p',
        ord('р'): 'r', ord('с'): 's', ord('т'): 't', ord('у'): 'u',
        ord('ф'): 'f', ord('х'): 'kh', ord('ц'): 'ts', ord('ч'): 'ch',
        ord('ш'): 'sh', ord('щ'): 'shch', ord('ю'): 'iu', ord('я'): 'ia',
        ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V', ord('Г'): 'H',
        ord('Ґ'): 'G', ord('Д'): 'D', ord('Е'): 'E', ord('Є'): 'Ye',
        ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'Y', ord('І'): 'I',
        ord('Ї'): 'Yi', ord('Й'): 'Y', ord('К'): 'K', ord('Л'): 'L',
        ord('М'): 'M', ord('Н'): 'N', ord('О'): 'O', ord('П'): 'P',
        ord('Р'): 'R', ord('С'): 'S', ord('Т'): 'T', ord('У'): 'U',
        ord('Ф'): 'F', ord('Х'): 'Kh', ord('Ц'): 'Ts', ord('Ч'): 'Ch',
        ord('Ш'): 'Sh', ord('Щ'): 'Shch', ord('Ю'): 'Yu', ord('Я'): 'Ya',
    }
    for ch in raw:
        if not (ch.isnumeric() or ch.isalpha()):
            raw = raw.replace(ch, '_')
    normalized = raw.translate(mapping)
    return normalized


# Сортування файлів
def walker(main_dir, dirs_paths):

    # Створення множин для відомих та невідомих розширень файлів
    known_ext = set()
    unknown_ext = set()
    # Створення словника для зберігання файлів по категоріях
    sorted_files = {
        'images': [], 'video': [], 'documents': [],
        'audio': [], 'archives': []
    }

    # Обхід всіх файлів та папок
    for root, dirs, files in os.walk(main_dir, topdown=False):
        dirs[:] = [d for d in dirs if d not in (dirs_paths.keys())]
        
        # Прохходження файлів
        if files:
            for file in files:
                # Переіменування файлу та створення дод. змінних
                old_file_path = os.path.join(root, file)
                name, ext = os.path.splitext(file)
                new_name = normalize(name) + ext
                new_file_path = os.path.join(root, new_name)

                os.rename(old_file_path, new_file_path)
                
                # Додавання розширення в відповідну множину
                if ext.lower() in sum(KNOWN_EXT.values(), []):
                    known_ext.add(ext.lower())
                else:
                    unknown_ext.add(ext.lower())

                #Сортування файлів по категоріях
                for k, v in KNOWN_EXT.items():
                    if ext.lower() in v:
                        # Сценарій для архіву
                        if k == 'archives':
                            arch_fold = os.path.splitext(new_name)[0]
                            arch_path = os.path.join(main_dir, 'archives', arch_fold)
                            # Створення директорії для архіву
                            os.makedirs(arch_path, exist_ok=True)
                            # Якщо архів справний, розпаковуємо
                            try:
                                shutil.unpack_archive(new_file_path, arch_path)
                                # Додавання файлу в словник
                                sorted_files[k].append(new_name)
                            # Якщо архів битий, помилка
                            except Exception:
                                print(f"Couldn't unpack archieve: {new_file_path}/n Exception: {Exception}")
                            # Видаляємо архів
                            finally:
                                os.remove(new_file_path)
                        # Сценарій для решти файлів
                        else:
                            try:
                                shutil.move(os.path.join(root, new_name), dirs_paths[k])
                                # Додавання файлу в словник
                                sorted_files[k].append(new_name)
                            except Exception:
                                None
                                # print(f"Something went wrong, but don't worry, everything is alright): {Exception}")
        
        # Прохід порожніх папок
        if dirs:
            for direc in dirs:
                dir_path = os.path.join(root, direc)
                # Якщо папка порожня, видаляємо
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
    
    return known_ext, unknown_ext, sorted_files


def sorter():
    # Перевірка sys.argv на правильну кількість аргументів
    if len(sys.argv) != 2:
        print("Usage: python sorter.py <path/file>")
        exit(1)

    # Перевірка sys.argv[1] на директорію
    if not os.path.isdir(sys.argv[1]):
        print(f'Directory {sys.argv[1]} does not exist.')
        exit(1)

    # Зміна робочої директорії
    os.chdir(sys.argv[1])

    # Створення директорій та їх шляхів
    dirs = ['images', 'documents', 'audio', 'video', 'archives']
    dirs_paths = {}
    for direc in dirs:
        os.makedirs(direc, exist_ok=True)
        dirs_paths[direc] = (os.path.join(os.getcwd(), direc))

    # Сортування файлів
    main_dir = os.getcwd()
    known_ext, unknown_ext, sorted_files = walker(main_dir, dirs_paths)

    # Вивід результатів
    print('Sorted files:')
    for k, v in sorted_files.items():
        print(f'Category: {k}')
        for file in v:
            print(f' - {file}')

    print(f'\nKnown extensions: {", ".join(known_ext)}')
    if unknown_ext:
        print(f'Unknown extensions: {", ".join(unknown_ext)}')


if __name__ == '__main__':
    sorter()