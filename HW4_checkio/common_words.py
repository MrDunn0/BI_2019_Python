# first_string = input()
# second_string = input()


def common_words(str1, str2):
    result = []
    for word in str1.split(","):
        if word in str2.split(",") and word not in result:
            result.append(word)
    return ",".join(result)


# print(common_words(first_string, second_string))
print(common_words("one,two,three", "four,five,one,two,six,three"))
print(common_words("hello,world", "hello,earth"))
print(common_words("one,two,three", "four,five,six"))
