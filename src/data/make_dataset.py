import os
import pandas as pd
from glob import glob

# Read single CSV file (for testing/development)
# single_file_acc = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")
# single_file_gyr = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")

# List all data in data/raw/MetaMotion
data_path = "../../data/raw/MetaMotion/"
files = glob(os.path.join(data_path, "*.csv"))
print(f"Found {len(files)} files.")

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        # Extract features cleanly from filename prefix before '_MetaWear_'
        basename = os.path.basename(f)
        parts = basename.split("_MetaWear_")[0].split("-")
        
        participant = parts[0]
        label = parts[1]
        # Strip all trailing digits from category (e.g. medium1 -> medium, heavy2 -> heavy)
        category = parts[2].rstrip("0123456789")

        df = pd.read_csv(f)
        df["participants"] = participant
        df["labels"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df])

        elif "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df])

    # Convert index to datetime and clean columns
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    for df in [acc_df, gyr_df]:
        del df["epoch (ms)"]
        del df["time (01:00)"]
        del df["elapsed (s)"]

    return acc_df, gyr_df

# Read and process all files
acc_df, gyr_df = read_data_from_files(files)

# Print info
print("\nAccelerometer Data Info:")
acc_df.info()

print("\nGyroscope Data Info:")
gyr_df.info()

# Merging datasets


# Resample data (frequency conversion)

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# Export dataset
