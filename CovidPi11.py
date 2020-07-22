#! /usr/bin/python3
import requests
import pandas as pd
from datetime import datetime


# returns specific table from website
def get_website(my_url):
    html = requests.get(my_url).content
    data = pd.read_html(html)
    for df in data:
        if df.shape[0] > 200:
            my_df = df
            return my_df


def create_df():
    covid_url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic'
    pop_url = 'https://www.worldometers.info/world-population/population-by-country/'

    # the list of countries I decided to track
    my_countries = ['United States', 'Canada', 'Mexico', 'Italy', 'France', 'Germany', 'Spain', 'United Kingdom',
                    'Japan', 'South Korea', 'India', 'Philippines', 'Brazil', 'Venezuela', 'Peru', 'South Africa',
                    'Egypt', 'Nigeria', 'Ethiopia', 'Iran', 'Israel', 'Australia']

    covid_data = get_website(covid_url)
    pop_data = get_website(pop_url)

    # covid_data.columns[1] returns the name of the column even if it is changed on the website
    covid_data[covid_data.columns[1]] = covid_data[covid_data.columns[1]].str.split('[', expand=True)

    df_1 = covid_data.set_index(covid_data.columns[1])
    df_2 = pop_data.set_index('Country (or dependency)')

    covid_df = df_1.loc[:, [df_1.columns[1]]]
    covid_df.index.name = 'Countries'
    covid_df.columns = ['Cases']

    pop_df = df_2.loc[:, ['Population (2020)']]
    pop_df.index.name = 'Countries'
    pop_df.columns = ['Population']

    combo = covid_df.merge(pop_df, on='Countries', how='inner')

    # errors='coerce' ignores empty data in the tables
    combo['Cases'] = pd.to_numeric(combo['Cases'], downcast='float', errors='coerce')
    combo['Population'] = pd.to_numeric(combo['Population'], downcast='float', errors='coerce')
    combo['Rate'] = (combo['Cases'] / combo['Population']) * 100

    combo = combo[combo.index.isin(my_countries)]
    combo = combo.reindex(my_countries)

    final_list = combo['Rate'].tolist()
    return final_list


def write_file():
    with open('Covidiot2.csv', 'a') as file:
        rate_list = create_df()
        dt = datetime.now()
        file.write('\n')
        file.write(str(dt) + '\t')
        for rate in rate_list:
            file.write(str(rate) + '\t')


if __name__ == '__main__':
    try:
        write_file()
    except Exception as e:
        with open('err_time.csv', 'a') as err:
            err.write(f'{e}' + '\n' + str(datetime.now()) + '\n')
