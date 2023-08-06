#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) Jason Young (杨郑鑫).
#
# E-Mail: <AI.Jason.Young@outlook.com>
# 2020-10-30 11:12
#
# This source code is licensed under the WTFPL license found in the
# LICENSE file in the root directory of this source tree.


import os
import sys
import importlib


def import_modules(directory, package=None):
    if os.path.isdir(directory):
        file_names = os.listdir(directory)
    else:
        file_names = list()

    if package is None:
        sys.path.insert(0, directory)
        print(sys.path)

    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            if file_name.startswith('_') or file_name.startswith('.'):
                continue
            if file_name.endswith('.py'):
                module_name = file_name[:file_name.find('.py')]
                if package is None:
                    module_name = f'user_{module_name}'
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                else:
                    importlib.import_module('.' + module_name, package=package)


class Registration(object):
    def __init__(self, registration_type):
        self.registration_type = registration_type
        self.registered_class_table = dict()
        self.registered_class_names = set()

    def __getitem__(self, registration_name):
        return self.registered_class_table[registration_name]

    def register(self, registration_name):
        def register_class(class_definition):
            self.check(registration_name, class_definition)
            self.registered_class_table[registration_name] = class_definition
            self.registered_class_names.add(class_definition.__name__)
            return class_definition
        return register_class

    def check(self, registration_name, class_definition):
        if registration_name in self.registered_class_table:
            raise ValueError(f'\'{registration_name}\'(type \'{self.registration_type}\') has been registered.')
        if not issubclass(class_definition, self.registration_type):
            raise ValueError(f'\'{registration_name}\':\'{class_definition}\' is being registered to a wrong type(\'{self.registration_type}\') of registry.')
        if class_definition.__name__ in self.registered_class_names:
            raise ValueError(f'The class name of \'{registration_name}\':\'{class_definition}\' has been used.')
