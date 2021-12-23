# Aralez
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
  * OS: Raspbian OS Lite.
  * Python 3 version: 3.6.9.
  * Pip 3 version: 9.0.1.

Install the required dependencies:
> sudo apt-get install -y mpg321

> sudo apt install python3-pip python3-pyaudio libatlas3-base

> pip3 install -r requirements.txt

### Components
  * 2 x DC motors. --->
  * Raspberry Pi 4 model B 64-bit 2GB RAM. ---> 30$
  * L298N motor driver. --->
  * SD card 32 GB (Samsung EVO Plus class 10). --->
  * Raspberry Pi CPU cooler. --->
  * Mono speaker. --->
  * Microphone. --->
  * Ultrasonic transducer. --->
  * Mono speaker amplifier. --->

Visual Question Answering
https://victorzhou.com/blog/easy-vqa/
https://tts.readthedocs.io/en/latest/what_makes_a_good_dataset.html%20
https://stt.readthedocs.io/en/latest/SUPPORTED_PLATFORMS.html

### GPIO setup

![alt text](https://github.com/Varuzhan97/Aralez/blob/main/gpio-pin.jpg)

  * On/Off button: 1 ---> GPIO03, PIN# 05 | 0 ---> Ground, PIN# 06
  * Motor/wheel 1: input_1 GPIO17, PIN# 11 | input_2 GPIO27, PIN# 13 | enable_1 GPIO22, PIN# 15 | GROUND KA???
  * Motor/wheel 2: input_3 GPIO23, PIN# 16 | input_4 GPIO24, PIN# 18 | enable_2 GPIO25, PIN# 22 | GROUND KA???
  * Red LED: 1 ---> GPIO11, PIN# 23 | 0 ---> GROUND KA???
  * Green LED: 1 ---> GPIO10, PIN# 19 | 0 ---> GROUND KA???
  * Blue LED: 1 ---> GPIO9, PIN# 21| 0 ---> GROUND KA???
  * Ultrasonic transducer: trigger ---> GPIO18, PIN# 12 | echo ---> GPIO15, PIN# 10 | 0 ---> GROUND KA???
  * L298N motor driver: ?????????????????????????????
  * Mono speaker: ??????????????????????????
  * Mono speaker amplifier: ????????????????????
