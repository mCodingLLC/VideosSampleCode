import json
import pandas as pd

import plotly.express as px


def load_json(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)


def load_json_df(filename):
    j = load_json(filename)["benchmarks"]
    df = pd.DataFrame(j)
    df['real_time_micros'] = df['real_time'] / 1000
    df['real_time_millis'] = df['real_time'] / 1000000
    return df


def main():
    cache_df = load_json_df("cache_access_pattern.json")

    cache_access_df = cache_df[cache_df['name'].str.contains("Access")]
    fig = px.line(cache_access_df, x='bytes_used', y='real_time_millis', color='label', title="Sum times", markers=True,
                  labels=dict(bytes_used="bytes", real_time_millis="time (milliseconds)", label="Access type"))
    fig.show()

    mm_df = cache_df[cache_df['name'].str.contains("MatrixMultiply")]
    fig = px.bar(mm_df, x='label', y='real_time_micros', title="Matrix multiply times",
                 labels=dict(label="Loop order", real_time_micros='time (microseconds)'))
    fig.show()

    branch_df = load_json_df("branch_prediction.json")
    fig = px.line(branch_df, x='thresh', y='real_time', title="Branch predictability in product", markers=True,
                  labels=dict(thresh="Percent branch false", real_time='time (nanoseconds)'))
    fig.update_yaxes(range=[0, 3000])
    fig.show()

    sort_df = load_json_df("small_sorting_comparison.json")
    fig = px.line(sort_df, x='n', y='real_time_millis', color='label', title="Sorting General", markers=True,
                  labels=dict(n='vector size', real_time_millis='time (milliseconds)', label='Algorithm'))
    fig.show()

    small_size = 16
    fig = px.bar(sort_df[sort_df["n"] == small_size], x='label', y='real_time_micros', title=f"Sorting Small (size {small_size})",
                 labels=dict(label="Algorithm", real_time_micros='time (microseconds)'))
    fig.show()


if __name__ == '__main__':
    main()
