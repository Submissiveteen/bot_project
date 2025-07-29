import os

def print_tree(startpath, indent=""):
    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)
        if os.path.isdir(path) and item not in [".venv", "venv"]:
            print(f"{indent}├── {item}/")
            print_tree(path, indent + "│   ")
        elif os.path.isfile(path):
            print(f"{indent}├── {item}")

print("project/")
print_tree(".")