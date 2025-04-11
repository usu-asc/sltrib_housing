import pandas as pd
import os
import camelot

# Path to your PDF file
path = os.path.dirname(__file__)

pdf = "\\UAR_01_2025.pdf"

pdf_path = path+pdf

# First try using the 'lattice' flavor for bordered tables
tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')

# If no tables were found with lattice, try the 'stream' flavor
if len(tables) == 0:
    print("No tables detected using lattice method; switching to stream mode.")
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

if tables:
    df_list = []
    for i, table in enumerate(tables, start=1):
        # Each table is extracted as a dataframe
        print(f"Extracted table {i} with shape {table.df.shape}")
        df_list.append(table.df)
    
    # Concatenate all tables into one DataFrame
    final_df = pd.concat(df_list, ignore_index=True)
    print("Final concatenated DataFrame preview:")
    print(final_df.head())
    
    # Optionally, save the DataFrame to a CSV file:
    final_df.to_csv("extracted_data.csv", index=False)
else:
    print("No tables were extracted from the PDF.")
