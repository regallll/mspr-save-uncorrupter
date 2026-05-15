import sys
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
                prefix = 'value = "'
                start_index = line.find(prefix) + len(prefix)
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

    # List of chunks to keep. Starts off as a base chunk list which is
    # equivalent to a 01.00 save with uncorruption method 2 or 3 selected.
    allowed_chunks = [
        "festival", "garage", "global", "online", "options", "rewards",
        "ticket", "track", "vehiclelams"
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
                chunk_name = line.split('"')[1].lower()
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


def key_keeper(file_path, game_version, method_choice):
    # Chunk name and allowed key snippets combinations. Starts off as a
    # base list with the essential keys - equivalent to a 01.00 save
    # with uncorruption method 2 or 3 selected.
    allowed_key_snippets = {
        'festival': [
            "credits.locked",
            "eliminator.unlocked",
            "medals",
            "player.points",
            "rank",
            "speed.unlocked",
            "trophy",
            "wins"
        ],
        'garage': [
            "avail",
            "character.name",
            "unlocked",
            "vehicleunlocks",
            "wins"
        ],
        'global': [
            "4playercompleted",
            "barrelroll",
            "boostexplosionwins",
            "boostfreewins",
            "devghostsbeaten",
            "distancetravelled",
            "dlcdevghostsonetrackbeaten",
            "freeplayraceswon",
            "friendsinrace",
            "heavyweightwins",
            "knockoffattacks",
            "largestvictory",
            "lightweightwins",
            "longestjump",
            "maxpunchesduringvictory",
            "mediumweightwins",
            "ms1_save_detected",
            "nummicrobadges",
            "numstdraces",
            "numwins",
            "numwrecks",
            "onlineracetime",
            "punchedfriendandwon",
            "successfulattacks",
            "surviourcount",
            "tightestvictory",
            "totalracetime",
            "xxxfilth"
        ],
        'online': [
            "casualgamesplayed",
            "customgamesplayed",
            "dropout",
            "globalgame",
            "locationid",
            "ranked.bronzes",
            "ranked.fullracecompleted",
            "ranked.gamesplayed",
            "ranked.golds",
            "ranked.longwinningstreak",
            "ranked.playersbeaten",
            "ranked.ranking",
            "ranked.silvers",
            "ranked.victories",
            "ranked.xp",
            "wreckfreerankedraces"
        ],
        'options': [
            "playernamestring"
        ],
        'rewards': [
            "reward"
        ],
        'ticket': [
            "bestmedal",
            "unlocked"
        ],
        'track': [
            "devghostsbeaten",
            "hardcorewins",
            "onlinewins",
            "splitscreenraces",
            "wins"
        ],
        'vehiclelams': [
            "monster20mudtest",
            "mudplugger22mudtest",
            "racetruck00",
            "rallycar00"
        ]
    }

    if game_version == '01.03':
        allowed_key_snippets.setdefault('character', []).append("dlcwins")
        allowed_key_snippets['garage'].extend(["collectionset", "dlc"])
        allowed_key_snippets.setdefault('speedweekend', []).extend(
            ["numbarrelraces", "numwins"])
        allowed_key_snippets['ticket'].append("speedweekend_complete")

    if method_choice == '1':
        allowed_key_snippets['garage'].extend(["avatar", "choice"])
        allowed_key_snippets['online'].append("eula")
        allowed_key_snippets.setdefault('audio', []).extend([
            "music.shuffle",
            "music.trackmaskupper",
            "music.trackindex",
            "vol.horn",
            "vol.music",
            "vol.sfx",
            "vol.voice",
            "voice.outputtype"
        ])
        allowed_key_snippets.setdefault('gui', []).extend([
            "gallery.controlsvisible",
            "osd.opc"
        ])
        allowed_key_snippets.setdefault('loading', []).append("visited")
        allowed_key_snippets['options'].extend([
            "camerapref.race",
            "controllerpref.invertphoto",
            "controllerpref.invertrace",
            "controllerpref.musiccontrol",
            "controllerpref.race",
            "controllerpref.rumble",
            "controllerpref.sixaxissensitivity",
            "horizontalsplit",
            "playernameflag",
            "tagpreference"
        ])
        allowed_key_snippets.setdefault('tutorial', []).extend([
            "atv", "bigrig", "bike", "buggy", "festivalguide", "lowrank",
            "monstertruck", "motorstorm1", "motorstorm2", "motorstorm3",
            "motorstorm4", "motorstorm5", "motorstorm6", "motorstorm7",
            "motorstorm8", "mudplugger", "newvehicle", "novehicle",
            "playerlist", "racingtruck", "rallycar", "rank1", "rank2",
            "rank3", "rank4", "rank5", "rank6", "rank7", "rank8",
            "targettime", "wrecklimit"
        ])

    if method_choice in ('1', '2'):
        allowed_key_snippets['global'].extend([
            "attackattempts",
            "furthestboostdistance",
            "minusedvehicle",
            "mostusedvehicle",
            "numoverheats",
            "numraces",
            "picturestaken",
            "wreckfreeraces"
        ])

    if game_version == '01.03' and method_choice == '1':
        allowed_key_snippets['tutorial'].extend([
            "microbadges", "speedweekend", "speedweekend.qualified"
        ])

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_chunk = None
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith("<Chunk name"):
                current_chunk = line.split('"')[1].lower()
                file.write(line)
            elif line.strip().startswith("</Chunk>"):
                current_chunk = None
                file.write(line)
            elif (current_chunk in allowed_key_snippets
                  and line.strip().startswith("<Key")):
                key_name = line.split('"')[1].lower()
                if any(snippet in key_name
                       for snippet in allowed_key_snippets[current_chunk]):
                    file.write(line)
            else:
                file.write(line)


def stat_adjuster(file_path, game_version):
    # Adjusts stats in the save to the minimum required value for rewards.
    # Only applies if the value exceeds the minimum - if below, it is left alone.

    stat_limits = {
        'character': {
            'f_capsgirl.dlcwins': 1,
            'f_kira.dlcwins': 1,
            'f_zoe.dlcwins': 1,
            'm_takagi.dlcwins': 1,
            'm_teuvo.dlcwins': 1,
            'm_tramp.dlcwins': 1,
        },
        'festival': {
            'eliminator.unlocked': 16,
            'medals.bronzesilvergold': 96,
            'medals.gold': 96,
            'medals.gold.eliminator': 16,
            'medals.gold.speed': 16,
            'medals.silverplusgold': 96,
            'player.points': 9600,
            'rank': 8,
            'speed.unlocked': 16,
            'trophy.canttouchthis': 1,
        },
        'garage': {
            'vehicle.atv.wins': 5,
            'vehicle.bigrig.wins': 5,
            'vehicle.bike.wins': 5,
            'vehicle.buggy.wins': 5,
            'vehicle.monster.wins': 5,
            'vehicle.mudplugger.wins': 5,
            'vehicle.racetruck.wins': 5,
            'vehicle.rallycar.wins': 5,
        },
        'global': {
            '4playercompleted': 1,
            'barrelroll': 40,
            'boostexplosionwins': 20,
            'boostfreewins': 1,
            'devghostsbeaten': 128,
            'distancetravelled': 2000000,
            'freeplayraceswon': 10,
            'friendsinrace': 4,
            'heavyweightwins': 50,
            'knockoffattacks': 10,
            'largestvictory': 15,
            'lightweightwins': 50,
            'longestjump': 185,
            'maxpunchesduringvictory': 5,
            'mediumweightwins': 50,
            'nummicrobadges': 39,
            'numstdraces': 250,
            'numwins': 250,
            'numwrecks': 250,
            'onlineracetime': 36000,
            'successfulattacks': 100,
            'surviourcount': 10,
            'totalracetime': 36000,
        },
        'online': {
            'casualgamesplayed': 50,
            'ranked.fullracecompleted': 1,
            'ranked.gamesplayed': 50,
            'ranked.golds': 50,
            'ranked.longwinningstreak': 3,
            'ranked.ranking': 5,
            'wreckfreerankedraces': 1,
        },
        'speedweekend': {
            'atv.numbarrelraces': 6,
            'atv.numwins': 6,
            'bigrig.numbarrelraces': 6,
            'bigrig.numwins': 6,
            'bike.numbarrelraces': 6,
            'bike.numwins': 6,
            'buggy.numbarrelraces': 6,
            'buggy.numwins': 6,
            'monster.numbarrelraces': 6,
            'monster.numwins': 6,
            'mudplugger.numbarrelraces': 6,
            'mudplugger.numwins': 6,
            'numwins': 48,
            'racetruck.numbarrelraces': 6,
            'racetruck.numwins': 6,
            'rallycar.numbarrelraces': 6,
            'rallycar.numwins': 6,
        },
        'track': {
            'track_blackrock.wins': 5,
            'track_calderaridgerace.wins': 5,
            'track_cavernous.hardcorewins': 1,
            'track_cavernous.onlinewins': 1,
            'track_cavernous.splitscreenraces': 1,
            'track_coastlinerun.wins': 5,
            'track_colossus_canyon.wins': 5,
            'track_davetona.wins': 5,
            'track_davetona_volcanic.devghostsbeaten': 8,
            'track_davetona_volcanic.onlinewins': 1,
            'track_davetona_volcanic.splitscreenraces': 1,
            'track_dunkirk.devghostsbeaten': 8,
            'track_dunkirk.onlinewins': 1,
            'track_dunkirk.splitscreenraces': 1,
            'track_edge.wins': 5,
            'track_happy_jungle.wins': 5,
            'track_jurassicwaterfall.wins': 5,
            'track_mudslide.wins': 5,
            'track_mudslidevolcanic.hardcorewins': 1,
            'track_mudslidevolcanic.onlinewins': 1,
            'track_mudslidevolcanic.splitscreenraces': 1,
            'track_raingod_spire.wins': 5,
            'track_reborn.wins': 5,
            'track_reefrunner.hardcorewins': 1,
            'track_reefrunner.onlinewins': 1,
            'track_reefrunner.splitscreenraces': 1,
            'track_rift.wins': 5,
            'track_scorched.wins': 5,
            'track_scorched_volcanic.hardcorewins': 1,
            'track_scorched_volcanic.onlinewins': 1,
            'track_scorched_volcanic.splitscreenraces': 1,
            'track_seacaves.devghostsbeaten': 8,
            'track_seacaves.onlinewins': 1,
            'track_seacaves.splitscreenraces': 1,
            'track_sugarplant.wins': 5,
            'track_torrentofabuse.devghostsbeaten': 8,
            'track_torrentofabuse.onlinewins': 1,
            'track_torrentofabuse.splitscreenraces': 1,
            'track_vol_badlands.hardcorewins': 1,
            'track_vol_badlands.onlinewins': 1,
            'track_vol_badlands.splitscreenraces': 1,
            'track_vol_calderaridgerace.devghostsbeaten': 8,
            'track_vol_calderaridgerace.onlinewins': 1,
            'track_vol_calderaridgerace.splitscreenraces': 1,
            'track_vol_edge.hardcorewins': 1,
            'track_vol_edge.onlinewins': 1,
            'track_vol_edge.splitscreenraces': 1,
            'track_vol_rift.devghostsbeaten': 8,
            'track_vol_rift.onlinewins': 1,
            'track_vol_rift.splitscreenraces': 1,
            'track_volcanic_hollowed_earth.hardcorewins': 1,
            'track_volcanic_hollowed_earth.onlinewins': 1,
            'track_volcanic_hollowed_earth.splitscreenraces': 1,
            'track_volcanicwastelands.wins': 5,
            'track_volcano_run.hardcorewins': 1,
            'track_volcano_run.onlinewins': 1,
            'track_volcano_run.splitscreenraces': 1,
            'track_xbeach.wins': 5,
        }
    }

    if game_version != '01.03':
        del stat_limits['character']
        del stat_limits['speedweekend']

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_chunk = None
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith("<Chunk name"):
                current_chunk = line.split('"')[1].lower()
                file.write(line)
            elif line.strip().startswith("</Chunk>"):
                current_chunk = None
                file.write(line)
            elif (current_chunk in stat_limits
                  and line.strip().startswith("<Key")):
                key_name = line.split('"')[1].lower()
                if key_name in stat_limits[current_chunk]:
                    limit = stat_limits[current_chunk][key_name]
                    value_str = line.split('"')[3]
                    try:
                        value = float(value_str)
                        if value > limit:
                            line = line.replace(
                                f'value = "{value_str}"',
                                f'value = "{limit}"'
                            )
                    except ValueError:
                        pass
                file.write(line)
            else:
                file.write(line)


def empty_chunk_remover(file_path):
    # Removes chunks that contain no keys.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        chunk_buffer = []
        inside_chunk = False
        has_keys = False

        for line in lines:
            if line.strip().startswith("<Chunk name"):
                inside_chunk = True
                has_keys = False
                chunk_buffer = [line]
            elif line.strip().startswith("</Chunk>"):
                chunk_buffer.append(line)
                if has_keys:
                    file.writelines(chunk_buffer)
                inside_chunk = False
                chunk_buffer = []
            elif inside_chunk:
                chunk_buffer.append(line)
                if line.strip().startswith("<Key"):
                    has_keys = True
            else:
                file.write(line)


def main():

    print("\033[94m\n╔═════════════════════════════════╗\n"
                    "║ MSPR Save Uncorrupter by regal. ║\n"
                    "╚═════════════════════════════════╝\n"
                    "Back up and decrypt your save before proceeding!\n"
                    "\n"
                    "Press any key to continue...")

    getch()  # 'Press any key' functionality

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("AUTOSAVE.DAT", "*.DAT"), ("All Files", "*")],
        title="Select AUTOSAVE.DAT"
    )

    if not file_path:
        print(
            "\033[91m\nERROR: No file selected. The program cannot "
            "continue and will now exit.\033[0m"
        )
        sys.exit()

    print("\nSelected file:", file_path)

    game_version = get_game_version(file_path)
    player_name = get_player_name(file_path)

    if game_version in (None, 'Unknown'):
        print(
            "\033[91m\nERROR: Could not detect game version! The program "
            "cannot continue and will now exit.\033[0m"
        )
        sys.exit()

    save_info = f"'{player_name}' " if player_name else ""
    print(f"\nDetected save {save_info}on version {game_version}.")

    method_choice = select_uncorruption_method()

    chunk_keeper(file_path, game_version, method_choice)
    key_keeper(file_path, game_version, method_choice)

    if method_choice == '3':
        stat_adjuster(file_path, game_version)

    empty_chunk_remover(file_path)

    print("\nSave uncorrupted successfully! Press any key to exit.")
    getch()


if __name__ == "__main__":
    main()