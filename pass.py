#!/usr/bin/python

import os
import re
import subprocess
import sys

COMMAND_LINUX = "sudo grep -r '^psk=' /etc/NetworkManager/system-connections/"
COMMAND_OSX = "defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.preferences |grep SSIDString"
COMMAND_WINDOWS_GENERIC = "netsh wlan show profile"
RE_LINUX = '/etc/NetworkManager/system-connections/(.*)'
RE_OSX = 'SSIDString = (.*);'
PASS_OSX = 'security find-generic-password -wa '
SAVED_PASSWORDS = dict()


def get_pass_wind_individual(name):
    output = subprocess.check_output(COMMAND_WINDOWS_GENERIC + " name=" + name + " key=clear", shell=True)
    output = re.findall('Key Content(.*)\n', output)[0].strip().split(':')[1].strip()
    return output


def make_pass_dict():
    if os.name == 'posix':
        try:
            output = subprocess.check_output(COMMAND_LINUX, shell=True).split('\n')
            for pair in output:
                try:
                    pair = re.findall(RE_LINUX, pair)[0].split(':')
                    name = pair[0]
                    passwd = pair[1].split('=')[1]
                    SAVED_PASSWORDS[name] = passwd
                except:
                    pass
        except:
            output = subprocess.check_output(COMMAND_OSX, shell=True).split('\n')
            for pair in output:
                try:
                    name = re.findall(RE_OSX, pair)[0]
                    passwd = subprocess.check_output(PASS_OSX + name, shell=True)
                    print "Getting password for " + name
                    SAVED_PASSWORDS[name] = passwd
                except:
                    pass

    elif os.name == 'nt':
        output = subprocess.check_output(COMMAND_WINDOWS_GENERIC, shell=True).split('\n')
        names = list()
        for name in output:
            name = name.split(':')
            try:
                names.append(name[1].strip())
            except:
                pass
        for names in names:
            try:
                password = get_pass_wind_individual(names)
                SAVED_PASSWORDS[names] = password
            except:
                pass


def get_passwords(**kwargs):
    if 'ssid' in kwargs:
        ssid = kwargs['ssid']
        try:
            SAVED_PASSWORDS[ssid]
        except KeyError:
            print "The SSID \'%s\' doesn't exist" % ssid
            return
        if os.name == 'nt':
            try:
                password = get_pass_wind_individual(ssid)
                print 'Network:', ssid, '|''Password:', password
            except:
                print "The SSID %s doesn't exist" % ssid
        else:
            print 'Network:', ssid, '|''Password:', SAVED_PASSWORDS[ssid]
    else:
        for name in SAVED_PASSWORDS.keys():
            print 'Network:', name, '|''Password:', SAVED_PASSWORDS[name]


def main():
    if len(sys.argv) < 2:
        make_pass_dict()
        get_passwords()
    elif os.name == 'posix':
        make_pass_dict()
        name_list = sys.argv[1:]
        for name in name_list:
            get_passwords(ssid=name)


if __name__ == "__main__":
    main()
