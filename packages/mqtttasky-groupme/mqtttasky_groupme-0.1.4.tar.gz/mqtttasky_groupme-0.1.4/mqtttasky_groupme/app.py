from mqtttasky_groupme import gpio_status_light_util as status_light
from mqtttasky_groupme import bot_calls
from mqtttasky_groupme import config_util
from mqtttasky_groupme import tasks
from threading import Thread
from time import sleep

import pkg_resources
import requests
import re


config_data = []
# Join the package's path with the data path to access config.
configfile = pkg_resources.resource_filename(__name__, 'config/groupme_bot_config.py')
with open(configfile, 'r') as f:
    for i, line in enumerate(f):
        # Parse user's string and store in config_data[]:
        if ('=' in line):
            split_str = line.split('=', 1)
            var = split_str[1].replace("'", '')
            config_data.append(re.sub(r'#.*', '', var).strip())

# Copy groupme data from file:
ACCESS_TOKEN = config_data[0]
BOT_ID       = config_data[1]
GROUP_ID     = config_data[2]
BOT_NAME     = config_data[3]
GROUP_NAME   = config_data[4]

# Now that symmetric has been generated, initialized the Fernet cipher
tasks.init_cipher()
tasks.init_mqtt_client()

POST_URL = 'https://api.groupme.com/v3/bots/post' # URL for POST requests
RESP_URL = 'https://api.groupme.com/v3/groups/' + GROUP_ID + '/messages' # URL to read messages from

request_params = { 'token': ACCESS_TOKEN }


def send_reply(reply, message):
    post_params = {
        'bot_id': BOT_ID,
        'text': reply
    }
    req = requests.post(POST_URL, params=post_params)
    request_params['since_id'] = message['id'] # Mark with since_id so previous messages aren't replied to.

    print(message['text'] + '\n')
    print('Sent reply: ' + reply)
    print(req) # Print the status code in response to the POST request.

# Check messages in group every 4 seconds, when a new message arrives, if it
# Does not come from a bot, convert it to lowercase and pass it to bot_calls'
# generate_reply function to process message and send reply back to user using
# send_reply function above.
def main():
    while True:
        try:
            response = requests.get(RESP_URL, params=request_params)

            if response.status_code == 200:
                response_messages = response.json()['response']['messages']
                
                # Indicate messages retreived okay:
                Thread(target=status_light.blink_successful_retrieval).start()
                
                # As long as this is printed, user knows bot is actively listening to group.
                print('\n#######################' +
                    '\n# Bot: ' + BOT_NAME + 
                    '\n# Group: ' + GROUP_NAME + 
                    '\n# Status: Listening' + 
                    '\n#######################')

                for message in response_messages:
                    if not (message['sender_type'] == 'bot'): # Bot doesn't reply to itself (infinite loop!).
                        # Indicate new message received:
                        Thread(target=status_light.blink_incoming).start()
                        if not (message['text'] == None):
                            send_reply(bot_calls.generate_reply(message['text'].lower()), message)
                            # Indicate message being replied to:
                            Thread(target=status_light.blink_outgoing).start()
                            break

                # Indicate message is being sent:
                Thread(target=status_light.blink_outgoing).start()
            else:
                print('Message retrieval failed: ' + response.status_code)
                # Indicate that messages were not retrieved:
                Thread(target=status_light.blink_unsuccessful_retrieval).start()

        except requests.exceptions.ConnectionError as e:
            print('No connection')
            print(e)

        except requests.exceptions.Timeout as e:
            print('Connection timed out')
            print(e)

        except requests.exceptions.RequestException as e:
            print('A request error ocurred')
            print(e)

        except Exception as e:
            print('An error occurred')
            print(e)

        sleep(4)

main()
