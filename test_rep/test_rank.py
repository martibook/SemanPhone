from numpy import arange

alphas = [str(round(i, 2)) for i in arange(0.5, 1, 0.05)]
scores = []

words = []
hooks = []
with open("hook_words_50", 'r') as f:
    for line in f:
        line = line.split()
        words.append(line[0])
        if len(line) > 1:
            hooks.append(line[1])
        else:
            hooks.append(None)

for a in alphas:
    filename = "alpha"+a
    dic = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.split()
            dic[line[0]] = line

    ans = 0
    for i in range(len(words)):
        w = words[i]
        h = hooks[i]
        if h is None:
            pass
        else:
            if h in dic[w]:
                idx = dic[w].index(h)
                ans += 6 - idx
    scores.append(ans)
    print('alpha = {a}: {ans}'.format(a=a, ans=ans))

print(alphas)
print(scores)
