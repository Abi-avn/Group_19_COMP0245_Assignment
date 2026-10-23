import os
import sys
import subprocess

# Number of trajectories to collect
NUM_TRAJECTORIES = 10

# Fixed target end-effector position (x, y, z)
TARGET = [0.0, 1.1, 0.5]

# Locate robotnik_arm_logger.py in the same directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGER_SCRIPT = os.path.join(
    SCRIPT_DIR, "robotnik_arm_logger.py"
)

# Check that the logger script exists
if not os.path.isfile(LOGGER_SCRIPT):
    print(f"ERROR: Could not find {LOGGER_SCRIPT}")
    sys.exit(1)

# Collect trajectories one at a time
for i in range(NUM_TRAJECTORIES):
    trajectory_id = f"trajectory_{i + 1:03d}"

    # Copy the current environment variables
    env = os.environ.copy()

    # Configure the current trajectory
    env["TRAJECTORY_ID"] = trajectory_id
    env["TARGET_X"] = str(TARGET[0])
    env["TARGET_Y"] = str(TARGET[1])
    env["TARGET_Z"] = str(TARGET[2])

    # Headless simulation (currently broken when switched off)
    env["ROBOENV_HEADLESS"] = "1"

    print(
        f"\n[{i + 1}/{NUM_TRAJECTORIES}] "
        f"Running {trajectory_id}, target={TARGET}",
        flush=True,
    )

    # Run the logger script and wait for it to finish
    result = subprocess.run(
        [sys.executable, LOGGER_SCRIPT],
        cwd=SCRIPT_DIR,
        env=env,
    )

    # Stop if a trajectory fails
    if result.returncode != 0:
        print(
            f"ERROR: {trajectory_id} failed "
            f"with exit code {result.returncode}.",
            flush=True,
        )
        print("Stopping collection.")
        sys.exit(result.returncode)

print("\nAll trajectories collected")
print("Saving dataset into robotnik_training_data.csv")