import sys
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata

def get_installed_packages():
    return {dist.metadata['Name'].lower() for dist in metadata.distributions()}

def read_requirements_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def check_missing_packages(requirements):
    installed_packages = get_installed_packages()
    return [pkg for pkg in requirements if pkg.split('==')[0].lower() not in installed_packages]

def main():
    requirements_file = 'requirements.txt'
    required_packages = read_requirements_file(requirements_file)
    missing_packages = check_missing_packages(required_packages)

    if missing_packages:
        for pkg in missing_packages:
            print(pkg)
        sys.exit(1)  # Exit with a status code indicating missing packages
    else:
        print("")
        sys.exit(0)  # Exit with a status code indicating success

if __name__ == "__main__":
    main()