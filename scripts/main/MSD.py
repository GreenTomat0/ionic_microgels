import numpy as np
import pandas as pd




samples = [5, 4, 34, 3, 32, 2, 9, 8, 7, 6]


data = pd.DataFrame()

for s in samples:

	file_path = f'../../S{s}/data_out/backup/feb20_S{s}_EMSD.csv'
	
	data_temp = pd.read_csv(file_path)

	data_temp['sample'] = s

	data = pd.concat([data, data_temp])


# S5_15 = data[data['sample number'] == 5]
# S6_15 = data[data['sample number'] == 6]

# S5_15.to_csv('output_data/MSD_S5.csv')
# S6_15.to_csv('output_data/MSD_S6.csv')
