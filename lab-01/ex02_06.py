x = int(input("Nhập số hàng X: "))
y = int(input("Nhập số cột Y: "))

matrix = []

for i in range(x):
    row = []
    for j in range(y):
        row.append(i * j)
    matrix.append(row)

print(matrix)