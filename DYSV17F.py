# Circuitpython code for DY-SV17F MP3 module
# 2024 Leif Bjornstad
#
# Note: seems like default behavior of this chip is max volume (30)

import board
import time
import busio

class DYSV17F:
    EQ_NORMAL = 0
    EQ_POP = 1
    EQ_ROCK = 2
    EQ_JAZZ = 3
    EQ_CLASSIC = 4

    FULL_CYCLE = 0
    SINGLE_CYCLE = 1
    SINGLE_STOP = 2
    RANDOM_BROADCAST = 3
    REPEAT_FOLDER = 4
    RANDOM_BROADCAST_FOLDER = 5
    ORDER_PLAY_FOLDER = 6
    ORDER_PLAY = 7

    def __init__(self, tx, volume = None):
        # create UART connection
        self.uart = busio.UART(tx, baudrate = 9600, bits = 8, stop = 1)

        # set volume
        if volume: self.set_volume(volume)

    def write(self, cmd):
        # Sequence reference:
        # START CODE: AA
        # CMD CODE
        # DATA (0 if no data)
        # CRC (LOW 8 BITS)

        code = 0xaa

        # calculate CRC (low 8 bit)
        crc = (code + sum(cmd)) % 256

        # make bytearray from command bytes
        message = bytearray([code] + [int(x) for x in cmd] + [crc])

        self.uart.write(message)

    def play(self, track = None):
        # Generic play command is AA 02 00
        # Specific track command is:
        #  AA 07 02 High Byte Low Byte SM
        #               ^ MUSIC # ^
        # For example: AA 07 02 00 08 BB is to play the specified 8th music.
        if track:
            high_byte = track // 256
            low_byte = track % 256
            self.write([0x07, 0x02, high_byte, low_byte])
        else:
            self.write([0x02, 0x00])

    def pause(self):
        self.write([0x03, 0x00])

    def stop(self):
        self.write([0x04, 0x00])

    def previous(self):
        self.write([0x05, 0x00])

    def next(self):
        self.write([0x06, 0x00])

    def volume_up(self):
        self.write([0x14, 0x00])

    def volume_down(self):
        self.write([0x15, 0x00])

    def set_volume(self, volume = 30):
        # Max volume is 30
        self.write([0x13, 0x1, volume])

    def mute(self):
        self.set_volume(0)

    def set_playmode(self, playmode = FULL_CYCLE):
        self.write([0x18, 0x01, playmode])

    def set_eq(self, eq = EQ_NORMAL):
        self.write([0x1a, 0x01, eq])
