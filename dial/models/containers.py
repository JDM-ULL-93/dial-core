# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .model_loader import VGG16Loader

PredefinedModels = containers.DynamicContainer()

PredefinedModels.VGG16 = providers.Factory(VGG16Loader)
