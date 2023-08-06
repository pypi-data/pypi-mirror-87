class _Sensor:

    def __init__(self, _sensor):
        self.info = f"rom.sensor.{_sensor}.info"
        self.read = f"rom.sensor.{_sensor}.read"
        self.stream = f"rom.sensor.{_sensor}.stream"
        self.close = f"rom.sensor.{_sensor}.close"
        self.sensitivity = f"rom.sensor.{_sensor}.sensitivity"


class _Base:
    def __init__(self, _base):
        self.info = f"rom.actuator.{_base}.info"
        self.write = f"rom.actuator.{_base}.write"
        self.stop = f"rom.actuator.{_base}.stop"


class Behavior:
    def __init__(self):
        self.info = "rom.optional.behavior.info"
        self.play = "rom.optional.behavior.play"
        self.stop = "rom.optional.behavior.stop"


class Audio:
    info = "rom.actuator.audio.info"
    volume = "rom.actuator.audio.volume"
    play = "rom.actuator.audio.play"
    stream = "rom.actuator.audio.stream"
    stop = "rom.actuator.audio.stop"


class Sensor:
    sight = _Sensor("sight")
    hearing = _Sensor("hearing")
    touch = _Sensor("touch")
    propio = _Sensor("proprio")


class Actuator:
    motor = _Base("motor")
    light = _Base("light")
    audio = Audio()


class Optional:
    behavior = Behavior()


class Rom:
    sensor = Sensor()
    actuator = Actuator()
    optional = Optional()
