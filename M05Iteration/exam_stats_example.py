scores = []

while True:
    user_input = input("Enter an exam score (enter a non-numeric value to stop): ")

    if user_input.isdigit():
        scores.append(int(user_input))
    else:
        break

pass_count = 0
fail_count = 0

for score in scores:
    if score >= 60:
        pass_count += 1
    else:
        fail_count += 1

total_count = len(scores)

if total_count > 0:
    pass_percentage = pass_count / total_count * 100
else:
    pass_percentage = 0

print(f"Total students: {total_count}")
print(f"Passing students: {pass_count}")
print(f"Failing students: {fail_count}")
print(f"Passing percentage: {pass_percentage:.2f}%")