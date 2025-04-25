
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import linprog
import plotly.io as pio

pio.renderers.default = 'browser'

# === 1. Parameters ===

n = 3       # trucks
m = 4       # places
C = 1000    # truck capacity
R = 600     # place max demand per time step
delivery_rate = 200  # liters/hour
time_blocks = 3  # morning, midday, afternoon
days = 7
T = time_blocks * days  # total time periods
D_min = 2000 * days     # total weekly delivery across all places
place_min = 1000        # minimum weekly delivery per place
truck_daily_min = 100   # minimum daily delivery per truck

truck_available_hours = [4] * n  # per time block
storage_capacities = [5000, 5200, 5800, 5100]  # max storage per place

# Base cost matrix (truck x place)
base_cost = np.array([
    [12, 15, 20, 18],
    [10, 13, 17, 14],
    [8, 11, 14, 10]
])

# Time-based cost multipliers
cost_multipliers = [1.0, 1.15, 1.05]  # morning, midday, afternoon

# === 2. Build time-varying cost matrix ===
cost = np.zeros((T, n, m))
for t in range(T):
    multiplier = cost_multipliers[t % time_blocks]
    cost[t] = base_cost * multiplier

# === 3. Decision variables x[i][j][t] ===
num_vars = n * m * T
c = cost.reshape(T, n * m).flatten()

# === 4. Constraints ===

A = []
b_vec = []

# Truck capacity per period
for t in range(T):
    for i in range(n):
        row = np.zeros(num_vars)
        for j in range(m):
            idx = t * n * m + i * m + j
            row[idx] = 1
        A.append(row)
        b_vec.append(C)

# Place demand per period
for t in range(T):
    for j in range(m):
        row = np.zeros(num_vars)
        for i in range(n):
            idx = t * n * m + i * m + j
            row[idx] = 1
        A.append(row)
        b_vec.append(R)

# Weekly minimum delivery
A.append(-np.ones(num_vars))
b_vec.append(-D_min)

# Time limit per truck per period
for t in range(T):
    for i in range(n):
        row = np.zeros(num_vars)
        for j in range(m):
            idx = t * n * m + i * m + j
            row[idx] = 1 / delivery_rate
        A.append(row)
        b_vec.append(truck_available_hours[i])

# Minimum weekly delivery per place
for j in range(m):
    row = np.zeros(num_vars)
    for t in range(T):
        for i in range(n):
            idx = t * n * m + i * m + j
            row[idx] = -1
    A.append(row)
    b_vec.append(-place_min)

# Minimum daily delivery per truck
for d in range(days):
    for i in range(n):
        row = np.zeros(num_vars)
        for block in range(time_blocks):
            t = d * time_blocks + block
            for j in range(m):
                idx = t * n * m + i * m + j
                row[idx] = -1
        A.append(row)
        b_vec.append(-truck_daily_min)

# NEW: Storage constraint per place (max total over week)
for j in range(m):
    row = np.zeros(num_vars)
    for t in range(T):
        for i in range(n):
            idx = t * n * m + i * m + j
            row[idx] = 1
    A.append(row)
    b_vec.append(storage_capacities[j])

# Bounds
bounds = [(0, None)] * num_vars

# === 5. Solve LP ===
res = linprog(c, A_ub=A, b_ub=b_vec, bounds=bounds, method='highs')

# === 6. Process + Plot ===
if res.success:
    x = res.x.reshape(T, n, m)
    print("Total cost:", res.fun)

    time_labels = [f'Day {t // 3 + 1} - {["Morn", "Noon", "Aft"][t % 3]}' for t in range(T)]
    fig = make_subplots(rows=1, cols=n, subplot_titles=[f'Truck {i}' for i in range(n)])

    for i in range(n):
        for j in range(m):
            fig.add_trace(
                go.Scatter(
                    x=time_labels,
                    y=x[:, i, j],
                    mode='lines+markers',
                    name=f'Place {j}',
                    legendgroup=f'Place {j}',
                    showlegend=(i == 0)
                ),
                row=1, col=i + 1
            )

    fig.update_layout(
        title='Water Delivery Over Time (Trucks × Places, Storage-Constrained)',
        height=500,
        template='plotly_white',
        hovermode='x unified'
    )

    fig.show()

else:
    print("Optimization failed:", res.message)
