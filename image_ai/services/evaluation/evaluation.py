import os
import json
from datetime import datetime

# creates evaluation directory
from image_ai.config import EVALUATION_DIR

os.makedirs(EVALUATION_DIR, exist_ok=True)


# saves evaluation data
def save_evaluation(data, session_id):
    evaluation_file = os.path.join(EVALUATION_DIR, f"{session_id}.json")
    with open(evaluation_file, "w") as file:
        json.dump(data, file, indent=4)
