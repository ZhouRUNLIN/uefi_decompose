import os
from uefi_checker import depart_file
import re

def print_list(ls):
    for l in ls:
        print(l, end="")

def store_data_list(file_name, data_list, list_name):
    file_name = re.sub(".EXE", "", file_name) + ".txt"

    with open(file_name, "a") as fic:
        starter = list_name + " :\n"
        fic.write(starter)
        for data in data_list:
            fic.write(data)
        fic.write("\n")
        fic.close()
    print("finish for wrting data :")
    print_list(data_list) 

def run_binwalk(file):
    """
    使用binwalk, 拆解BMC文件
    """
    command = f"binwalk {file}"
    return command

def extract_file_by_binwalk(file):
    command = f"binwalk -e {file}"
    os.system(command)

def execute_command(command):
    outputs = os.popen(command).readlines()
    if len(outputs) != 0:
        # print("finish command of binwalk ")
        return outputs
    else:
        print("No match output")
    return None

class BMC:
    def get_compressed_methode(file):
        command = run_binwalk(file) + " | grep compressed | tr -s ' ' | cut -d ' ' -f 3,4,5,6 "
        outputs = execute_command(command)
        
        methode_list = []
        if outputs != None:
            for output in outputs:
                if output not in methode_list:
                    methode_list.append(output)
        
        return methode_list

    def get_zImage_version(file):
        command = run_binwalk(file) + " | grep zImage "
        outputs = execute_command(command)

        for output in outputs:
            print(output)
        return outputs

    def get_squash_fs(file):
        command = run_binwalk(file) + " | grep Squashfs "
        outputs = execute_command(command)

        for output in outputs:
            print(output)
        return outputs

    def get_info(file):
        # 路径准备
        file_path, file_name = depart_file(file)
        extracted_file_path = file_path + "_" + file_name + ".extracted/"
        file_d9 =  extracted_file_path + "payload/firmimgFIT.d9"

        if not os.path.isdir(extracted_file_path):
            extract_file_by_binwalk(file)
        compressed_methode = BMC.get_compressed_methode(file_d9)
        zImage_version = BMC.get_zImage_version(file_d9)
        squash_fs = BMC.get_squash_fs(file_d9)

        store_data_list(file_name, compressed_methode, "compressed data algo")
        store_data_list(file_name, zImage_version, "zImage Version")
        store_data_list(file_name, squash_fs, "squash fs")

if __name__=='__main__':
    file_path = "downloads/BMC/_7_00_00_00.EXE"
    
    if os.path.exists("_7_00_00_00.txt"):
        os.remove("_7_00_00_00.txt")
    
    BMC.get_info(file_path)


