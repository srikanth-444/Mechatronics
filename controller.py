import numpy as np
import cvxpy as cp

# Parameters
T = 0.1  # Sampling time (seconds)
N = 2
00   # Prediction horizon
Q = np.eye(2)*1  # State error weight matrix
R = np.eye(2)/10 # Control effort weight matrix
v_max = 1    # Max velocity (m/s)

# Reference trajectory
x_ref = np.array([[5, 5]] * N)  # Target position (staying constant for simplicity)

# Initial state
x0 = np.array([0, 0])  # Start at origin

# Optimization variables
x = cp.Variable((N, 2))  # Predicted states
u = cp.Variable((N, 2))  # Control inputs

# Cost function
cost = 0
constraints = []
for k in range(N):
    cost += cp.quad_form(x[k] - x_ref[k], Q) + cp.quad_form(u[k], R)
    constraints += [cp.norm(u[k],"inf") <= v_max]  # Control constraints

# Dynamics constraints
for k in range(N - 1):
    constraints += [x[k + 1] == x[k] + T * u[k]]

# Initial state constraint
constraints += [x[0] == x0]

# Solve MPC
problem = cp.Problem(cp.Minimize(cost), constraints)

# Simulation
current_state = x0
for _ in range(100):  # Simulate for 50 timesteps
    # Update initial state constraint
    constraints[-1] = (x[0] == current_state)
    problem.solve()

    # Get optimal control input
    optimal_u = u.value[0]  # First control action
    current_state = current_state + T * optimal_u  # Update state
    current_state += np.random.normal(0, 0.1, size=current_state.shape)
    print(f"Current state: {current_state},input:{optimal_u}")
