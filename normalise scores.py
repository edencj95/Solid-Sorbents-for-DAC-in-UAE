# Neutral penalty score for missing values
NEUTRAL = 0.4

# Property weights
weights = {
    "capacity_norm": 0.30,
    "temp_norm": 0.25,
    "time_norm": 0.15,
    "heat_norm": 0.10,
    "stability_norm": 0.10,
    "temp_tol_norm": 0.10
}

# Normalisation functions
def normalize_higher_is_better(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

def normalize_lower_is_better(x, xmin, xmax):
    return (xmax - x) / (xmax - xmin)

# Max/min values from your dataset
max_vals = {
    "capacity": 4.3,
    "temp": 150,
    "time": 240,
    "heat": 104,
    "stability": 1,
    "temp_tol": 1
}

min_vals = {
    "capacity": 0.425,
    "temp": 25,
    "time": 5,
    "heat": 24,
    "stability": 0.075,
    "temp_tol": 0
}

# Function to safely get input (with missing value handling)
def get_value(prompt):
    val = input(prompt)
    if val.strip().lower() == "q":
        return "q"
    return float(val) if val.strip() != "" else None

print("Sorbent normalisation tool (type 'q' at any prompt to quit)\n")

while True:
    print("\n--- New Sorbent Entry ---")

    start = input("Press Enter to continue or type 'q' to quit: ")
    if start.lower() == "q":
        print("Exiting.")
        break

    # Collect sorbent properties
    capacity = get_value("Adsorption capacity (mmol/g): ")
    if capacity == "q": break

    temp = get_value("Regeneration temperature (°C): ")
    if temp == "q": break

    time = get_value("Regeneration time (min): ")
    if time == "q": break

    heat = get_value("Heat of adsorption (kJ/mol): ")
    if heat == "q": break

    stability = get_value("Stability (fraction retained): ")
    if stability == "q": break

    temp_tol = get_value("Temperature tolerance (0–1): ")
    if temp_tol == "q": break

    sorbent = {
        "capacity": capacity,
        "temp": temp,
        "time": time,
        "heat": heat,
        "stability": stability,
        "temp_tol": temp_tol
    }

    # Normalisation with missing value handling
    scores = {}

    for prop in sorbent:
        x = sorbent[prop]

        # Missing value → assign neutral penalty score
        if x is None:
            scores[prop + "_norm"] = NEUTRAL
            continue

        xmin = min_vals[prop]
        xmax = max_vals[prop]

        # Higher-is-better properties
        if prop in ["capacity", "stability", "temp_tol"]:
            scores[prop + "_norm"] = normalize_higher_is_better(x, xmin, xmax)
        else:
            scores[prop + "_norm"] = normalize_lower_is_better(x, xmin, xmax)

    # ---- WEIGHTED TOTAL SCORE ----
    total_score = sum(weights[k] * scores[k] for k in scores)

    # Output results
    print("\nNormalised scores (0–1):")
    for k, v in scores.items():
        print(f"{k}: {v:.3f}")

    print(f"\nWeighted Total Score: {total_score:.3f}")
