import os
import re

def get_all_files(folder):
    # 返回folder下所有文件路径
    all_files = []
    for root, directories, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            all_files.append(filepath)
    return all_files

def split_by_slash(file_path):
    # 使用正则表达式以斜杠为分隔符拆分字符串
    pattern = r"/"
    result = re.split(pattern, file_path)
    return result

def depart_file(file_path):
    """
    将文件路径拆分为文件名和相对路径
    eg: file_path = folder/sub_folder/file_name.iso
        depart_file(file_path) == [folder/sub_folder, file_name.iso]
    """
    parts_of_list = split_by_slash(file_path)
    file_name = parts_of_list[len(parts_of_list) - 1]
    path = ""

    for count in range(len(parts_of_list) - 1):
        path += parts_of_list[count]
        path += "/"

    return [path, file_name]

def run_parser(file):
    command = "uefi-firmware-parser -b " + file + " | grep 'Firmware Volume' "
    return os.system(command)
    
def write_head(file, fic_name):
    fic = open(fic_name, "a")
    fic.write(file + "\n")
    fic.close()

def write_end(fic_name):
    fic = open(fic_name, "a")
    fic.write("\n")
    fic.close()

def write_content(command, fic_name, file):
    fic = open(fic_name, "a")
    outputs = os.popen(command).readlines()
    for line in outputs:
        fic.write(line)
    fic.close()

    if outputs != []:
        return file
    else:
        return None

def detect_uefi_file(files_list):
    res_list = []
    for file in files_list:
        write_head(file, "resultat.txt")
        
        # os.system(f"uefi-firmware-parser -b {file}")
        command = "uefi-firmware-parser -b -p " + file + " | grep 'Firmware Volume' "
        att_list = write_content(command, "resultat.txt", file)
        os.system(f"uefi-firmware-parser -b {file} | grep 'Firmware Volume' ")
        if att_list != None:
            res_list.append(att_list)
        
        write_end("resultat.txt")

    return res_list

def zip_file(file_path, file_name):
    real_file = file_path + file_name
    command = f"unzip -d {file_path} {real_file}"
    os.system(command)
    os.remove(real_file)

if __name__ == '__main__':
    file_list = get_all_files("downloads/")
    for file in file_list:
        if file.endswith(".zip"):
            zip_file(depart_file(file)[0], depart_file(file)[1])

    new_file_list = get_all_files("downloads/")
    if os.path.exists("resultat.txt"):
        os.remove("resultat.txt")
    bios_list = detect_uefi_file(new_file_list)
    
    if os.path.exists("is_bios.txt"):
        os.remove("is_bios.txt")
    with open("is_bios.txt", "a") as fic:
        for bios in bios_list:
            fic.write(bios + "\n")
    fic.close()

            