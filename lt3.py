#!/usr/bin/env python2.7

# lt3.py -- HiLink network mode switcher
#
# Copyright (C) 2016 Damian Ziemba
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import argparse
import BeautifulSoup
import requests

BASE_URL = "http://192.168.8.1/api/"
PAYLOAD_TEMPLATE = '<request>' \
                   '<NetworkMode>{mode}</NetworkMode>' \
                   '<NetworkBand>3FFFFFFF</NetworkBand>' \
                   '<LTEBand>800C5</LTEBand></request>'

class CommunicationError(Exception):
    pass

def get_token():
    res = requests.get(BASE_URL + "webserver/token")
    return str(BeautifulSoup.BeautifulSoup(res.text).token.string)

def _switch_impl(mode):
    response = requests.post(
        BASE_URL + 'net/net-mode',
        data=PAYLOAD_TEMPLATE.format(mode=mode),
        headers={'__RequestVerificationToken': get_token()}
    )

    response_string = BeautifulSoup.BeautifulSoup(response.text).response.string
    if response_string != "OK":
        raise CommunicationError("Error when switching to %s mode: %s" % ("LTE", response_string))

def switch_to_lte():
    _switch_impl('03')

def switch_to_3g():
    _switch_impl('02')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="Transmission mode to which modem should be switched", choices=["lte", "3g"])
    
    args = parser.parse_args()
    
    if args.mode == "lte":
        switch_to_lte()
    else:
        switch_to_3g()

if __name__ == "__main__": 
    main()
