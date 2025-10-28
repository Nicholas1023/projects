import os
import shutil
import subprocess
import json
import uuid
import time
import platform
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

directories = []
osname = os.name
defaultpath = ""

if osname == "nt":
    defaultpath = rf"{os.path.expandvars("%USERPROFILE%")}\Documents\Nicholas1023 Projects"
elif osname == "posix":
    defaultpath = rf"{os.path.expandvars("$HOME")}/Documents/Nicholas1023 Projects"
os.chdir(defaultpath)

def setup():
    print("Welcome to Nicholas1023 Projects!\n\nYour projects:")
    for dir in os.scandir("."):
        if dir.is_dir():
            print(dir.name)
            directories.append(dir.name)
    print("")
    while True:
        command = input("Would you like to create another project? (Type Y or N): ").lower()
        if command == "y":
            while True:
                name = input("Enter project name: ")
                if name not in directories:
                    os.mkdir(name)
                    directories.append(name)
                    try:
                        print("")
                        shutil.copy("Project Files (Do Not Remove)/project.log", f"{name}/project.log")
                        load(10, "Copying 'project.log'...  ")
                        with open(f"{name}/project.log", "a") as log:
                            log.write(f"{datetime.now()}: Log for '{name}' created.")
                            shutil.copy("Project Files (Do Not Remove)/index.html", f"{name}/index.html")
                            load(20, "Copying 'index.html'...   ")
                            log.write(f"\n{datetime.now()}: 'index.html' copied.")
                            shutil.copy("Project Files (Do Not Remove)/style.css", f"{name}/style.css")
                            load(30, "Copying 'style.css'...    ")
                            log.write(f"\n{datetime.now()}: 'style.css' copied.")
                            shutil.copy("Project Files (Do Not Remove)/metadata.json", f"{name}/metadata.json")
                            load(40, "Copying 'metadata.json'...")
                            log.write(f"\n{datetime.now()}: 'metadata.json' copied.")
                            contents = json.load(open(f"{name}/metadata.json", "r"))
                            load(50, "Loading 'metadata.json'...")
                            contents["name"] = name
                            load(60, "Editing 'metadata.json'...")
                            id = str(uuid.uuid4())
                            load(70, "Editing 'metadata.json'...")
                            contents["id"] = id
                            load(80, "Editing 'metadata.json'...")
                            json.dump(contents, open(f"{name}/metadata.json", "w"))
                            load(90, "Editing 'metadata.json'...")
                            log.write(f"\n{datetime.now()}: 'metadata.json' edited.")
                            load(100, "Project creation completed.")
                            log.write(f"\n{datetime.now()}: Project creation completed.")
                            print("\n")
                    except FileNotFoundError:
                        print("Warning: Default files for new project could not be found.\nYou can still use this project, but default files will not be included.")
                    break
                else:
                    print(f"The project name '{name}' is already used.")
            break
        if command == "n":
            break
    interface()

def interface():
    if directories != ["Project Files (Do Not Remove)"]:
        while True:
            project = input("Enter project name to use: ")
            if project in directories and project != "Project Files (Do Not Remove)":
                if osname == "nt":
                    projectdir = defaultpath + "\\" + project
                else:
                    projectdir = defaultpath + "/" + project
                os.chdir(projectdir)
                log = open(f"{projectdir}/project.log", "a")
                print(f"\nNicholas1023 Projects Interface 1.0.1.\nProject: {project}\nFolder: {os.getcwd()}")
                log.write(f"\n{datetime.now()}: Session started.")
                checkexit = False
                try:
                    contents = json.load(open(f"metadata.json", "r"))
                    print(f"ID: {contents["id"]}")
                except:
                    print("Warning: Unable to retrive ID from 'metadata.json'.")
                    checkexit = True
                    exitcode = 2
                while True:
                    command = input(">> ").lower()

                    # Help command.
                    if command == "help":
                        print("""
Available commands:
clear:  Clears the screen.
cli:    Launches the operating system's command line interface with the project directory.
        Add '--default' or '-d' to launch in the default directory.
create: Creates a new file or folder within the project.
        Add '--file' or '-i' to create a file.
        Add '--folder' or '-o' to create a folder.
delete: Deletes the selected project.
        Add '--noprompt' or '-n' to remove confirmation prompts.
exit:   Quits this interface.
help:   Display this message.
        Add '--assist' or '-a' for assistant.
host:   Creates a server on localhost port 8000.
info:   Display information about the selected project.
launch: Launches the application specified after the command.
        For example: launch nicholas1023-projects
log:    Load the project's log file.
""")
                        checkexit = False

                    # Exit command.
                    elif command == "exit":
                        if checkexit == True:
                            log.write(f"\n{datetime.now()}: Session ended. (Exit code {exitcode})")
                            log.close()
                            exit(exitcode)
                        else:
                            log.write(f"\n{datetime.now()}: Session ended. (Exit code 0)")
                            log.close()
                            exit(0)
                    
                    # Clear screen command.
                    elif command == "clear":
                        if osname == "nt":
                            subprocess.run("cls", shell=True)
                            checkexit = False
                        elif osname == "posix":
                            subprocess.run("clear", shell=True)
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3

                    # CLI command: project directory.
                    elif command == "cli":
                        print("\nLaunching OS command line interface...\nType 'exit' to return to Nicholas1023 Projects.\n")
                        os.chdir(projectdir)
                        if osname == "nt":
                            subprocess.run("cmd", shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        elif osname == "posix":
                            try:
                                subprocess.run("bash", shell=True)
                            except:
                                subprocess.run("zsh", shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3

                    # CLI command: default directory.
                    elif command == "cli --default" or command == "cli -d":
                        print("\nLaunching OS command line interface...\nType 'exit' to return to Nicholas1023 Projects.\n")
                        os.chdir(defaultpath)
                        if osname == "nt":
                            subprocess.run("cmd", shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        elif osname == "posix":
                            try:
                                subprocess.run("bash", shell=True)
                            except:
                                subprocess.run("zsh", shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3

                    # Web server command.
                    elif command == "host":
                        while True:
                            check = input("\nWarning: You can only run one server at a time and this applies to all projects on this device.\nRunning this server may stop another on this device.\nDo you want to continue? (Type Y or N): ").lower()
                            if check == "y":    
                                server = HTTPServer(("", 8000), SimpleHTTPRequestHandler)
                                print("Server is hosted at http://localhost:8000.\nTo stop the server, close this application.")
                                log.write(f"\n{datetime.now()}: Server started.")
                                log.close()
                                server.serve_forever()
                            elif check == "n":
                                print("")
                                break

                    # Project information command.
                    elif command == "info":
                        print(f"\nProject name: {project}\nProject folder: {os.getcwd()}\nProject ID: {contents["id"]}\nOperating System: {platform.system() + " " + platform.version()}\n")
                        checkexit = False

                    # Project deletion command: confirmation prompts.
                    elif command == "delete":
                        while True:
                            check = input(f"\nAre you sure about deleting '{project}'? This action is irreversible. (Type Y or N): ").lower()
                            if check == "y":
                                os.chdir(defaultpath)
                                shutil.rmtree(projectdir)
                                print(f"Project '{project}' deleted successfully.")
                                print("Exiting Nicholas1023 Projects...")
                                log.write(f"\n{datetime.now()}: Session ended. (Exit code 0)")
                                log.close()
                                exit(0)
                            elif check == "n":
                                print("")
                                break

                    # Project deletion command: no confirmation prompts.
                    elif command == "delete --noprompt" or command == "delete -n":
                        os.chdir(defaultpath)
                        shutil.rmtree(projectdir)
                        print(f"\nProject '{project}' deleted successfully.")
                        print("Exiting Nicholas1023 Projects...")
                        log.write(f"\n{datetime.now()}: Session ended. (Exit code 0)")
                        log.close()
                        exit(0)

                    # Assistant command.
                    elif command == "help --assist" or command == "help -a":
                        assistant()
                        checkexit = False

                    # Create file command.
                    elif command == "create --file" or command == "create -i":
                        os.chdir(projectdir)
                        while True:
                            filename = input("\nEnter filename: ")
                            if filename == "metadata.json":
                                print("Error: Creating a file named 'metadata.json' removes the project's metadata. Try another filename.")
                                checkexit = True
                                exitcode = 2
                            else:
                                create = open(filename, "w")
                                create.close()
                                print(f"'{filename}' created successfully.\n")
                                checkexit = False
                                break

                    # Create folder command.
                    elif command == "create --folder" or command == "create -o":
                        os.chdir(projectdir)
                        foldername = input("\nEnter folder name: ")
                        os.makedirs(foldername, exist_ok=True)
                        print(f"'{foldername}' created successfully.\n")
                        checkexit = False

                    # Display log command.
                    elif command == "log":
                        print(f"\nLog for '{project}':")
                        os.chdir(projectdir)
                        if osname == "nt":
                            subprocess.run("type project.log", shell=True)
                            checkexit = False
                        elif osname == "posix":
                            subprocess.run("cat project.log", shell=True)
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3
                        print("\n")

                    # Launch app command.
                    elif command.startswith("launch "):
                        appnamelist = command.split(" ", 1)
                        appname = appnamelist[1]
                        if osname == "nt":
                            subprocess.run(f"start {appname}", shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        elif osname == "posix":
                            subprocess.run(appname, shell=True)
                            print("\nWelcome back to Nicholas1023 Projects!")
                            checkexit = False
                        else:
                            print("This command is not compatible with your OS.")
                            checkexit = True
                            exitcode = 3

                    # Command does not exist or options not provided.
                    else:
                        if (command.startswith("create") and
                        command != "create -i" and
                        command != "create -o" and
                        command != "create --file" and
                        command != "create --folder"):
                            print("The command 'create' requires '--file', '--folder', '-i' or '-o'.")
                            checkexit = True
                            exitcode = 4
                        elif command == "launch":
                            print("The command 'launch' requires an application name following it.")
                            checkexit = True
                            exitcode = 4
                        elif command != "":
                            print(f"The command '{command}' does not exist.")
                            checkexit = True
                            exitcode = 1

            else:
                print("Invalid project name.")
    else:
        print("There are no available projects.")

def load(percentage: int, status: str):
    percentagebar = int(percentage / 2)
    bar = "\u2588" * percentagebar + "\u2591" * (50 - percentagebar)
    if percentage != 100:
        print(f"\r{str(percentage)}%  {bar} Status: {status}", end="", flush=True)
    else:
        print(f"\r{str(percentage)}% {bar} Status: {status}", end="", flush=True)
    time.sleep(0.2)

def assistant():
    print("\nWelcome to Nicholas1023 Projects Assistant.\nType 'exit' to return to Nicholas1023 Projects Interface.")
    while True:
        query = input("\nEnter your question: ").lower()
        if "serve" in query or "host" in query:
            print("\nYou can host your project using the command 'host'. Your server will be located at http://localhost:8000.")
        elif "delete" in query or "remove" in query:
            print("\nYou can delete a project with the 'delete' command. Add '--noprompt' or '-n' to remove confirmation prompts.")
        elif "file" in query and "create" in query:
            print("\nTo create a file, you can use the command 'create --file' or 'create -i'.")
        elif "folder" in query and "create" in query:
            print("\nTo create a folder, you can use the command 'create --folder' or 'create -o'.")
        elif query == "exit":
            print("")
            break
        else:
            print("\nSorry, I can't answer your question. Try 'exit', then 'help' and see if you can find a solution.")

setup()