# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Red Hat, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    Pykwalify extensions module.

    Module containing custom validation functions used for schema checking.

    :copyright: (c) 2020 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""


def valid_creds_combo(value, obj_rule, path):

    cloud_file_keys = set(['cloud_file', 'cloud'])
    non_cloud_required_keys = set(['auth_url', 'username', 'password', 'tenant_name'])
    cred_dict = dict()
    
    for c in list(value.values()):
        cred_dict = c

    if len(cred_dict.keys()) > 2 and cloud_file_keys.issubset(cred_dict.keys()):
        raise AssertionError('The cloud_file and cloud credential keys should be used by themselves.')

    if not non_cloud_required_keys.issubset(cred_dict.keys()) and not cloud_file_keys.issubset(cred_dict.keys()):
        raise AssertionError('A required credentials key of auth_url, username, password, or tenant_name is missing.')

    return True
