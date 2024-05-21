import os, shutil

def copy_dir(source, target):
    try:
        os.mkdir(target)
    except FileExistsError:
        print(f"The {target} directory already exists. Remove it and try again.")
        return
    except FileNotFoundError:
        print("Something is wrong with the path provided. Check it and try again.")
        return
    for dir_or_file in os.listdir(source):
        source_file = os.path.join(source, dir_or_file)
        if os.path.isfile(source_file):
            shutil.copy(source_file, target)
        else:
            target_file = os.path.join(target, dir_or_file)
            copy_dir(source_file, target_file)