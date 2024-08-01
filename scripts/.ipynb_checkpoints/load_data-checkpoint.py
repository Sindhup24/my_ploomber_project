# +
import pandas as pd

def run(product):
    df = pd.read_csv('/Users/sinugp/my_ploomber_project/fc_geoglows_random_20240429.csv')
    df.to_csv(product['data'], index=False)

if __name__ == "__main__":
    product = {
        'data': 'data/loaded_data.csv'
    }
    run(product)



