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
    teflo_openstack_client_plugin.teflo_openstack_client_plugin.os_client_provisioner

    Provisionern Plugin module for the openstack client

    :copyright: (c) 2020 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""
import yaml
import os
import copy
import time
from os import path
from teflo.core import ProvisionerPlugin
from teflo.exceptions import TefloProvisionerError
from teflo.helpers import schema_validator, filter_host_name, gen_random_str
from .helpers import generate_cbn_response, set_key_permissions, map_cbn_resp_to_opts, concurrent_cmd_execute
from ospclientsdk import ClientShell


class OpenstackClientProvisionerPlugin(ProvisionerPlugin):
    __plugin_name__ = 'openstack-client'

    __schema_file_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                        "files/schema.yml"))
    __schema_ext_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "files/osp_schema_extensions.py"))

    def __init__(self, asset):
        super(OpenstackClientProvisionerPlugin, self).__init__(asset)
        # creating logger for this plugin to get added to teflo's loggers
        self.create_logger(name='teflo_openstack_client_plugin', data_folder=self.config.get('DATA_FOLDER'))
        self.create_logger(name='ospclientsdk', data_folder=self.config.get('DATA_FOLDER'))
        self.osp_client = ClientShell()
        self.config_params = dict()
        for item in self.config['PROVISIONER_OPTIONS']:
            if item['name'] == self.__plugin_name__:
                self.config_params = item
                break

    def _load_credentials(self):
        """
        Will load the credentials into the ospclientsdk

        :return:
        """

        if self.provider_credentials:
            if 'cloud_file' in self.provider_credentials:
                with open(path.abspath(path.expanduser(path.expanduser(self.provider_credentials.get('cloud_file'
                                                                                                     )
                                                                       )
                                                       )
                                       )
                          ) as f:
                    cloud_dict = yaml.safe_load(f)
                    cloud = 'openstack' if 'cloud' not in self.provider_credentials else \
                        self.provider_credentials.get('cloud')
                    self.osp_client.load_cloud_config(cloud_dict=cloud_dict, cloud=cloud)
                    return
            self.osp_client.load_cloud_config(self.provider_credentials)
        else:
            self.logger.warning('No teflo credential is being used. Assuming using provisioner specific method. ')

    def find_best_available_network(self, server_opts):
        """
        High level API to be able to locate the best network available ips for a
        as server to be attached to. It updates the command options with the network

        :param server_opts: dictionary of server options
        :return: dictionary of server options
        """

        if self.config_params.get('best_available_network', False) == 'True':
            self.logger.info("Looking for best available network.")
            nets = dict()
            net_filter = self.config_params.get('best_available_network_filter', [])
            if net_filter:
                net_filter = [net for net in net_filter.replace(' ', '').split(',')]
            count = self.config_params.get('best_available_network_count', None)
            ip_opts = dict(ip_version=str(4)) if 'best_available_network_ip_version' not in self.config_params \
                else dict(ip_version=self.config_params.get('best_available_network_ip_version', {}))
            results = self.osp_client.network.ip_availability_list(ip_opts)
            if results['rc'] != 0:
                self.logger.error('Command did not execute successfully')
                self.logger.error(results['stderr'])
                raise TefloProvisionerError('There was an error trying to check the available ips of network.')
            networks = results['stdout']
            if filter:
                networks = [net for net in networks for fil in net_filter if net['Network Name'] == fil]
            for net in networks:
                nets[net.get('Network Name')] = net.get('Total IPs') - net.get('Used IPs')

            nets = sorted(nets.items(), key=lambda x: x[1], reverse=True)
            if count and count > len(nets):
                self.logger.error("The count value is higher than the available networks.")
                raise TefloProvisionerError('Failed to find the available list of networks.')
            elif count:
                if 'network' in server_opts:
                    server_opts.get('network').extend([nets[i][0] for i in range(0, count)])
                else:
                    server_opts.update(dict(network=
                                            [nets[i][0] for i in range(0, count)]
                                            )
                                       )
            else:
                self.logger.info("Found network %s with the most ips." % nets[0][0])
                if 'network' in server_opts:
                    nets = list(set([nets[0][0]]).union(server_opts.get('network')))
                    server_opts.update(dict(network=nets))
                else:
                    server_opts.update(dict(network=[nets[0][0]]))
        return server_opts

    def wait_for_asset_status(self, asset_opts, name):
        """
        High level api that has the logic on how to use
        the server max function naming scheme and whether to call
        the lower level API directly for single server status checking
        or the helper function for 'max' concurrent status checking


        :param asset_opts: tuple of command and dictionary of options
        :param name: string name of the asset
        :return: a list of the dictionary response
        """

        resp = []
        max_inst = []
        if 'max' in asset_opts[1] and asset_opts[1]['max']:
            max_inst.append(name)
            for i in range(2, asset_opts[1]['max']+1):
                max_inst.append(name[:-1]+str(i))

        if 'server' in asset_opts and not max_inst:
            resp = [self._wait_for_active_state(asset_opts, name)]
        else:
            resp = concurrent_cmd_execute(getattr(self, '_wait_for_active_state'), asset_opts, max_inst)
        return resp

    def _wait_for_active_state(self, *args, **kwargs):
        """
        This implements the low-level status checking for Server resources.

        :param args: a tuple of arguments
        :param kwargs: a dictionary of arguments
        :return: a dictionary of the response status of the asset
        """

        cmd = args[0][0]
        name = args[1]
        status = 0
        attempt = 1
        cmd = '%s_show' % cmd
        cg = ""
        for cg, cs in getattr(self.osp_client, 'all_osp_cmd_groups').items():
            for c in cs:
                if cmd == c:
                    while attempt <= 30:
                        results = getattr(getattr(self.osp_client, cg), cmd)(dict(res=name))
                        if results['rc'] != 0:
                            self.logger.error(results['stderr'])
                            raise TefloProvisionerError('Waiting for asset status failed.')
                        results = results['stdout']
                        msg = '%s. ASSET %s, STATE=%s' % (attempt, results.get('name'), results.get('status'))

                        if results.get('status').lower() == 'error':
                            self.logger.info(msg)
                            self.logger.error('Asset %s got an into an error state!' %
                                              results.get('name'))
                            break
                        elif results.get('status').lower() == 'active':
                            self.logger.info(msg)
                            self.logger.info('Asset %s successfully finished building!' %
                                             results.get('name'))
                            status = 1
                            break
                        else:
                            self.logger.info('%s, rechecking in 20 seconds.', msg)
                            time.sleep(20)

                    if status:
                        self.logger.info('Node %s successfully finished building.' %
                                         results.get('name'))
                        return results
                    else:
                        raise TefloProvisionerError('Node was unable to build, %s' %
                                                     results.get('name'))

    def _process_create_results(self, results, cp_opts, name):
        """
        Final processing of the dictionary results from the provider. This will monitor
        for status of a server, modify keypair properties, and will generate the teflo response.

        :param results: a dictionary respone of the output
        :param cp_opts: a tuple of command and dictionary options
        :param name: a string of the asset name
        :return: list of teflo generated response dictionaries
        """
        resp = []
        if len(results['stdout']) != 0:
            resp.append(results['stdout'])
            self.logger.debug(resp)
            if 'server' in cp_opts:
                resp = self.wait_for_asset_status(cp_opts, resp[-1].get('name'))
            if 'keypair' in cp_opts:
                set_key_permissions(cp_opts)
            resp = generate_cbn_response(resp, self.config_params.get('public_network', None))
            self.logger.debug(resp)
            self.logger.info('Provisioning Asset %s is complete.' % name)

        return resp

    def _create(self, cp_opts, name):
        """
        Implements the actually create/add/set logic to the ospclientsdk

        :param cp_opts: tuple of command and dictionary options
        :param name: string anme of the resource
        :return: dictionary information about the asset from the provider
        """

        cmd = cp_opts[0]
        opts = cp_opts[1]

        if not self.osp_client.is_valid_command(cmd):
            cmd = '%s_create' % cmd
            if not self.osp_client.is_valid_command(cmd):
                raise TefloProvisionerError('%s is not a valid command supported by this provisioner.' % cmd)
        if cmd == 'server_create':
            opts = self.find_best_available_network(opts)
        if not opts.get('res', False):
            opts.update(res=name)
        try:
            for cg, cs in getattr(self.osp_client, 'all_osp_cmd_groups').items():
                for c in cs:
                    if cmd == c:
                        results = getattr(getattr(self.osp_client, cg), cmd)(opts)
                        break
        except AttributeError as ex:
            results = self.osp_client.run_command(cmd, opts)

        return results

    def _delete(self, cp_opts, name):
        """
        Implements the actual delete/remove logic to the ospclientsdk

        :param cp_opts: a tuple of command and arguments
        :param name: string name of the asset being deleted
        :return: dictionary response of the output
        """
        asset = getattr(self.asset, 'asset_id') if getattr(self.asset, 'asset_id', None) else name
        opts = {'res': asset}
        cmd = cp_opts[0]
        if cmd.find('add') == -1:
            cmd += '_delete'
        else:
            cmd = cmd.replace('add', 'remove')
            opts.update({'tgt_res': cp_opts[1].get('tgt_res')})
        time.sleep(15)
        try:
            for cg, cs in getattr(self.osp_client, 'all_osp_cmd_groups').items():
                for c in cs:
                    if cmd == c:
                        return getattr(getattr(self.osp_client, cg), cmd)(opts)
        except AttributeError as ex:
            return self.osp_client.run_command(cmd, opts)

    def _run_action(self, *args, **kwargs):
        """
        Runs the action desired and provides the retry logic when an action fails

        :param args:  a tuple of arguments
        :param kwargs: a dictionary of arguments
        :return: a dictionary of resource information from the provider
        """

        attempts = 1
        action = args[0]
        cp_opts = args[1]
        name = args[2]
        retries = int(self.config_params.get('retry_attempts', 0))
        wait_time = int(self.config_params.get('retry_wait', 0))
        results = getattr(self, action)(cp_opts, name)
        cleaned_up = False

        if results['rc'] != 0:
            if retries > 0 and wait_time > 0:
                # let's a attempt a cleanup before we do the retries just in case the
                # failure is the type that leaves a partially provisioned resource.
                # Perfect example is when an instance is being provisioned but ends up in
                # an error state because ips on the network have been exhausted.
                if action == '_create' and not cleaned_up:
                    rs = self._delete(cp_opts, name)
                    if rs['rc'] == 0:
                        self.logger.info("Successfully cleaned up failed attempt.")
                    else:
                        self.logger.warning("Attempted cleanup up failed. Resource might not exist.")
                    cleaned_up = True
                while attempts <= retries:
                    self.logger.error(results['stderr'])
                    self.logger.warning("Failed but retrying in %s seconds." % wait_time)
                    time.sleep(wait_time)
                    results = getattr(self, action)(cp_opts, name)
                    if results and results['rc'] != 0:
                        self.logger.warning("Failed retry attempt %s." % attempts)
                        attempts += 1
                        continue
                    return results
            self.logger.error('Command did not execute successfully')
            raise TefloProvisionerError(results['stderr'])

        return results

    def create(self):
        """Create method. (must implement!)

        Provision the asset supplied.
        """
        results = []
        # checking if unique_name is set in the teflo.cfg file.
        if self.config_params.get('unique_name', 'false').lower() == 'true':
            name = filter_host_name(getattr(self.asset, 'name')) + '_%s' % gen_random_str(5)
        else:
            name = getattr(self.asset, 'name')
        self.logger.info('Provisioning Asset %s.' % name)
        self._load_credentials()
        cp_opts = copy.deepcopy(self.provider_params)
        for cp_opt in cp_opts.items():
            if not isinstance(cp_opt[1], list):
                # This will provide users an abstraction of 'max' for non server resources
                if 'server' != cp_opt[0] and 'max' in cp_opt[1] and cp_opt[1]['max']:
                    max_inst = list()
                    for i in range(1, cp_opt[1]['max']+1):
                        max_inst.append(name + '-' + str(i))
                    del cp_opt[1]['max']
                    rs = concurrent_cmd_execute(getattr(self, '_run_action'), '_create', cp_opt, max_inst)
                    for r in rs:
                        results.extend(self._process_create_results(r, cp_opt, name))
                    continue

                # if not 'max' proceed as normal
                result = self._run_action('_create', cp_opt, name)
                results.extend(self._process_create_results(result, cp_opt, name))
            else:
                # This is so that when a user specifies multiple actions like add/set
                # in a single asset block
                for opt in cp_opt[1]:
                    result = self._run_action('_create', (cp_opt[0], opt), name)
                    results.extend(self._process_create_results(result, (cp_opt[0], opt), name))

        # Finalize mapping
        results = map_cbn_resp_to_opts(results, self.provider_params)

        return results

    def delete(self):
        """Delete method. (must implement!)

        Teardown the asset supplied.
        """

        name = getattr(self.asset, 'name')
        self.logger.info('Destroying Asset %s.' % name)
        self._load_credentials()
        cp_opts = copy.deepcopy(self.provider_params)
        # Filter out any 'set' actions since we really don't need to issue 'unset'
        cp_opts = {k:v for k, v in cp_opts.items() if k.find('set') == -1}

        # reverse the order in case actions like 'add' were called during create
        # this way the 'remove' action can be called before 'delete' calls
        for cp_opt in sorted(cp_opts.items(), key=lambda x: x[0], reverse=True):
            if not isinstance(cp_opt[1], list):
                self._run_action('_delete', cp_opt, name)
            else:
                # This is so that when a user specifies multiple actions like add/set
                # in a single asset block
                for opt in cp_opt[1]:
                    self._run_action('_delete', (cp_opt[0], opt), name)


    def authenticate(self):
        raise NotImplementedError

    def validate(self):

        # Validate commands with the osp client api
        for cmd in self.provider_params:
            if cmd.find('add') != -1 or cmd.find('set') != -1:
                if not self.osp_client.is_valid_command(cmd):
                    raise TefloProvisionerError('There is no command group that supports this command: %s.' % cmd)
                continue
            if not self.osp_client.is_valid_command("%s_create" % cmd) \
                    or not self.osp_client.is_valid_command("%s_delete" % cmd):
                raise TefloProvisionerError('There is no command group that supports this command: %s.' % cmd)
            continue

        # validate teflo plugin schema
        schema_validator(schema_data=self.build_profile(self.asset),
                         schema_files=[self.__schema_file_path__],
                         schema_ext_files=[self.__schema_ext_path__])
