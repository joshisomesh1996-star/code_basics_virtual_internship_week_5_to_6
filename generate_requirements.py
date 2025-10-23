import os
import pkg_resources

def find_imports(directory="."):
    imports = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("import ") or line.startswith("from "):
                            parts = line.replace(",", " ").split()
                            if parts[0] == "import":
                                imports.add(parts[1].split(".")[0])
                            elif parts[0] == "from":
                                imports.add(parts[1].split(".")[0])
    return imports

def main():
    imports = find_imports(".")
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    with open("requirements.txt", "w") as req:
        for imp in sorted(imports):
            if imp in installed:
                req.write(f"{imp}=={installed[imp]}\n")
    print("✅ requirements.txt generated with detected imports.")

if __name__ == "__main__":
    main()
