import os
import json
from appinfo import Appinfo


class PEAKLaunchSwapper:
    PEAK_APP_ID = 3527290
    APP_DIR = os.path.join(os.environ['LOCALAPPDATA'], 'PEAKLaunchSwapper')
    BACKUP_PATH = os.path.join(APP_DIR, 'launch_backup.json')

    def __init__(self, vdf_path):
        self.vdf_path = vdf_path
        self.appinfo = Appinfo(vdf_path, True, apps=[self.PEAK_APP_ID])
        os.makedirs(self.APP_DIR, exist_ok=True)

    def print_current_launch_options(self):
        launch_dict = self.appinfo.parsedAppInfo[self.PEAK_APP_ID]["sections"]["appinfo"]['config']['launch']
        print(json.dumps(launch_dict, indent=4))
        return launch_dict

    def swap_launch_options(self):
        self.backup_launch_options()
        launch_dict = self.appinfo.parsedAppInfo[self.PEAK_APP_ID]["sections"]["appinfo"]['config']['launch']
        obj5 = launch_dict["5"].copy()
        obj6 = launch_dict["6"].copy()

        launch_dict["5"] = {}
        launch_dict["6"] = {}

        launch_dict["5"] = obj6
        launch_dict["6"] = obj5

        launch_dict["5"]["type"] = "option1"
        launch_dict["6"]["type"] = "option2"
        self.save_changes()

    def backup_launch_options(self):
        launch_dict = self.appinfo.parsedAppInfo[self.PEAK_APP_ID]["sections"]["appinfo"]['config']['launch']

        if os.path.isfile(self.BACKUP_PATH):
            print(f"Backup file {self.BACKUP_PATH} already exists. Skipping backup.")

        with open(self.BACKUP_PATH, 'w', encoding='utf-8') as f:
            json.dump(launch_dict, f, indent=4)
        print(f"Backup of launch options saved to {self.BACKUP_PATH}")

    def save_changes(self):
        self.appinfo.update_app(self.PEAK_APP_ID)
        self.appinfo.write_data()
        print("Changes saved to appinfo.vdf")

    def revert_original_launch_options(self):
        if not os.path.isfile(self.BACKUP_PATH):
            print("No backup file found. Cannot revert.")
            return

        with open(self.BACKUP_PATH, 'r', encoding='utf-8') as f:
            backup_launch_dict = json.load(f)

        self.appinfo.parsedAppInfo[self.PEAK_APP_ID]["sections"]["appinfo"]['config']['launch'] = backup_launch_dict
        self.save_changes()
        print(f"Launch options reverted to original from {self.BACKUP_PATH}")
