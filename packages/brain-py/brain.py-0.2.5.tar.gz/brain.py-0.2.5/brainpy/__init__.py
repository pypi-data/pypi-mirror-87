# -*- coding: utf-8 -*-

__version__ = "0.2.5"

# "profile" module
from . import profile

# "numpy" module
from . import numpy as numpy

# "connectivity" module
from . import connectivity as connect

# "core_system" module
from . import core_system as core
from .core_system.base import *
from .core_system.neurons import *
from .core_system.synapses import *
from .core_system.network import *
from .core_system import types

# "integration" module
from . import integration
from .integration import integrate
from .integration import DiffEquation
from .integration.integrator import *

# "dynamics" module
from . import dynamics
from .dynamics import PhasePortraitAnalyzer
from .dynamics import BifurcationAnalyzer

# "tools" module
from . import tools

# "visualization" module
from . import visualization as visualize

# other modules
from . import inputs
from . import measure
from . import running
