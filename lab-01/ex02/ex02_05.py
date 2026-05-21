hours = float(input("Nhập số giờ làm việc trong tuần: "))
salary_per_hour = float(input("Nhập lương theo giờ: "))

standard_hours = 44

if hours <= standard_hours:
    salary = hours * salary_per_hour
else:
    overtime = hours - standard_hours
    salary = standard_hours * salary_per_hour + overtime * salary_per_hour * 1.5

print("Tiền lương thực nhận là:", salary)