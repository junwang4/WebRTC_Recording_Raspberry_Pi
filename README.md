# Recording Conversation on Raspberry Pi

You can use this code for recording conversation with a Raspberry Pi - it takes only about 1% CPU.
Note that one hour of recording files takes about 100M storage.

## Getting Started
### Prerequisites
Hardware
* Raspberry Pi (you may want to set timezone with `sudo dpkg-reconfigure tzdata`)
* USB microphone

Software
* for best practice, create a virtual environment for python3 (see below)
```
cd /home/pi
sudo apt-get install python3-pip
python3 -m pip install --user virtualenv
python3 -m virtualenv env
source env/bin/activate
```
You may want to append a line `source env/bin/activate` to your `~/.bashrc` so that it is ready to use next time when you ssh to login

* PyAudio - [how to install officially](https://people.csail.mit.edu/hubert/pyaudio/)
```
sudo apt-get update
sudo apt-get install python-pyaudio python3-pyaudio
sudo apt-get install portaudio19-dev
pip install pyaudio
pip install webrtcvad
```

### Step by step
#### Step 1
ssh to your raspberry pi
```
sudo apt-get install wget git-core
cd /home/pi
mkdir git
cd git
git clone https://github.com/junwang4/WebRTC_Recording_Raspberry_Pi
```
To give it a quick test,
```
cd ~/git/WebRTC_Recording_Raspberry_Pi
# note that the folder for saving your recordings is hardwired to /home/pi/data
# to change the default folder, edit the file webrtc_recording.py
python webrtc_recording.py
```

**Sound card setting and information**
* If it doesn't work, the problem is likely related to sound card configuration.
   - ~/.asoundrc for user "pi" (for a quick test)
   - /etc/asound.conf for user "root"  (needed for setting up the following service)
* In my case, I used a USB mic (Logitec 720p), and my setting of /etc/asound.conf is (you may want to run "arecord -l" to find your device number for "hw")
```
pcm.!default {
  type asym
  capture.pcm "mic"
  playback.pcm "speaker"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
pcm.speaker {
  type plug
  slave {
    pcm "hw:0,0"
  }
}
```

#### Step 2: create a service so that the program can auto start when the Raspberry Pi boots (e.g. after power off and on)
```
cd /lib/systemd/system/
sudo vi voice_recording.service
```

Note that in the following service setting, my executable **python** is located at **/home/pi/env/bin/python**, because I installed a virtual env there. If you want to use the virtual env too, see far below of this document.

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

#### Step 3
```
sudo systemctl daemon-reload

sudo systemctl enable voice_recording.service

sudo systemctl start voice_recording.service

sudo systemctl restart voice_recording.service  # you may want to run these later
sudo systemctl stop voice_recording.service

# To check the service's log
sudo journalctl -f -u voice_recording.service
```

### If you want to use virtual env of python3
```
cd /home/pi
sudo apt-get install python3-pip
python3 -m pip install --user virtualenv
python3 -m virtualenv env
source env/bin/activate
```
You may want to append a line `source env/bin/activate` to your `~/.bashrc` so that it is ready to use next time when you ssh to login


## Acknowledgement
* WebRTC VAD could be the fastest one for filtering out non-speech when recording human conversation in real-time situation.
* Wiseman wrote a [python interface to the WebRTC Voice Activity Detector (VAD)](https://github.com/wiseman/py-webrtcvad). In his repository, he provides an excellent example to demonstrate how to segment a wave file to a group of voiced ones.  My code is based on his example.
