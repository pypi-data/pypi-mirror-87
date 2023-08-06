# -*- coding: utf-8 -*-
"""
    points_fl public
"""
from points_fl.permission import Permission
from points_fl.log_provider import LogProvider
from points_fl.inference import Inference
from points_fl.federated_learning import FederatedLearning


class FLServer(FederatedLearning, Inference, LogProvider, Permission):
    """
    FL SDK
    """
    pass
