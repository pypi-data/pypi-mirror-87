from __future__ import division

from .container import Container, interact


class Servo(Container):
    def __init__(self, id, alias, device):
        Container.__init__(self, 'Servo', id, alias, device)
        self._max_angle = 180.0
        self._min_pulse = 0.0005
        self._max_pulse = 0.0015
        self._angle = 0.0

    @property
    def rot_position(self):
        return self._angle

    @rot_position.setter
    def rot_position(self, new_pos):
        self._angle = new_pos
        self._push_value('target_rot_position', new_pos)

    @property
    def max_angle(self):
        return self._max_angle

    @max_angle.setter
    def max_angle(self, new):
        self._max_angle = new
        param = [self._max_angle, self._min_pulse, self._max_pulse]
        self._push_value('parameters', param)

    @property
    def min_pulse(self):
        return self._min_pulse

    @min_pulse.setter
    def min_pulse(self, new):
        self._min_pulse = new
        param = [self._max_angle, self._min_pulse, self._max_pulse]
        self._push_value('parameters', param)

    @property
    def max_pulse(self):
        return self._max_pulse

    @max_pulse.setter
    def max_pulse(self, new):
        self._max_pulse = new
        param = [self._max_angle, self._min_pulse, self._max_pulse]
        self._push_value('parameters', param)

    def _update(self, new_state):
        Container._update(self, new_state)

    def control(self):
        def move(position):
            self.position = position

        return interact(move, position=(0, 180, 1))
