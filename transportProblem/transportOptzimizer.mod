
param n, integer, >= 1;
param m, integer, >= 1;

set W;  # Warehouses
set S;  # Stores

param supply{W} >= 0;
param demand{S} >= 0;
param cost{W,S} >= 0;

var x{W,S} >= 0;  # Amount shipped from warehouse i to store j

minimize total_cost:
    sum{i in W, j in S} cost[i,j] * x[i,j];

subject to Supply_Constraint{i in W}:
    sum{j in S} x[i,j] <= supply[i];

subject to Demand_Constraint{j in S}:
    sum{i in W} x[i,j] = demand[j];

# Ensure non-negativity
subject to Non_Negativity_Constraint{i in W, j in S}:
    x[i,j] >= 0;

solve;

printf "Optimal Total Cost: %f\n", total_cost;
printf "Shipping Plan:\n";
for {i in W, j in S : x[i,j] > 0} {
    printf "From Warehouse %s to Store %s: %f\n", i, j, x[i,j];
}

data;
end;
