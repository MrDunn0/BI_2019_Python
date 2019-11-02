# Вроде теперь O(n)


def common_words(str1, str2):
    str_1_words = str1.split(",")
    str_2_words = str2.split(",")
    result = set(str_1_words) & set(str_2_words)
    return ",".join(result)


# print(common_words("one,two,three", "four,five,one,two,six,three"))
# print(common_words("hello,world", "hello,earth"))
# print(common_words("one,two,three", "four,five,six"))
