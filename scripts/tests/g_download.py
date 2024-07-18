import gdown
import pandas as pd

#google_drive_urls of WP's
MBO_WPs = {
    'WP2':'https://drive.google.com/file/d/1qfNib1599OQBJ2QrbAVrMVxbCwxMlAj3/view?usp=sharing',
    'WP3': 'https://drive.google.com/file/d/1D-YJbsiO3KOJyRUrEvUKZjpiOrhXXKcS/view?usp=sharing',
    'WP4':'https://drive.google.com/file/d/1GjFiBIG964WXEogLzb89qhGGLFDLHy63/view?usp=sharing',
    'WP5':'https://drive.google.com/file/d/1jH8Gp50y9w_SsoFELYTKV6ohPlkO3nqm/view?usp=sharing'
}

for wp,gd_url in MBO_WPs.items():
    # Extract file ID from the Google Drive URL
    file_id = gd_url.split('/')[-2]

    # Download the file from Google Drive
    output_file = f'input/MARCO-BOLO_Metadata_Dataset_Record_{wp}.xlsx'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output_file, quiet=False)

    # Read the specified Excel sheet into a DataFrame & save to csv
    descr_df = pd.read_excel(output_file, sheet_name='Datasets Description')
    descr_df.to_csv(f'input/MARCO-BOLO_Metadata_Dataset_Record_{wp}_description.csv', index=False)

    agent_df = pd.read_excel(output_file, sheet_name='Agent')
    agent_df.to_csv(f'input/MARCO-BOLO_Metadata_Dataset_Record_{wp}_agent.csv', index=False)
    # Now you have your data in a DataFrame
    #print(df)