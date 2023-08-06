from DobotRPC import DobotlinkAdapter, RPCClient


class MagicianGoApi(object):
    def __init__(self):
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    def set_running_mode(self, port_name, mode):
        return self.__dobotlink.MagicianGO.SetRunningMode(portName=port_name,
                                                          runningMode=mode)

    def set_direction_speed(self, port_name, direction, speed):
        return self.__dobotlink.MagicianGO.SetDirectionSpeed(
            portName=port_name, dir=direction, speed=speed)

    def set_move_speed(self, port_name, x, y, r):
        return self.__dobotlink.MagicianGO.SetMoveSpeed(portName=port_name,
                                                        x=x,
                                                        y=y,
                                                        r=r)

    def set_rotate_deg_speed(self, port_name, r, Vr):
        return self.__dobotlink.MagicianGO.SetMoveDistance(
            portName=port_name,
            r=r,
            Vr=Vr,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def set_xy_speed_distance(self, port_name, x, y, Vx, Vy):
        return self.__dobotlink.MagicianGO.SetFixedOrientationMoveDistance(
            portName=port_name,
            x=x,
            y=y,
            Vx=Vx,
            Vy=Vy,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def moveto_destination(self, port_name, x, y, s):
        return self.__dobotlink.MagicianGO.SetWorldCoordinateMovePoint(
            portName=port_name,
            x=x,
            y=y,
            s=s,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def move_radius_arc(self, port_name, velocity, radius, angle, mode):
        return self.__dobotlink.MagicianGO.SetTraceRadiusARC(
            portName=port_name,
            velocity=velocity,
            radius=radius,
            angle=angle,
            mode=mode,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def move_circular_arc(self, port_name, velocity, x, y, angle, mode):
        return self.__dobotlink.MagicianGO.SetTraceCenterARC(
            portName=port_name,
            velocity=velocity,
            x=x,
            y=y,
            angle=angle,
            mode=mode,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def set_coord_closed_loop(self, port_name, isEnable, angle):
        return self.__dobotlink.MagicianGO.SetCoordClosedLoop(
            portName=port_name, isEnable=isEnable, angle=angle)

    def set_increment_closed_loop(self, port_name, x, y, angle):
        return self.__dobotlink.MagicianGO.SetIncrementClosedLoop(
            portName=port_name,
            x=x,
            y=y,
            angle=angle,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    def set_rgb_light(self, port_name, number, effect, r, g, b, cycle, counts):
        return self.__dobotlink.MagicianGO.SetLightRGB(portName=port_name,
                                                       number=number,
                                                       effect=effect,
                                                       r=r,
                                                       g=g,
                                                       b=b,
                                                       cycle=cycle,
                                                       counts=counts)

    def set_buzzer_sound(self, port_name, index, tone, beat):
        return self.__dobotlink.MagicianGO.SetBuzzerSound(portName=port_name,
                                                          index=index,
                                                          tone=tone,
                                                          beat=beat)

    def get_ultrasonic_data(self, port_name):
        return self.__dobotlink.MagicianGO.GetUltrasoundData(
            portName=port_name)

    def get_odometer_data(self, port_name):
        return self.__dobotlink.MagicianGO.GetSpeedometer(portName=port_name)

    def get_power_voltage(self, port_name):
        return self.__dobotlink.MagicianGO.GetBatteryVoltage(
            portName=port_name)

    def get_imu_angle(self, port_name):
        return self.__dobotlink.MagicianGO.GetTraceAngle(portName=port_name)

    def get_imu_acce_anglespeed(self, port_name):
        return self.__dobotlink.MagicianGO.GetImuAcceAnglespeed(
            portName=port_name)

    def set_auto_trace(self, port_name, trace):
        return self.__dobotlink.MagicianGO.SetTraceAuto(portName=port_name,
                                                        isTrace=trace)

    def set_trace_speed(self, port_name, speed):
        return self.__dobotlink.MagicianGO.SetTraceSpeed(portName=port_name,
                                                         speed=speed)

    def set_trace_pid(self, port_name, p, i, d):
        return self.__dobotlink.MagicianGO.SetTracePid(portName=port_name,
                                                       p=p,
                                                       i=i,
                                                       d=d)


# k210

    def get_lite_angle(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210ArmAngleData(
            portName=port_name)

    def get_car_angle(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210CarAngleData(
            portName=port_name)

    def get_lite_deeplearning(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210ArmDeepLearningObj(
            portName=port_name)

    def get_car_deeplearning(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210CarDeepLearningObj(
            portName=port_name)

    def get_lite_apriltag(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210ArmAprilTag(
            portName=port_name)

    def get_car_apriltag(self, port_name):
        return self.__dobotlink.MagicianGO.GetK210CarAprilTag(
            portName=port_name)
