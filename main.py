from abc_filter import AbcFilter
from nouns_dict import NounsDict


def main():
    nounsDict = NounsDict()
    abc_filter = AbcFilter(5)
    print("Loaded {0}".format(len(nounsDict.nouns)))

    random_word = nounsDict.find_rnd_start_word()
    print("Start word: ", random_word)
    print("Commands: ?existing chars (^г***б)")
    print("          -not existing chars (-жп)")
    print("          *chars positions (*а***)")
    print("          press ENTER to suggest a new word")
    print("          exit for exit")
    exit = False
    while not exit:
        cmd = input("Enter command: ")
        if "+" in cmd:
            abc_filter.add(cmd[1:])
        elif "?" in cmd:
            abc_filter.add_exists(cmd[1:])
        elif "-" in cmd:
            abc_filter.exclude(cmd[1:])
        elif "*" in cmd:
            abc_filter.set_positions(cmd)
        elif cmd == "exit":
            print("Завершаем работу...")
            break
        else:
            print("Поиск новых слов для фильтра: " + abc_filter.to_str())
            matched_words = abc_filter.find_matched_words(nounsDict.get_nouns())
            print("Найдено %s слов: %s" % (len(matched_words), nounsDict.sort_by_frequency(matched_words)))
            print("--------------------------------------------------------------------------------------------------")


if __name__ == '__main__':
    main()
