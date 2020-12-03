# Cat

import numpy as np
import pandas as pd
import seaborn as sns
import csv
import matplotlib.pyplot as plt


def make_cat_plot():
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14,10))

    with open('cat_weights.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        in_data = [row for row in reader]

    cat_data = list()
    for i in range(1,len(in_data)):
        cat = dict()
        for j in range(len(in_data[0])):
            cat[in_data[0][j]] = in_data[i][j]
        cat_data.append(cat)

    dates = pd.date_range("2020-11-2", periods=(len(cat_data[0])-1), freq="D")
    all_dates = [str(date)[0:10] for date in dates]
    none_dates = ['2020-11-03', '2020-11-05', '2020-11-09']
    new_dates = [date for date in all_dates]

    for date in none_dates:
        new_dates.remove(date)

    for cat in cat_data:
        for date in none_dates:
            cat[date] = None

    for cat in cat_data:
        for date in new_dates:
            cat[date] = float(cat[date])

    for i in range(len(cat_data)):
        for date in range(len(all_dates)):
            if cat_data[i][all_dates[date]] is None:  # If weight not taken that day, use average of adjacent weights
                cat_data[i][all_dates[date]] = (cat_data[i][all_dates[date-1]] + cat_data[i][all_dates[date+1]]) / 2

    values = list()
    for cat in cat_data:
        row = list()
        for date in all_dates:
            row.append(cat[date])
        values.append(row)
    values = np.array(values)
    values = values.transpose()

    data = pd.DataFrame(values, dates, columns=[row['foster_cat_plot'] for row in cat_data])
    data = data.fillna(value=np.nan)

    sns.lineplot(ax=ax, data=data, palette="tab10", linewidth=2.5)
    plt.ylabel("weight in lbs")
    plt.title("Foster kitties weight growth")
    plt.show()


if __name__ == '__main__':
    make_cat_plot()
