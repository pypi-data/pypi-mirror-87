import pathlib
import argparse
import venv
import subprocess
import re
import os


def handler():
    parser = argparse.ArgumentParser(
        prog="JAVEC",
        description="""Just another virtual environment creator.""",
        )

    parser.add_argument(
        "-a",
        action="store_true",
        help="create activator in main folder",
        )

    parser.add_argument(
        "-g",
        "--gitignore",
        action="store_true",
        help="create .gitignore file in the root directory",
        )

    parser.add_argument(
        "--swap-gitignore",
        help="""Choose your own .gitignore file. This file will change the
        default .gitignore file used in JAVEC.""",
        default=None,
    )

    parser.add_argument(
        "-i",
        "--install",
        required=False,
        nargs="*",
        help="""Install given packages and put them in requirements_javec.txt"""
    )

    parser.add_argument(
        "-r",
        "-u",
        "--uninstall",
        "--remove",
        nargs="*",
        help="""Remove given packages."""
    )

    parser.add_argument(
        "--versionRequirements",
        action="store_true",
        help="""Create requirements with package version"""
    )

    args = parser.parse_args()

    currentDirectory = pathlib.Path.cwd()
    virtualenvDirectory = pathlib.Path(
        currentDirectory,
        f".{currentDirectory.stem}"
        )
    if os.name == "posix":
        pythonExecutable = "python3"
    elif os.name == "nt":
        pythonExecutable = "python.exe"

    # if not virtualenvDirectory.exists():
    #     for parent in list(virtualenvDirectory.parents)[:-1]:
    #         tempdir = parent/f".{parent.stem}"
    #         if not tempdir.exists():
    #             continue
    #         else:
    #             virtualenvDirectory = tempdir
    #             break

    if not virtualenvDirectory.exists():
        builder = venv.EnvBuilder(with_pip=True, system_site_packages=True)
        builder.create(virtualenvDirectory)
    else:
        print(f"Virtual environment already created at {virtualenvDirectory}")

    if args.a:
        activatorPath = virtualenvDirectory.parent/".activator.sh"
        if activatorPath.exists():
            print("Virtual environment activator already exists.")
        else:
            with open(activatorPath, "w") as f:
                f.write(f"source {virtualenvDirectory}/bin/activate")
            print("Virtual environment activator created")

    if args.swap_gitignore:
        newGitignoreExamplePath = pathlib.Path(args.swap_gitignore)
        exampleGitignorePath = pathlib.Path(__file__).parent/"gitignore_example"
        if newGitignoreExamplePath.exists():
            with open(newGitignoreExamplePath, "r") as f:
                newGitignoreToWrite = f.readlines()
            with open(exampleGitignorePath, "w") as f:
                f.write("".join(newGitignoreToWrite))
            print("Gitignore swapped")
        else:
            print("New .gitignore path does not exist.")

    if args.gitignore:
        gitignorePath = virtualenvDirectory.parent/".gitignore"
        if gitignorePath.exists():
            print(".gitignore already exists.")
        else:
            exampleGitignorePath = pathlib.Path(__file__).parent/"gitignore_example"
            with open(exampleGitignorePath, "r") as f:
                gitignoreToWrite = f.readlines()
            with open(gitignorePath, "w") as f:
                f.write("".join(gitignoreToWrite))
            print("Gitignore file created")

    if args.install:
        if len(args.install) > 0:
            completed = subprocess.run(
                [f"{virtualenvDirectory}/bin/{pythonExecutable}", "-m", "pip", "install", *args.install],
                capture_output=True,
            )
            print(completed.stdout.decode("utf-8"))
            print(completed.stderr.decode("utf-8"))
            if not completed.stderr:
                with open("requirements_javec.txt", "r") as f:
                    installedPackages = {x.strip() for x in f.readlines()}
                with open("requirements_javec.txt", "w") as f:
                    for package in args.install:
                        installedPackages.add(f"{package}")
                    f.write("".join([f"{package}\n" for package in installedPackages]))
        else:
            print("Nothing to install.")

    if args.uninstall:
        if len(args.uninstall) > 0:
            completed = subprocess.run(
                [f"{virtualenvDirectory}/bin/{pythonExecutable}", "-m", "pip", "uninstall", "-y", *args.uninstall],
                capture_output=True,
            )
            print(completed.stdout.decode("utf-8"))
            print(completed.stderr.decode("utf-8"))
            if not completed.stderr:
                requirementsJavecDirectory = virtualenvDirectory.parent/"requirements_javec.txt"
                if (requirementsJavecDirectory).exists():
                    with open(requirementsJavecDirectory, "r") as f:
                        installedPackages = {x.strip() for x in f.readlines()}
                else:
                    installedPackages = set()
                with open(requirementsJavecDirectory, "w") as f:
                    for package in args.uninstall:
                        installedPackages.discard(f"{package}")
                    f.write("".join([f"{package}\n" for package in installedPackages]))

    if args.versionRequirements:
        completed = subprocess.run(
            [f"{virtualenvDirectory}/bin/{pythonExecutable}", "-m", "pip", "freeze"],
            capture_output=True
        )
        print(completed.stderr.decode("utf-8"))
        if not completed.stderr:
            requirementsJavecDirectory = virtualenvDirectory.parent/"requirements_javec.txt"
            pipFreezeOutput = completed.stdout.decode("utf-8")
            installedPackagesVersion = set()
            if (requirementsJavecDirectory).exists():
                with open(requirementsJavecDirectory, "r") as f:
                    installedPackages = {x.strip() for x in f.readlines()}
            else:
                installedPackages = set()
            for package in installedPackages:
                installedPackagesVersion.add(
                    re.search(f"{package}.+?(?=\\n)", pipFreezeOutput).group(0)
                )
            with open(requirementsJavecDirectory.parent/"requirements.txt", "w") as f:
                f.write("".join([f"{package}\n" for package in installedPackagesVersion]))
            print("Requirements file created.")
