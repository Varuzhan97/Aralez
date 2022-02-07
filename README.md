# Ruby
Supported languages are:
  - [x] English(En)
  - [x] Russian(Ru)

Games are:
  - [x] Capitals
  - [x] Twenty one

Language courses are:
  - [x] English
  - [x] Russian

STT training results are:
  - [x] English
    * Train loss: 0.000000
    * Validation loss: -0.000000
    * Dataset: ~/En/clips                                    
    * Checkpoint: ~/En/Checkpoints/best_dev-1818201
    * Test WER: 0.000000
    * Test CER: 0.000000
    * Test Loss: -0.000000
  - [x] Russian
    * Train loss: 0.000001
    * Validation loss: -0.000000
    * Dataset: ~/Ru/clips                 
    * Checkpoint: ~/Ru/Checkpoints/best_dev-2228668
    * Test WER: 0.000000
    * Test CER: 0.000000
    * Test Loss: 0.000038

### Environment and Requirements
  * OS: Raspberry Pi OS Lite 32-bit(Legacy / Debian Buster 10)
  * Python 3 version: 3.7.3.
  * Pip 3 version: 18.1.

Install the required dependencies:
> sudo apt-get update

> sudo apt-get install python3-pip python3-pyaudio libatlas3-base

> sudo apt-get install -y mpg321

> sudo apt-get install git

> pip3 install -r requirements.txt

> scipy error solving command ---> $ sudo apt-get install libatlas-base-dev gfortran

### Components
  * (board) Raspberry Pi 4 model B 64-bit 2GB RAM.
  * (board cooler) ALAMSCN aluminum heat sink cooling fan with heatsink set
  * (board storage) Samsung 32GB EVO Plus microSDHC(2017 model) class 10.
  * (motor driver) Qunqi L298N motor drive controller board module dual H bridge DC stepper.
  * (motor) Yeeco DC electric motor 3V-6V dual shaft DC gear motor 1:120 reduction ratio geared TT magnetic gearbox
    engine with plastic car tire wheel.
  * (mono speaker) ???.
  * (microphone) ???.
  * (distance sensor) Ultrasonic transducer.
  * (RGB LED)3 RGB LED lights.
  * (ON/OFF push button) mxuteuk 19mm latching push button switch (1 NO 1 NC SPDT ON/OFF SILVER WITH 12V blue power symbol light.)

Visual Question Answering
https://victorzhou.com/blog/easy-vqa/
https://tts.readthedocs.io/en/latest/what_makes_a_good_dataset.html%20
https://stt.readthedocs.io/en/latest/SUPPORTED_PLATFORMS.html

Manual examples https://fccid.io/png.php?id=859841&page=0
Lullaby https://www.youtube.com/watch?v=ZqMN0g5gi2I&ab_channel=JB-Audio
Plastic:
1) https://www.creatingrapid.com/low-volume-rapid-prototyping-manufacturer/?keyword=plastic%20parts%20manufacturer&matchtype=b&network=g&device=c&adposition=&placement=&gclid=CjwKCAjw7--KBhAMEiwAxfpkWB-6NnmezUFYj9J2Amv43gfpI7uAFGE4G38S8CYgkbHgQ3MTD7My4hoCX7sQAvD_BwE
2) https://www.cnmould.com/plastic-moulding-service.html?gclid=CjwKCAjw7--KBhAMEiwAxfpkWCcVCRIBYnQ5AErR4dFUfTiQh5pxSuK1zXFFMYM1ZQGbFVtOSrY7SRoCN88QAvD_BwE
3) https://www.immould.com/professional-plastic-molding-company/?keyword=china%20plastic%20products%20manufacturers&matchtype=e&network=g&device=c&adposition=&gclid=CjwKCAjw7--KBhAMEiwAxfpkWDRqMwiFTCMnwOMpCFiWXgFbJaMeUc4xYU7KyD3-2LMV4NFEwl7yshoCgfUQAvD_BwE

mic https://www.adafruit.com/product/3421
mic pdf https://cdn-learn.adafruit.com/downloads/pdf/adafruit-i2s-mems-microphone-breakout.pdf
fact https://www.hackster.io/news/why-mems-microphones-are-the-best-choice-for-your-project-fb4c3a61f33d
speaker https://www.adafruit.com/product/3351
amplifier https://www.adafruit.com/product/3006
speaker pdf https://cdn-learn.adafruit.com/downloads/pdf/adafruit-max98357-i2s-class-d-mono-amp.pdf

#deepspeech-tflite for linux desktop without gpu

### GPIO setup

![alt text](https://github.com/Varuzhan97/Aralez/blob/main/gpio-pin.jpg)
![alt text](https://github.com/Varuzhan97/Aralez/blob/main/RGBLED_Pinout.jpeg)

  * + On/Off button: 1 ---> GPIO03, PIN# 05 | 0 ---> Ground, PIN# 09
  * Motor/wheel 1: input_1 GPIO17, PIN# 11 | input_2 GPIO27, PIN# 13 | enable_1 GPIO22, PIN# 15 | GROUND KA???
  * Motor/wheel 2: input_3 GPIO23, PIN# 16 | input_4 GPIO24, PIN# 18 | enable_2 GPIO25, PIN# 22 | GROUND KA???
  * RGB LED: Red ---> PIN# 11 | Green ---> PIN# 13 | Blue ---> PIN# 15 | 0 ---> Ground, PIN# 25
  * Ultrasonic transducer: trigger ---> GPIO18, PIN# 12 | echo ---> GPIO15, PIN# 10 | 0 ---> GROUND KA???
  * L298N motor driver: ?????????????????????????????
  * + Mono speaker: 1 ---> amplifier 1 | 0 ---> amplifier 0
  * + Mono speaker amplifier: Amp Vin to 5V  (Pi 2) | Amp GND to GND (Pi 20) | Amp DIN to  Pi 21 | Amp BCLK to  Pi 18 | Amp LRCLK to  Pi 19
  * + Microphone: Mic 3V to Pi 3.3V (PIN# 17) | Mic GND to Pi GND (PIN# 34) | Mic SEL to Pi GND (this is used for channel selection, connect to either 3.3V or GND, PIN# 39) | Mic BCLK to BCM 18 (PIN# 12) | Mic DOUT to BCM 20 (PIN# 38) | Mic LRCL to BCM 19 (PIN# 35)
  * + Cooler: 1 5V PIN#4 | 0 PIN#6

### Auto-login

To enable auto-login with raspi-config:
  * Run: sudo raspi-config
  * Choose option: 1 System Options
  * Choose option: S5 Boot / Auto Login
  * Choose option: B2 Console Autologin
  * Select Finish, and reboot the Raspberry Pi.

### First time startup steps

  * Prepare SD card
  * Connect components
  * Start OS
  * Enable auto-login
  * Enable SSH server(if not using HDMI display)
  * Configure ALSA for microphone and speaker
  * Git-clone repository
  * Install requirements
  * Install on/off configurations (make it auto start application)
  * Install project configurations (make it auto start application)

### ISO making steps

  * lsblk
  * sudo mkdir /dev/iso
  * sudo mount /dev/sda1 /dev/iso
  * sudo dd if=/dev/mmcblk0 of=/dev/iso/ruby.img bs=1M

### Microphone and speaker setup

> aplay -l ---> check speaker ID

> arecord -l ---> check microphone ID

sudo nano ~/.asoundrc

pcm.!default {
  type asym
  playback.pcm {
    type hw
    card 0
  }
  capture.pcm {
    type plug
    slave {
      pcm {
        type hw
        card 1
        device 0
      }
    }
  }
}

### On startup run setup

> sudo nano /home/pi/.bashrc

Go to the last line of the script and add:

> python3 /home/pi/sample.py

ya garjus s taboi
