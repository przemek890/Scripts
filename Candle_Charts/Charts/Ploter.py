import seaborn as sns
import pandas as pd
import plotly.io as pio
from plotly.graph_objs import Candlestick, Figure
import matplotlib.pyplot as plt
from plotly.graph_objs import Scatter
from PIL import Image
import os
""""""""""""""
def matrix_correlation(df_dict,start,end):

    if len(df_dict) < 2: return
    new_df = pd.DataFrame()
    for currency, df in df_dict.items():
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        filtered_df = df[(df.index >= start) & (df.index <= end)]

        new_df[f'{currency}'] = (filtered_df['Open'] + filtered_df['Close']) / 2

    correlation_matrix = new_df.corr()
    plt.figure(figsize=(16, 16))
    sns.set(font_scale=1)

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True)
    plt.title(f'Exchange rate correlation from {start.date()} to {end.date()}')

    if not os.path.exists(os.getcwd() + f"/Charts/{start.date()}_{end.date()}"):
        os.makedirs(os.getcwd() + f"/Charts/{start.date()}_{end.date()}")

    plt.savefig(os.getcwd() + f"/Charts/{start.date()}_{end.date()}_Correlation_matrix.pdf")
    plt.show()
    plt.close()
def candle_charts(df_dict, start, end, freq):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    dates = pd.date_range(start, end, freq=f'{freq}D')

    for currency, df in df_dict.items():
        df = df.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        prev_days = None

        for i in range(len(dates) - 1):
            start_date = dates[i]
            end_date = dates[i + 1]
            df_time = df[(df.index >= start_date) & (df.index < end_date)]

            df_time = pd.concat([prev_days, df_time])

            df_time = df_time[df_time.index.dayofweek < 5]

            if len(df_time) == 0:
                continue

            fig = Figure(data=[Candlestick(x=df_time.index.astype(str),
                                           open=df_time['Open'],
                                           high=df_time['High'],
                                           low=df_time['Low'],
                                           close=df_time['Close'])])

            fig.update_layout(xaxis_rangeslider_visible=False,
                              xaxis=dict(
                                  type='category',
                                  range=[df_time.index.min().strftime('%Y-%m-%d'),
                                         df_time.index.max().strftime('%Y-%m-%d')],
                                  showticklabels=False,
                                  autorange=True,
                              ),
                              yaxis_range=[df_time['Low'].min(), df_time['High'].max()])

            # fig.add_trace(Scatter(x=df_time.iloc[1:].index.astype(str), y=ma, mode='lines', name='MA',
            #                       line=dict(color='black', width=1), opacity=0.5))

            directory = os.path.join(os.getcwd(), f"Charts/{start.date()}_{end.date()}")
            if not os.path.exists(directory):
                os.makedirs(directory)

            last_close_price = df_time['Close'].iloc[-1]

            future_prices = df.loc[df.index > end_date, 'Close']
            if len(future_prices) > 4:
                future_close_price = future_prices.iloc[4]
                X = 1 if future_close_price > last_close_price else 0
                output_path = os.path.join(directory, f"Candlestick_{currency}_{start_date.date()}_{end_date.date()}_{X}.png")
                pio.write_image(fig, output_path, scale=3)

                img = Image.open(output_path)

                left = 240
                top = 300
                right = img.width - 240
                bottom = img.height - 240

                img_cropped = img.crop((left, top, right, bottom))
                img_cropped.save(output_path)


    print("Charts have been saved.")
