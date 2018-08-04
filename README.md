![](https://blog.inach.is/uart-finder/images/uart-finder-labelled.jpg)

## Description

Uart-finder is a portable, DIY-friendly tool for quickly detecting echo-enabled UART on otherwise unknown pads and traces on a PCB. It actively sends data on both probes in order to detect an echo from the target device. An echo-enabled console behind UART strongly suggests an interactive shell or a script/program that might be faulted into an interactive shell.

Uart-finder is easy to modify since it is about 50 lines of CircuitPython (v3). Modifications are made, under an emulated FAT filesystem when connected to a computer, by modifying 'main.py'. The device will reset with the new code every time 'main.py' is written. If you have a Trinket M0 without CircuitPython loaded, please refer to [Adafruit's instructions](https://learn.adafruit.com/adafruit-trinket-m0-circuitpython-arduino/circuitpython) to get started.

Uart-finder also takes advantage of the Trinket M0's hardware UART with remappable pins.
Each probe gets reassigned between RX and TX every 10 milliseconds, so you don't have to care which is which, and hardware UART ensures signals will not be dropped while the M0 is busy TXing and comparing values.

By default, it takes about 20 ms to test a pair of unknown pads for UART per baudrate. Included are four common baudrates to scan: 9600, 19200, 57000, 115200.

The concept is based on the "UART discovery assistant module" in [*Opening Pandora’s Box: Effective Techniques for Reverse Engineering IoT Devices*](https://iss.oy.ne.ro/Pandora.pdf). Unfortunately I could not find the source code for the original.

## Requirements

  - [Trinket M0](https://learn.adafruit.com/adafruit-trinket-m0-circuitpython-arduino/overview)
  - Wires

#### Optional (see BOM and SCHEMATIC):

  - A 2x 2032 coin battery holder with a switch (6v output with 2x 3v batteries). This should give 20 - 40 hours of constant use. Alternatively, 2 to 4 AA batteries can be used for increased capacity.

  - 2x 100K Ohm resistors. These will be used as pull-up resistors for pins 0 and 4, which provide additional signal integrity.

  - Mulitmeter probes and corresponding plugs.

  - A box, wooden block or equivalent to mount everything on (not in BOM).

## Install

With a Trinket M0 and CircuitPython already installed on it, copy the contents of 'firmware' to the Trinket's root directory

## Instructions

[Demo video [2 MB]](https://blog.inach.is/uart-finder/images/uart-finder-demo.mp4)

Uart-finder is an active measurement tool since it drives 3.3V signals on each probe. Both probes need to be used since both TX and RX are required to send and receive a byte. After each probe sends the test byte, the process is repeated for all common baudrates defined in 'main.py'.

There are two probes and a ground clip. Generally, the ground clip can be hooked onto metal shielding or a connector on the target board, or another point that is determined to be the target's ground. Both probes should be applied to suspect RX/TX points on the target board. Since the RX/TX pins on the uart-finder get swapped internally, there is no need to account for a false-negative due to inverting RX and TX against the target.

There are three LED indicators. The green 'on' LED is on while the device is running. The red LED on the other side of the USB connector is the 'sweep' indicator: it flashes every time all baudrates have been scanned on each probe. You should time your tests so that you get at least two flashes per permutation. Unfortunately, the red LED is not visible in the demo gif.

The dotstar RGB LED in the middle indicates if the sent byte has been received by a probe. The color of the RGB LED indicates which probe received the byte. By default, 'red' indicates pin 4 (red probe in the picture) was the receiver and 'blue' indicates pin 0 (black probe in the picture) as the receiver. If the uart-finder is connected to a computer, the baudrate of the received byte can be read from a serial terminal.

Sometimes an ASCII byte might be received from the target device (i.e. text from a boot-up sequence). If the uart-finder receives an ASCII byte that isn't a space, the dotstar LED will either glow 'yellow' if the ASCII byte is received on pin 4, and 'cyan' if the byte is received on pin 0. The baudrate and received byte is output to the serial terminal.

When a byte is received, all transmission is halted for one second while the dotstar indicates the receiving probe. This avoids spamming what might be a legitimate interactive console with spaces.

## Precautions and considerations

Uart-finder on the trinket M0 consumes ~ 11.5 mAh @ 3-6 V.

To avoid damaging the target device, avoid or at least measure areas that are close to the MCU / RAM peripherals as they might not tolerate the 3.3V signals from the uart-finder.

To avoid damaging the uart-finder, use a multimeter to ensure that the target test points are not outputting more than 3.3 V.

Start with any obvious straight sets of 4 pins or pads on the PCB. Look for any unpopulated pads near the edge which may have been used to the development version of the device to manage or attach debug ports. Test unlabeled or hidden connectors as well.

To ensure accuracy:

  - Add 100K-Ohm pull-up resistors on pin 4 and pin 0 of the uart-finder, especially when using long probe wires. This will reduce false-positives from signal reflection and EM cross-talk between the two probe wires.

  - Use probes with highly conductive, sharp tips. See BOM for recommended probes.

  - Test for false positives by swapping probe positions and observing a change of color from the dotstar LED.

  - Alternating blue/red on the dotstar LED indicates a short between the probes or test points.

