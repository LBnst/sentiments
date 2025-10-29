import pandas as pd
import re

INPUT_FILE = "twitter_training.csv"
OUTPUT_FILE = "clean_dataset.csv"

df = pd.read_csv(INPUT_FILE, header=None)

df = df[[df.columns[-1]]]

df.columns = ["message"]
df["message"] = df["message"].astype(str).str.strip()

#cleaning des messages
def is_valid_message(msg):
    msg = str(msg).strip()
    if not msg or msg.lower() == "nan":
        return False
    if not re.search(r"[a-zA-Z]", msg):
        return False
    if len(msg.split()) < 2:
        return False
    return True

df = df[df["message"].apply(is_valid_message)]

df["author"] = "unknown"
df["source"] = "twitter"
df = df[["author", "source", "message"]]

df.to_csv(OUTPUT_FILE, index=False)
print(df.head(5))