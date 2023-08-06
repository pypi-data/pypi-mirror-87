# This file is part of atooms
# Copyright 2010-2018, Daniele Coslovich

"""Velocity autocorrelation function."""

import numpy

from .correlation import Correlation
from .progress import progress

__all__ = ['Fraction']


class Fraction(Correlation):

    """Fraction"""

    symbol = 'fraction'
    short_name = 'fraction()'
    long_name = 'fraction'
    phasespace = []

    def __init__(self, trajectory, condition=None, norigins=None):
        Correlation.__init__(self, trajectory, grid=[], norigins=norigins)
        self.condition = condition
        tag = condition.replace(' ', '')
        tag = tag.replace('and', '_')
        tag = tag.replace('or', '+')
        tag = tag.replace('"', '')
        tag = tag.replace("'", '')
        tag = tag.replace('==', '')
        tag = tag.replace('!=', '.not')
        tag = tag.replace(',', '-')
        self.tag = tag
        self.tag_description = condition

    def _compute(self):
        origins = range(0, len(self.trajectory), self.skip)
        result = 0.0
        norm = 0
        for i in progress(origins):
            norm += 1
            system = self.trajectory.read(i)
            cnt = 0
            for particle in system.particle:
                if eval(self.condition, particle.__dict__):
                    cnt += 1
            # TODO: fixme
            # result += float(cnt) /
        self.value = []
        self.grid = []
        self.analysis = {'fraction': result / float(norm)}
