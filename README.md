# Recording Conversation on Raspberry Pi

You can use this code for recording conversation with a Raspberry Pi - it takes only about 1% CPU.
Suppose on average you have 2 hours of recording a day, you will need about 7G storage for the generated wave files.

## Getting Started
### Prerequisites
Hardware
* Raspberry Pi
* USB microphone

Software
* PyAudio

### Sound card setting and information

## Acknowledgement
* WebRTC VAD could be the fastest one for filtering out non-speech when recording human conversation in real-time situation.
* Wiseman wrote a [python interface to the WebRTC Voice Activity Detector (VAD)](https://github.com/wiseman/py-webrtcvad). In his repository, he provides an excellent example to demonstrate how to segment a wave file to a group of voiced ones.  My code is based on his example.
