# import plotext as plt

import matplotlib.pyplot as plt


def bar_plot(freq_map: dict[str, int]):
    x, y = _sanitize(freq_map)
    plt.bar(x, y)
    plt.tight_layout(pad=0.05)
    plt.show()


def _sanitize(freq_map: dict[str, int]):
    freq_list = sort_list_of_tuple(list(freq_map.items()))
    x, y = [ngram for ngram, _ in freq_list], [freq for _, freq in freq_list]
    return x, y


# def _threshold(freq_map, threshold) -> dict[str, int]:
#     freq_list = sort_list_of_tuple(list(freq_map.items()))
#     result = dict({})
#     for x, y in freq_list:
#         if y > threshold:
#             result[x] = y


def sort_list_of_tuple(list_of_tuple) -> tuple:
    lst = len(list_of_tuple)
    for x in range(0, lst):
        for y in range(0, lst - x - 1):
            if list_of_tuple[y][1] < list_of_tuple[y + 1][1]:
                temp = list_of_tuple[y]
                list_of_tuple[y] = list_of_tuple[y + 1]
                list_of_tuple[y + 1] = temp
    return list_of_tuple
