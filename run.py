#!/usr/bin/env python3

import argparse
import collections
import functools
import http.server
import json
import logging
import socketserver
import subprocess
import time


DEFAULT_CONFIG_PATH = '/data/options.json'
DEFAULT_PORT = 80

LOG = logging.getLogger(__file__)


def do_call(sip):
    cmd = ['pjsua',
        '--id', f'sip:{sip.sip_user}@{sip.sip_host}',
        '--registrar', f'sip:{sip.sip_host}',
        '--realm', '*',
        '--username', sip.sip_user,
        '--password', sip.sip_password,
        '--null-audio',
        '--auto-loop',
        '--auto-conf',
        '--auto-play',
        f'--play-file={sip.play_file}',
        f'sip:{sip.call_extension}@{sip.sip_host}',
    ]

    LOG.info('call ' + ' '.join(cmd))

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    try:
        time.sleep(sip.call_time_secs)
        process.stdin.write(b'ha\n')
        process.stdin.write(b'q\n')
        process.stdin.flush()
        process.stdin.close()
        process.wait()
    except Exception as e:
        LOG.warning(f'pjsua communication error: {e}')


class VoipRequestHandler(http.server.SimpleHTTPRequestHandler):
    def request_call(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
        sip = self.server.sip_config
        print(sip)
        do_call(sip)

    def do_GET(self):
        if self.path == '/config.yaml':
            return super().do_GET()
        elif self.path == '/call':
            return self.request_call()
        else:
            return self.send_error(404)


SipConfig = collections.namedtuple('SipConfig', ['sip_host', 'sip_user', 'sip_password', 'call_extension', 'play_file', 'call_time_secs'])


def load_config(path):
    with open(path, 'r') as f:
        d = json.load(f)

    return SipConfig(**d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=DEFAULT_CONFIG_PATH, help=f'path to config file (default: {DEFAULT_CONFIG_PATH})')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help=f'port of this server to listen (default: {DEFAULT_PORT})')

    args = parser.parse_args()

    logging.basicConfig()

    with socketserver.TCPServer(("", args.port), VoipRequestHandler) as httpd:
        httpd.sip_config = load_config(args.config)
        LOG.info('listening')
        httpd.serve_forever()
