# with open('readme.txt', 'r') as f:
#     lines = f.read()
#     print(lines)

with open('readme.txt', 'r') as f:
    lines = f.readlines()
    [print(line.strip()) for line in lines]