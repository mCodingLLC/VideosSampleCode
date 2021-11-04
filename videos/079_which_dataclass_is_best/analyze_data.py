import json
import pandas as pd
import plotly.express as px
from dataclasses_comparison import support_keys
import plotly.graph_objects as go


def cases_to_df(data):
    dfs = (pd.DataFrame.from_records(data=val, index='name', columns=['name', key]) for key, val in data.items())
    df = pd.concat(dfs, axis='columns')
    df = df.sort_index()
    return df


def make_plots(df):
    print(df.index)
    fig = px.bar(df[['create', 'getattr', 'setattr']], labels=dict(value='time (ns)'))
    fig.show()

    fig = px.bar(df['mem'], labels=dict(value='mem (bytes)'))
    fig.show()

    sdf = df[support_keys].reset_index()
    def TF(v):
        if v is True:
            return 'T'
        if v is False:
            return 'F'
        return v

    sdf = sdf.applymap(TF)
    sdf = sdf[~sdf['name'].str.contains('slots')]

    colors = {'T': '#79DE79', 'F': '#FB6962'}
    fig = go.Figure(data=[go.Table(
        header=dict(values=[s.removeprefix("supports_").replace("_", " ") for s in sdf.columns],
                    fill_color="lavender",
                    align='center'),
        cells=dict(values=sdf.transpose().values.tolist(),
                   align='center',
                   fill_color=['lavender']+[[colors.get(v, '#FCFC99') for v in l] for l in sdf.transpose().values.tolist()[1:]],
                   line_color="white",
                   ),
        columnwidth=[1.5] + [1]*(len(sdf.columns)-1),
    )])
    fig.show()


def main():
    with open('results.out', 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = cases_to_df(data)
    make_plots(df)


if __name__ == '__main__':
    main()
