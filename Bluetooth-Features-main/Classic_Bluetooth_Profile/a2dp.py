# import subprocess
# import time
# from logger_mod import *
# import os 

# def connect_a2dp(device_mac):
#     """
#     Connect to Bluetooth device for A2DP.
#     """
#     try:
#         log.info(f"Connecting to A2DP device: {device_mac}")
#         subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
#         time.sleep(2)
#         log.info(f"Successfully connected to {device_mac}")
#         return True
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to connect to device: {device_mac}\n{e}")
#         return False

# def disconnect_a2dp(device_mac):
#     """
#     Disconnect from Bluetooth device.
#     """
#     try:
#         log.info(f"Disconnecting from A2DP device: {device_mac}")
#         subprocess.run(["bluetoothctl", "disconnect", device_mac], check=True)
#         time.sleep(1)
#         log.info(f"Disconnected from {device_mac}")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to disconnect from device: {device_mac}\n{e}")

# def play_media():
#     """
#     Play media using playerctl (Linux only).
#     """
#     try:
#         log.debug("Sending play command via playerctl...")
#         subprocess.run(["playerctl", "play"], check=True)
#         log.info("Media playback started.")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to play media.\n{e}")

# def pause_media():
#     """
#     Pause media using playerctl.
#     """
#     try:
#         log.debug("Sending pause command via playerctl...")
#         subprocess.run(["playerctl", "pause"], check=True)
#         log.info("Media paused.")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to pause media.\n{e}")

# def skip_track():
#     """
#     Skip to the next media track.
#     """
#     try:
#         log.debug("Sending next track command via playerctl...")
#         subprocess.run(["playerctl", "next"], check=True)
#         log.info("Skipped to next track.")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to skip track.\n{e}")

# def simulate_call_interrupt():
#     """
#     Simulate a call interruption by pausing media, waiting, and resuming.
#     """
#     try:
#         log.info("Simulating incoming call interruption...")
#         pause_media()
#         log.info("Simulating call duration...")
#         time.sleep(5)  # Simulate 5-second call
#         play_media()
#         log.info("Resumed media after simulated call.")
#     except Exception as e:
#         log.error(f"Failed during call simulation.\n{e}")

# def get_volume():
#     """
#     Get the current system volume (0-100 scale).
#     """
#     try:
#         output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
#         # Output format: 'Volume: front-left: 65536 / 100% / 0.00 dB, ...'
#         for line in output.splitlines():
#             if "Volume:" in line:
#                 percent = line.split('/')[1].strip().replace('%', '')
#                 log.debug(f"Current system volume: {percent}%")
#                 return int(percent)
#     except Exception as e:
#         log.error(f"Failed to get volume: {e}")
#         return 0  # Fallback default

# def set_volume(level):
#     """
#     Set the system volume.
#     Level is expected in range 0 to 10. It will be converted to 0-100%.
#     """
#     try:
#         volume_percent = max(0, min(level * 10, 100))  # Clamp between 0-100
#         log.debug(f"Setting system volume to {volume_percent}%")
#         subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{volume_percent}%"], check=True)
#         log.info(f"System volume set to {volume_percent}%")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to set volume.\n{e}")

# def previous_track():
#     """
#     Go to the previous media track.
#     """
#     try:
#         log.debug("Sending previous track command via playerctl...")
#         subprocess.run(["playerctl", "previous"], check=True)
#         log.info("Went to previous track.")
#     except subprocess.CalledProcessError as e:
#         log.error(f"Failed to go to previous track.\n{e}")


# # def list_and_play_local_music(music_dir="/home/engineer/Music"):
# #     """
# #     Lists files in the Music folder and allows selection for playback.
# #     """
# #     try:
# #         files = [f for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a'))]
# #         if not files:
# #             log.warning("No audio files found in the music directory.")
# #             return

# #         log.info("Available music files:")
# #         for idx, file in enumerate(files):
# #             print(f"{idx + 1}. {file}")

# #         choice = int(input("Enter the number of the file you want to play: ")) - 1
# #         if 0 <= choice < len(files):
# #             selected_file = os.path.join(music_dir, files[choice])
# #             log.info(f"Playing: {selected_file}")
# #             subprocess.Popen(["mpv", selected_file])  # You can replace `mpv` with `vlc`, `ffplay`, etc.
# #         else:
# #             log.warning("Invalid choice.")

# #     except Exception as e:
# #         log.error(f"Error during music selection or playback: {e}")




# mpv_process = None
# music_playlist = []
# current_index = 0
# mpv_fifo = "/tmp/mpv-fifo"

# def list_and_play_local_music(music_dir="/home/engineer/Music"):
#     """
#     Lists music files and plays them with control options.
#     """
#     global mpv_process, music_playlist, current_index

#     try:
#         # Get all audio files
#         music_playlist = [f for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a'))]
#         if not music_playlist:
#             log.warning("No music files found.")
#             return

#         # Show files to user
#         log.info("Available music files:")
#         for idx, file in enumerate(music_playlist):
#             print(f"{idx + 1}. {file}")

#         choice = int(input("Enter the number of the file to start playing: ")) - 1
#         if not (0 <= choice < len(music_playlist)):
#             log.warning("Invalid choice.")
#             return

#         current_index = choice

#         # Create FIFO if not exists
#         if not os.path.exists(mpv_fifo):
#             os.mkfifo(mpv_fifo)

#         # Launch mpv in slave mode with FIFO
#         selected_file = os.path.join(music_dir, music_playlist[current_index])
#         mpv_process = subprocess.Popen(
#             ["mpv", "--input-file=" + mpv_fifo, selected_file],
#             stdout=subprocess.DEVNULL,
#             stderr=subprocess.DEVNULL
#         )
#         log.info(f"Playing: {selected_file}")
#         time.sleep(1)

#         # Interactive control loop
#         while True:
#             print("\n===== 🎧 Media Control Options =====")
#             print("1. ⏸️  Pause")
#             print("2. ▶️  Play")
#             print("3. ⏭️  Skip (Next Track)")
#             print("4. ⏮️  Previous Track")
#             print("5. 🔊 Volume Up")
#             print("6. 🔉 Volume Down")
#             print("7. ❌ Stop & Exit")
#             choice = input("Select an option: ").strip()

#             if choice == "1":
#                 send_to_mpv("set pause yes")
#             elif choice == "2":
#                 send_to_mpv("set pause no")
#             elif choice == "3":
#                 next_track(music_dir)
#             elif choice == "4":
#                 previous_track(music_dir)
#             elif choice == "5":
#                 send_to_mpv("add volume 10")
#             elif choice == "6":
#                 send_to_mpv("add volume -10")
#             elif choice == "7":
#                 send_to_mpv("quit")
#                 log.info("Stopping playback.")
#                 break
#             else:
#                 log.warning("Invalid option.")

#     except Exception as e:
#         log.error(f"Error: {e}")
#         if mpv_process:
#             mpv_process.terminate()

# def send_to_mpv(command):
#     """
#     Sends a command to the mpv FIFO.
#     """
#     try:
#         with open(mpv_fifo, 'w') as fifo:
#             fifo.write(command + '\n')
#     except Exception as e:
#         log.error(f"Failed to send command to mpv: {e}")

# def next_track(music_dir):
#     """
#     Play next track in the playlist.
#     """
#     global current_index, music_playlist
#     if current_index + 1 < len(music_playlist):
#         current_index += 1
#         send_to_mpv("quit")
#         time.sleep(1)
#         next_file = os.path.join(music_dir, music_playlist[current_index])
#         subprocess.Popen(["mpv", "--input-file=" + mpv_fifo, next_file],
#                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         log.info(f"Playing: {next_file}")
#     else:
#         log.warning("Already at last track.")

# def previous_track(music_dir):
#     """
#     Play previous track in the playlist.
#     """
#     global current_index, music_playlist
#     if current_index - 1 >= 0:
#         current_index -= 1
#         send_to_mpv("quit")
#         time.sleep(1)
#         prev_file = os.path.join(music_dir, music_playlist[current_index])
#         subprocess.Popen(["mpv", "--input-file=" + mpv_fifo, prev_file],
#                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         log.info(f"Playing: {prev_file}")
#     else:
#         log.warning("Already at first track.")






import subprocess
import time
import os
from logger_mod import *

# Global variables for mpv handling
mpv_process = None
music_playlist = []
current_index = 0
mpv_fifo = "/tmp/mpv-fifo"

def connect_a2dp(device_mac):
    try:
        log.info(f"Connecting to A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "connect", device_mac], check=True)
        time.sleep(2)
        log.info(f"Successfully connected to {device_mac}")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to connect to {device_mac}: {e}")
        return False

def disconnect_a2dp(device_mac):
    try:
        log.info(f"Disconnecting from A2DP device: {device_mac}")
        subprocess.run(["bluetoothctl", "disconnect", device_mac], check=True)
        time.sleep(1)
        log.info(f"Disconnected from {device_mac}")
    except subprocess.CalledProcessError as e:
        log.error(f"Failed to disconnect: {e}")

def play_media():
    try:
        subprocess.run(["playerctl", "play"], check=True)
        log.info("Playback started.")
    except subprocess.CalledProcessError as e:
        log.error(f"Play failed: {e}")

def pause_media():
    try:
        subprocess.run(["playerctl", "pause"], check=True)
        log.info("Playback paused.")
    except subprocess.CalledProcessError as e:
        log.error(f"Pause failed: {e}")

def skip_track():
    try:
        subprocess.run(["playerctl", "next"], check=True)
        log.info("Skipped to next track.")
    except subprocess.CalledProcessError as e:
        log.error(f"Skip failed: {e}")

def previous_track():
    try:
        subprocess.run(["playerctl", "previous"], check=True)
        log.info("Went to previous track.")
    except subprocess.CalledProcessError as e:
        log.error(f"Previous track failed: {e}")

def get_volume():
    try:
        output = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode()
        for line in output.splitlines():
            if "Volume:" in line:
                percent = line.split('/')[1].strip().replace('%', '')
                return int(percent)
    except Exception as e:
        log.error(f"Get volume failed: {e}")
    return 0

def set_volume(level):
    try:
        level = max(0, min(level * 10, 100))
        subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"], check=True)
        log.info(f"Volume set to {level}%")
    except subprocess.CalledProcessError as e:
        log.error(f"Set volume failed: {e}")

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
    log.info(f"Now playing: {file}")

def list_and_play_local_music(music_dir="/home/engineer/Music"):
    global mpv_process, music_playlist, current_index

    try:
        music_playlist = [f for f in os.listdir(music_dir)
                          if f.lower().endswith(('.mp3', '.wav', '.aac', '.flac', '.m4a'))]
        if not music_playlist:
            log.warning("No audio files found.")
            return

        log.info("Available tracks:")
        for idx, f in enumerate(music_playlist):
            print(f"{idx + 1}. {f}")

        choice = int(input("Enter track number: ")) - 1
        if not (0 <= choice < len(music_playlist)):
            log.warning("Invalid track selected.")
            return

        current_index = choice

        if not os.path.exists(mpv_fifo):
            os.mkfifo(mpv_fifo)

        play_selected_track(music_dir, current_index)

        while True:
            print("\n===== 🎧 Media Control Options =====")
            print("1. ⏸️  Pause")
            print("2. ▶️  Play")
            print("3. ⏭️  Next Track")
            print("4. ⏮️  Previous Track")
            print("5. 🔊 Volume Up")
            print("6. 🔉 Volume Down")
            print("7. ❌ Stop & Exit")
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
                send_to_mpv("add volume 10")
            elif choice == "6":
                send_to_mpv("add volume -10")
            elif choice == "7":
                send_to_mpv("quit")
                log.info("Stopping playback.")
                break
            else:
                log.warning("Invalid option.")

    except Exception as e:
        log.error(f"Playback error: {e}")
        if mpv_process:
            mpv_process.terminate()

