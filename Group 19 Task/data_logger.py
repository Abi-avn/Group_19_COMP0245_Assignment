"""Simple CSV logger """
import csv
from datetime import datetime


class DataLogger:
    def __init__(self, filename="robotnik_training_data.csv", trajectory_id=None):
        self.filename = filename
        self.trajectory_id = trajectory_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.file = open(self.filename, "a", newline="")
        self.writer = None

    def log_step(self, time_s, base_pos, base_bearing, q_mes, qd_mes,
                 ee_pos, target_pos, wheel_cmds, torque_arm):
        """Log one state/action sample to the CSV."""
        row = {
            "trajectory_id": self.trajectory_id,
            "time_s": time_s,
            "base_x": base_pos[0],
            "base_y": base_pos[1],
            "base_z": base_pos[2],
            "base_bearing": base_bearing,
            "ee_x": ee_pos[0],
            "ee_y": ee_pos[1],
            "ee_z": ee_pos[2],
            "target_x": target_pos[0],
            "target_y": target_pos[1],
            "target_z": target_pos[2],
            "error_x": target_pos[0] - ee_pos[0],
            "error_y": target_pos[1] - ee_pos[1],
            "error_z": target_pos[2] - ee_pos[2],
        }

        # Measured wheel velocities and arm state 
        for i in range(4):
            row[f"wheel_velocity_{i+1}"] = qd_mes[i]
        for i in range(7):
            row[f"arm_q_{i+1}"] = q_mes[4 + i]
            row[f"arm_qd_{i+1}"] = qd_mes[4 + i]

        # Expert wheel commands and arm torque commands
        for i in range(4):
            row[f"cmd_wheel_{i+1}"] = wheel_cmds[i]
        for i in range(7):
            row[f"cmd_arm_torque_{i+1}"] = torque_arm[i]

        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=list(row.keys()))
            if self.file.tell() == 0:
                self.writer.writeheader()
        self.writer.writerow(row)

    def close(self):
        if not self.file.closed:
            self.file.close()


if __name__ == "__main__":
    print("DataLogger for simulation data.")

