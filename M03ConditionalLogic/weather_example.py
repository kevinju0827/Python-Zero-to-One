temp_str = input("Enter the current temperature (°C): ")
temperature = float(temp_str)

rain_input = input("Is it raining? (yes/no): ")
is_raining = rain_input.lower() == "yes"

if temperature > 30 and is_raining:
    print("Hot and raining — light clothes and an umbrella!")
elif temperature > 30:
    print("Hot and sunny — sunscreen recommended.")
elif temperature >= 20 and not is_raining:
    print("Perfect weather for a walk.")
elif temperature >= 10 and is_raining:
    print("Cool and raining — bring a jacket and an umbrella.")
elif is_raining:
    print("Take an umbrella regardless of temperature.")
else:
    print("Bundle up!")
