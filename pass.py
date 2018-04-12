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

    def __init__(self):
        pass

    @staticmethod
    def get_pass_wind_individual(Name):
        output = subprocess.check_output(PassRetrievalTool.COMMAND_WINDOWS_GENERIC + " name=" + Name + " key=clear", shell=True)
        output = re.findall('Contenido de la clave(.*)\n', output)[0].strip().split(':')[1].strip()
        return output

    @staticmethod
    def get_wifi_password_dictionary():
        wifi_password_dictionary = dict()
        if os.name == 'posix':
            try:
                output = subprocess.check_output(PassRetrievalTool.COMMAND_LINUX, shell=True).split('\n')
                for pair in output:
                    try:
                        pair = re.findall(PassRetrievalTool.RE_LINUX, pair)[0].split(':')
                        name = pair[0]
                        password = pair[1].split('=')[1]
                        wifi_password_dictionary[name] = password
                    except:
                        pass
            except:
                output = subprocess.check_output(PassRetrievalTool.COMMAND_OSX, shell=True).split('\n')
                for pair in output:
                    try:
                        name = re.findall(PassRetrievalTool.RE_OSX, pair)[0]
                        password = subprocess.check_output(PassRetrievalTool.PASS_OSX + name, shell=True)
                        wifi_password_dictionary[name] = password
                    except:
                        pass


        elif os.name == 'nt':
            output = subprocess.check_output(PassRetrievalTool.COMMAND_WINDOWS_GENERIC, shell=True).split('\n')
            wifi_names = list()
            for line in output:
                values = line.split(':')
                try:
                    wifi_names.append(values[1].strip())
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
        wifi_password_dictionary = PassRetrievalTool.get_wifi_password_dictionary()
        PassRetrievalTool.print_passwords(wifi_password_dictionary)


if __name__ == "__main__":
    pass_retrieval_tool = PassRetrievalTool()
    pass_retrieval_tool.main()
