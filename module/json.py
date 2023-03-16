import seaborn as sns
import matplotlib.pyplot as plt


class JSON:
    def __init__(self, json):
        self.json = json
        self.get_info()
        self.get_statistic()
        self.get_tailAndhead()
        self.get_result()
        self.get_data_visualization()

    def get_info(self):
        info_rows = f'\n In this file are 15 rows and 14 columns: {self.json.shape}'
        info_data = f'\n In this file type of data present in the columns(int,object): {self.json.info()}'
        info_columns = f'\n Displaying all the column names present in data {self.json.columns}'
        return info_rows, info_data, info_columns

    def get_statistic(self):
        info_statistic = f'\nViewing the descriptive statistics of the data like mean, std deviation, ' \
                         f'min and max values present in the dataset: {self.json.describe()}'
        print(info_statistic)

    def get_tailAndhead(self):
        info_head = f'Display the first 4 rows: {self.json.head(4)}'
        info_tail = f'Display the last 6 rows : {self.json.tail(6)}'
        print(info_head, info_tail)
        return info_head, info_tail

    def get_result(self):
        result_active = f'\nThe total number of active cases in Poland: {self.json["active"].sum(axis=0)}'
        result_death = f'\nThe total number of deaths cases in Poland: {self.json["death"].sum(axis=0)}'
        result_positive = f'\nThe total number of positive cases in Poland: {self.json["positive"].sum(axis=0)}'
        result_cured = f'\nThe total number of cured cases in Poland: {self.json["cured"].sum(axis=0)}'
        result_new_active = f'\nThe total number of new_active cases in Poland: {self.json["new_active"].sum(axis=0)}'
        result_new_death = f'\nThe total number of new_death cases in Poland: {self.json["new_death"].sum(axis=0)}'
        result_new_positive = f'\nThe total number of new_positive cases in Poland: {self.json["new_positive"].sum(axis=0)}'
        result_new_cured = f'\nThe total number of new_cured cases in Poland: {self.json["new_cured"].sum(axis=0)}'
        print(result_active, result_death, result_positive, result_cured,
              result_new_active, result_new_death, result_new_positive, result_new_cured)
        return result_active, result_death, result_positive, result_cured, \
            result_new_active, result_new_death, result_new_positive, result_new_cured

    def get_data_visualization(self):
        # Plotting scatter plots of all data
        sns.pairplot(data=self.json)

        # Chart visualization
        my_data = [472, 117455, 11139697, 11021770]
        my_labels = 'Active', 'Positive', 'Cured', 'Death'
        my_explode = (0, 0.2, 0.1, 0.1)
        fig1, ax1 = plt.subplots(figsize=(13, 8))
        plt.pie(my_data, labels=my_labels, autopct='%1.1f%%', startangle=15, shadow=True, explode=my_explode)
        plt.axis('equal')

        # Chart visualization
        my_data = [472, 117455, 11139697, 11021770, 582, 98483, 11139848, 11027971]
        my_labels = 'Active', 'Positive', 'Cured', 'Death', 'New Active', 'New Positive', 'New Cured', 'New Death'
        my_explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 1.5)
        my_colors = ['gray', 'navajowhite', 'blanchedalmond', 'grey', 'lightblue', 'papayawhip', 'moccasin',
                     'lightpink']
        fig1, ax1 = plt.subplots(figsize=(13, 8))
        plt.pie(my_data, labels=my_labels, autopct='%1.1f%%', startangle=15, shadow=True, colors=my_colors,
                explode=my_explode)
        plt.axis('equal')
        plt.show()

        #  Number of active cases
        plt.figure(figsize=(13, 8))
        plt.xticks(rotation=90)
        sns.barplot(x='state_name', y='active', color='teal', data=self.json)
        plt.show()

        # Stacked bar plot
        self.json = self.json.set_index('state_name')
        self.json.plot.barh(stacked=True, figsize=(13, 8))
