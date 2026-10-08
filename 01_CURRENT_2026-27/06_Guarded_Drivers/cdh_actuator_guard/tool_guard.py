"""Fail-stop tool interlocks, independent of the Pico serial implementation."""
import math


def pico_packet(command):
    """Encode the dump,dig,pivot protocol recovered from auto_pico.py."""
    dump,dig,pivot = command
    if (dump not in (0,1) or dig not in (0,1) or
        not isinstance(pivot,(int,float)) or not math.isfinite(pivot) or
        abs(pivot) > 1 or (dump and dig)):
        raise ValueError('invalid Pico command')
    return f'{int(dump)},{int(dig)},{pivot:.4f}\n'.encode('ascii')


class ToolGuard:
    def __init__(self, down_sign=0, lift_speed=0.0, min_rpm=1.0, timeout=.25):
        if (down_sign not in (-1,1) or not 0 < lift_speed <= .25 or
            min_rpm <= 0 or timeout <= 0):
            raise ValueError('measured lift sign and bounded pivot speed required')
        self.down_sign,self.lift = down_sign,lift_speed
        self.min_rpm,self.timeout = min_rpm,timeout
        self.command,self.command_time = 'stop',-1e9

    def accept(self, command, now):
        if command not in ('stop','lower','dig','raise','dump') or not math.isfinite(now):
            raise ValueError('invalid tool command')
        self.command,self.command_time = command,now

    def output(self, now, estop, estop_time, upper, upper_time,
               lower, lower_time, dig_rpm=0.0, dig_time=-1e9,
               dump_rpm=0.0, dump_time=-1e9):
        stop = (0.0,0.0,0.0)
        if (estop or now-self.command_time > self.timeout or
            now-estop_time > self.timeout or
            now-upper_time > self.timeout or now-lower_time > self.timeout or
            any(t > now+.1 for t in (self.command_time,estop_time,upper_time,lower_time)) or
            (upper and lower)):
            return stop,'fault'
        if self.command == 'stop':
            return stop,('raised' if upper else 'lowered' if lower else 'stopped')
        if self.command == 'lower':
            if lower:
                return stop,'lowered'
            return (0.0,0.0,self.down_sign*self.lift),'lowering'
        if self.command == 'raise':
            if upper:
                return stop,'raised'
            return (0.0,0.0,-self.down_sign*self.lift),'raising'
        if self.command == 'dig' and lower:
            if now-dig_time <= self.timeout and abs(dig_rpm) >= self.min_rpm:
                return (0,1,0.0),'digging'
            # Command can spin briefly while waiting for measured RPM.
            return (0,1,0.0),'lowered'
        if self.command == 'dump' and upper:
            if now-dump_time <= self.timeout and abs(dump_rpm) >= self.min_rpm:
                return (1,0,0.0),'dumping'
            return (1,0,0.0),'raised'
        return stop,'fault'
