import os
import stat
import concurrent.futures
from logging import getLogger
from fnmatch import fnmatch
from concurrent.futures import ThreadPoolExecutor
from teflo.helpers import HelpersError
from teflo.exceptions import TefloProvisionerError

LOG = getLogger(__name__)


def concurrent_cmd_execute(func, *args, **kwargs):
    """
    provides the ability to execute a function concurrently using
    threads

    :param func: the function to execute
    :param args: args to pass to function
    :param kwargs: kwargs to pass to function
    :return: list
    """
    resp = []
    future_to_inst = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with it's instance name
        if len(args) == 3:
            # Assume we are running a function like run_action that takes 3 arguments
            future_to_inst = {executor.submit(func, args[0], args[1], name):
                                  name for name in args[-1]}
        if len(args) == 2:
            # Assume it's a function that only takes two arguments
            future_to_inst = {executor.submit(func, args[0], name):
                                  name for name in args[-1]}
        for future in concurrent.futures.as_completed(future_to_inst):
            inst = future_to_inst[future]
            try:
                data = future.result()
                resp.append(data)
            except Exception as exc:
                raise TefloProvisionerError(exc)
    return resp


def map_cbn_resp_to_opts(reslist, cp_opts):
    """
    Meant to take response dictionaries and map them to their appropriate
    options. This is specifically for when you try to use max count
    functionality and you also want to run add/set type actions once max
    resources are provisioned. So that when the asset_provisioner gets the
    list of response. It will create separate assets with their appropriate
    actions.

    :param reslist: list of cbn response dictionaries
    :param cp_opts: dictionary of command options provided
    :return: list of updated cbn response dictionaries
    """
    new_list = list()
    for res in reslist:
        for cmd, opts in cp_opts.items():
            if isinstance(opts, list):
                for opt in opts:
                    if opt.get('res', False) and res.get('name', False):
                        if opt.get('res') == res.get('name'):
                            res.update({cmd: opt})
                            continue
    return reslist


def set_key_permissions(opts):
    """
    If a keypair is generated with a private key file as part of provisioning
    set the permissions on it to be strict so that it can be used successfully
    in orchestrate/execute phases.

    :param opts: dictionary of command options
    :return:
    """

    if not opts[1].get('private_key', None):
        return

    # set permission of the key
    key = opts[1].get('private_key', None)
    try:
        LOG.info('Changing permissions on the private key file.')
        os.chmod(os.path.abspath(key), stat.S_IRUSR | stat.S_IWUSR)
    except OSError as ex:
        raise HelpersError(
            'Error setting private key file permissions: %s' % ex
        )


def generate_cbn_response(res, public_net_key=None):
    """
    This will generate the teflo response dictionary
    the asset_provisioner will use to update the asset
    with the appropriate info

    :param res: dictionary response from the provider
    :param public_net_key: optionnal key to specifically designate the ip from said network as public
           for later use when generating the inventory
    :return: list of teflo responses
    """
    os_res = []
    ip_add = None
    for r in res:
        ip_add = parse_network_addresses_to_dict(r, public_net_key)
        if ip_add and len(res) > 1:
            os_res.append(dict(asset_id=r.get('id'), ip=ip_add, name=r.get('name')))
            continue
        if ip_add and len(res) == 1:
            os_res.append(dict(asset_id=r.get('id'), ip=ip_add, name=r.get('name')))
            continue
        os_res.append(dict(asset_id=r.get('id'), name=r.get('name')))

    return os_res


def parse_network_addresses_to_dict(json_resp, public_net_key):
    """
    This will iterate over the dictionary extracting ip information and formatting
    in a way that is supported by the asset_provisioner

    :param json_resp: dictionary response from the provider
    :param public_net_key: optionnal key to specifically designate the ip from said network as public
           for later use when generating the inventory
    :return:
    """
    ips = dict()
    if json_resp.get('addresses', {}):
        addresses = json_resp.get('addresses').replace(' ', '').split(';')
        addy_dict = dict()
        for addy in addresses:
            net_item = addy.split('=')
            if net_item[-1].find(',') != -1:
                addy_dict.update({net_item[0]: net_item[-1].split(',')})
                continue
            addy_dict.update({net_item[0]: net_item[-1]})
        LOG.info(addy_dict)
        if len(addy_dict) == 1:
            for key, val in addy_dict.items():
                if isinstance(val, list):
                    for ele in val:
                        if ele.find(':') != -1:
                            ips.update(dict(public_ipv6=ele))
                            continue
                        ips.update(dict(public=ele))
                    continue
                ips = addy_dict.get(key)
            LOG.info(ips)
            return ips

        priv_ips = []
        for key, val in addy_dict.items():
            if (public_net_key and fnmatch(key, public_net_key)) or (not public_net_key and key.find('provider') != -1):
                if isinstance(val, list):
                    for ele in val:
                        if ele.find(':') != 1:
                            ips.update(dict(public_ipv6=ele))
                            continue
                        ips.update(dict(public=ele))
                    continue
                ips.update(dict(public=val))
                continue
            priv_ips.append(val)

        if len(priv_ips) > 1:
            ips.update(dict(private=priv_ips))
            return ips

        if len(priv_ips) ==1:
            ips.update(dict(private=priv_ips[-1]))
            return ips

        return ips
