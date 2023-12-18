import os
import keyboard

def list_folders(directory):
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    print("Availabe rule profiles in directory",directory,":")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    return folders

def choose_folder():
    directory = 'Rules/'
    folders = list_folders(directory)
    if not folders:
        print("No folders found in the specified directory.")
        return None
    return(choose_option(folders))

def choose_sched_change():
    options_list = ["Schedule duration change", "Schedule deletion", "Schedule Frequency change", "Aircraft Type change", "Possible Schedule Time change"]
    selected_option = choose_option(options_list)

def choose_option(options):
    num_options = len(options)
    selected_index = 0

    while True:
        print("Choose an option using UP/DOWN arrow keys:")
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"\033[1;37;40m> {i + 1}. {option}\033[0m")  # Highlighted option
            else:
                print(f"  {i + 1}. {option}")

        key = keyboard.read_event(suppress=True).name

        if key == 'up' and selected_index > 0:
            selected_index -= 1
        elif key == 'down' and selected_index < num_options - 1:
            selected_index += 1
        elif key == 'enter':
            break

        # Move the cursor up to overwrite the previous lines
        print("\033[F" * (num_options + 1), end="")

    selected_option = options[selected_index]
    print(f"You chose: {selected_option}")

    # Perform actions based on the selected option
    # Add your custom logic here

    return selected_option

