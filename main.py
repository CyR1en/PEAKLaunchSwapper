import os
import argparse

from swapper import PEAKLaunchSwapper

DEFAULT_STEAM_PATH = "C:\\Program Files (x86)\\Steam"

def restart_steam():
    os.system("taskkill /F /IM steam.exe")
    os.startfile(os.path.join(DEFAULT_STEAM_PATH, "steam.exe"))

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
    args = parser.parse_args()

    try:
        swapper = PEAKLaunchSwapper(args.path)
    except FileNotFoundError:
        print(f"appinfo.vdf not found at {args.path}")
        exit(1)

    swapper.print_current_launch_options()
    if args.print_only:
        exit(0)
    if args.revert:
        swapper.revert_original_launch_options()
    else:
        swapper.swap_launch_options()
    restart_steam()
