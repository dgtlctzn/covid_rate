#! /usr/bin/python3
import requests
import pandas as pd
from datetime import datetime


def create_df():

    # creates covid df from json
    web_df = requests.get('https://covid.ourworldindata.org/data/owid-covid-data.json')
    covid_df = pd.read_json(web_df.content)
    covid_dict = {}
    for i in range(0, covid_df.shape[1]):
        if 'total_cases' in covid_df.loc['data', :][i][-1]:
            covid_dict[covid_df.loc['location', :][i]] = covid_df.loc['data', :][i][-1]['total_cases']
    covid_df = pd.DataFrame.from_dict(covid_dict, orient='index', columns=['Total Cases'])

    # creates population df from web
    pop_url = 'https://www.worldometers.info/world-population/population-by-country/'
    html = requests.get(pop_url).content
    pop_data = pd.read_html(html)
    pop_data = pop_data.set_index('Country (or dependency)')
    pop_df = pop_data.loc[:, ['Population (2020)']]
    pop_df.index.name = 'Countries'
    pop_df.columns = ['Population']

    combo = covid_df.merge(pop_df, on='Countries', how='inner')
    combo['Rate'] = (combo['Total Cases'] / combo['Population']) * 100

    my_countries = ['United States', 'Canada', 'Mexico', 'Italy', 'France', 'Germany', 'Spain', 'United Kingdom',
                    'Japan', 'South Korea', 'India', 'Philippines', 'Brazil', 'Venezuela', 'Peru', 'South Africa',
                    'Egypt', 'Nigeria', 'Ethiopia', 'Iran', 'Israel', 'Australia']

    combo = combo[combo.index.isin(my_countries)]
    combo = combo.reindex(my_countries)

    final_list = combo['Rate'].tolist()
    return final_list


def write_file():
    with open('/home/pi/PiPy/Covidiot2.csv', 'a') as file:
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
        with open('/home/pi/PiPy/err_time.csv', 'a') as err:
            err.write(f'{e}' + '\n' + str(datetime.now()) + '\n')
