import math
from cereal import log
from common.realtime import DT_CTRL
from selfdrive.controls.lib.latcontrol import LatControl, MIN_STEER_SPEED

STEER_ANGLE_SATURATION_TIMEOUT = 1.0 / DT_CTRL
STEER_ANGLE_SATURATION_THRESHOLD = 2.5  # Degrees


class LatControlAngle(LatControl):
   def update(self, active, CS, CP, VM, params, desired_curvature, desired_curvature_rate, roll):
    angle_log = log.ControlsState.LateralAngleState.new_message()

    if CS.vEgo < MIN_STEER_SPEED or not active:
      angle_log.active = False
      angle_steers_des = float(CS.steeringAngleDeg)
    else:
      angle_log.active = True
      angle_steers_des = math.degrees(VM.get_steer_from_curvature(-desired_curvature, CS.vEgo, roll))
      angle_steers_des += params.angleOffsetDeg

    angle_control_saturated = abs(angle_steers_des - CS.steeringAngleDeg) > STEER_ANGLE_SATURATION_THRESHOLD
    angle_log.saturated = self._check_saturation(angle_control_saturated, CS)
    angle_log.steeringAngleDeg = angle_steers_des
    return 0, float(angle_steers_des), angle_log
