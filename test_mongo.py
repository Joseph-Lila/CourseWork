def get_respective_values(ans):
    res = []
    for i in range(len(ans[-1])):
        res.append(tuple([ans[0][i], ans[1][i]]))
    return tuple(res)


print(get_respective_values([("a", "b", "c"), ("d", "e", "f")]))