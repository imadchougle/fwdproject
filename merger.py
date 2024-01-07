import pandas as pd


df_45_days = pd.read_csv('csv_files/D45_cycle.csv', index_col='stock')
df_15_days = pd.read_csv('csv_files/D15_cycle.csv', index_col='stock')

merged_df = pd.concat([df_45_days, df_15_days],
                      axis=1
                      # keys=['45_days', '15_days']
)

merged_df.to_csv('csv_files/merged_data_without_LTP.csv')

print("Done")
