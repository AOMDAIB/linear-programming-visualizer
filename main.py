import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.optimize import linprog

print("Welcome to the Linear Programming Solver with Feasible Region Plotter!")


obj_type = input("Enter objective (max or min): ").strip().lower()
a = float(input("Enter coefficient of x in the objective function: "))
b = float(input("Enter coefficient of y in the objective function: "))


while True:
    num_constraints = int(input("Enter number of constraints (2 to 4): "))
    if 2 <= num_constraints <= 4:
        break
    else:
        print("Please enter a valid number of constraints (2 to 4).")

constraints = []
for i in range(num_constraints):
    print(f"\nConstraint {i+1}: a₁x + b₁y ≤/≥ c₁")
    a1 = float(input("Enter coefficient of x: "))
    b1 = float(input("Enter coefficient of y: "))
    sign = input("Enter inequality sign (<= or >=): ").strip()
    c1 = float(input("Enter right-hand side value: "))
    constraints.append((a1, b1, sign, c1))


c = np.array([-a, -b]) if obj_type == 'max' else np.array([a, b])

lhs_ineq = []
rhs_ineq = []
for a1, b1, sign, c1 in constraints:
    if sign == '<=':
        lhs_ineq.append([a1, b1])
        rhs_ineq.append(c1)
    elif sign == '>=':
        lhs_ineq.append([-a1, -b1])
        rhs_ineq.append(-c1)
    else:
        print(f"Invalid sign: {sign}. Skipping.")


lhs_ineq += [[-1, 0], [0, -1]]
rhs_ineq += [0, 0]

lhs_ineq = np.array(lhs_ineq)
rhs_ineq = np.array(rhs_ineq)


res = linprog(c, A_ub=lhs_ineq, b_ub=rhs_ineq, method='highs')


x_max = max([abs(c1/a1) if a1 != 0 else 0 for a1, b1, sign, c1 in constraints] + [10]) * 1.5
y_max = max([abs(c1/b1) if b1 != 0 else 0 for a1, b1, sign, c1 in constraints] + [10]) * 1.5
x_vals = np.linspace(0, x_max, 400)
y_vals = np.linspace(0, y_max, 400)
X, Y = np.meshgrid(x_vals, y_vals)
feasible = np.ones_like(X, dtype=bool)

for a1, b1, sign, c1 in constraints:
    if sign == '<=':
        feasible &= (a1*X + b1*Y <= c1 + 1e-6)
    elif sign == '>=':
        feasible &= (a1*X + b1*Y >= c1 - 1e-6)

feasible &= (X >= -1e-6) & (Y >= -1e-6)

plt.figure(figsize=(10,8))
plt.imshow(feasible, extent=(0, x_max, 0, y_max), origin='lower', cmap='Greens', alpha=0.3)


for i, (a1, b1, sign, c1) in enumerate(constraints):
    label = f'Constraint {i+1}: {a1}x + {b1}y {sign} {c1}'
    if abs(b1) > 1e-6:
        y_line = (c1 - a1*x_vals) / b1
        plt.plot(x_vals, y_line, label=label)
    elif abs(a1) > 1e-6:
        x_line = np.full_like(y_vals, c1 / a1)
        plt.plot(x_line, y_vals, label=label)

feasible_patch = Patch(facecolor='green', edgecolor='green', alpha=0.3, label='Feasible Region')
handles, labels = plt.gca().get_legend_handles_labels()
handles = [feasible_patch] + handles
labels = ['Feasible Region'] + labels


if res.success:
    x_opt, y_opt = res.x
    z_value = -res.fun if obj_type == "max" else res.fun
    plt.plot(x_opt, y_opt, 'ro', markersize=10, label='Optimal Solution')
    plt.annotate(f'Optimal Point\nx={x_opt:.2f}, y={y_opt:.2f}\nZ={z_value:.2f}',
                 (x_opt, y_opt), textcoords="offset points", xytext=(10,10),
                 ha='left', color='green', fontsize=10, weight='bold')
    plt.title(f'Optimal Solution: Z = {z_value:.2f}', fontsize=12)
else:
    plt.title("No feasible solution found", fontsize=12)


obj_sign = "+" if b >= 0 else "-"
objective_str = f"{a}x {obj_sign} {abs(b)}y"
objective_type = "Maximize" if obj_type == "max" else "Minimize"
plt.suptitle(f"{objective_type} Z = {objective_str}", fontsize=14, weight='bold', color='darkblue')

plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0, x_max)
plt.ylim(0, y_max)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(handles=handles, loc='upper right', fontsize=9)
plt.tight_layout()
plt.show()
