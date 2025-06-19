import subprocess
import time
import os
from logger_mod import *

# Global variables for mpv (used in offline mode, not used here)
mpv_process = None
music_playlist = []
current_index = 0
mpv_fifo = "/tmp/mpv-fifo"



#########################################################################################################################################
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
                Volume_up()
            elif choice == "6":
                Volume_down()
            elif choice == "7":
                vol = get_player_volume()
                log.info(f"🔈 Current Volume: {vol}%")
            elif choice == "8":
                log.info("❌ Exiting media control menu.")
                break
            else:
                log.warning("⚠️ Invalid option selected.")
    except Exception as e:
        log.error(f"❌ Media control error: {e}")




###############################################################################################################################################
# ========== OFFLINE MUSIC CONTROL USING PLAYERCTL ===================================================================================

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
                Volume_up()       # 🔁 Integrated system volume
            elif choice == "6":
                Volume_down()     # 🔁 Integrated system volume
            elif choice == "7":
                get_player_volume()     # 🔁 Integrated system volume
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




###############################################################################################################################################
# ========== Online Media Control Options================================================================================================

ALLOWED_PLAYERS = ["spotify", "chrome", "firefox", "brave"]

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
            print("\n===== 🎧 Online Media Control Options =====")
            print("1. ⏸️  Pause")
            print("2. ▶️  Play")
            print("3. ⏭️  Next Track")
            print("4. ⏮️  Previous Track")
            print("5. 🔊 Volume Up")
            print("6. 🔉 Volume Down")
            print("7. 🔈 Volume GET")
            print("8. ❌ Stop & Exit")

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
                Volume_up()
            elif choice == "6":
                Volume_down()
            elif choice == "7":
                get_player_volume()
            elif choice == "8":
                log.info("❌ Stopping media control.")
                break
            else:
                log.warning("⚠️ Invalid option.")
    except Exception as e:
        log.error(f"❌ Playback control error: {e}")




###############################################################################################################################################
# ========== SYSTEM VOLUME CONTROL =====================================================================================================================
def get_active_sink_name():
    try:
        output = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode()
        for line in output.splitlines():
            if "bluez" in line or "a2dp" in line:
                sink_name = line.split()[1]
                log.info(f"🎧 Using Bluetooth sink: {sink_name}")
                return sink_name
        # fallback: return first available sink
        fallback = output.splitlines()[0].split()[1]
        log.warning(f"⚠️ Falling back to sink: {fallback}")
        return fallback
    except Exception as e:
        log.error(f"❌ Failed to detect sink: {e}")
        return "@DEFAULT_SINK@"  # fallback if detection fails

def get_volume():
    try:
        sink = get_active_sink_name()
        output = subprocess.check_output(["pactl", "list", "sinks"]).decode()
        sink_block = output.split(f"Name: {sink}")[1]
        for line in sink_block.splitlines():
            line = line.strip()
            if line.startswith("Volume:"):
                percent = line.split('/')[1].strip().replace('%', '')
                return int(percent)
    except Exception as e:
        log.error(f"❌ Get volume failed: {e}")
    return 0

def set_volume(level):
    try:
        sink = get_active_sink_name()
        level = max(0, min(level, 100))
        subprocess.run(["pactl", "set-sink-volume", sink, f"{level}%"], check=True)
        log.info(f"🔊 Volume set to {level}%")
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Set volume failed: {e}")

def Volume_up():
    current = get_volume()
    if current < 100:
        new_volume = min(current + 10, 100)
        set_volume(new_volume)
    else:
        log.info("🔊 Already at max volume.")

def Volume_down():
    current = get_volume()
    if current > 0:
        new_volume = max(current - 10, 0)
        set_volume(new_volume)
    else:
        log.info("🔉 Already at min volume.")

def get_player_volume():
    current = get_volume()
    log.info(f"🔈 Current system volume: {current}%")
    return current


if __name__ == "__main__":
    Player_Box_MUSIC_CONTROL_Control()
    list_and_play_local_music()
    Online_Play_Music_Control()