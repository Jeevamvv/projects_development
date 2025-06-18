import subprocess
import time
import os
from logger_mod import *

# Global variables for mpv (used in offline mode, not used here)
mpv_process = None
music_playlist = []
current_index = 0
mpv_fifo = "/tmp/mpv-fifo"


# ========== A2DP CONNECTION HANDLING ==========

def connect_a2dp(device_mac):
    try:
        log.info(f"🔗 Connecting to A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
        time.sleep(2)
        log.info(f"✅ Connected to {device_mac}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Failed to connect to {device_mac}: {e}")
        return False


def disconnect_a2dp(device_mac):
    try:
        log.info(f"🔌 Disconnecting from A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "disconnect", device_mac], check=True)
        time.sleep(1)
        log.info(f"✅ Disconnected from {device_mac}")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Failed to disconnect: {e}")


# ========== SYSTEM VOLUME CONTROL ==========

# def get_volume():
#     try:
#         output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
#         for line in output.splitlines():
#             if "Volume:" in line:
#                 percent = line.split('/')[1].strip().replace('%', '')
#                 log.info(f"🔈 Current volume: {percent}%")
#                 return int(percent)
#     except Exception as e:
#         log.error(f"❌ Get volume failed: {e}")
#     return 0


# def set_volume(level_percent):
#     try:
#         level = max(0, min(level_percent, 100))
#         subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
#         log.info(f"🔊 Volume set to {level}%")
#     except subprocess.CalledProcessError as e:
#         log.error(f"❌ Set volume failed: {e}")


# def volume_up():
#     current = get_volume()
#     new_level = min(current + 10, 100)
#     set_volume(new_level)
#     log.info("🔊 Increased volume.")


# def volume_down():
#     current = get_volume()
#     new_level = max(current - 10, 0)
#     set_volume(new_level)
#     log.info("🔉 Decreased volume.")



# ========== SYSTEM VOLUME CONTROL ===========================================================
# ====== SYSTEM VOLUME CONTROL (for mpv/local player) ======

# def get_system_volume_local():
#     try:
#         output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
#         for line in output.splitlines():
#             if "Volume:" in line:
#                 percent = line.split('/')[1].strip().replace('%', '')
#                 log.info(f"🔈 Current system volume: {percent}%")
#                 return int(percent)
#     except Exception as e:
#         log.error(f"❌ Get system volume failed: {e}")
#     return 0

# def set_system_volume_local(level_percent):
#     try:
#         level = max(0, min(level_percent, 100))
#         subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
#         log.info(f"🔊 System volume set to {level}%")
#     except subprocess.CalledProcessError as e:
#         log.error(f"❌ Set system volume failed: {e}")

# def increase_system_volume_local():
#     current = get_system_volume_local()
#     new_level = min(current + 10, 100)
#     set_system_volume_local(new_level)
#     log.info("🔊 Increased system volume.")

# def decrease_system_volume_local():
#     current = get_system_volume_local()
#     new_level = max(current - 10, 0)
#     set_system_volume_local(new_level)
#     log.info("🔉 Decreased system volume.")



# # ====== PLAYERCTL VOLUME CONTROL (for online players like Spotify, Chrome) ======

# def get_player_volume_online(player):
#     try:
#         result = subprocess.check_output(["playerctl", "--player", player, "volume"]).decode().strip()
#         vol_percent = round(float(result) * 100)
#         log.info(f"🔈 Current media player volume: {vol_percent}%")
#         return vol_percent
#     except Exception as e:
#         log.error(f"❌ Get player volume failed: {e}")
#         return 0

# def set_player_volume_online(player, level_percent):
#     try:
#         level = max(0, min(level_percent, 100)) / 100
#         subprocess.run(["playerctl", "--player", player, "volume", str(level)], check=True)
#         log.info(f"🔊 Media player volume set to {level_percent}%")
#     except subprocess.CalledProcessError as e:
#         log.error(f"❌ Set player volume failed: {e}")

# def increase_player_volume_online(player):
#     current = get_player_volume_online(player)
#     set_player_volume_online(player, min(current + 10, 100))

# def decrease_player_volume_online(player):
#     current = get_player_volume_online(player)
#     set_player_volume_online(player, max(current - 10, 0))




# =================== A2DP / Bluetooth Sink Volume Control ===================

def get_active_sink_name():
    try:
        output = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode()
        for line in output.splitlines():
            if "bluez" in line or "a2dp" in line:
                sink_name = line.split()[1]
                log.info(f"🎧 Using Bluetooth sink: {sink_name}")
                return sink_name
        if output:
            sink_name = output.splitlines()[0].split()[1]
            log.info(f"🔊 Using default sink: {sink_name}")
            return sink_name
    except Exception as e:
        log.error(f"❌ Failed to get sink name: {e}")
    return None

def get_system_volume_bt():
    sink = get_active_sink_name()
    if not sink:
        return 0
    try:
        output = subprocess.check_output(["pactl", "get-sink-volume", sink]).decode()
        for line in output.splitlines():
            if "Volume:" in line:
                percent = line.split('/')[1].strip().replace('%', '')
                log.info(f"🔈 Bluetooth volume: {percent}%")
                return int(percent)
    except Exception as e:
        log.error(f"❌ Bluetooth volume get failed: {e}")
    return 0

def set_system_volume_bt(level_percent):
    sink = get_active_sink_name()
    if not sink:
        return
    try:
        level = max(0, min(level_percent, 100))
        subprocess.run(["pactl", "set-sink-volume", sink, f"{level}%"], check=True)
        log.info(f"🔊 Bluetooth volume set to {level}%")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Bluetooth volume set failed: {e}")

def increase_system_volume_bt():
    current = get_system_volume_bt()
    set_system_volume_bt(min(current + 10, 100))
    log.info("🔊 Increased Bluetooth volume.")

def decrease_system_volume_bt():
    current = get_system_volume_bt()
    set_system_volume_bt(max(current - 10, 0))
    log.info("🔉 Decreased Bluetooth volume.")

# =================== Local Sink Volume Control ===================

def get_system_volume_local():
    try:
        output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
        for line in output.splitlines():
            if "Volume:" in line:
                percent = line.split('/')[1].strip().replace('%', '')
                log.info(f"🔈 Local system volume: {percent}%")
                return int(percent)
    except Exception as e:
        log.error(f"❌ Local volume get failed: {e}")
    return 0

def set_system_volume_local(level_percent):
    try:
        level = max(0, min(level_percent, 100))
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
        log.info(f"🔊 Local volume set to {level}%")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Local volume set failed: {e}")

def increase_system_volume_local():
    current = get_system_volume_local()
    set_system_volume_local(min(current + 10, 100))
    log.info("🔊 Increased local volume.")

def decrease_system_volume_local():
    current = get_system_volume_local()
    set_system_volume_local(max(current - 10, 0))
    log.info("🔉 Decreased local volume.")

# =================== Playerctl Online Media Volume Control ===================

def get_player_volume_online(player):
    try:
        result = subprocess.check_output(["playerctl", "--player", player, "volume"]).decode().strip()
        vol_percent = round(float(result) * 100)
        log.info(f"🔈 {player} volume: {vol_percent}%")
        return vol_percent
    except Exception as e:
        log.error(f"❌ {player} volume get failed: {e}")
        return 0

def set_player_volume_online(player, level_percent):
    try:
        level = max(0, min(level_percent, 100)) / 100
        subprocess.run(["playerctl", "--player", player, "volume", str(level)], check=True)
        log.info(f"🔊 {player} volume set to {level_percent}%")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ {player} volume set failed: {e}")

def increase_player_volume_online(player):
    current = get_player_volume_online(player)
    set_player_volume_online(player, min(current + 10, 100))
    log.info(f"🔊 Increased {player} volume.")

def decrease_player_volume_online(player):
    current = get_player_volume_online(player)
    set_player_volume_online(player, max(current - 10, 0))
    log.info(f"🔉 Decreased {player} volume.")








    
#########################################################################################################################################
# ========== PLAYERCTL MUSIC CONTROLS ==========
# ========== INTERACTIVE MENU FOR PLAYER BOX CONTROL ==========


def play_media():
    try:
        subprocess.run(["playerctl", "play"], check=True)
        log.info("▶️ Playback started.")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Play failed: {e}")


def pause_media():
    try:
        subprocess.run(["playerctl", "pause"], check=True)
        log.info("⏸️ Playback paused.")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Pause failed: {e}")


def skip_track():
    try:
        subprocess.run(["playerctl", "next"], check=True)
        log.info("⏭️ Skipped to next track.")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Skip failed: {e}")


def previous_track():
    try:
        subprocess.run(["playerctl", "previous"], check=True)
        log.info("⏮️ Went to previous track.")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Previous track failed: {e}")


def Player_Box_MUSIC_CONTROL_Control():
    try:
        while True:
            log.info("\n===== 🎧 Media Control Options =====")
            log.info("1. ⏸️  Pause")
            log.info("2. ▶️  Play")
            log.info("3. ⏭️  Next Track")
            log.info("4. ⏮️  Previous Track")
            log.info("5. 🔊 Volume Up")
            log.info("6. 🔉 Volume Down")
            log.info("7. 🔈 Get Volume")
            log.info("8. ❌ Stop & Exit")
            choice = input("Select an option: ").strip()

            if choice == "1":
                pause_media()
            elif choice == "2":
                play_media()
            elif choice == "3":
                skip_track()
            elif choice == "4":
                previous_track()
            elif choice == "5":
                increase_system_volume_local()
            elif choice == "6":
                decrease_system_volume_local()
            elif choice == "7":
                vol = get_system_volume_local()
                log.info(f"🔈 Current Volume: {vol}%")
            elif choice == "8":
                log.info("❌ Exiting media control menu.")
                break
            else:
                log.warning("⚠️ Invalid option selected.")
    except Exception as e:
        log.error(f"❌ Media control error: {e}")



###############################################################################################################

# ========== OFFLINE MUSIC CONTROL USING PLAYERCTL ==========


def send_to_mpv(command):
    try:
        with open(mpv_fifo, 'w') as fifo:
            fifo.write(command + '\n')
    except Exception as e:
        log.error(f"Failed sending to mpv: {e}")

def next_track(music_dir):
    global current_index, music_playlist
    if current_index + 1 < len(music_playlist):
        current_index += 1
        send_to_mpv("quit")
        time.sleep(1)
        play_selected_track(music_dir, current_index)
    else:
        log.warning("Already at last track.")

def previous_track_local(music_dir):
    global current_index, music_playlist
    if current_index - 1 >= 0:
        current_index -= 1
        send_to_mpv("quit")
        time.sleep(1)
        play_selected_track(music_dir, current_index)
    else:
        log.warning("Already at first track.")

def play_selected_track(music_dir, index):
    global mpv_process
    file = os.path.join(music_dir, music_playlist[index])
    mpv_process = subprocess.Popen(
        ["mpv", "--input-file=" + mpv_fifo, file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    log.info(f"🎵 Now playing: {file}")

def list_and_play_local_music(music_dir="/home/engineer/Music"):
    global mpv_process, music_playlist, current_index

    try:
        music_playlist = [f for f in os.listdir(music_dir)
                          if f.lower().endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a'))]
        if not music_playlist:
            log.warning("No audio files found.")
            return

        log.info("🎶 Available tracks:")
        for idx, f in enumerate(music_playlist):
            log.info(f"{idx + 1}. {f}")

        choice = int(input("Enter track number: ")) - 1
        if not (0 <= choice < len(music_playlist)):
            log.warning("Invalid track selected.")
            return

        current_index = choice

        if not os.path.exists(mpv_fifo):
            os.mkfifo(mpv_fifo)

        play_selected_track(music_dir, current_index)

        while True:
            log.info("\n===== 🎧 Media Control Options =====")
            log.info("1. ⏸️  Pause")
            log.info("2. ▶️  Play")
            log.info("3. ⏭️  Next Track")
            log.info("4. ⏮️  Previous Track")
            log.info("5. 🔊 Volume Up")
            log.info("6. 🔉 Volume Down")
            log.info("7. 🔈 Volume GET")
            log.info("8. ❌ Stop & Exit")
            choice = input("Select an option: ").strip()

            if choice == "1":
                send_to_mpv("set pause yes")
            elif choice == "2":
                send_to_mpv("set pause no")
            elif choice == "3":
                next_track(music_dir)
            elif choice == "4":
                previous_track_local(music_dir)
            elif choice == "5":
                increase_system_volume_local()       # 🔁 Integrated system volume
            elif choice == "6":
                decrease_system_volume_local()     # 🔁 Integrated system volume
            elif choice == "7":
                get_system_volume_local()     # 🔁 Integrated system volume
            elif choice == "8":
                send_to_mpv("quit")
                log.info("🛑 Stopping playback.")
                break
            else:
                log.warning("⚠️ Invalid option.")

    except Exception as e:
        log.error(f"Playback error: {e}")
        if mpv_process:
            mpv_process.terminate()



# ##########################################################################################################
# # ========== ONLINE MUSIC CONTROL (PLAYERCTL) ==========######################################



ALLOWED_PLAYERS = ["spotify", "chrome", "firefox", "brave"]  # You can add "vlc", "opera", etc., if needed

def get_active_online_player():
    try:
        output = subprocess.check_output(["playerctl", "-l"]).decode().splitlines()
        for player in output:
            if any(allowed in player.lower() for allowed in ALLOWED_PLAYERS):
                return player
        log.warning("⚠️ No supported online media player found.")
        return None
    except Exception as e:
        log.error(f"❌ Failed to get player list: {e}")
        return None

def online_play(player):
    try:
        subprocess.run(["playerctl", "--player", player, "play"], check=True)
        log.info("▶️ Playing music.")
    except Exception as e:
        log.error(f"❌ Play error: {e}")

def online_pause(player):
    try:
        subprocess.run(["playerctl", "--player", player, "pause"], check=True)
        log.info("⏸️ Paused music.")
    except Exception as e:
        log.error(f"❌ Pause error: {e}")

def online_next(player):
    try:
        subprocess.run(["playerctl", "--player", player, "next"], check=True)
        log.info("⏭️ Next track.")
    except Exception as e:
        log.error(f"❌ Next track error: {e}")

def online_previous(player):
    try:
        subprocess.run(["playerctl", "--player", player, "previous"], check=True)
        log.info("⏮️ Previous track.")
    except Exception as e:
        log.error(f"❌ Previous track error: {e}")


def Online_Play_Music_Control():
    player = get_active_online_player()
    if not player:
        return

    try:
        while True:
            log.info("\n===== 🎧 Online Media Control Options =====")
            log.info("1. ⏸️  Pause")
            log.info("2. ▶️  Play")
            log.info("3. ⏭️  Next Track")
            log.info("4. ⏮️  Previous Track")
            log.info("5. 🔊 Volume Up")
            log.info("6. 🔉 Volume Down")
            log.info("7. 🔈 Volume GET")
            log.info("8. ❌ Stop & Exit")

            choice = input("Select an option: ").strip()

            if choice == "1":
                online_pause(player)
            elif choice == "2":
                online_play(player)
            elif choice == "3":
                online_next(player)
            elif choice == "4":
                online_previous(player)
            elif choice == "5":
                increase_player_volume_online(player)
            elif choice == "6":
                decrease_player_volume_online(player)
            elif choice == "7":
                get_player_volume_online(player)
            elif choice == "8":
                log.info("❌ Stopping media control.")
                break
            else:
                log.warning("⚠️ Invalid option.")

    except Exception as e:
        log.error(f"❌ Playback control error: {e}")
# ========== OPTIONAL TEST BLOCK ==========

if __name__ == "__main__":
    Player_Box_MUSIC_CONTROL_Control()
    list_and_play_local_music()
    Online_Play_Music_Control()