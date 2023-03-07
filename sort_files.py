import sys
import re
import shutil
from pathlib import Path


formats = {
    "images": ['jpeg', 'png', 'jpg', 'svg'],
    "documents": ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    "audio": ['mp3', 'ogg', 'wav', 'amr'],
    "video": ['avi', 'mp4', 'mov', 'mkv'],
    "archives": ['zip', 'gz', 'tar']
}

vocabulary = {
    ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "H", ord("Ґ"): "G",
    ord("Д"): "D", ord("Е"): "E", ord("Є"): "Ie", ord("Ж"): "Zh", ord("З"): "Z",
    ord("И"): "Y", ord("І"): "I", ord("Ї"): "I", ord("Й"): "I", ord("К"): "K",
    ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O", ord("П"): "P",
    ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F",
    ord("Х"): "Kh", ord("Ц"): "Ts", ord("Ч"): "Ch", ord("Ш"): "Sh", ord("Щ"): "Shch",
    ord("Ь"): "", ord("Ю"): "Iu", ord("Я"): "Ia", ord("Ъ"): "", ord("Ы"): "Y", ord("Ё"): "Yo",
    ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "h", ord("ґ"): "g",
    ord("д"): "d", ord("е"): "e", ord("є"): "ie", ord("ж"): "zh", ord("з"): "z",
    ord("и"): "y", ord("і"): "i", ord("ї"): "i", ord("й"): "i", ord("к"): "k",
    ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o", ord("п"): "p",
    ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "u", ord("ф"): "f",
    ord("х"): "kh", ord("ц"): "ts", ord("ч"): "ch", ord("ш"): "sh", ord("щ"): "shch",
    ord("ь"): "", ord("ю"): "iu", ord("я"): "ia", ord("ъ"): "", ord("ы"): "y", ord("ё"): "yo",
}

result = {
    "images": [],
    "documents": [],
    "audio": [],
    "video": [],
    "archives": [],
    "others": []
}


def sort_tree(path):

    for p in path.iterdir():

        if p.is_dir():

            if p.name in formats.keys():
                continue
            sort_tree(p)

        else:

            file_format = get_file_format(p.name)
            new_folder_name = chose_folder(file_format)
            check_and_create_folder(new_folder_name)
            full_file_name = normalize(p.name)

            if new_folder_name == "archives":
                unpack_archive(p, full_file_name, new_folder_name)
            else:
                relocate_file(p, full_file_name, new_folder_name)
                add_filename_to_result(full_file_name, new_folder_name)

    check_folder_and_delete_if_empty(path)


def add_filename_to_result(filename, foldername):
    result[foldername].append(filename)


def check_and_create_folder(folder_name):
    new_folder_path = Path(folder_name)
    new_folder_path.mkdir(exist_ok=True)


def get_file_format(file):
    return file.split(".")[-1].lower()


def get_file_name(file):
    return ''.join(file.split(".")[:-1])


def chose_folder(file_format):

    for name, values in formats.items():
        if file_format in values:
            return name

    return "others"


def normalize(file_name):

    file_format = get_file_format(file_name)
    file_name = get_file_name(file_name)

    file_name = file_name.translate(vocabulary)
    file_name = re.sub("[^\w\s_]", "_", file_name)

    return f"{file_name}.{file_format}"


def relocate_file(file, new_name, folder_name):
    try:
        file.replace(Path(folder_name) / Path(new_name))
    except FileExistsError:
        pass


def unpack_archive(archive, file_name, folder_name):

    file_name = get_file_name(file_name)
    shutil.unpack_archive(archive, f"{folder_name}/{file_name}")
    archive.unlink()


def check_folder_and_delete_if_empty(path):

    dirs = list(path.glob('**/*'))

    if not len(dirs):
        path.rmdir()


def print_result_in_file():

    with open("result.txt", 'w') as fh:

        for key in result.keys():
            fh.write(f"FOLDER {key}: {'NO FILES' if not result[key] else ''}\n")

            for file in result[key]:
                fh.write(f"    {file}\n")


def clean():
    try:
        folder_path = sys.argv[1]
        p = Path(folder_path)
        sort_tree(p)
        print_result_in_file()
    except IndexError:
        print("You haven't provided the path")
    except FileNotFoundError:
        print("No such path")


if __name__ == "__main__":
    clean()






