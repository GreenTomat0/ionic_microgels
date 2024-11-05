import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




temperature = [18, 25, 27, 29, 31, 33]


data = pd.DataFrame()

for t in temperature:

	file_path = f'../../S6nwT{t}/data_out/backup/S6T{t}_EMSD.csv'
	
	data_temp = pd.read_csv(file_path)

	data_temp['temperature'] = t

	data = pd.concat([data, data_temp])


# print(data)