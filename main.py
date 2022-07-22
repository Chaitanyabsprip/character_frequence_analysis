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
    single_char_freq_map = get_ngram_frequency_map(logs, 1)
    bigram_freq_map = get_ngram_frequency_map(logs, 2)
    trigram_freq_map = get_ngram_frequency_map(logs, 3)
    tetragram_freq_map = get_ngram_frequency_map(logs, 4)
    # print(single_char_freq_map)
    # print(bigram_freq_map)
    # print(trigram_freq_map)
    # print(tetragram_freq_map)
    bar_plot(single_char_freq_map)
    bar_plot(dict(list(bigram_freq_map.items())[:30]))
    bar_plot(dict(list(trigram_freq_map.items())[:30]))
    bar_plot(dict(list(tetragram_freq_map.items())[:30]))


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
