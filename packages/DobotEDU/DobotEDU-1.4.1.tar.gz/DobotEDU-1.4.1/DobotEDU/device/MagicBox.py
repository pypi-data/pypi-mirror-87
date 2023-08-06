from DobotRPC import DobotlinkAdapter, RPCClient, loggers
import inspect


class MagicBoxApi(object):
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

    def search_dobot(self):
        return self.__dobotlink.MagicBox.SearchDobot()

    @get_portname
    def connect_dobot(self, port_name, queue_start=True, is_queued=False):
        return self.__dobotlink.MagicBox.ConnectDobot(portName=port_name,
                                                      queueStart=queue_start,
                                                      isQueued=is_queued)

    @get_portname
    def disconnect_dobot(self,
                         port_name,
                         queue_stop=True,
                         queue_clear=True,
                         is_queued=False):
        return self.__dobotlink.MagicBox.DisconnectDobot(
            portName=port_name,
            queueStop=queue_stop,
            queueClear=queue_clear,
            isQueued=is_queued)

    @get_portname
    def get_devicesn(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceSN(portName=port_name,
                                                     isQueued=is_queued)

    @get_portname
    def set_devicename(self, port_name, device_name: str, is_queued=False):
        return self.__dobotlink.MagicBox.SetDeviceName(portName=port_name,
                                                       deviceName=device_name,
                                                       isQueued=is_queued)

    @get_portname
    def get_devicename(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceName(portName=port_name,
                                                       isQueued=is_queued)

    @get_portname
    def get_deviceversion(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceVersion(portName=port_name,
                                                          isQueued=is_queued)

    @get_portname
    def set_devicewithl(self,
                        port_name,
                        enable=True,
                        version=1,
                        is_queued=False):
        return self.__dobotlink.MagicBox.SetDeviceWithL(portName=port_name,
                                                        enable=enable,
                                                        version=version,
                                                        isQueued=is_queued)

    @get_portname
    def get_devicewithl(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceWithL(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def get_devicetime(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceTime(portName=port_name,
                                                       isQueued=is_queued)

    @get_portname
    def get_deviceid(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetDeviceID(portName=port_name,
                                                     isQueued=is_queued)

    @get_portname
    def get_productname(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetProductName(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def set_oleddisplay(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.SetOLEDDisplay(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def queuedcmd_start(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.QueuedCmdStart(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def queuedcmd_stop(self, port_name, force_stop=False, is_queued=False):
        return self.__dobotlink.MagicBox.QueuedCmdStop(portName=port_name,
                                                       forceStop=force_stop,
                                                       isQueued=is_queued)

    @get_portname
    def queuedcmd_clear(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.QueuedCmdClear(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def queuedcmd_startdownload(self,
                                port_name,
                                total_loop: int,
                                lineper_loop: int,
                                is_queued=False):
        return self.__dobotlink.MagicBox.QueuedCmdStartDownload(
            portName=port_name,
            totalLoop=total_loop,
            linePerLoop=lineper_loop,
            isQueued=is_queued)

    @get_portname
    def queuedcmd_stopdownload(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.QueuedCmdStopDownload(
            portName=port_name, isQueued=is_queued)

    @get_portname
    def get_queuedcmd_currentindex(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetQueuedCmdCurrentIndex(
            portName=port_name, isQueued=is_queued)

    @get_portname
    def get_queuedcmd_leftspace(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetQueuedCmdLeftSpace(
            portName=port_name, isQueued=is_queued)

    @get_portname
    def set_servo_angle(self,
                        port_name,
                        index: int,
                        set_value: float,
                        is_queued=False):
        return self.__dobotlink.MagicBox.SetServoAngle(portName=port_name,
                                                       index=index,
                                                       value=set_value,
                                                       isQueued=is_queued)

    @get_portname
    def get_servo_angle(self, port_name, index: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetServoAngle(portName=port_name,
                                                       index=index,
                                                       isQueued=is_queued)

    @get_portname
    def set_lspeed_ratio(self,
                         port_name,
                         set_type: int,
                         set_value: int,
                         is_queued=False):
        return self.__dobotlink.MagicBox.SetLSpeedRatio(portName=port_name,
                                                        type=set_type,
                                                        value=set_value,
                                                        isQueued=is_queued)

    @get_portname
    def get_lspeed_ratio(self, port_name, get_type: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetLSpeedRatio(portName=port_name,
                                                        type=get_type,
                                                        isQueued=is_queued)

    @get_portname
    def get_posel(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetPoseL(portName=port_name,
                                                  isQueued=is_queued)

    @get_portname
    def set_ptpwith_lcmd(self,
                         port_name,
                         set_l: float,
                         is_queued=True,
                         iswait_forfinish=True,
                         timeout=30000):
        return self.__dobotlink.MagicBox.SetPTPWithLCmd(
            portName=port_name,
            l=set_l,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=timeout)

    @get_portname
    def set_iomultiplexing(self,
                           port_name,
                           port: int,
                           multiplex: int,
                           is_queued=False):
        return self.__dobotlink.MagicBox.SetIOMultiplexing(portName=port_name,
                                                           port=port,
                                                           multiplex=multiplex,
                                                           isQueued=is_queued)

    @get_portname
    def get_iomultiplexing(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetIOMultiplexing(portName=port_name,
                                                           port=port,
                                                           isQueued=is_queued)

    @get_portname
    def set_iodo(self, port_name, port: int, level: int, is_queued=False):
        return self.__dobotlink.MagicBox.SetIODO(portName=port_name,
                                                 port=port,
                                                 level=level,
                                                 isQueued=is_queued)

    @get_portname
    def get_iodo(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetIODO(portName=port_name,
                                                 port=port,
                                                 isQueued=is_queued)

    @get_portname
    def set_iopwm(self,
                  port_name,
                  port: int,
                  frequency: float,
                  duty_cycle: float,
                  is_queued=False):
        return self.__dobotlink.MagicBox.SetIOPWM(portName=port_name,
                                                  port=port,
                                                  frequency=frequency,
                                                  dutyCycle=duty_cycle,
                                                  isQueued=is_queued)

    @get_portname
    def get_iopwm(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetIOPWM(portName=port_name,
                                                  port=port,
                                                  isQueued=is_queued)

    @get_portname
    def get_iodi(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetIODI(portName=port_name,
                                                 port=port,
                                                 isQueued=is_queued)

    @get_portname
    def get_ioadc(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetIOADC(portName=port_name,
                                                  port=port,
                                                  isQueued=is_queued)

    @get_portname
    def set_emotor(self,
                   port_name,
                   index: int,
                   enable: bool,
                   speed,
                   is_queued=False):
        return self.__dobotlink.MagicBox.SetEMotor(portName=port_name,
                                                   index=index,
                                                   enable=enable,
                                                   speed=speed,
                                                   isQueued=is_queued)

    @get_portname
    def set_emotors(self,
                    port_name,
                    index: int,
                    enable: bool,
                    speed,
                    distance,
                    is_queued=False):
        return self.__dobotlink.MagicBox.SetEMotorS(portName=port_name,
                                                    index=index,
                                                    enable=enable,
                                                    speed=speed,
                                                    distance=distance,
                                                    isQueued=is_queued)

    @get_portname
    def set_color_sensor(self,
                         port_name,
                         port: int,
                         enable: bool,
                         version: int,
                         is_queued=False):
        return self.__dobotlink.MagicBox.SetColorSensor(portName=port_name,
                                                        port=port - 1,
                                                        enable=enable,
                                                        version=version,
                                                        isQueued=is_queued)

    @get_portname
    def get_color_sensor(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetColorSensor(portName=port_name,
                                                        isQueued=is_queued)

    @get_portname
    def set_infrared_sensor(self,
                            port_name,
                            port: int,
                            enable: bool,
                            version: int,
                            is_queued=False):
        return self.__dobotlink.MagicBox.SetInfraredSensor(portName=port_name,
                                                           port=port - 1,
                                                           enable=enable,
                                                           version=version,
                                                           isQueued=is_queued)

    @get_portname
    def get_infrared_sensor(self, port_name, port: int, is_queued=False):
        return self.__dobotlink.MagicBox.GetInfraredSensor(portName=port_name,
                                                           port=port - 1,
                                                           isQueued=is_queued)

    @get_portname
    def set_homecmd(self,
                    port_name,
                    is_queued=True,
                    iswait_forfinish=True,
                    time_out=25000):
        return self.__dobotlink.MagicBox.SetHOMECmd(
            portName=port_name,
            isQueued=is_queued,
            isWaitForFinish=iswait_forfinish,
            timeout=time_out)

    @get_portname
    def set_jogl_params(self,
                        port_name,
                        velocity,
                        acceleration,
                        is_queued=False):
        return self.__dobotlink.MagicBox.SetJOGLParams(
            portName=port_name,
            velocity=velocity,
            acceleration=acceleration,
            isQueued=is_queued)

    @get_portname
    def get_jogl_params(self, port_name, is_queued=False):
        return self.__dobotlink.MagicBox.GetJOGLParams(portName=port_name,
                                                       isQueued=is_queued)

    @get_portname
    def set_jogcmd(self, port_name, is_joint: bool, cmd: int, is_queued=True):
        return self.__dobotlink.MagicBox.SetJOGCmd(portName=port_name,
                                                   isJoint=is_joint,
                                                   cmd=cmd,
                                                   isQueued=is_queued)
