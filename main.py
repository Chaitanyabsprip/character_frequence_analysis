import json
import os
import re

from display import bar_plot

DATE_REGEX = "\\d{2}:\\d{2}:\\d{2}"
SPECIAL_KEYS_REGEX = "(\\[\\[??[^\\[]*?\\])"


def main():
    logs = stringify(remove_unwanted_line(get_log_data()))
    # no_of_special_keys = len(re.findall(SPECIAL_KEYS_REGEX, logs))
    # print(no_of_special_keys)
    logs = re.sub(SPECIAL_KEYS_REGEX, "", logs)
    logs = logs.replace(" ", "")
    single_char_freq_map = remove_repeated_letters(
        get_ngram_frequency_map(logs, 1)
    )
    bigram_freq_map = remove_repeated_letters(get_ngram_frequency_map(logs, 2))
    sorted_bigram_freq_map = dict(
        sorted(bigram_freq_map.items(), key=lambda item: item[1])
    )
    trigram_freq_map = remove_repeated_letters(get_ngram_frequency_map(logs, 3))
    tetragram_freq_map = remove_repeated_letters(
        get_ngram_frequency_map(logs, 4)
    )
    save_as_json(single_char_freq_map, "character_frequency.json")
    save_as_json(sorted_bigram_freq_map, "bigram_frequency.json")
    save_as_json(trigram_freq_map, "trigram_frequency.json")
    save_as_json(tetragram_freq_map, "tetragram_frequency.json")
    bar_plot(single_char_freq_map)
    bar_plot(dict(list(bigram_freq_map.items())[:30]))
    bar_plot(dict(list(trigram_freq_map.items())[:30]))
    bar_plot(dict(list(tetragram_freq_map.items())[:30]))


def save_as_json(freq_map: dict[str, int], filename: str):
    with open(
        os.getenv("HOME", "/Users/chaitanyasharma") + "/.cache/" + filename,
        "w+",
        encoding="UTF-8",
    ) as file:
        json.dump(freq_map, file)


def remove_repeated_letters(frequency_map: dict[str, int]):
    freq_map = dict({})
    for x in frequency_map:
        if len(set(x)) == len(x):
            freq_map[x] = frequency_map[x]
    return freq_map


def get_ngram_frequency_map(logs: str, n: int):
    frequency_map = dict({})
    for index in range(len(logs)):
        if index < n - 1:
            continue
        ngram = ""
        for i in range(n):
            ngram += logs[index - i]
        val = frequency_map.get(ngram, 0)
        frequency_map[ngram] = val + 1
    return frequency_map


def stringify(logs: list[str]):
    data = ""
    for line in logs:
        data += line
    return data


def remove_unwanted_line(logs: list[str]):
    data = []
    for line in logs:
        date_line = re.search(DATE_REGEX, line)
        if (
            date_line is not None
            or "Keystrokes are now being recorded" in line
            or line == "\n"
        ):
            continue
        data.append(line)
    return data


def get_log_data():
    with open(
        "/Users/chaitanyasharma/.cache/keylogger.log", encoding="UTF-8"
    ) as file:
        content = file.readlines()
    return content


if __name__ == "__main__":
    main()
