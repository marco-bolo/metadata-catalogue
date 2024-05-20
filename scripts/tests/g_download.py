import gdown
import pandas as pd

# URL of the Excel file in the shared Google Drive folder
google_drive_url = 'https://drive.google.com/file/d/1GjFiBIG964WXEogLzb89qhGGLFDLHy63/view?usp=sharing'
# Extract file ID from the Google Drive URL
file_id = google_drive_url.split('/')[-2]

# Download the file from Google Drive
output_file = 'scripts/tests/input/MARCO-BOLO_Metadata_Dataset_Record_WP4.xlsx'
gdown.download(f'https://drive.google.com/uc?id={file_id}', output_file, quiet=False)

# Read the Excel file into a DataFrame
df = pd.read_excel(output_file)

# Now you have your data in a DataFrame
print(df)