from cryptography.fernet import Fernet

import pkg_resources

def main():
    config_data = []
    loop_input = True

    print('################ MQTTTasky Configuration ################')
    print('\nWelcome! Yes, MQTTTasky is a terrible name! If you haven\'t')
    print('\nalready, take the time to read README.rst before')
    print('\ncontinuing with setup.')
    usr_input = input('\n     Press Enter to continue or \'q\' to quit. >> ')

    if (usr_input.lower() == 'q'):
        exit(0)

    # Collect all user input
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
        # Check for missing data; if found, clear and start over
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
            loop_input = False # Assuming all needed data recorded; break out of loop to write to file.

    groupme_file = pkg_resources.resource_filename(__name__, 'config/groupme_bot_config.py')
    mqtt_file = pkg_resources.resource_filename(__name__, 'config/mqtt_config.py')
    # Write recorded groupme info to file:
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
        
    # Write recorded mqtt info + fernet cipher key to file:
    with open(mqtt_file, 'w') as f:
        f.write('CONFIG = {')
        f.write('\n   \'port\': ' + config_data[5] + ',')
        f.write('\n   \'host\': \'' + config_data[6] + '\',')
        f.write('\n   \'username\': \'' + config_data[7] + '\',')
        f.write('\n   \'password\': \'' + config_data[8] + '\',')
        f.write('\n   \'cipher_key\': \'' + key_str + '\'')
        f.write('\n}')

    # Share cipher key so any client can use fernet algorithm to decrypt payloads:
    print('\nBytes published by the MQTT client are encrypted')
    print('using Fernet encryption. Record the following')
    print('cipher key and use it with subscribers to decrypt')
    print('MQTTTasky\'s payloads:')
    print('\n' + key_str)
    print('\n\nThe program must be restarted. Re-run')
    print('\'mqttasky_groupme\' to restart it.')
    input('\nPress enter to continue...')
    exit(0)

main()