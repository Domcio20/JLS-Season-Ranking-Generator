import json
import re
import pandas as pd
from os import listdir
from os.path import isfile, join

punkty = {"points": [100, 80, 60, 50, 45, 40, 36, 32, 29, 26, 24, 22, 20, 18, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
          "place": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 23, 25, 26, 27, 28, 29, 30]}
punktacja = pd.DataFrame(punkty)


def date_checker(string, start_year, end_year, start_month, end_month):
    if start_month < 10:
        start_month = '0'+str(start_month)

    if end_month < 10:
        end_month = '0'+str(end_month)

    if str(start_year)+'.'+str(start_month)+'.'+'01' <= string <= str(end_year)+'.'+str(end_month)+'.'+'31':
        return True
    return False


def funkcja(mypath, start_year, end_year, start_month, end_month, name):
    onlyfiles = [f for f in listdir(mypath) if f.endswith(".ndjson")]

    table = pd.DataFrame(columns=['player'])

    for file in onlyfiles:
        f = open(mypath + '/' + file)

        date = re.search(r"....\...\...", file)[0]

        if date_checker(date, start_year, end_year, start_month, end_month):
            data = pd.read_json(mypath + '/' + file, lines = True)

            data_points = data.merge(punktacja, left_on='rank', right_on='place')

            table[date] = {}

            for points, user in zip(data_points['points_y'], data_points['username']):
                if user not in table['player'].values:
                    table.loc[len(table.index)] = {'player': user, date: points}
                else:
                    table.loc[table['player'] == user, date] = points

        f.close()

    table.fillna(0, inplace=True)

    table['SUMA'] = table.sum(axis=1, numeric_only=True)
    table.sort_values(by='SUMA', ascending=False, inplace=True)

    excel_path = join(mypath, f"{name}.xlsx")
    table.to_excel(excel_path, index=False)

funkcja(mypath = "", start_year = 2025, end_year = 2026, start_month = 8, end_month=6, name="")