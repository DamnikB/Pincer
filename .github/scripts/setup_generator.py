from os import walk, chdir

chdir("../../")

from pincer import __version__


def get_packages():
    return '\n\t'.join(
        item[0].replace("./", "").replace("\\", ".").replace("/", ".")
        for item in list(walk('pincer')) if "__pycache__" not in item[0]
    )


def get_dependencies(path: str) -> str:
    with open(path) as f:
        return '\n\t'.join(f.read().strip().splitlines())


def main():
    with open("VERSION", "w") as f:
        f.write(repr(__version__))

    packages = get_packages()

    with open(".github/scripts/setup_base.cfg") as f:
        base = f.read()

    dependencies = {
        "requires": get_dependencies("requirements.txt"),
        "testing_requires": get_dependencies("packages/dev.txt"),
        "images_requires": get_dependencies("packages/img.txt")
    }

    with open("setup.cfg", "w") as f:
        f.write(
            base.format(
                version=repr(__version__),
                packages=packages,
                **dependencies
            )
        )


if __name__ == '__main__':
    main()
