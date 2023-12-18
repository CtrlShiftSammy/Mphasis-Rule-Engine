import os
import keyboard
import time

def list_folders(directory):
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    print("Availabe rule profiles in directory",directory,":")
    for i, folder in enumerate(folders, start=1):
        print(f"{i}. {folder}")
    return folders

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} (Default: {default_value}): ")
    return user_input.strip() if user_input else default_value

def choose_folder(directory):
    folders = list_folders(directory)
    if not folders:
        print("No folders found in the specified directory.")
        return None
    return(choose_option(folders))

def append_file(source_path, target_path):
    try:
        with open(source_path, 'r') as source_file, open(target_path, 'a') as target_file:
            # Read all lines from the source file
            lines = source_file.readlines()

            # Skip the first line (header) and append the rest to the target file
            target_file.writelines(lines[1:])

        print(f"File appended successfully.")
    except FileNotFoundError:
        print(f"Error: One of the files not found.")
    except Exception as e:
        print(f"Error: {e}")


def choose_sched_change(DEP_KEY):
    options_list = ["Schedule Duration change", "Schedule Deletion", "Schedule Frequency change", "Aircraft Type change", "Possible Schedule Time change"]
    selected_option = choose_option(options_list)

    if selected_option != "Schedule Deletion":
        inv_file_location = get_user_input(f"Enter the location of INV-ZZ file of flight(s) after {selected_option}:", None)
        # Perform actions based on the selected_option and inv_file_location
        # Add your custom logic here
        print(f"Selected option: {selected_option}, INV-ZZ file location: {inv_file_location}")
        target_file_path = 'Data/mphasis_dataset/INV-ZZ-20231208_041852.csv'

        if inv_file_location is not None:
            append_file(inv_file_location, target_file_path)
            print(f"Selected option: {selected_option}, INV-ZZ file location: {inv_file_location}")
        else:
            print(f"No INV-ZZ file location provided for {selected_option}")
    else:
        print(f"Selected option: {selected_option}, No INV-ZZ file location needed for Schedule Deletion")

# Rest of the code (get_user_input and choose_option functions) remains unchanged
    

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

