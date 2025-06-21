from wifi_function import scan_wifi
from wifi_function import connect_wifi, list_saved_networks, remove_saved_network
from logger_mod import logger

def main():
    print("=== Wi-Fi Automation Menu ===")
    print("1. Scan Available Networks")
    print("2. Connect to Wi-Fi")
    print("3. List Saved Networks")
    print("4. Remove Saved Network")
    print("0. Exit")

    while True:
        choice = input("\nEnter choice: ")

        if choice == "1":
            networks = scan_wifi()
            for i, (ssid, strength) in enumerate(networks, 1):
                print(f"{i}. {ssid} (Strength: {strength})")

        elif choice == "2":
            ssid = input("Enter SSID: ")
            pwd = input("Enter Password (leave blank if open network): ")
            success = connect_wifi(ssid, pwd or None)
            print("Connection Successful!" if success else "Failed to connect.")

        elif choice == "3":
            print("Saved Networks:")
            for ssid in list_saved_networks():
                print(f"- {ssid}")

        elif choice == "4":
            ssid = input("Enter SSID to remove: ")
            remove_saved_network(ssid)

        elif choice == "0":
            print("Exiting.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
