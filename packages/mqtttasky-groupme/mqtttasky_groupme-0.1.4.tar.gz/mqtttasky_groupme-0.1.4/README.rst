*****************
mqtttasky_groupme
*****************

Turn your Raspberry Pi into a Task notification system.
*******************************************************
| |task-notification|

.. |task-notification| image:: images/task-notification.png

.. contents:: Contents


What is MQTTTasky?
##################
| I once created a desktop application called Tasky which would allow
| me to create tasks in sticky-note-like windows. I could set
| notifications for each task and have notifications sent to my phone.
| The UI was nice and but that was about it; Tasky was clunky and buggy
| and I couldn't conventiently schedule tasks from my smart phone.

| MQTTTasky is much less terrible, despite its name. The basic idea is,
| using GroupMe on my phone, I can schedule a task, then A GroupMe bot
| I have configured will interact with me and schedule the tasks. When
| a task notification occurs, the Raspberry Pi running MQTTTasky will
| display a notification window about the task and read the task aloud
| using a separate GitHub project called simple_google_tts. Additionally,
| when LEDs are connected to the Raspberry Pi's BCM pins 18, 23, and 24,
| they serve as status lights. Of course, it wouldn't be MQTTTasky
| without some MQTT action now would it? MQTTTasky connects to a Mosquito
| broker and when a task notification occurs, the notification is also
| published to pub/tasks. Payloads are encrypted with Fernet and a
| base-64 32-byte key can be used by any MQTT client to decrypt the
| message payloads using a Fernet decryption.
|

System Design
#############
| |system-design|

.. |system-design| image:: images/system-design.png
    :height: 300
    :width: 750

| In case my artistic endeavors are lost on you, I will try to explain
| my system design. We can think of it in terms of the HTTP(S) side of
| the architecture, what happens locally on Pi (Pi side?), and the MQTT
| side.
|
| Sitting on the Raspberry Pi, we have the mqtttasky_groupme
| package running. This package includes the GroupMe bot which communicates
| with users over HTTP. The the bot code processes requests in the group
| to act on the scheduling component of mqtttasky_groupme which schedules
| tasks. So on the 'Pi side', the bot and the scheduler will blink the LEDs
| to indicate the status of messages and task notifications. The scheduler
| will display graphical task notifications at the notification time of
| each task and it will also cause the task information to be read aloud
| through a connected speaker using a system call to simple_google_tts.
|
| Lastly, mqtttasky_groupme also includes an MQTT client. When it is time
| for a notification to be sent, the scheduler also calls on the MQTT client
| to publish the data to the topic, 'pub/tasks'. The client publishes
| payloads which are encrypted using Fernet encryption for which the client
| provides the symmetric key during initial configuration so that another
| MQTT client (such as the one contained in this repo in
| ./node_mqtttasky_pi_client) can use the key to create Fernet tokens and
| decrypt the payloads.
|
| The Node.js client pictured in the above design is an example of another
| client which subscribes to 'pub/tasks' on the same broker as MQTTasky is
| publishing to. For instructions on setting up a broker for which to connect
| your clients, see the section, 'Setting up a Mosquitto broker'.
|
| For me, this design is nifty because it is fully functional with just one
| Pi but the MQTT architecture allows me to implement multiple displays and/or
| speakers for task notifications such as on my monitor, my Raspberry
| Pi touch display, or even a television.

Equipment/Requirements
######################
- A Raspberry Pi 3B/3B+ or 4B/4B+ running Raspberry Pi OS w/ desktop
- A display connected to the Raspberry Pi
- A speaker connected to the Raspberry Pi
- A stable Internet connection on the Pi
- Three LED lights (preferably a red, yellow, and green)
- Four female to male jumper wires
- One ~100-220 Ohm resistor
- One breadboard


Setup
#####

Connecting the LEDs
-------------------
| Please refer to the following diagram (I tried):
| |gpio-diagram|
|
| 1) Connect one jumper wire to physical pin 1 (3.3V); connect the other
|    end to the positive side of the breadboard to share its voltage.
|
| 2) Connect the resistor to the positive side of the breadboard after
|    the jumper wire.
|
| 3) Connect the longer end (anode) of the first (red) LED to the positive
|    side of the breadboard after the resistor.
|
| 4) Connect the next wire to physical pin 12 (BCM 18); connect the other
|    end to the shorter end (cathode) of the first (red) LED.
|
| 5) Connect the longer end (anode) of the second (yellow) LED to the
|    positive side of the breadboard after the first LED.
|
| 6) Connect the next wire to physical pin 16 (BCM 23); connect the other
|    end to the shorter end (cathode) of the second (yellow) LED.
|
| 7) Connect the longer end (anode) of the third (green) LED to the
|    positive side of the breadboard after the second LED.
|
| 8) Connect the next and final wire to physical pin 18 (BCM 24); connect
|    the other end to the shorter end (cathode) of the third (green) LED.
|

.. |gpio-diagram| image:: images/gpio-diagram.png

Setting up simple_google_tts
----------------------------
| 1) As per the instructions from `this link <https://github.com/alexylem/jarvis/issues/129#issuecomment-248072872>`_, download each of the following
| files on your Raspberry Pi:
|   - `libttspico-data <http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-data_1.0+git20130326-3_all.deb>`_
|   - `libttspico0_1.0 <http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-3_armhf.deb>`_
|   - `libttspico-utils <http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-3_armhf.deb>`_
|
| 2) And following the same instructions, install each of the packages onto your Pi:

.. code:: bash

    sudo dpkg -i libttspico-data_1.0+git20130326-3_all.deb
    sudo dpkg -i libttspico0_1.0+git20130326-3_armhf.deb
    sudo dpkg -i libttspico-utils_1.0+git20130326-3_armhf.deb

| 3) If git is not installed, you will need to install it:

.. code:: bash

    sudo apt install git

| 4) As instrcuted in the `simple_google_tts readme <https://github.com/glutanimate/simple-google-tts>`_, run the following command:
|

.. code:: bash

    sudo apt-get install xsel libnotify-bin libttspico0 libttspico-utils libttspico-data libwww-perl libwww-mechanize-perl libhtml-tree-perl sox libsox-fmt-mp3

| 5) Clone the repo into the home directory and then open ~/.bashrc:

.. code:: bash

    cd /home/pi; git clone https://github.com/Glutanimate/simple-google-tts.git
    nano .bashrc

| 6) On a new line, at the end of .bashrc, add the following:

.. code:: bash

    export PATH="$PATH:`pwd`/simple-google-tts"

|

Installing the Python packages
------------------------------
| 1) First, ensure python3-pip is installed on your Raspberry Pi:

.. code:: bash

    sudo apt install python3-pip

| 2) Now install mqtttasky_groupme from the package index:

.. code:: bash

    pip3 install mqtttasky-groupme==0.1.4

|

Registering for GroupMe, Creating a Group
-----------------------------------------
| 1) If you do not already, you will need to create a GroupMe account
|    since this is what MQTTTasky will use to allow you to schedule
|    tasks. You may sign up for groupme `here <https://web.groupme.com/signup>`_.
|
| 2) Afer registering, login. You will need to create at least one group
|    to which you will add your GroupMe bot after having created it. For
|    help with creating a group, see `this page <https://support.microsoft.com/en-us/office/how-do-i-start-a-group-in-groupme-d7488e15-4429-43ff-85fa-a5c7775305e2>`_.
|

Creating your GroupMe bot
-------------------------
| 1) First, register a developer account after logging in at
|    (https://dev.groupme.com/).
|
| 2) After your are logged in, click the 'Bots' link in the main site
|    navigation or visit (https://dev.groupme.com/bots).
|
| 3) Click "Create Bot", and select thr group to which it
|    will belong and name it. You will not need to enter
|    a callback URL and you may give the bot an avatar
|    by entering a public image URL.
|
| 4) After having created your bot, it will be visible on the page at
|    (https://dev.groupme.com/bots).
|
| 5) Copy your bot's ID, as well as the Group ID to which it belongs.
|    Finally, find the 'Access Token' link in the main site navigation
|    and copy it as well. You will need all of this information shortly.
|

Setting up a Mosquitto broker
------------------------------
| MQTTTasky requires to be connected to an MQTT broker which uses
| authentication. The broker can be hosted on another computer or
| Raspberry Pi. It is not recommended to host the broker on the same Pi
| as MQTTTasky will be running on. To set up a Mosquitto broker on a
| Raspberry Pi, please refer to `these instructions <https://medium.com/@eranda/setting-up-authentication-on-mosquitto-mqtt-broker-de5df2e29afc>`_.
|
| Please note while following along with the instructions above, that
| there are a couple of descrepancies. In the first step, you will have
| to change the line

.. code:: bash

    sudo wget http://repo.mosquitto.org/debian/mosquitto-wheezy.list

| to the following:

.. code:: bash

    sudo wget http://repo.mosquitto.org/debian/mosquitto-buster.list

| Furthermore, the line that says

.. code:: bash

    sudo stop mosquitto

| in step 2 should instead read:

.. code:: bash

    sudo systemctl stop mosquitto

| Finally, please record the username and password you used in this
| configuration as you will need it when configuring MQTTTasky.

Configure MQTTTasky
-------------------
| After having completed the above setup, you are ready to start the
| mqtttasky_groupme program. This may be done simply by entering:

.. code:: bash

    mqtttasky_groupme

| On first launch, you will be prompted to enter your GroupMe information
| as well as your MQTT broker and authentication information. You should
| have already recorded these. If you are unsure of your broker's port
| number, it is likely 1883 and if it is hosted on a Linux machine, the
| IP address can be found using the 'ifconfig' command (or 'ipconfig' on 
| Windows). If the configuration is successful, you will see similar
| output to that below:

.. code:: bash

    [ MQTT Client ] Connected to broker.


    #######################
    # Bot: Tarnoff Bot
    # Group: IoT Dev Server
    # Status: Listening
    #######################

| Note that you can break out of the program using Ctrl-C. Any time you
| need to re-run the configuration, you may enter the command:

.. code:: bash

    mqtttasky_groupme_config


MQTTTasky: Status lights, notifications, and usage
##################################################

Status lights and notifications
-------------------------------
| First you will notice that MQTTTasky's MQTT client has connected to
| the broker. Once the broker is connected, MQTTTasky will start
| listening for messages every 4 seconds.
|
| Each time the program successfully retrieves the messages, the second 
| (yellow) LED will blink on and off.
|
| Each time a message retrieval fails, the first (red) LED will blink on
| and off.
|
| Each time a new message is discovered, the third (green) LED will blink
| on and off several times.
|
| Each time a new response is sent back from the bot, the second (yellow)
| LED will blink on and off several times.
|
| Finally, when a notification is being shown and the MQTT client is
| publishing data, all three lights will blink several times in a sequence.
| Additionally, MQTTTasky will display the task notification in a graphical
| window and read the task information aloud using simple_google_tts. Every
| time a task notification is published, the payload is encrypted using
| Fernet encryption and the key provided during the configuration of
| mqtttasky_groupme. This key can be used to create a Fernet cipher in other
| MQTT clients on the network so that they may decrypt the payload. Included
| in the 'node_mqtttasky_pi_client' directory is an example of such a client
| in Node.js. It's instructions can be found in a separate readme file within
| that directory.

Usage
------
| The MQTTTasky bot will make it fairly clear what you need to do to create
| a task, however, other options, such as resetting task data or deleting
| all scheduled tasks are available. The usage for communicating with the
| bot is as follows:
|
| MQTTasky Usage
| ===============================
| - Initiate a new task:
| 'Schedule task'
| 'Schedule task <title> with description <description>'
| 
| - Date and time:
| MQTTTasky will let you know how
| to enter date or time when prompted.
| If the year is not provided in a date
| string, the current year is assumed.
|
| Time strings ending in AM or PM are
| automatically converted into 24-hr
| format.
|
| - Notifications:
| Notifications are specified by a unit
| of time before the time of the task.
| You may use the following units of
| time:
|
| Minutes:
| E.g. '15 minutes before'
| Hours:
| E.g. '15 hours before'
| Days:
| E.g. '15 days before'
| Weeks:
| E.g. '15 weeks before'
|
| - Reset:
| If you want to cancel or restart the
| creation of a task, use the command:
| '/reset'
| 
| - Delete:
| To delete all active tasks:
| '/deleteall'
| 
| - Bonus:
| Ask bot to tell a joke or proverb.

MQTT Topic Details
##################
| The MQTT topic to which MQTTasky publishes its encrypted payloads
| is pub/tasks. The first topic level denotes published data. The
| second topic level denotes that task data is being published.
| The task data published is a message designed to be read over a
| speaker using TTS. Since a payload is published by the scheduler
| when a notification is set to occur, this allows subscribed MQTT
| clients to display and/or speak the notification when it is
| received.
|
| Since payloads are encrypted using Fernet encryption, the symmetric
| key provided during the initial mqtttasky_groupme configuration can
| be used by clients to implement Fernet decryption tokens to decrypt
| the payloads which can then be decoded to UTF-8 strings.

MQTT Encryption
###############

Fernet (symmetric encryption)
-----------------------------
| MQTTTasky uses the Python Fernet class from cryptography.fernet.
| This class is popular because of its ease of use, and the security
| it offers for the lightweight encryption/decryption that is needed
| in IoT.
|
| The algorithm used in Fernet is AES using CBC mode with signing
| using HMAC and SHA256. Thus Fernet not only encrypts/decrypts but
| allows for the authentication of messages to ensure integrity
| (`McBride, 2020 <https://www.pythoninformer.com/python-libraries/cryptography/fernet/>`_).
|

CBC
===
| In cipher block chaining (CBC), plaintext blocks get XORed with
| previous ciphertext blocks prior to the encryption process. That
| is why it is referred to as block chaining, because each ciphertext
| block depends on ever processed plaintext block at each that moment.
| This preserves the integrity of the data
| (`Block cipher mode of operation, 2020 <https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)>`_).
|

HMAC
====
| Hashing for Message authentication (HMAC) applies a hash function
| over the data and the symmetric key. HMAC using SHA256 is the part
| of Fernet that ensures the authenticity and integrity of the message
| (`John C. Villanueva, 2016 <https://www.jscape.com/blog/what-is-hmac-and-how-does-it-secure-file-transfers>`_).
|
| As Villanueva (`2016 <https://www.jscape.com/blog/what-is-hmac-and-how-does-it-secure-file-transfers>`_) points out, one advantage of using HMAC for data
| transfer is that hash functions create a fixed-length digest
| regardless of the arbitrary length of the message hashed; this
| results in mitigating the amount of bandwidth needed to transfer
| data over a network.

Fernet Key Format
=================
| Key generation using the cryptography.fernet library's Fernet class
| renders a 32-byte key which is actually a composite of two 16-byte
| keys. The first 16 bytes being a signing key used to sign the HMAC
| and the second 16 bytes being a private key used by the encryption
| (`McBride, 2020 <https://www.pythoninformer.com/python-libraries/cryptography/fernet/>`_).
| 

Fernet Token Format
====================
| The Fernet token used in the Fernet class consists of:
|    • Version, 1 byte - the only valid value currently is 128.
|    • Timestamp 8 bytes - a 64 bit, unsigned, big-endian integer
|    that indicates when the ciphertext was created. Time is
|    represented as the number of seconds since the start of Jan 1,
|    1970, UTC.
|    • IV 32 bytes - the 128 bit Initialization Vector used in AES
|    encryption and decryption.
|    • Ciphertext - the encrypted version of the plaintext message. This is
|    encrypted using AES, in CBC mode, using the encryption key section
|    of the Fernet key. The ciphertext is padded to be a multiple of 128
|    bits, which is the AES block size, using the PKCS7 padding algorithm.
|    This menas that the ciphertest will always be a multiple of 16 bytes
|    in length, but the padding will be automatically removed when the
|    data is decrypted.
|    • HMAC - a 256-bit HMAC of the concatenated Version, Timestamp, IV,
|    and Ciphertext fields. The HMAC is signed using the signing key
|    section [of the] Fernet key.
|    (`McBride, 2020 <https://www.pythoninformer.com/python-libraries/cryptography/fernet/>`_).   
|
| Once the HMAC has been calculated using the binary data from the Version,
| Timestamp, IV, and Ciphertext, the entire token is encoded in Base64
| encoding (`McBride, 2020 <https://www.pythoninformer.com/python-libraries/cryptography/fernet/>`_). According to Base64 (`2020 <https://developer.mozilla.org/en-US/docs/Glossary/Base64>`_), this encoding
| method is used to encode binary data which may need to be transferred to
| and stored on media designed to handle ASCII. This is a convenient format
| for the Web since it would allow binary data to be represented within a
| URL as ASCII text. This encoding does come at a price -- increased size.
| Every Base64 digit represents exactly 6 bits of data. Base64 can increase
| the size of a string by as much as ~33 percent (`Base64, 2020 <https://developer.mozilla.org/en-US/docs/Glossary/Base64>`_).


Node.js MQTT client for reading task notifications
##################################################

| In the `node_mqtttasky_pi_client <https://github.com/haasr/mqtttasky_groupme/tree/master/node_mqtttasky_pi_client>`_,
| directory of this repository is a Node.js client which can be configured
| to use the mqtttasky_groupme client's Fernet key to decrypt the message
| payloads published by MQTTasky and read them aloud using
| simple_google_tts. See the separate README file `on this page <https://github.com/haasr/mqtttasky_groupme/tree/master/node_mqtttasky_pi_client>`_ for details
| about pacakges used, setup, and usage.