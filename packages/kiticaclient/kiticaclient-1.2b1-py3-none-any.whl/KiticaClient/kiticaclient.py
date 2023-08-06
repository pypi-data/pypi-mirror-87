# -*- coding: utf-8 -*-

# Copyright (C) 2020 Spiralworks Technologies Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#  _     _ _       _             _______ _  _
# (_)   | (_)  _  (_)           (_______) |(_)             _
#  _____| |_ _| |_ _  ____ _____ _      | | _ _____ ____ _| |_
# |  _   _) (_   _) |/ ___|____ | |     | || | ___ |  _ (_   _)
# | |  \ \| | | |_| ( (___/ ___ | |_____| || | ____| | | || |_
# |_|   \_)_|  \__)_|\____)_____|\______)\_)_|_____)_| |_| \__)
# kitica Client
# Created by    : Joshua Kim Rivera
# Date          : September 22 2020 19:52 UTC-8
# Company       : Spiralworks Technologies Inc.
#
import argparse
import sys
import time
import subprocess
from KiticaClient import (
    Constants,
    AdbClient,
    iOSClient
)


def parser():
    """ Parser Function.

    :return argparse.ArgumentParser Object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-k",
                        "--kiticaserver",
                        help="Kitica API Server URI",
                        default=Constants.KITICA_SERVER
                        )
    parser.add_argument("-w",
                        "--webdriverpath",
                        help="Web Driver PATH",
                        default='default'
                        )
    parser.add_argument("-ip",
                        "--hostip",
                        help="Host IP Bypass Value",
                        default=None
                        )
    return parser


def adb():
    """
    """
    args = parser()
    args.add_argument("-a",
                      "--adbhost",
                      help="The adb host to connect to. Defaults to localhost.",
                      default='localhost'
                      )
    args.add_argument("-p",
                      "--adbport",
                      help="The ADB port of the host. Defaults to 5037",
                      default=5037
                      )
    options = args.parse_args()
    try:
        client = AdbClient(options.kiticaserver, options.hostip)
        try:
            client.initialize_connection(options.adbhost,
                                         options.adbport)
        except Exception:
            print('ADB Server is not Running, Starting ADB Server....')
            subprocess.run(['adb devices'], shell=True)
            client.initialize_connection(options.adbhost,
                                         options.adbport)
        print(Constants.ADB_START)
        print('adbhost:' + str(options.adbhost))
        print('adbport:' + str(options.adbport))
        client.update()
        while(True):
            client.listen()
            time.sleep(3)
    except KeyboardInterrupt:
        client.stop()


def ios():
    """
    """
    args = parser()
    options = args.parse_args()
    try:
        service = iOSClient(options.kiticaserver, options.hostip)
        print(Constants.IOS_START)
        service.update()
        service.initialize_devices()
        while(True):
            service.listen()
    except KeyboardInterrupt:
        service.stop()
