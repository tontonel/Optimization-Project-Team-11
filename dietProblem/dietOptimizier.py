import pandas as pd
import glpk

# Read the CSV files
constraint_matrix = pd.read_csv("constraint_matrix.csv", header=None)
objective_coefficients = pd.read_csv("objective_function.csv", header=None)
nutritional_constraints = pd.read_csv("nutritional_requirements.csv")

# Determine the number of rows and columns
num_constraints = constraint_matrix.shape[0]
num_vars = constraint_matrix.shape[1] - 1  # Last column is RHS

# Create a GLPK problem object
lp = glpk.LPX()
lp.name = 'diet optimizer' 
lp.obj.maximize = False     # Set this as a minimization problem

# Add rows (constraints)
lp.rows.add(num_constraints)
for i in range(num_constraints):
    lp.rows[i].name = f'constraint_{i}'

    constraint_type = nutritional_constraints.iloc[i]['Type']
    constraint_value = nutritional_constraints.iloc[i]['Value']

    # Set the bounds based on the constraint type
    if constraint_type == 'GE':
        lp.rows[i].bounds = constraint_value, None
    elif constraint_type == 'LE':
        lp.rows[i].bounds = None, constraint_value  
    elif constraint_type == 'EQ':
        lp.rows[i].bounds = constraint_value, constraint_value 

# Add columns (variables)
lp.cols.add(num_vars)
for j in range(num_vars):
    lp.cols[j].name = f'x{j}'
    lp.cols[j].bounds = 0.0, None  # Set bounds 0 <= xi < inf
    lp.obj[j] = objective_coefficients.iloc[0, j]  # Set objective coefficients

# Create the constraint matrix
matrix = []
for i in range(num_constraints):
    for j in range(num_vars):
        matrix.append((i + 1, j + 1, constraint_matrix.iloc[i, j]))

# Convert the matrix to GLPK format
ar = [item[2] for item in matrix]

# Load the cost matrix into GLPK
lp.matrix = ar

# Solve the LP using the simplex method
lp.simplex()

# Retrieve and print the objective function optimal value
print(f'Objective value: {lp.obj.value}')

# Print the variable names and their primal values
for col in lp.cols:
    print(f'{col.name} = {col.primal}')
