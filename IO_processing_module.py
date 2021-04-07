import pandas as pd

csv_file_path = "data.csv"


def read_form_csv():
    csv_data = pd.read_csv(csv_file_path, low_memory=False)
    csv_df = pd.DataFrame(csv_data)
    return csv_df


def write_to_csv(data):
    pass
