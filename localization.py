import numpy as np
from communication import Subscriber

class EKFLocalization:
    def __init__(self, dt=0.1, process_noise=0.01, measurement_noise=0.1):
        # Initial state (x, y, theta)
        self.x = np.zeros(3)
        
        # Initial uncertainty (covariance matrix)
        self.P = np.eye(3) * 1e-3
        
        # Time step (dt)
        self.dt = dt
        
        # Process noise (Q)
        self.Q = np.eye(3) * process_noise
        
        # Measurement noise (R)
        self.R = np.eye(3) * measurement_noise

        self.Position = Subscriber(topic="XandY")
  
        
    def predict(self, v_x, v_y, omega):
        # State prediction using motion model
        theta = self.x[2]
        
        # Motion model update
        self.x[0] += v_x * np.cos(theta) * self.dt
        self.x[1] += v_y * np.sin(theta) * self.dt
        self.x[2] += omega * self.dt
        
        # State transition matrix (Jacobian of the motion model)
        F = np.eye(3)
        F[0, 2] = -v_x * np.sin(theta) * self.dt
        F[1, 2] = v_y * np.cos(theta) * self.dt
        
        # Update the covariance matrix (prediction step)
        self.P = np.dot(F, np.dot(self.P, F.T)) + self.Q
        
    def update(self, z):
        # Measurement update (z is the measurement vector [x, y, theta])
        H = np.eye(3)  # Measurement matrix (assume we only measure [x, y])
        
        # Kalman gain
        S = np.dot(H, np.dot(self.P, H.T)) + self.R
        K = np.dot(self.P, np.dot(H.T, np.linalg.inv(S)))
        
        # Measurement residual
        y = z - np.dot(H, self.x)
        
        # Update the state estimate and the covariance matrix
        self.x = self.x + np.dot(K, y)
        self.P = self.P - np.dot(K, np.dot(H, self.P))
        
    def get_state(self):
        return self.x

# Example usage of EKFLocalization
if __name__ == "__main__":
    ekf = EKFLocalization()

    # Simulated sensor data (control inputs)
    v_x = 1.0  # velocity in x-direction (m/s)
    v_y = 0.0  # velocity in y-direction (m/s)
    omega = 0.1  # angular velocity (rad/s)

    # Simulated measurements (x, y, theta)
    while True:
        # ekf.receiver.request_data()
        ekf.Position.receive_data()
    # z = np.array([1.0, 1.0, 0.05])  # Example measurement (measured x, y, and theta)

    # for t in range(100):
    #     # Prediction step
    #     ekf.predict(v_x, v_y, omega)
        
    #     # Update step with measurements (this is where we fuse the sensor data)
    #     ekf.update(z)
        
    #     # Get the current state estimate
    #     estimated_state = ekf.get_state()
    #     print(f"Time step {t}: x={estimated_state[0]:.2f}, y={estimated_state[1]:.2f}, theta={estimated_state[2]:.2f}")
