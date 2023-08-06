# -*- coding: utf-8 -*-
'''
datatypes module for reinforcement learning
===========================================

This module contains datatypes used in `reil`

Classes
-------
Feature: a datatype that accepts initial value and feature generator and
generates new values.

Entity: a datatype to specify `agent` or `subject` information. Used in
`InteractionProtocol`.

InteractionProtocol: a datatype to specifies how an `agent` and a `subject`
interact in an `environment`.

ReilData: the main datatype used to communicate `state`s, `action`s, and `reward`s,
between objects in `reil`.


'''

from .feature import Feature, FeatureType
from .interaction_protocol import InteractionProtocol, Entity
from .reildata import ReilData
