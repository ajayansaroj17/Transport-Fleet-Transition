import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value

# data
years = [2024, 2025, 2026, 2027, 2028]
vehicle_data = {
    "Diesel": {
        "S1": {"cost": 50000, "range": 50000, "fuel_cost": 0.4, "maintenance": 0.1, "emissions": 1.0},
        "S2": {"cost": 80000, "range": 60000, "fuel_cost": 0.4, "maintenance": 0.1, "emissions": 1.0},
    },
    "Electric": {
        "S1": {"cost": 70000, "range": 40000, "fuel_cost": 0.2, "maintenance": 0.05, "emissions": 0.2},
        "S2": {"cost": 100000, "range": 45000, "fuel_cost": 0.2, "maintenance": 0.05, "emissions": 0.2},
    },
}
demand = {"S1": 100000, "S2": 150000}
carbon_limits = {2024: 200000, 2025: 180000, 2026: 150000, 2027: 120000, 2028: 100000}

prob = LpProblem("Fleet_Transition_Optimization", LpMinimize)

# Decision variables
buy = LpVariable.dicts("Buy", (years, vehicle_data, ["S1", "S2"]), 0, None, cat="Integer")
sell = LpVariable.dicts("Sell", (years, vehicle_data, ["S1", "S2"]), 0, None, cat="Integer")
operate = LpVariable.dicts("Operate", (years, vehicle_data, ["S1", "S2"]), 0, None, cat="Continuous")

# Objective: Minimize total costs
total_cost = lpSum(
    buy[y][v][t] * vehicle_data[v][t]["cost"] +
    operate[y][v][t] * vehicle_data[v][t]["fuel_cost"] * demand[t] +
    operate[y][v][t] * vehicle_data[v][t]["cost"] * vehicle_data[v][t]["maintenance"] -
    sell[y][v][t] * vehicle_data[v][t]["cost"] * 0.5
    for y in years for v in vehicle_data for t in vehicle_data[v]
)
prob += total_cost

# Constraints

# 1. Demand must be met
for y in years:
    for t in demand:
        prob += lpSum(operate[y][v][t] * vehicle_data[v][t]["range"] for v in vehicle_data) >= demand[t], f"Demand_{y}_{t}"

# 2. Carbon emissions must stay within yearly limits
for y in years:
    prob += lpSum(
        operate[y][v][t] * vehicle_data[v][t]["emissions"] * demand[t]
        for v in vehicle_data for t in vehicle_data[v]
    ) <= carbon_limits[y], f"Carbon_Limit_{y}"

# 3. Operating ranges must not exceed vehicle capacity
for y in years:
    for v in vehicle_data:
        for t in vehicle_data[v]:
            prob += operate[y][v][t] <= buy[y][v][t] - sell[y][v][t], f"Range_{y}_{v}_{t}"

# 4. Non-negativity for Operate
for y in years:
    for v in vehicle_data:
        for t in vehicle_data[v]:
            prob += operate[y][v][t] >= 0, f"Non_Negative_Operate_{y}_{v}_{t}"

# 5. Maximum 30% of the fleet can be sold each year
for y in years:
    for v in vehicle_data:
        for t in vehicle_data[v]:
            prob += sell[y][v][t] <= 0.3 * buy[y][v][t], f"Sell_Limit_{y}_{v}_{t}"

# Solve
prob.solve()

results = []
for y in years:
    for v in vehicle_data:
        for t in vehicle_data[v]:
            results.append({
                "Year": y,
                "Vehicle Type": v,
                "Truck Size": t,
                # "Buy": int(value(buy[y][v][t])),
                # "Sell": int(value(sell[y][v][t])),
                # "Operate": round(value(operate[y][v][t]), 2),
                "Buy": int(round(value(buy[y][v][t]))),  
                "Sell": int(round(value(sell[y][v][t]))), 
                "Operate": round(value(operate[y][v][t]), 2)  
            })

df = pd.DataFrame(results)
df.to_csv("Refined_Fleet_Transition_Plan.csv", index=False)
print("Results saved to Refined_Fleet_Transition_Plan.csv")

# Debug
print("Status:", prob.status)
for v in prob.variables():
    print(f"{v.name}: {v.varValue}")
print("Total Cost:", value(prob.objective))