# -*- coding: utf-8 -*-

from .client import FrpcClient


def main():
    import argparse
    import requests

    from requests.packages import urllib3

    parser = argparse.ArgumentParser(description="FRPC netcat for interactive connection to FRPC server")
    parser.add_argument("--insecure", action='store_true', help="Do not check server's cert")
    parser.add_argument("url", metavar="URL", help="URL of FRPC server to connect to")
    args = parser.parse_args()

    session = requests.session()

    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        session.verify = False

    client = FrpcClient(args.url, session=session)

    import IPython

    IPython.start_ipython(
        argv=[],
        user_ns={
            "client": client.rpc
        }
    )
