import os
import sys
import argparse
import hashlib
import subprocess

from swapper import PEAKLaunchSwapper

DEFAULT_STEAM_PATH = "C:\\Program Files (x86)\\Steam"
MD5_LOG_FILE = "MD5.txt"

def generate_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(4096):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        return f"Error generating MD5: {e}"

def log_md5(label, md5_hash):
    try:
        with open(MD5_LOG_FILE, "a") as f:
            f.write(f"{label}: {md5_hash}\n")
    except Exception as e:
        print(f"Could not log MD5: {e}")

def restart_steam(info_path):
    try:
        # Run taskkill and capture output
        result = subprocess.run(
            ["taskkill", "/F", "/IM", "steam.exe"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Closed Steam Successfully")
        else:
            print("Failed to close Steam. Process is not likely open.")
        steam_path = os.path.dirname(os.path.dirname(info_path))
        os.startfile(os.path.join(steam_path, "steam.exe"))
        print("Steam restarted successfully.")
    except Exception as e:
        print(f"Failed to restart Steam: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Swap or revert PEAK launch options in appinfo.vdf")
    parser.add_argument(
        "-p", "--path",
        type=str,
        default=os.path.join(DEFAULT_STEAM_PATH, "appcache", "appinfo.vdf"),
        help="Path to appinfo.vdf"
    )
    parser.add_argument(
        "-r", "--revert",
        action="store_true",
        help="Revert launch options to backup"
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="Only print the current launch options and exit"
    )
    parser.add_argument(
        "--md5",
        action="store_true",
        help="Log MD5 hash before and after changes to MD5.txt"
    )
    args = parser.parse_args()

    path = args.path

    # Clear MD5.txt at the start if logging is enabled
    if args.md5 and os.path.exists(path):
        try:
            open(MD5_LOG_FILE, "w").close()
        except Exception as e:
            print(f"Failed to clear MD5 log file: {e}")

    while True:
        try:
            if args.md5 and os.path.exists(path):
                md5_before = generate_md5(path)
                log_md5("Initial MD5", md5_before)

            swapper = PEAKLaunchSwapper(path)
            break
        except FileNotFoundError:
            path = input(f"appinfo.vdf not found at {args.path}, input the correct path, or type X to exit: ")
            if path.lower() == 'x':
                print("Exiting...")
                sys.exit(0)
            try:
                path = os.path.join(path, "appcache", "appinfo.vdf")
            except:
                print("Invalid path format. Exiting.")
                sys.exit(0)

    print("Current launch options:")
    swapper.print_current_launch_options()

    if args.print_only:
        sys.exit(0)

    if args.revert:
        swapper.revert_original_launch_options()
        print("Reverted to original launch options:")
        swapper.print_current_launch_options()
    else:
        swapper.swap_launch_options()
        print("New launch options:")
        swapper.print_current_launch_options()

    if args.md5 and os.path.exists(path):
        md5_after = generate_md5(path)
        log_md5("Final MD5", md5_after)

    restart_steam(path)
