import pandas as pd
import os
from datetime import datetime

class DetectionResultsSaver:
    def __init__(self, filename="detection_results.xlsx"):
        self.filename = filename
        self.results = []

    def add_result(self, timestamp, emotion, confidence, concentration):
        self.results.append({
            "Timestamp": timestamp,
            "Emotion": emotion,
            "Confidence (%)": confidence,
            "Concentration (%)": concentration
        })

    def save_to_excel(self):
        df = pd.DataFrame(self.results)
        if os.path.exists(self.filename):
            # Append to existing file
            with pd.ExcelWriter(self.filename, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                # Write to a new sheet with timestamp to avoid overwriting
                sheet_name = datetime.now().strftime("Results_%Y%m%d_%H%M%S")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        else:
            df.to_excel(self.filename, index=False)
