import json
import locale
import subprocess
import re
import os
import sys


class PassRetrievalTool:
    # Static Variables
    COMMAND_LINUX = "sudo grep -r '^psk=' /etc/NetworkManager/system-connections/"
    COMMAND_OSX = "defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.preferences |grep SSIDString"
    COMMAND_WINDOWS_GENERIC = "netsh wlan show profile"
    RE_LINUX = '/etc/NetworkManager/system-connections/(.*)'
    RE_OSX = 'SSIDString = (.*);'
    PASS_OSX = 'security find-generic-password -wa '
    LANGUAGE_STRINGS = {
        "en_GB" : "Key Content",
        "en_US" : "Key Content",
        "es_ES" : "Contenido de la clave"
    }
    def __init__(self):
        pass

    @staticmethod
    def get_pass_wind_individual(Name):
        output = subprocess.check_output(PassRetrievalTool.COMMAND_WINDOWS_GENERIC + " name=" + Name + " key=clear", shell=True)
        output = re.findall(PassRetrievalTool.getLanguageString() + '(.*)\n', output)[0].strip().split(':')[1].strip()
        return output

    @staticmethod
    def get_all_wifi_password_dictionary():
        return PassRetrievalTool.get_specific_wifi_password_dictionary(None)
    @staticmethod
    def get_specific_wifi_password_dictionary(filter_ssid):
        wifi_password_dictionary = dict()
        if os.name == 'posix':
            try:
                output = subprocess.check_output(PassRetrievalTool.COMMAND_LINUX, shell=True).split('\n')
                for pair in output:
                    try:
                        pair = re.findall(PassRetrievalTool.RE_LINUX, pair)[0].split(':')
                        name = pair[0]
                        password = pair[1].split('=')[1]

                        if filter_ssid and name != filter_ssid:
                            continue # Ignore if filter is set and doesn't match

                        wifi_password_dictionary[name] = password
                    except:
                        pass
            except:
                output = subprocess.check_output(PassRetrievalTool.COMMAND_OSX, shell=True).split('\n')
                for pair in output:
                    try:
                        name = re.findall(PassRetrievalTool.RE_OSX, pair)[0]
                        password = subprocess.check_output(PassRetrievalTool.PASS_OSX + name, shell=True)

                        if filter_ssid and name != filter_ssid:
                            continue # Ignore if filter is set and doesn't match

                        wifi_password_dictionary[name] = password
                    except:
                        pass


        elif os.name == 'nt':
            output = subprocess.check_output(PassRetrievalTool.COMMAND_WINDOWS_GENERIC, shell=True).split('\n')
            wifi_names = list()
            for line in output:
                values = line.split(':')
                try:
                    name = values[1].strip()

                    if filter_ssid and name != filter_ssid:
                        continue  # Ignore if filter is set and doesn't match

                    wifi_names.append(name)
                except:
                    pass
            for name in wifi_names:
                try:
                    password = PassRetrievalTool.get_pass_wind_individual(name)
                    wifi_password_dictionary[name] = password
                except:
                    pass
        return wifi_password_dictionary

    @staticmethod
    def print_passwords(wifi_password_dictionary):
        for name in wifi_password_dictionary.keys():
            print "WiFi SSID: {}  - Password: {}".format(name, wifi_password_dictionary[name])

    def main(self):
        print_json = False
        wifi_password_dictionary = None
        if len(sys.argv) == 1:
            # Regular search and print
            wifi_password_dictionary = PassRetrievalTool.get_all_wifi_password_dictionary()
        elif len(sys.argv) == 2:
            # With 1 argument (either --json or custom SSID)
            if "--json" in sys.argv:
                # Print a json version of every SSID found
                wifi_password_dictionary = PassRetrievalTool.get_all_wifi_password_dictionary()
                print_json = True
            else:
                # Regular print with custom SSID
                ssid = sys.argv[1]
                wifi_password_dictionary = PassRetrievalTool.get_specific_wifi_password_dictionary(ssid)
        elif len(sys.argv) >= 3:
            # With 2 or more arguments (--json and customs SSID)
            args = list(sys.argv)

            if "--json" in sys.argv:
                print_json = True
                args.remove("--json")
            ssid = args[1]
            wifi_password_dictionary = PassRetrievalTool.get_specific_wifi_password_dictionary(ssid)

        if print_json:
            print json.dumps(wifi_password_dictionary)
        else:
            PassRetrievalTool.print_passwords(wifi_password_dictionary)

    @staticmethod
    def getLanguageString():
        language = locale.getdefaultlocale()[0]
        return PassRetrievalTool.LANGUAGE_STRINGS[language]


if __name__ == "__main__":
    pass_retrieval_tool = PassRetrievalTool()
    pass_retrieval_tool.main()
