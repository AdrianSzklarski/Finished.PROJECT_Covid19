from os.path import join
import glob
import csv


class County:
    def __init__(self, teryt, county_name, *args, **kwargs):
        self.teryt = teryt
        self.county_name = county_name
        self.counties = {}


class Covid(County):
    def __init__(self, teryt, county_name, *args, **kwargs):
        County.__init__(self, teryt, county_name, *args, **kwargs)
        # run modules
        self.get_links()
        self.get_sickPaths()
        self.get_vacsPaths()
        self.get_data()

    def get_links(self):
        self.sickPaths = glob.glob(
            r'/home/adrian/Pulpit/GitHub_Public/Covid_19/district/*.csv')
        self.vacsPaths = glob.glob(
            r'/home/adrian/Pulpit/GitHub_Public/Covid_19/vaccinations/*.csv')
        # Record of results
        self.resultPath = join(
            r'/home/adrian/Pulpit/GitHub_Public/Covid_19/result', 'result.csv')

    def get_sickPaths(self):

        for path in self.sickPaths:

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
                        self.counties[teryt].total_tests_performed += float(tests)
                        self.counties[teryt].total_sick_count += float(newSick)
                        self.counties[teryt].total_deaths += float(deaths)
                    except KeyError:
                        self.counties[teryt] = County(teryt, countyName)
                        self.counties[teryt].total_tests_performed = float(tests)
                        self.counties[teryt].total_sick_count = float(newSick)
                        self.counties[teryt].total_deaths = float(deaths)

    def get_vacsPaths(self):

        for path in self.vacsPaths:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    allDoses = float(row['liczba_szczepien_dziennie'])
                    secondDose = float(row['dawka_2_dziennie'])
                    teryt = row['teryt']
                    if teryt != 't00':  # Omit the empty province
                        try:
                            self.counties[teryt].allDoses += allDoses
                            self.counties[teryt].secondDose += secondDose
                            self.counties[teryt].days += 1
                        except AttributeError:
                            self.counties[teryt].allDoses = allDoses
                            self.counties[teryt].secondDose = secondDose
                            self.counties[teryt].days = 1

    def get_data(self):
        # Preparing the list for recording
        rows = []
        for county in self.counties.values():
            countyRow = [county.county_name, county.teryt, county.allDoses, round(county.allDoses / county.days, 2),
                         county.secondDose, round(county.secondDose / county.days, 2), county.total_tests_performed,
                         county.total_sick_count, county.total_deaths]
            rows.append(countyRow)

        headers = ['county_name', 'teryt', 'vacs_total', 'vacs_daily_mean', 'vacs_2nd_dose_total',
                   'vacs_2nd_dose_daily_mean', 'total_tests_performed',
                   'total_sick_count', 'total_deaths']

        with open(self.resultPath, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(headers)
            writer.writerows(rows)
