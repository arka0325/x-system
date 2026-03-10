import os
import json
from datetime import datetime


class ReportStorage:

    def __init__(self, folder="reports"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def get_report_path(self, file_name):
        return os.path.join(self.folder, file_name)

    def save_report(self, brand_name, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_brand = brand_name.replace(" ", "_").lower()

        filename = f"{safe_brand}_{timestamp}.json"
        filepath = os.path.join(self.folder, filename)

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        return filepath

    def list_reports(self):
        return sorted(os.listdir(self.folder), reverse=True)

    def load_report(self, filename):
        filepath = os.path.join(self.folder, filename)
        with open(filepath, "r") as f:
            return json.load(f)
    
    def delete_report(self, filename):
        filepath = os.path.join(self.folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)