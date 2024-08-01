# +
import pandas as pd

def run(upstream, product):
    df = pd.read_csv(upstream['load_data']['data'])
    filtered_df = df  # Example: no filtering for now
    filtered_df.to_csv(product['data'], index=False)

if __name__ == "__main__":
    upstream = {
        'load_data': {
            'data': 'data/loaded_data.csv'
        }
    }
    product = {
        'data': 'data/filtered_data.csv'
    }
    run(upstream, product)



