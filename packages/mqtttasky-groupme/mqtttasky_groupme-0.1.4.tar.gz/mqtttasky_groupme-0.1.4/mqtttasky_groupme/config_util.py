from cryptography.fernet import Fernet

import pkg_resources
import re

def main():
    config_data = []
    loop_input = True
    missing_data = False

    # Initialize all data necessary to run the program from config.

    # Join the package's path with the data path to access config.
    groupme_file = pkg_resources.resource_filename(__name__, 'config/groupme_bot_config.py')
    mqtt_file = pkg_resources.resource_filename(__name__, 'config/mqtt_config.py')
    # Check the groupme config file to see if it has all the values in it:
    with open(groupme_file, 'r') as f:
        for i, line in enumerate(f):
            # Parse user's string and store in config_data[]:
            if ('=' in line):
                split_str = line.split('=', 1)
                var = split_str[1].replace("'", '')
                config_data.append(re.sub(r'#.*', '', var).strip())

                if (len(config_data[i]) == 0):
                    missing_data = True

    # Check the mqtt config file to see if it has all the values in it:
    with open(mqtt_file, 'r') as f:
        for i, line in enumerate(f):
            if (':' in line):
                split_str = line.split(': ', 1)
                var = split_str[1].replace(",", '')
                try:
                    config_data.append(var)

                    if (len(config_data[i]) == 0):
                        missing_data = True
                except:
                    missing_data = True

    # If files are completely blank.
    if (len(config_data) == 0):
        missing_data = True

    # IF any missing data, collect all the necessary data from the beginning:
    if (missing_data):
        del(config_data[:])
        print('################ MQTTTasky Configuration ################')
        print('\nWelcome! Yes, MQTTTasky is a terrible name! If you haven\'t')
        print('\nalready, take the time to read README.rst before')
        print('\ncontinuing with setup.')
        usr_input = input('\n     Press Enter to continue or \'q\' to quit. >> ')

        if (usr_input.lower() == 'q'):
            exit(0)

        while loop_input:
            print('\n ---------------- GroupMe Configuration ----------------')
            usr_input = input('1) Enter the your GroupMe access token >> ')
            config_data.append(usr_input)
            usr_input = input('2) Now enter your GroupMe bot ID >> ')
            config_data.append(usr_input)
            usr_input = input('3) Now enter your GroupMe group ID >> ')
            config_data.append(usr_input)

            print('\n ------------ Optional GroupMe Configuration ------------')
            usr_input = input('*Optional* Enter the name for your Bot (only' +
                            '\ndisplays in this program) >> ')
            if (len(usr_input) == 0):
                    usr_input = 'MQTTTasky Bot'

            config_data.append(usr_input)

            usr_input = input('*Optional* Enter the name for your Group (only' +
                            '\ndisplays in this program) >> ')
            if (len(usr_input) == 0):
                    usr_input = 'MQTTTasky Notifications'

            config_data.append(usr_input)

            print('\n ------------------ MQTT Configuration ------------------')
            usr_input = input('1) Enter your MQTT port (usually 1883) >> ')
            config_data.append(usr_input)
            usr_input = input('2) Enter your MQTT host address >> ')
            config_data.append(usr_input)
            usr_input = input('3) Enter your MQTT username >> ')
            config_data.append(usr_input)
            usr_input = input('4) Enter your MQTT password >> ')
            config_data.append(usr_input)

            missing_data = False
            # Check once again to see if all the data has been entered:
            for i in range(9):
                if (len(config_data[i]) == 0):
                    # tell user first line left blank
                    print('\nYou left one or more lines blank starting with' +
                        '\nline ' + str(i + 1) + '\n')
                    # clear contents of array if user forgot to enter line
                    # don't let code crash if user entered nothing
                    if (len(config_data) > 0):
                        del(config_data[:])
                    missing_data = True
                    break

            if not (missing_data):
                loop_input = False # Assuming all the correct info has been supplied.

        # Write the recorded groupme data to groupme config file
        with open(groupme_file, 'w') as f:
            f.write('ACCESS_TOKEN = \'' + config_data[0] +
                        '\'     # GROUPME ACCESS TOKEN\n')

            f.write('BOT_ID = \'' + config_data[1] +
                        '\'         # GROUPME BOT ID\n')

            f.write('GROUP_ID = \'' + config_data[2] +
                        '\'       # GROUPME GROUP ID\n')

            f.write('BOT_NAME = \'' + config_data[3] +
                        '\'       # GROUPME BOT NAME (ARBITRARY)\n')

            f.write('GROUP_NAME = \'' + config_data[4] +
                        '\'     # GROUPME GROUP NAME (ARBITRARY)')

        cipher_key = Fernet.generate_key()
        key_str = cipher_key.decode('utf-8')

        # Write the recorded mqtt data to groupme config file + write the cipher key to be used:
        with open(mqtt_file, 'w') as f:
            f.write('CONFIG = {')
            f.write('\n   \'port\': ' + config_data[5] + ',')
            f.write('\n   \'host\': \'' + config_data[6] + '\',')
            f.write('\n   \'username\': \'' + config_data[7] + '\',')
            f.write('\n   \'password\': \'' + config_data[8] + '\',')
            f.write('\n   \'cipher_key\': \'' + key_str + '\'')
            f.write('\n}')

        # Share the cypher key so any client can use fernet to decrypt:
        print('\nBytes published by the MQTT client are encrypted')
        print('using Fernet encryption. Record the following')
        print('cipher key and use it with subscribers to decrypt')
        print('MQTTTasky\'s payloads:')
        print('\n' + key_str)
        print('\n\nThe program must be restarted.')
        print('Press Ctrl-C to exit')
        exit(1)

main()