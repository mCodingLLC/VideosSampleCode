from __future__ import annotations

import dataclasses
from collections.abc import Iterator, Mapping
from typing import TypeVar, overload

_K = TypeVar('_K')

_V1 = TypeVar('_V1')
_V2 = TypeVar('_V2')
_V3 = TypeVar('_V3')


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
) -> Iterator[tuple[_K, _V1]]:
    ...


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
        m2: Mapping[_K, _V2],
) -> Iterator[tuple[_K, _V1, _V2]]:
    ...


@overload
def dict_zip(
        m1: Mapping[_K, _V1],
        m2: Mapping[_K, _V2],
        m3: Mapping[_K, _V3],
) -> Iterator[tuple[_K, _V1, _V2, _V3]]:
    ...


def dict_zip(*dicts):
    if not dicts:
        return

    n = len(dicts[0])
    if any(len(d) != n for d in dicts):
        raise ValueError('arguments must have the same length')

    for key, first_val in dicts[0].items():
        yield key, first_val, *(other[key] for other in dicts[1:])


def dict_zip_intersection(*dicts):
    if not dicts:
        return

    keys = set(dicts[0]).intersection(*dicts[1:])
    for key in keys:
        yield key, *(d[key] for d in dicts)


def dict_zip_union(*dicts, fillvalue=None):
    if not dicts:
        return

    keys = set(dicts[0]).union(*dicts[1:])
    for key in keys:
        yield key, *(d.get(key, fillvalue) for d in dicts)


def combined_dict_example():
    @dataclasses.dataclass
    class ChannelData:
        id: str
        name: str
        sub_count: int

    channels = [
        ChannelData(id="UCaiL2GDNpLYH6Wokkk1VNcg", name="mCoding", sub_count=122_000),
        ChannelData(id="UC7_gcs09iThXybpVgjHZ_7g", name="PBS Space Time", sub_count=2_630_000),
        ChannelData(id="UCxHAlbZQNFU2LgEtiqd2Maw", name="Cᐩᐩ Weekly With Jason Turner", sub_count=85_000),
    ]

    data = {channel.id: channel for channel in channels}

    for cid, channel in data.items():
        print(f'{channel.name} has {channel.sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def separate_dicts_example_1():
    names = {"UCaiL2GDNpLYH6Wokkk1VNcg": "mCoding",
             "UC7_gcs09iThXybpVgjHZ_7g": "PBS Space Time",
             "UCxHAlbZQNFU2LgEtiqd2Maw": "Cᐩᐩ Weekly With Jason Turner"}
    sub_counts = {"UCaiL2GDNpLYH6Wokkk1VNcg": 122_000,
                  "UC7_gcs09iThXybpVgjHZ_7g": 2_630_000,
                  "UCxHAlbZQNFU2LgEtiqd2Maw": 85_000}

    for cid in names:
        name = names[cid]
        sub_count = sub_counts[cid]
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def separate_dicts_example_2():
    names = {"UCaiL2GDNpLYH6Wokkk1VNcg": "mCoding",
             "UC7_gcs09iThXybpVgjHZ_7g": "PBS Space Time",
             "UCxHAlbZQNFU2LgEtiqd2Maw": "Cᐩᐩ Weekly With Jason Turner"}
    sub_counts = {"UCaiL2GDNpLYH6Wokkk1VNcg": 122_000,
                  "UC7_gcs09iThXybpVgjHZ_7g": 2_630_000,
                  "UCxHAlbZQNFU2LgEtiqd2Maw": 85_000}

    for cid, name in names.items():
        sub_count = sub_counts[cid]
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def separate_dicts_example_3():
    names = {"UCaiL2GDNpLYH6Wokkk1VNcg": "mCoding",
             "UC7_gcs09iThXybpVgjHZ_7g": "PBS Space Time",
             "UCxHAlbZQNFU2LgEtiqd2Maw": "Cᐩᐩ Weekly With Jason Turner"}
    sub_counts = {"UCaiL2GDNpLYH6Wokkk1VNcg": 122_000,
                  "UC7_gcs09iThXybpVgjHZ_7g": 2_630_000,
                  "UCxHAlbZQNFU2LgEtiqd2Maw": 85_000}

    for cid, name, sub_count in dict_zip(names, sub_counts):
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def plain_zip_example():
    ids = ["UCaiL2GDNpLYH6Wokkk1VNcg", "UC7_gcs09iThXybpVgjHZ_7g", "UCxHAlbZQNFU2LgEtiqd2Maw"]
    names = ["mCoding", "PBS Space Time", "Cᐩᐩ Weekly With Jason Turner"]
    sub_counts = [122_000, 2_630_000, 85_000]

    for cid, name, sub_count in zip(ids, names, sub_counts, strict=True):
        print(f'{name} has {sub_count} subscribers! Watch here: youtube.com/channel/{cid}')


def main() -> None:
    combined_dict_example()
    separate_dicts_example_1()
    plain_zip_example()
    separate_dicts_example_2()
    separate_dicts_example_3()


if __name__ == '__main__':
    main()
