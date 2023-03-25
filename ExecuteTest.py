with open("test.txt", 'r') as fd:
    exec(fd.read())
    print(thing(12))