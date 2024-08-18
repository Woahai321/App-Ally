import subprocess
import os
import time
import json
import sys
from colorama import init, Fore, Style
import signal

# Initialize colorama for color support
init(autoreset=True)

# Load application configurations from JSON file
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config['applications']

applications = load_config()
running_processes = {}
signal_received = False

def generate_gradient_colors(start_color, end_color, steps):
    """Generate a gradient from start_color to end_color over the specified number of steps."""
    gradient = []
    for i in range(steps):
        ratio = i / (steps - 1)
        red = int((end_color[0] - start_color[0]) * ratio + start_color[0])
        green = int((end_color[1] - start_color[1]) * ratio + start_color[1])
        blue = int((end_color[2] - start_color[2]) * ratio + start_color[2])
        gradient.append(f'\033[38;2;{red};{green};{blue}m')
    return gradient

def typewriter_print(text, gradient_colors):
    os.system('clear')
    color_index = 0
    gradient_length = len(gradient_colors)
    for line in text.splitlines():
        for char in line:
            print(gradient_colors[color_index % gradient_length] + char, end='', flush=True)
            time.sleep(0.005)
            color_index += 1
        print()  # Move to the next line

def print_branding():
    branding = """

███████╗ ██████╗ ██╗     ██╗   ██╗██╗███████╗██╗   ██╗
██╔════╝██╔═══██╗██║     ██║   ██║██║██╔════╝╚██╗ ██╔╝
███████╗██║   ██║██║     ██║   ██║██║█████╗   ╚████╔╝ 
╚════██║██║   ██║██║     ██║   ██║██║██╔══╝    ╚██╔╝  
███████║╚██████╔╝███████╗╚██████╔╝██║██║        ██║   
╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝╚═╝        ╚═╝   

⭐ App Ally - Your Ally in Application Management ⭐
    """
    start_color = (128, 0, 128)  # Purple
    end_color = (0, 255, 0)      # Green
    steps = len(branding.replace('\n', ''))  # Number of characters to colorize
    gradient_colors = generate_gradient_colors(start_color, end_color, steps)
    typewriter_print(branding, gradient_colors)

def start_application(name):
    if name in running_processes:
        print(Fore.YELLOW + f"{name} is already running in tmux session {running_processes[name]} ⚠️")
        return

    app = applications[name]
    session_name = f"woahai_{name}"
    try:
        command = f"tmux new-session -d -s {session_name} \"echo 'Starting {name}...'; {app['start_command']} &> {app['log_file']} && echo '{name} started successfully' || echo '{name} failed to start'; tail -f {app['log_file']}\""
        subprocess.run(command, shell=True)
        running_processes[name] = session_name
        print(Fore.GREEN + f'{name} started in tmux session {session_name} ✅')
    except Exception as e:
        print(Fore.RED + f"Failed to start {name}: {e} ❌")

def stop_application(name):
    if name in running_processes:
        session_name = running_processes[name]
        command = f"tmux kill-session -t {session_name}"
        subprocess.run(command, shell=True)
        print(Fore.GREEN + f'{name} stopped ❌')
        del running_processes[name]
    else:
        print(Fore.YELLOW + f'{name} is not running ⚠️')

def restart_application(name):
    stop_application(name)
    start_application(name)

def view_logs(name):
    if name in applications:
        with open(applications[name]["log_file"], "r") as log_file:
            print(Fore.BLUE + log_file.read())
    else:
        print(Fore.RED + f'No logs found for {name} ❌')

def start_all():
    for name in applications:
        start_application(name)

def stop_all():
    for name in list(running_processes.keys()):
        stop_application(name)

def list_applications():
    print(Fore.MAGENTA + Style.BRIGHT + "Available applications:")
    for name in applications:
        status = Fore.GREEN + "UP" if name in running_processes else Fore.RED + "DOWN"
        print(Fore.YELLOW + f" - {name} ({status})")

def check_running_processes():
    result = subprocess.run("tmux list-sessions -F '#S'", shell=True, capture_output=True, text=True)
    sessions = result.stdout.split()
    for name in applications:
        session_name = f"woahai_{name}"
        if session_name in sessions:
            running_processes[name] = session_name
            print(Fore.GREEN + f'{name} is already running in tmux session {session_name} ✅')

def signal_handler(sig, frame):
    global signal_received
    signal_received = True
    print(Fore.CYAN + "\nYou used CTRL+C instead of using exit. Click enter, then type y/n to keep your applications running, or have them shutdown", end="")
    sys.stdout.flush()  # Ensure the prompt is displayed before input

def process_signal():
    while True:
        choice = input().strip().lower()
        if choice == 'y':
            os._exit(0)
        elif choice == 'n':
            stop_all()
            os._exit(0)
        else:
            print(Fore.RED + "Please enter 'y' or 'n' to keep your applications running, or have them closed. Next time use the exit command for a graceful shutdown ❌")
            sys.stdout.flush()  # Ensure the prompt is displayed before input

def exit_handler():
    print(Fore.CYAN + "Exiting... 🛑")
    choice = input(Fore.CYAN + "Do you want to keep all applications running? (y/n): ").strip().lower()
    if choice == 'y':
        print(Fore.GREEN + "Keeping applications running. Exiting script. ✅")
    elif choice == 'n':
        stop_all()
        print(Fore.GREEN + "All applications stopped. Exiting script. ✅")
    else:
        print(Fore.RED + "Invalid choice. Exiting without stopping applications. ❌")
    os._exit(0)

def show_help():
    print(Fore.CYAN + "Available commands:")
    print(Fore.YELLOW + "  start <app_name> - Start a specific application")
    print(Fore.YELLOW + "  stop <app_name> - Stop a specific application")
    print(Fore.YELLOW + "  restart <app_name> - Restart a specific application")
    print(Fore.YELLOW + "  view <app_name> - View logs of a specific application")
    print(Fore.YELLOW + "  list - List all available applications and their status")
    print(Fore.YELLOW + "  start all - Start all applications")
    print(Fore.YELLOW + "  stop all - Stop all applications")
    print(Fore.YELLOW + "  add - Add a new application")
    print(Fore.YELLOW + "  remove <app_name> - Remove an application")
    print(Fore.YELLOW + "  edit <app_name> - Edit an existing application")
    print(Fore.YELLOW + "  exit - Exit the script, with an option to keep applications running or shut them down")
    print(Fore.YELLOW + "  help - Show this help message")

def add_application():
    name = input(Fore.CYAN + "Enter the name of the application: ").strip()
    directory = input(Fore.CYAN + "Enter the directory of the application (leave blank if not applicable): ").strip()
    start_command = input(Fore.CYAN + "Enter the command to start the application: ").strip()
    log_file = input(Fore.CYAN + "Enter the log file path for the application: ").strip()
    
    if directory:
        start_command = f"cd '{directory}' && {start_command}"
    
    applications[name] = {
        "directory": directory,
        "start_command": start_command,
        "log_file": log_file
    }
    
    save_config()
    print(Fore.GREEN + f'Application {name} added successfully ✅')

def remove_application(name):
    if name in running_processes:
        print(Fore.RED + f"Application {name} is currently running. Please stop it first before removing. ❌")
        return
    
    if name in applications:
        confirm = input(Fore.RED + f"Are you sure you want to remove {name}? This action cannot be undone. (y/n): ").strip().lower()
        if confirm == 'y':
            del applications[name]
            save_config()
            print(Fore.GREEN + f'Application {name} removed successfully ✅')
        else:
            print(Fore.YELLOW + f'Removal of {name} canceled ⚠️')
    else:
        print(Fore.RED + f'Application {name} does not exist ❌')

def edit_application(name=None):
    if not name:
        name = input(Fore.CYAN + "Enter the name of the application to edit (or press Enter to cancel): ").strip()
        if not name:
            print(Fore.YELLOW + "Edit operation canceled ⚠️")
            return
    
    if name not in applications:
        print(Fore.RED + f'Application {name} does not exist ❌')
        return
    
    print(Fore.CYAN + f"Editing application: {name}")
    print(Fore.CYAN + "What do you want to edit?")
    print(Fore.YELLOW + "  1. Directory")
    print(Fore.YELLOW + "  2. Start Command")
    print(Fore.YELLOW + "  3. Cancel")
    choice = input(Fore.CYAN + "Enter your choice (1/2/3): ").strip()
    
    if choice == '1':
        current_directory = applications[name].get('directory', 'Not set')
        print(Fore.CYAN + f"Current directory: {current_directory}")
        new_directory = input(Fore.CYAN + "Enter the new directory for the application (or press Enter to cancel): ").strip()
        if not new_directory:
            print(Fore.YELLOW + "Edit operation canceled ⚠️")
            return
        confirmation = input(Fore.CYAN + f"Are you sure you want to change the directory of {name} to {new_directory}? (y/n): ").strip().lower()
        if confirmation == 'y':
            applications[name]['directory'] = new_directory
            if new_directory:
                applications[name]['start_command'] = f"cd '{new_directory}' && {applications[name]['start_command'].split(' && ', 1)[-1]}"
            save_config()
            print(Fore.GREEN + f'Directory for {name} updated successfully ✅')
        else:
            print(Fore.YELLOW + 'Update canceled ⚠️')
    
    elif choice == '2':
        current_command = applications[name].get('start_command', 'Not set')
        print(Fore.CYAN + f"Current start command: {current_command}")
        new_command = input(Fore.CYAN + "Enter the new start command for the application (or press Enter to cancel): ").strip()
        if not new_command:
            print(Fore.YELLOW + "Edit operation canceled ⚠️")
            return
        confirmation = input(Fore.CYAN + f"Are you sure you want to change the start command of {name} to {new_command}? (y/n): ").strip().lower()
        if confirmation == 'y':
            if applications[name]['directory']:
                applications[name]['start_command'] = f"cd '{applications[name]['directory']}' && {new_command}"
            else:
                applications[name]['start_command'] = new_command
            save_config()
            print(Fore.GREEN + f'Start command for {name} updated successfully ✅')
        else:
            print(Fore.YELLOW + 'Update canceled ⚠️')
    
    elif choice == '3':
        print(Fore.YELLOW + "Edit operation canceled ⚠️")
    
    else:
        print(Fore.RED + 'Invalid choice ❌')

def save_config():
    with open('config.json', 'w') as f:
        json.dump({"applications": applications}, f, indent=4)

def main():
    print_branding()
    check_running_processes()
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        if signal_received:
            process_signal()
        else:
            command = input(Fore.CYAN + "Enter Command (enter help if unsure): ").strip().lower()
            parts = command.split()
            
            if command == "start all":
                start_all()
            elif command == "stop all":
                stop_all()
            elif command == "exit":
                exit_handler()
            elif command == "list":
                list_applications()
            elif command == "help":
                show_help()
            elif len(parts) == 2:
                action, app_name = parts
                if app_name in applications:
                    if action == "start":
                        start_application(app_name)
                    elif action == "stop":
                        stop_application(app_name)
                    elif action == "restart":
                        restart_application(app_name)
                    elif action == "view":
                        view_logs(app_name)
                    elif action == "remove":
                        remove_application(app_name)
                    elif action == "edit":
                        edit_application(app_name)
                    else:
                        print(Fore.RED + f'Invalid action: {action} ❌')
                else:
                    print(Fore.RED + f'Invalid application name: {app_name} ❌')
            elif len(parts) == 1 and parts[0] == "edit":
                edit_application()
            elif len(parts) == 1 and parts[0] == "add":
                add_application()
            else:
                print(Fore.RED + "Invalid command. Enter 'help' for a list of available commands. ❌")

if __name__ == "__main__":
    main()
