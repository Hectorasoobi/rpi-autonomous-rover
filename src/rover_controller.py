"""Differential-drive autonomous rover navigation and sensor safety controller."""

from dataclasses import dataclass


@dataclass
class SensorTelemetry:
    front_distance_cm: float
    left_distance_cm: float
    right_distance_cm: float
    ir_edge_detected: bool
    heartbeat_age_ms: int


def compute_drive_pwm(telemetry: SensorTelemetry, max_pwm: int = 255) -> tuple[int, int]:
    """Return (left_pwm, right_pwm) motor commands with obstacle and watchdog safety."""
    if telemetry.heartbeat_age_ms > 500 or telemetry.ir_edge_detected:
        return (0, 0)

    safe_clearance_cm = 35.0
    if telemetry.front_distance_cm < safe_clearance_cm:
        turn_pwm = int(max_pwm * 0.55)
        if telemetry.left_distance_cm >= telemetry.right_distance_cm:
            return (-turn_pwm, turn_pwm)
        return (turn_pwm, -turn_pwm)

    cruise_pwm = int(max_pwm * 0.75)
    steering_bias = int((telemetry.right_distance_cm - telemetry.left_distance_cm) * 0.4)
    left_pwm = max(0, min(max_pwm, cruise_pwm - steering_bias))
    right_pwm = max(0, min(max_pwm, cruise_pwm + steering_bias))
    return (left_pwm, right_pwm)


if __name__ == "__main__":
    sample = SensorTelemetry(
        front_distance_cm=28.5,
        left_distance_cm=95.0,
        right_distance_cm=40.0,
        ir_edge_detected=False,
        heartbeat_age_ms=42,
    )
    print("Drive PWM:", compute_drive_pwm(sample))
