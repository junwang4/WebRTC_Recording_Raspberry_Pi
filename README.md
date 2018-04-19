# Recording Conversation on Raspberry Pi

You can use this code for recording conversation with a Raspberry Pi - it takes only about 1% CPU.
Note that one hour of recording files takes about 100M storage.

## Getting Started
### Prerequisites
Hardware
* Raspberry Pi
* USB microphone

Software
* for best practice, create a virtual environment for python3
* PyAudio [how to install](https://people.csail.mit.edu/hubert/pyaudio/)

### Step by step
#### Step 1
* ssh to your raspberry pi
```
cd /home/pi/git
git clone https://github.com/junwang4/WebRTC_Recording_Raspberry_Pi
```
To give it a quick test,
```
cd ~/git/WebRTC_Recording_Raspberry_Pi
# note that the folder for saving your recordings is hardwired to /home/pi/data
# to change the default folder, edit the file webrtc_recording.py
python webrtc_recording.py
```

#### Step 2: set up service
* cd /lib/systemd/system/
* sudo vi voice_recording.service
```
[Unit]
Description=Voice Recording
After=multi-user.target

[Service]
Type=simple
ExecStart=/home/pi/env/bin/python /home/pi/git/WebRTC_Recording_Raspberry_Pi/webrtc_recording.py

Restart=on-abort

[Install]
WantedBy=multi-user.target
```
#### STEP 3.
```
sudo systemctl daemon-reload

sudo systemctl enable voice_recording.service

sudo systemctl start voice_recording.service
sudo systemctl restart voice_recording.service
sudo systemctl stop voice_recording.service

# To check the service's log
sudo journalctl -f -u voice_recording.service
```


### Sound card setting and information
If it doesn't work, the problem is very likely related to sound card configuration.
* ~/.asoundrc for user "pi"
* /etc/asound.conf for user "root"  (needed if you want to launch the voice recording as a service) see Part 2 of this

## Acknowledgement
* WebRTC VAD could be the fastest one for filtering out non-speech when recording human conversation in real-time situation.
* Wiseman wrote a [python interface to the WebRTC Voice Activity Detector (VAD)](https://github.com/wiseman/py-webrtcvad). In his repository, he provides an excellent example to demonstrate how to segment a wave file to a group of voiced ones.  My code is based on his example.
