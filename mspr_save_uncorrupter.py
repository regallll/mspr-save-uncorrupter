import tkinter as tk
from tkinter import filedialog
from msvcrt import getch


def get_game_version(file_path):

    with open(file_path, 'r') as file:
        for line in file:
            if 'ProfileVersion' in line:
                if 'Beta 2' in line:  # <ProfileVersion version = "Beta 2"/>
                    return '01.00'
                elif 'Beta 3' in line:  # <ProfileVersion version = "Beta 3"/>
                    return '01.03'
                else:
                    return 'Unknown'
    return None


def get_player_name(file_path):

    with open(file_path, 'r') as file:
        for line in file:
            # <Key name="playernamestring" value = "..." />
            if 'playernamestring' in line:
                start_index = line.find('value = "') + 9  # len('value = "') = 9
                end_index = line.find('"', start_index)
                return line[start_index:end_index]
    return None


def select_uncorruption_method():
    method_choice = None

    while method_choice not in ['1', '2', '3']:
        method_choice = input(
            "\nSelect uncorruption method:"
            "\n    [1] Uncorrupts the save using techniques that have no "
            "impact on the user experience whatsoever. "
            "\033[92m\n        Recommended for the vast majority of cases."
            "\n\033[94m    [2] Does everything in option 1 and additionally "
            "clears all user preferences, which can be readjusted in-game. "
            "\033[93m\n        Use this if option 1 fails to resolve the issue."
            "\033[94m\n    [3] Does everything in options 1 and 2 and "
            "adjusts all stats (excluding rewarded stats where the reward "
            "hasn't yet been achieved). These cannot be readjusted in-game. "
            "\033[91m\n        Use this if option 2 fails to resolve the issue."

            "\033[94m\n\nEnter uncorruption method (1, 2, or 3): "
        )

    return method_choice

def chunk_keeper(file_path, game_version, method_choice):
    # Keeps chunks from the save based on the game version and
    # uncorruption method selected. All other chunks are removed.
    
    # List of chunks to keep. Starts off as a base chunk list which is equivalent
    # to a 01.00 save with uncorruption method 2 or 3 selected.
    allowed_chunks = [
        "festival", "garage", "global", "online", "options", "rewards", "ticket",
        "track", "vehiclelams"
    ]

    if game_version == '01.03':
        allowed_chunks.extend(["character", "speedweekend"])

    if method_choice == '1':
        allowed_chunks.extend(["audio", "gui", "loading", "tutorial"])

    if game_version == '01.03' and method_choice == '1':
        allowed_chunks.append("microbadges")

    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        keep_chunk = True
        for line in lines:
            if line.strip().startswith("<Chunk name"):
                # '<Chunk name = "', chunk_name, '">'
                chunk_name = line.split('"')[1]
                if chunk_name in allowed_chunks:
                    keep_chunk = True
                    file.write(line)
                else:
                    keep_chunk = False
            elif line.strip().startswith("</Chunk>"):
                if keep_chunk:
                    file.write(line)
            elif keep_chunk:
                file.write(line)

def main():

    print("\033[94m\n╔═════════════════════════════════╗\n"
                    "║ MSPR Save Uncorrupter by regal. ║\n"
                    "╚═════════════════════════════════╝\n"
                    "EXTREMELY EARLY WIP.\n"
                    "Make sure your save is decrypted before proceeding!\n"
                    "\n"
                    "Press any key to continue...")

    getch() # 'Press any key' functionality

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("AUTOSAVE.DAT", "*.DAT"), ("All Files" , "*")],
        title="Select AUTOSAVE.DAT"
        )

    print("\nSelected file:", file_path)

    game_version = get_game_version(file_path)
    player_name = get_player_name(file_path)

    if game_version != None and player_name != None:
        print(
            "\nDetected save '" + str(player_name) + "' on version",
              str(game_version) + "."
              )
    elif game_version != None and player_name == None:
        print(
            "\nDetected save on version", str(game_version) + "."
            )
    elif game_version == 'Unknown':
        print(
            "\033[91m\nERROR: Detected unknown game version! The program "
              "cannot continue and will now exit."
            )
        exit()
    else:  # game_version == None
        print(
            "\033[91m\nERROR: Could not detect game version! The program "
              "cannot continue and will now exit."
            )
        exit()

    method_choice = select_uncorruption_method()

    method_choice = 1 # For safety as other methods are not fully implemented yet.
    
    chunk_keeper(file_path, game_version, method_choice)

    print("\nSave uncorrupted successfully! Press any key to exit.")
    getch()

if __name__ == "__main__":
    main()