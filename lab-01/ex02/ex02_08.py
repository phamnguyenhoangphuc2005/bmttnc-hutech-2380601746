items = [x for x in input().split(',')]

result = []

for p in items:
    intp = int(p, 2)

    if not intp % 5:
        result.append(p)

print(','.join(result))