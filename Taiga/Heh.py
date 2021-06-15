m = '글자로만들어진무언가를당신은보고있습니다'
l = len(m)

for i in range(l + l):
    if i <= l:
        print(m[:i])
    else:
        print(m[:l - i])