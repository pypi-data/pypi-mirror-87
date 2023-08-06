from DobotRPC import DobotlinkAdapter, RPCClient, loggers
import inspect


class MagicianGoApi(object):
    def __init__(self, port_name=None):
        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)
        self._port_name = port_name

    def get_portname(func):
        def wrapper(self, *args, **kwargs):
            if self._port_name:
                if not kwargs.get("port_name", None):
                    kwargs["port_name"] = self._port_name
            else:
                inspect.signature(func)
                if len(kwargs) + len(args) + len(
                        func.__defaults__) != func.__code__.co_argcount - 1:
                    loggers.get('liteApi').error(
                        "Your parameters are not enough, please check them carefully."
                    )
            return func(self, *args, **kwargs)

        return wrapper

    @get_portname
    def set_running_mode(self, port_name, mode):
        return self.__dobotlink.MagicianGO.SetRunningMode(portName=port_name,
                                                          runningMode=mode)

    @get_portname
    def set_move_speed_direct(self, port_name, direction, speed):
        return self.__dobotlink.MagicianGO.SetMoveSpeedDirect(
            portName=port_name, dir=direction, speed=speed)

    @get_portname
    def set_move_speed(self, port_name, x, y, r):
        return self.__dobotlink.MagicianGO.SetMoveSpeed(portName=port_name,
                                                        x=x,
                                                        y=y,
                                                        r=r)

    @get_portname
    def set_rotate(self, port_name, r, Vr):
        return self.__dobotlink.MagicianGO.SetRotate(
            portName=port_name,
            r=r,
            Vr=Vr,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_move_dist(self, port_name, x, y, Vx, Vy):
        return self.__dobotlink.MagicianGO.SetMoveDist(
            portName=port_name,
            x=x,
            y=y,
            Vx=Vx,
            Vy=Vy,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_move_pos(self, port_name, x, y, s):
        return self.__dobotlink.MagicianGO.SetMovePos(
            portName=port_name,
            x=x,
            y=y,
            s=s,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_arc_rad(self, port_name, velocity, radius, angle, mode):
        return self.__dobotlink.MagicianGO.SetArcRad(
            portName=port_name,
            velocity=velocity,
            radius=radius,
            angle=angle,
            mode=mode,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_arc_cent(self, port_name, velocity, x, y, angle, mode):
        return self.__dobotlink.MagicianGO.SetArcCent(
            portName=port_name,
            velocity=velocity,
            x=x,
            y=y,
            angle=angle,
            mode=mode,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_coord_closed_loop(self, port_name, isEnable, angle):
        return self.__dobotlink.MagicianGO.SetCoordClosedLoop(
            portName=port_name, isEnable=isEnable, angle=angle)

    @get_portname
    def set_increment_closed_loop(self, port_name, x, y, angle):
        return self.__dobotlink.MagicianGO.SetIncrementClosedLoop(
            portName=port_name,
            x=x,
            y=y,
            angle=angle,
            isQueued=True,
            isWaitForFinish=True,
            timeout=604800000)

    @get_portname
    def set_rgb_light(self, port_name, number, effect, r, g, b, cycle, counts):
        return self.__dobotlink.MagicianGO.SetLightRGB(portName=port_name,
                                                       number=number,
                                                       effect=effect,
                                                       r=r,
                                                       g=g,
                                                       b=b,
                                                       cycle=cycle,
                                                       counts=counts)

    @get_portname
    def set_buzzer_sound(self, port_name, index, tone, beat):
        return self.__dobotlink.MagicianGO.SetBuzzerSound(portName=port_name,
                                                          index=index,
                                                          tone=tone,
                                                          beat=beat)

    @get_portname
    def get_ultrasonic_data(self, port_name):
        return self.__dobotlink.MagicianGO.GetUltrasoundData(
            portName=port_name)

    @get_portname
    def get_odometer_data(self, port_name):
        return self.__dobotlink.MagicianGO.GetSpeedometer(portName=port_name)

    @get_portname
    def get_power_voltage(self, port_name):
        return self.__dobotlink.MagicianGO.GetBatteryVoltage(
            portName=port_name)

    @get_portname
    def get_imu_angle(self, port_name):
        return self.__dobotlink.MagicianGO.GetImuAngle(portName=port_name)

    @get_portname
    def get_imu_speed(self, port_name):
        return self.__dobotlink.MagicianGO.GetImuSpeed(
            portName=port_name)

    @get_portname
    def set_auto_trace(self, port_name, trace):
        return self.__dobotlink.MagicianGO.SetTraceAuto(portName=port_name,
                                                        isTrace=trace)

    @get_portname
    def set_trace_speed(self, port_name, speed):
        return self.__dobotlink.MagicianGO.SetTraceSpeed(portName=port_name,
                                                         speed=speed)

    @get_portname
    def set_trace_pid(self, port_name, p, i, d):
        return self.__dobotlink.MagicianGO.SetTracePid(portName=port_name,
                                                       p=p,
                                                       i=i,
                                                       d=d)

    @get_portname
    def get_trace_angle(self, port_name):
        return self.__dobotlink.MagicianGO.GetCarCameraAngle(
            portName=port_name)

    @get_portname
    def get_arm_camera_obj(self, port_name):
        return self.__dobotlink.MagicianGO.GetArmCameraObj(
            portName=port_name)

    @get_portname
    def get_car_camera_obj(self, port_name):
        return self.__dobotlink.MagicianGO.GetCarCameraObj(
            portName=port_name)

    @get_portname
    def get_arm_camera_tag(self, port_name):
        return self.__dobotlink.MagicianGO.GetArmCameraTag(
            portName=port_name)

