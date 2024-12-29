
# Fleet Transition Optimization Solution

This project aims to optimize the fleet composition of a logistics company transitioning to environmentally friendly vehicles from 2024 to 2028. The objective is to minimize total costs while meeting yearly carbon emission limits and operational constraints.

## Problem Approach

The problem is formulated as a Linear Programming (LP) optimization problem where the goal is to minimize the total costs of vehicle acquisition, operation, and resale. The model considers the following key factors:

- **Demand**: The number of trucks needed each year for each truck size.
- **Vehicle Types**: Diesel and Electric vehicles with two sizes (S1 and S2).
- **Cost Factors**: 
  - Purchase cost
  - Fuel cost per km
  - Maintenance cost as a percentage of the vehicle cost
  - Resale value (50% of purchase cost when sold)
- **Carbon Emissions**: Constraints on the total carbon emissions each year.
- **Operational Constraints**: 
  - Fleet operational limits based on vehicle range and demand.
  - Sell limits, where no more than 30% of the fleet can be sold each year.

The model provides optimal solutions for:
- How many vehicles to buy each year.
- How many vehicles to sell.
- How many vehicles to operate each year.

## Solution Strategy

The solution strategy consists of the following steps:

1. **Problem Formulation**:
    - The fleet transition problem is modeled as an LP optimization problem using the PuLP library.
    - Decision variables represent the number of vehicles to buy, sell, and operate each year for each vehicle type and size.
    - The objective is to minimize the total cost, including the purchase cost, operational costs (fuel and maintenance), and resale values when selling vehicles.

2. **Constraints**:
    - **Demand Fulfillment**: The total range of vehicles operated in each year must meet the demand for small and large trucks.
    - **Carbon Emission Limits**: The total carbon emissions of the fleet in each year must stay within the specified carbon limits.
    - **Vehicle Range**: The operational range for each vehicle cannot exceed its maximum capacity.
    - **Sell Limit**: No more than 30% of the fleet can be sold each year.
    - **Non-Negativity**: The number of vehicles operated cannot be negative.

3. **Solution Tools**:
    - **PuLP**: A Python library used for modeling and solving linear programming problems. It is used here to define the decision variables, objective function, and constraints.
    - **Pandas**: For handling and processing the input data (vehicle data, demand, constraints) and saving the results to a CSV file.
    - **Python**: For writing the LP optimization script, running the solver, and generating the output.

4. **Optimization**:
    - The LP problem is solved using the `prob.solve()` function from the PuLP library, which finds the optimal solution.
    - Results are extracted from the solver and saved to a CSV file, which includes the number of vehicles to buy, sell, and operate each year.

## Tools Used

- **PuLP**: A library for linear programming in Python, used to solve the optimization problem.
- **Pandas**: A data manipulation library in Python, used for handling input and output data in CSV format.
- **Python**: The programming language used for scripting the optimization model and managing the overall process.

## File Structure

The project includes the following files:

- **Fleet_Transition_Optimization.py**: The main script that defines the LP optimization model and solves the problem.
- **Vehicles.csv**: A CSV file containing the vehicle data (cost, range, fuel cost, maintenance, and emissions for each vehicle type).
- **Yearly_Demand.csv**: A CSV file containing the demand data for small and large trucks, along with the carbon emission limits for each year.
- **Transition_Constraints.csv**: A CSV file containing the transition constraints, including the maximum percentage of the fleet that can be sold each year and the operable years for each vehicle.

## Usage

To run the solution, ensure you have the following libraries installed:

```bash
pip install pulp pandas
```

Run the optimization script:

```bash
python Fleet_Transition_Optimization.py
```

The results will be saved to **Refined_Fleet_Transition_Plan.csv**.

## Example Output

The output CSV file will contain the following columns:

- **Year**: The year of the fleet transition (2024 to 2028).
- **Vehicle Type**: The type of vehicle (Diesel or Electric).
- **Truck Size**: The size of the truck (S1 or S2).
- **Buy**: The number of vehicles to buy in that year.
- **Sell**: The number of vehicles to sell in that year.
- **Operate**: The number of vehicles to operate in that year.

## Future Improvements

- Incorporate additional operational costs (e.g., insurance, taxes).
- Include more detailed vehicle characteristics and constraints.
- Optimize for other factors like operational efficiency or profitability.

## License

This project is licensed under the MIT License.
