import csv
import glob
from os.path import join


class County:
    def __init__(self, teryt, county_name):
        self.teryt = teryt
        self.county_name = county_name


counties = {}

# Sick data
sickPaths = glob.glob(
    r'/home/adrian/Pulpit/GitHub_Public/Covid_19/sick/*.csv')

for path in sickPaths:

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            try:
                tests = row['liczba_wykonanych_testow'] if row['liczba_wykonanych_testow'] != '' else 0
            except KeyError:
                tests = 0
            try:
                newSick = row['liczba_przypadkow'] if row['liczba_przypadkow'] != '' else 0
            except KeyError:
                newSick = row['liczba_nowych_zakazen'] if row['liczba_nowych_zakazen'] != '' else 0
            deaths = row['zgony'] if row['zgony'] != '' else 0
            try:
                countyName = row['powiat_miasto']
            except KeyError:
                countyName = row['powiat']
            teryt = row['teryt']

            try:
                counties[teryt].total_tests_performed += float(tests)
                counties[teryt].total_sick_count += float(newSick)
                counties[teryt].total_deaths += float(deaths)
            except KeyError:
                counties[teryt] = County(teryt, countyName)
                counties[teryt].total_tests_performed = float(tests)
                counties[teryt].total_sick_count = float(newSick)
                counties[teryt].total_deaths = float(deaths)

# Vacs data
vacsPaths = glob.glob(
    r'/home/adrian/Pulpit/GitHub_Public/Covid_19/vacs/*.csv')

for path in vacsPaths:
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            allDoses = float(row['liczba_szczepien_dziennie'])
            secondDose = float(row['dawka_2_dziennie'])
            teryt = row['teryt']
            if teryt != 't00':  # Omit the empty province
                try:
                    counties[teryt].allDoses += allDoses
                    counties[teryt].secondDose += secondDose
                    counties[teryt].days += 1
                except AttributeError:
                    counties[teryt].allDoses = allDoses
                    counties[teryt].secondDose = secondDose
                    counties[teryt].days = 1

# Code verification
# death_counter = 0
# for county in counties.values():
#     if county.teryt != 't0000':
#         death_counter += county.total_deaths

# print(death_counter)

# Preparing the list for recording
rows = []
for county in counties.values():
    countyRow = [county.county_name, county.teryt, county.allDoses, round(county.allDoses/county.days, 2), county.secondDose, round(county.secondDose/county.days, 2), county.total_tests_performed,
                 county.total_sick_count, county.total_deaths]
    rows.append(countyRow)

# Record of results
resultPath = join(
    r'/home/adrian/Pulpit/GitHub_Public/Covid_19', 'result.csv')

headers = ['county_name', 'teryt', 'vacs_total', 'vacs_daily_mean', 'vacs_2nd_dose_total', 'vacs_2nd_dose_daily_mean', 'total_tests_performed',
           'total_sick_count', 'total_deaths']

with open(resultPath, 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(headers)
    writer.writerows(rows)
