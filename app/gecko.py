#!/usr/bin/python3

import os
import subprocess

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'Ava Labs, Inc.'
}

DOCUMENTATION = '''
---
module: gecko

short_description: Ansible module for Gecko (ava implementation)

version_added: "2.9"

options:
    api_admin_enabled:
        description: If true, this node exposes the Admin API (default true)
        required: false
        type: bool
    api_keystore_enabled:
        description: If true, this node exposes the Keystore API (default true)
        required: false
        type: bool
    api_metrics_enabled:
        description: If true, this node exposes the Metrics API (default true)
        required: false
        type: bool
    assertions_enabled:
        description: Turn on assertion execution (default true)
        required: false
        type: bool
    ava_tx_fee:
        description: Ava transaction fee, in $nAva
        required: false
        type: int
    bootstrap_ids:
        description: Comma separated list of bootstrap peer ids to connect to.
        required: false
        type: str
    bootstrap_ips:
        description: Comma separated list of bootstrap peer ips to connect to.
        required: false
        type: str
    db_dir:
        description: Database directory for Ava state (default "db")
        required: false
        type: str
    db_enabled:
        description: Turn on persistent storage (default true)
        required: false
        type: bool
    http_port:
        description: Port of the HTTP server (default 9650)
        required: false
        type: int
    http_tls_cert_file:
        description: TLS certificate file for the HTTPs server
        required: false
        type: str
    http_tls_enabled:
        description: Upgrade the HTTP server to HTTPs (default true)
        required: false
        type: bool
    http_tls_key_file:
        description: TLS private key file for the HTTPs server
        required: false
        type: str
    log_dir:
        description: Logging directory for Ava
        required: false
        type: str
    log_display_level:
        description:
            - The log display level. If left blank, will inherit the value of
              log_level. Otherwise, should be one of {all, debug, info, warn,
              error, fatal, off}
        required: false
        type: str
    log_level:
        description:
            - The log level. Should be one of {all, debug, info, warn, error,
              fatal, off} (default "info")
        required: false
        type: str
    network_id:
        description: Network ID this node will connect to (default "mainnet")
        required: false
        type: str
    public_ip:
        description: Public IP of this node
        required: false
        type: str
    signature_verification_enabled:
        description: Turn on signature verification (default true)
        required: false
        type: bool
    snow_avalanche_batch_size:
        description:
            - Number of operations to batch in each new vertex (default 30)
        required: false
        type: int
    snow_avalanche_num_parents:
        description:
            - Number of vertexes for reference from each new vertex (default 5)
        required: false
        type: int
    snow_quorum_size:
        description:
            - Alpha value to use for required number positive results (default
              18)
        required: false
        type: int
    snow_rogue_commit_threshold:
        description: Beta value to use for rogue transactions (default 30)
        required: false
        type: int
    snow_sample_size:
        description:
            - Number of nodes to query for each network poll (default 20)
        required: false
        type: int
    snow_virtuous_commit_threshold:
        description: Beta value to use for virtuous transactions (default 20)
        required: false
        type: int
    staking_port:
        description: Port of the consensus server (default 9651)
        required: false
        type: int
    staking_tls_cert_file:
        description: TLS certificate file for staking connections
        required: false
        type: str
    staking_tls_enabled:
        description:
            - Require TLS to authenticate staking connections (default true)
        required: false
        type: str
    staking_tls_key_file:
        description: TLS private key file for staking connections
        required: false
        type: str
    xput_server_enabled:
        description: If true, throughput test server is created
        required: false
        type: str
    xput_server_port uint
        description:
            - Port of the deprecated throughput test server (default 9652)
        required: false
        type: str

author:
    - Ted Yin (@Tederminant)
'''

EXAMPLES = '''
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        bin=dict(
            type='str',
            default='~/go/src/github.com/ava-labs/gecko/build/ava'),
        cwd=dict(
            type='str',
            default='~/go/src/github.com/ava-labs/gecko/'),
        api_admin_enabled=dict(type='bool', required=False),
        api_keystore_enabled=dict(type='bool', required=False),
        api_metrics_enabled=dict(type='bool', required=False),
        assertions_enabled=dict(type='bool', required=False),
        ava_tx_fee=dict(type='int', required=False),
        bootstrap_ids=dict(type='str', required=False),
        bootstrap_ips=dict(type='str', required=False),
        db_dir=dict(type='str', required=False),
        db_enabled=dict(type='bool', required=False),
        http_port=dict(type='int', required=False),
        http_tls_cert_file=dict(type='str', required=False),
        http_tls_enabled=dict(type='bool', required=False),
        http_tls_key_file=dict(type='str', required=False),
        log_dir=dict(type='str', required=False),
        log_display_level=dict(type='str', required=False),
        log_level=dict(type='str', required=False),
        network_id=dict(type='str', required=False),
        public_ip=dict(type='str', required=False),
        signature_verification_enabled=dict(type='bool', required=False),
        snow_avalanche_batch_size=dict(type='int', required=False),
        snow_avalanche_num_parents=dict(type='int', required=False),
        snow_quorum_size=dict(type='int', required=False),
        snow_rogue_commit_threshold=dict(type='int', required=False),
        snow_sample_size=dict(type='int', required=False),
        snow_virtuous_commit_threshold=dict(type='int', required=False),
        staking_port=dict(type='int', required=False),
        staking_tls_cert_file=dict(type='str', required=False),
        staking_tls_enabled=dict(type='bool', required=False),
        staking_tls_key_file=dict(type='str', required=False),
        xput_server_enabled=dict(type='bool', required=False),
        xput_server_port=dict(type='int', required=False)
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    ava_args = [
        'api_admin_enabled',
        'api_keystore_enabled',
        'api_metrics_enabled',
        'assertions_enabled',
        'ava_tx_fee',
        'bootstrap_ids',
        'bootstrap_ips',
        'db_dir',
        'db_enabled',
        'http_port',
        'http_tls_cert_file',
        'http_tls_enabled',
        'http_tls_key_file',
        'log_dir',
        'log_display_level',
        'log_level',
        'network_id',
        'public_ip',
        'signature_verification_enabled',
        'snow_avalanche_batch_size',
        'snow_avalanche_num_parents',
        'snow_quorum_size',
        'snow_rogue_commit_threshold',
        'snow_sample_size',
        'snow_virtuous_commit_threshold',
        'staking_port',
        'staking_tls_cert_file',
        'staking_tls_enabled',
        'staking_tls_key_file',
        'xput_server_enabled',
        'xput_server_port'
    ]

    expanduser = [
        'bin',
        'cwd',
        'db_dir',
        'log_dir',
    ]

    for arg in expanduser:
        module.params[arg] = os.path.expanduser(module.params[arg])

    try:
        cmd = ['nohup', module.params['bin']]
        for arg in ava_args:
            val = module.params[arg]
            if not (val is None):
                _arg = "-{}".format(arg.replace('_', '-'))
                if type(val) == bool:
                    cmd.append("{}={}".format(_arg, "true" if val else "false"))
                else:
                    cmd.append("{}={}".format(_arg, val))
        null = open("/dev/null", "w")
        pid = subprocess.Popen(
            cmd,
            cwd=module.params['cwd'],
            stdout=null, stderr=null, env=os.environ).pid
        module.exit_json(changed=False, status=0, pid=pid, cmd=" ".join(cmd))
    except (OSError, subprocess.SubprocessError) as e:
        module.fail_json(msg=str(e), changed=False, status=1)


def main():
    run_module()


if __name__ == '__main__':
    main()
