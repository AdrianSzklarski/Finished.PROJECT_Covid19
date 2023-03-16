from module.json import JSON
import pandas as pd

if __name__ == '__main__':
    df = pd.read_json('/home/adrian/Pulpit/GitHub_Public/Covid_19/Covid19.json')
    print('The dataset below is as of 10-02-2023.')
    print(df)
    JSON(df)


