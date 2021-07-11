import subprocess
import os
import re
from sys import stdout


def welcome():
    print('Hello, please note this is for educational purposes only. Ensure to use responsibly')
    print('Printing WiFi profiles and passwords')
    print('Just a sec...')
# look for all saved Wifi profiles & if they have passwords, show them:

# we check if the os system in use is Windows, that way we get to use netsh command:
os_name = os.name

wifi_names = []

def show_profiles(os_name):
    # run netsh command on cmd
    if os_name == 'nt':
        output = subprocess.run('netsh wlan show profiles', shell=True, stdout=subprocess.PIPE, text=True)
        response = output.stdout # capture response as string hence, string methods

        # we need to get the individual WiFi names to pass to the netsh command
        
        for entry in response.splitlines():
            #x.append(entry.strip())
            #y.append(entry)
            #print(entry)
            strip_entry = entry.strip() # gets rid of spaces
            prog = re.compile('All') # All WiFi names have a All User Profiles "key"
            if prog.match(strip_entry):
                # we need to get rid of "All User Profiles" & be left with WiFi names only
                split_entry = strip_entry.split(":") 
                wifi_names.append(split_entry[1]) # add WiFi names to our list
    else:
        print("This works on Windows only!")

wifi_with_key = {}
def pass_present():
    # we need to check for profiles with passkeys
    for profile in wifi_names:
        strip_profile = profile.strip()
        
        output = subprocess.run(['netsh', 'wlan', 'show', 'profile', f"{strip_profile}", 'key=clear'], shell=True, stdout=subprocess.PIPE, text=True)

        response = output.stdout.strip()
        r = response.splitlines() # creates a list of strings
        
        # loop through the output looking for profiles with passwords
        for index, entry in enumerate(r):
            prog = re.compile('^Key Content') # matches all profiles with keys
            m = prog.match(entry.strip())
            if m:
                # if profile has a key we add the profile & key to a dictionary
                wifi_name = r[19].split(':') # getting rid of SSID string
                wifi_pass = r[index].split(':') # getting rid of Key content string
                wifi_with_key[wifi_name[1].strip("")] = wifi_pass[1]
                
def print_wifi_keys(wifi_with_key):
    for k, v in wifi_with_key.items():
        print(f"{k} WiFi password is: {v}")
                
def main():
    proceed = input("Welcome to ethical hacking, do you plan on being ethical? \nEnter Yes to continue or No to exit: ").lower()
    
    if proceed in ('y', 'ye', 'yes'):
        welcome()
        show_profiles(os_name=os.name)
        #print(wifi_names)
        pass_present()
        print('*' * 100)
        print_wifi_keys(wifi_with_key)
    elif proceed in ('n', 'no', 'nope'):
        subprocess.run("exit", shell=True)
    else:
        print("Oops! Please re-check entry.")


if __name__ == '__main__':
    main()










