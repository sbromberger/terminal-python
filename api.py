from os.path import expanduser
import json
import urllib
import urllib2
from sslv3 import HTTPSHandlerV3

API = {
    'PROTO': "https",
    'BASE_URL': "api.terminal.com",
    'VERSION': 'v0.1',
    'USER_TOK': '',
    'ACCESS_TOK': ''
}

API_FILENAME = ".terminal-apikeys"


def get_api_key(fn=API_FILENAME):
    """
    Will return the api key stored in API_FILENAME (default
    ~/.terminal-apikeys) or False
    if any error was encountered.
    """
    api_tokens = {
        'user_token': '',
        'access_token': ''
    }
    try:
        apifile = "%s/%s" % (expanduser("~"), fn)
        print "apifile = %s" % apifile
        f = open(apifile, "r")

        for line in f.readlines():
            print "read %s" % line
            (k, v) = line.split('=')
            if k in api_tokens:
                api_tokens[k] = v.strip()
    except:
        print "error"
    return api_tokens


def gen_api_call(func_name):
    return "{}://{}/{}/{}".format(
        API['PROTO'],
        API['BASE_URL'],
        API['VERSION'],
        func_name)


class Session(object):
    def __init__(
        self,
        user_token=None,
        access_token=None,
        *args,
        **kwargs
    ):
        api_tokens = get_api_key()
        self.user_token = user_token or api_tokens['user_token']
        self.access_token = access_token or api_tokens['access_token']

    @property
    def tokens(self):
        return {
            'user_token': self.user_token,
            'access_token': self.access_token
        }

    def generic_api(func_name, api_args=[], *args, **kwargs):
        def inner_api(self, *args, **kwargs):
            def _call_api(url, data):
                params = urllib.urlencode(data)
                urllib2.install_opener(urllib2.build_opener(HTTPSHandlerV3()))
                jsondata = urllib2.urlopen(url, params).read()
                return json.loads(jsondata)

            url = gen_api_call(func_name)
            data = self.tokens
            zip_args = zip(api_args, args)
            data.update(zip_args)
            data.update(kwargs)
            print "calling %s with %s" % (url, data)
            return _call_api(url, data)
        return inner_api

    who_am_i = generic_api('who_am_i')
    get_snapshot = generic_api('get_snapshot', ['snapshot_id'])
    get_profile = generic_api('get_profile', ['username'])
    list_public_snapshots = generic_api('list_public_snapshots', [
        'username',
        'tag',
        'featured',
        'title',
        'page',
        'perPage',
        'sortby'
        ]
    )
    count_public_snapshots = generic_api('count_public_snapshots', [
        'username',
        'tag',
        'featured',
        'title'
        ]
    )
    list_terminals = generic_api('list_terminals')
    get_terminal = generic_api('get_terminal', [
        'container_key',
        'subdomain'
        ]
    )
    start_snapshot = generic_api('start_snapshot', [
        'snapshot_id',
        'cpu',
        'ram',
        'temporary',
        'name',
        'autopause',
        'startup_script',
        'custom_data'
        ]
    )

    delete_terminal = generic_api('delete_terminal', ['container_key', ])
    restart_terminal = generic_api('restart_terminal', ['container_key', ])
    pause_terminal = generic_api('pause_terminal', ['container_key', ])
    resume_terminal = generic_api('resume_terminal', ['container_key', ])
    edit_terminal = generic_api('edit_terminal', [
        'container_key',
        'cpu',
        'ram',
        'diskspace',
        'name'
        ]
    )
    list_snapshots = generic_api('list_snapshots', [
        'username',
        'tag',
        'featured',
        'title',
        'page',
        'perPage',
        'sortby'
        ]
    )
    count_snapshots = generic_api('count_snapshots', [
        'username',
        'tag',
        'featured',
        'title'
        ]
    )

    delete_snapshot = generic_api('delete_snapshot', ['snapshot_id', ])
    edit_snapshot = generic_api('edit_snapshot', [
        'snapshot_id',
        'body',
        'title',
        'readme',
        'tags',
        'public',
        'custom_data'
        ]
    )
    snapshot_terminal = generic_api('snapshot_terminal', [
        'container_key',
        'body',
        'title',
        'readme',
        'tags',
        'public'
        ]
    )
    add_terminal_links = generic_api('add_terminal_links', [
        'container_key',
        'links'
        ]
    )

    remove_terminal_links = generic_api('remove_terminal_links', [
        'container_key',
        'links'
        ]
    )

    list_terminal_access = generic_api(
        'list_terminal_access', ['container_key', ]
    )

    edit_terminal_access = generic_api('edit_terminal_access', [
        'container_key',
        'is_public_list',
        'access_rules'
        ]
    )

    get_cname_records = generic_api('get_cname_records')
    add_domain_to_pool = generic_api('add_domain_to_pool', ['domain', ])
    remove_domain_from_pool = generic_api(
        'remove_domain_from_pool', ['domain', ]
    )
    add_cname_record = generic_api('add_cname_record', [
        'domain',
        'subdomain',
        'port'
        ]
    )
    remove_cname_record = generic_api('remove_cname_record', ['domain', ])
    set_terminal_idle_settings = generic_api('set_terminal_idle_settings', [
        'container_key',
        'triggers',
        'action'
        ]
    )
    get_terminal_idle_settings = generic_api(
        'get_terminal_idle_settings', ['container_key', ]
    )
    instance_types = generic_api('instance_types')
    instance_price = generic_api('instance_price', ['status', ])
    balance = generic_api('balance')
    balance_added = generic_api('balance_added')
    gift = generic_api('gift', ['email', 'cents'])
    burn_history = generic_api('burn_history')
    terminal_usage_history = generic_api('terminal_usage_history')
    burn_state = generic_api('burn_state')
    burn_estimates = generic_api('burn_estimates')
    add_authorized_key_to_terminal = generic_api(
        'add_authorized_key_to_terminal',
        ['container_key', 'publicKey']
    )
    add_authorized_key_to_ssh_proxy = generic_api(
        'add_authorized_key_to_ssh_proxy'
    )
    del_authorized_key_to_ssh_proxy = generic_api(
        'del_authorized_key_to_ssh_proxy'
    )
    get_authorized_keys_from_ssh_proxy = generic_api(
        'get_authorized_keys_from_ssh_proxy'
    )
    request_progress = generic_api('request_progress', ['request_id', ])
