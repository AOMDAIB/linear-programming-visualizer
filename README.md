
# Linear Programming Visualizer with Feasible Region Plotting

This Python project allows users to solve **2-variable linear programming problems** and visualize the **feasible region** and **optimal solution** on a 2D plot.

It was inspired while studying the *Linear Programming* chapter in **"Production/Operations Management" by William J. Stevenson** and was built with the support of **AI (ChatGPT)** to reinforce learning through code.

---

## 🔍 Features

- Accepts user-defined **objective function** (maximize or minimize)
- Supports up to **4 linear constraints** (`<=` or `>=`)
- Uses `scipy.optimize.linprog` with the `highs` method for solving
- Plots:
  - Constraint lines
  - Feasible region (shaded)
  - Optimal point with annotated coordinates and objective value

---

## 🛠 Technologies Used

- Python 3.x
- NumPy
- Matplotlib
- SciPy

---

## 📦 Installation

1. Clone the repository or download the code.
2. Install the required libraries:

```bash
pip install -r requirements.txt
