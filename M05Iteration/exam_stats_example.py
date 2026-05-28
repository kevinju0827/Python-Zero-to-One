scores = []

print("Enter exam scores one at a time.")
print("Type anything non-numeric when done.\n")

while True:
    user_input = input("Score: ")

    if user_input.isnumeric():
        scores.append(int(user_input))
    else:
        print("Input ended.")
        break

pass_count = 0
fail_count = 0

for score in scores:
    if score >= 60:
        pass_count += 1
    else:
        fail_count += 1

total = len(scores)

if total == 0:
    print("No scores entered.")
else:
    pass_rate = pass_count / total * 100
    average   = sum(scores) / total

    print(f"\n=== Exam Statistics ===")
    print(f"Total:    {total}")
    print(f"Passed:   {pass_count}  ({pass_rate:.1f}%)")
    print(f"Failed:   {fail_count}")
    print(f"Average:  {average:.1f}")
    print(f"Highest:  {max(scores)}")
    print(f"Lowest:   {min(scores)}")

    print("\n=== Individual Scores ===")
    for rank, score in enumerate(sorted(scores, reverse=True), start=1):
        status = "PASS" if score >= 60 else "FAIL"
        print(f"  {rank}. {score:>3}  [{status}]")
