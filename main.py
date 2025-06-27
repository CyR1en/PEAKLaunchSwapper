import os
import sys
import argparse

from swapper import PEAKLaunchSwapper

DEFAULT_STEAM_PATH = "C:\\Program Files (x86)\\Steam"


def restart_steam(info_path):
    os.system("taskkill /F /IM steam.exe")
    steam_path = os.path.dirname(os.path.dirname(info_path))
    os.startfile(os.path.join(steam_path, "steam.exe"))


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
        sys.exit(1)

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

    restart_steam(args.path)
