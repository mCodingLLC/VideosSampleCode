import numpy as np
import pandas as pd

# noinspection PyUnresolvedReferences
import janitor








company_sales = {
    'SalesMonth': ['Jan', 'Feb', 'Mar', 'Apr'],
    'Company1': [150.0, 200.0, 300.0, 400.0],
    'Company2': [180.0, 250.0, np.nan, 500.0],
    'Company3': [400.0, 500.0, 600.0, 675.0]
}


def pandas_way():
    df = pd.DataFrame.from_dict(company_sales)
    del df['Company1']
    df = df.dropna(subset=['Company2', 'Company3'])
    df = df.rename(
        {
            'Company2': 'Amazon',
            'Company3': 'Facebook',
        },
        axis=1,
    )
    df['Google'] = [450.0, 550.0, 800.0]
    print()
    print(df)


def pyjanitor_way():
    df = (
        pd.DataFrame.from_dict(company_sales)
            .remove_columns(["Company1"])
            .dropna(subset=["Company2", "Company3"])
            .rename_column("Company2", "Amazon")
            .rename_column("Company3", "Facebook")
            .add_column("Google", [450.0, 550.0, 800.0])
    )

    print()
    print(df)


def main():
    pyjanitor_way()


if __name__ == '__main__':
    main()



def thanks():
    ...














