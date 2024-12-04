import cvxpy as cp
import numpy as np

# Parameters
T = 0.1  # Sampling time (seconds)
N = 20   # Prediction horizon
Q = np.diag([100, 100, 1])  # Stronger emphasis on x, y, and theta errors
R = np.eye(3) * 0.01  # Penalize control inputs less

v_max = 1  # Max linear velocity (m/s)
w_max = 1  # Max angular velocity (rad/s)
ly = 18
lx = 24
r = 4

# Wheel velocities mapping matrix (inverse kinematics for mecanum wheels)
wheel_transform = 1 / r * np.array([
    [1, -1, -(lx + ly)],  # Wheel 1 LF
    [1,  1, -(lx + ly)],  # Wheel 2 LR
    [1,  1,  (lx + ly)],  # Wheel 3 RF
    [1, -1,  (lx + ly)]   # Wheel 4 RR
]) / np.sqrt(2)

# Reference trajectory (staying at origin for simplicity)
x_ref = np.array([[5, 0, 0]] * N)

# Initial state
x0 = np.array([0, 0, 0])  # Start at origin with zero orientation

# Optimization variables
x = cp.Variable((N, 3))  # Predicted states: [x, y, theta]
u = cp.Variable((N, 3))  # Control inputs: [vx, vy, omega]

# Cost function and constraints
cost = 0
constraints = []
for k in range(N):
    cost += cp.quad_form(x[k] - x_ref[k], Q) + cp.quad_form(u[k], R)
    constraints += [
        cp.norm(u[k, :2], "inf") <= v_max,  # Linear velocity constraint
        cp.abs(u[k, 2]) <= w_max            # Angular velocity constraint
    ]

# Dynamics constraints (using the new system dynamics equations)
for k in range(N - 1):
    constraints += [
        x[k + 1, 0] == x[k, 0] + u[k, 0] * cp.Variable(1) * T,  # x update (this is a placeholder; will be calculated after solving)
        x[k + 1, 1] == x[k, 1] + u[k, 1] * cp.Variable(1) * T,  # y update (same as above)
        x[k + 1, 2] == x[k, 2] + u[k, 2] * T                    # theta update
    ]

# Initial state constraint
constraints += [x[0] == x0]

# Solve MPC problem
problem = cp.Problem(cp.Minimize(cost), constraints)

# Simulation
current_state = x0
for _ in range(100):  # Simulate for 100 timesteps
    constraints[-1] = (x[0] == current_state)
    problem.solve()

    optimal_u = u.value[0]  # Get optimal control input: [vx, vy, omega]

    # Compute wheel velocities and map to 8-bit integer range (0-255)
    wheel_velocities = wheel_transform @ optimal_u
    wheel_vel_8bit = np.clip((wheel_velocities + v_max) / (2 * v_max) * 255, -255, 255)

    u_o = np.linalg.pinv(wheel_transform) @ wheel_velocities
    print(f"Current state: {current_state}, Wheel Velocities (8-bit): {wheel_vel_8bit}, Optimal u: {optimal_u}, u_o: {u_o}")

    # Update state using the new system dynamics (with numpy functions)
    current_state = np.array([
        current_state[0] + optimal_u[0] * np.cos(current_state[2]) * T,
        current_state[1] + optimal_u[1] * np.sin(current_state[2]) * T,
        current_state[2] + optimal_u[2] * T
    ])  # New state update

    # Add some noise for realism (optional)
    current_state += np.random.normal(0, 0.1, size=current_state.shape)
