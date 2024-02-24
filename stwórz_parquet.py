import os
import pandas as pd

def stworz_parquet():
    main_directory = os.getcwd()
    specified_dirs = ['Płachta godzinowa', 'Profile', 'Strefy']

    for specified_dir in specified_dirs:
        specified_path = os.path.join(main_directory, specified_dir)
        if os.path.exists(specified_path):
            for root, dirs, files in os.walk(specified_path):
                for file in files:
                    if file.endswith('.xlsx'):
                        excel_path = os.path.join(root, file)
                        parquet_subfolder = os.path.join(root, 'Parquet_Files')
                        if not os.path.exists(parquet_subfolder):
                            os.mkdir(parquet_subfolder)
                        df = pd.read_excel(excel_path)
                        parquet_path = os.path.join(parquet_subfolder, file.replace('.xlsx', '.parquet'))
                        df.to_parquet(parquet_path, index=False)

    print("Wszystkie pliki zostały przetworzone.")

if __name__ == '__main__':
    stworz_parquet()

