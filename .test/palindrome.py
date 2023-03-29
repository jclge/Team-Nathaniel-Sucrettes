def is_there_a_palindrome(string: str):
    for i in range(len(string)):
        if string[::-1][i:] == string[:len(string)-i]:
            return i
    return False


def palindrome(content: list[str]) -> str:
    for element in content:
        res = is_there_a_palindrome(element)
        if res != False:
            return element[:res]
    return ""
