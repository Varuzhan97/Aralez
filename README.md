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
