temperature_text = input("What is the temperature today? ")
temperature = float(temperature_text)

if temperature > 30:
    print("It's a hot day!")
elif temperature >= 20:
    print("It's a nice day.")
else:
    print("It's cold!")
