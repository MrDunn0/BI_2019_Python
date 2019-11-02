# Вроде теперь O(n)


def common_words(str1, str2):
    str_1_words = str1.split(",")
    str_2_words = str2.split(",")
    result = []
    dict_with_str_1_words = {word for word in str_1_words}
    for word in str_2_words:
        if word in dict_with_str_1_words:
            result.append(word)
    return result

# print(common_words("one,two,three", "four,five,one,two,six,three"))
# print(common_words("hello,world", "hello,earth"))
# print(common_words("one,two,three", "four,five,six"))
