"""
logx: nice print.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2020 Min Latt.
License: MIT, see LICENSE for more details.
"""

import logging
from rich import print as p


class Plug:
    def __init__(self, _log=False):
        """Use __constructor__.out method, this will handle the rest.
        """
        self.debug = _log
        self.t_io, self.shape, self.m_io = [] , [], []

        _format = "%(asctime)s: %(self.m_io)s"
        _level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(format=_format, level=_level, datefmt="%H:%M:%S")

    def c(self, *argv):
        self.m_io.clear()
        self.t_io.clear()
        self.shape.clear()

        for arg in argv:
            try:
                self.m_io.append(arg)
                self.t_io.append(type(arg))
                self.shape.append(arg.shape)
            except AttributeError:
                self.shape.append(None)

            except Exception as e:
                p(e)

        if not self.debug:
            for i in range(len(self.m_io)):
                self.print_danger(self.m_io[i])
                if (self.shape[i]) == None:
                    p('{0}'.format(self.t_io[i]))
                else:
                    p('{0} => shape: {1}'.format(self.t_io[i], self.shape[i]))
        else:
            pass

    def print_danger(self, m):
        p('[italic red]{0}[/italic red]'.format(m))


""" this? maybe I previously play with JS -'D """

def print(*argv):
    data, data_type, data_shape = [], [], []
    for arg in argv:
        try:
            data.append(arg)
            data_type.append(type(arg))
            data_shape.append(arg.shape)
        except AttributeError:
            data_shape.append(None)
        except Exception as e:
            print_danger(e)

    for i in range(len(data)):
        print_danger(data[i])
        if (data_shape[i] != None):
            p('{0} => shape: {1}'.format(data_type[i], data_shape[i]))
        else:
            p('{0}'.format(data_type[i]))


def print_danger(m):
    p('[italic red]{0}[/italic red]'.format(m))