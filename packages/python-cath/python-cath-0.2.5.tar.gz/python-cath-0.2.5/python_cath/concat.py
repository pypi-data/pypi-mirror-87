import os


def concat(file_list, output_file):
    os.system(f"head -1 {file_list[0]} > {output_file}")
    for afile in file_list:
        os.system(f"tail -n +2 {afile} >> {output_file}")
