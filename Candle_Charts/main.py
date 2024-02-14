from datetime import datetime, timedelta
from Charts import Ploter
from Data import DataManager
import os
from Settings.Cleaner import clear_subdirectory
""""""""""""""""""""""""""""""""""""""""""
end_date = datetime.now()
start_date = (datetime.now() - timedelta(days=365))
data_catalog = os.getcwd() + f"/Data/csv/{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"

currencies = ["nokpln","usdpln","chfpln","gbppln","jpypln","eurpln", "cadpln", "audpln",
              "krwpln", "sekpln","cnypln","hufpln","nzdpln","dkkpln","iskpln"]

DataManager.download_data(currencies,start_date,end_date)
df_dictionary = DataManager.create_dataframe_dict(data_catalog)
Ploter.matrix_correlation(df_dictionary,start_date,end_date)
Ploter.candle_charts(df_dictionary,start_date,end_date,freq=30)

# clear_subdirectory(os.getcwd() + "/Data/csv")
# clear_subdirectory(os.getcwd() + "/Charts")


