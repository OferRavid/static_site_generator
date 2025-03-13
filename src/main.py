import sys
from copy_static import copy_dir
from generate_content import generate_pages_recursive

import os, shutil

dir_path_static = "static"
dir_path_docs = "docs"
dir_path_content = "content"
template_path = "template.html"


def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
    if not os.path.exists(dir_path_static):
        print("Missing static directory... Aborting.")
        exit(1)
    copy_dir(dir_path_static, dir_path_docs)
    try:
        generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)
    except FileNotFoundError:
        print("Missing file or directory")
        exit(1)
    except ValueError as e:
        print(e)
        exit(1)

if __name__ == "__main__":
    main()

