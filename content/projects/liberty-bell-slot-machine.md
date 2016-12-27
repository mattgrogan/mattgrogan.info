+++
date = "2016-12-26T13:31:34-05:00"
title = "Liberty Bell Slot Machine"
draft = true
type= "Blog"
+++

## The Idea

The [Liberty Bell](http://bit.ly/2hrTtj6) was the first mechanical slot machine. It was created in 1895 by Charles Fey in San Francisco. The five-cent game had three reels and six symbols: diamond, heart, spade, horseshoe, star, and the Liberty Bell.

For some time I have been curious as to the "feel" of the gameplay on such an old machine. So built and programmed a replica using modern technology.

This was a fun project because it has everything: probability, statistics, gameplay, databases, analytical dashboards, buttons, LEDs, color displays, monochrome display, seven segment displays, sound, and historical significance.

## Research

### Casino Trip

This project was the perfect excuse to visit Mohegan Sun! I had a few outstanding questions, for example: when exactly does the machine debit your credits? A: The instant you hit spin.

As you can see, I'm not the gambling type...

<iframe width="560" height="315" src="https://www.youtube.com/embed/oe1jpN7Fwbo" frameborder="0" allowfullscreen></iframe>

### Reel Layout

I found the reel layout in [_Slot Machines: A Pictorial History of the First 100 Years_](http://a.co/6dcRtuM) by Marshall Fey.

|           | Reel 1 | Reel 2 | Reel 3 |
|-----------|--------|--------|--------|
| Star      |        |        | 2      |
| Horseshoe | 5      | 5      |        |
| Spade     | 2      | 2      | 2      |
| Diamond   | 1      | 1      | 3      |
| Heart     | 1      | 1      | 1      |
| Bell      | 1      | 1      | 2      |
|           | 10     | 10     | 10     |

### Pay Table

|                       | Reel 1 | Reel 2 | Reel 3 | Hits | Credits Paid | Total Paid Out |
|-----------------------|--------|--------|--------|--------------|--------------|------------------------|
| 2 Horseshoes          |    5   |    5   | (10-2) |          200 |       2      |                    400 |
| 2 Horseshoes and Star |    5   |    5   | (10-8) |           50 |       4      |                    200 |
| 3 Spades              |    2   |    2   |    2   |            8 |       8      |                     64 |
| 3 Diamonds            |    1   |    1   |    3   |            3 |      12      |                     36 |
| 3 Hearts              |    1   |    1   |    1   |            1 |      16      |                     16 |
| 3 Liberty Bells       |    1   |    1   |    2   |            2 |      20      |                     40 |
|                       |        |        |        |          264 |              |                    756 |

With ten symbols per reel, there are 10 * 10 * 10 = 1,000 possible outcomes. This means that 26.4% of the spins will result in a payout and the machine will return 75.6% of the amount wagered to the player.

## Components

### Electronics

* Raspberry Pi version 3
* 3x OLED BREAKOUT BOARD - 16-BIT COLOR 1.5" from [Adafruit](https://www.adafruit.com/products/1431)
* MONOCHROME 1.3" 128X64 OLED GRAPHIC DISPLAY from [Adafruit](https://www.adafruit.com/products/938)
* 3x 0.56" 4-DIGIT 7-SEGMENT DISPLAY W/I2C BACKPACK - BLUE from [Adafruit](https://www.adafruit.com/products/881)
* RPi Proto Breadboard PCB Kit for Raspberry Pi 3 from [Amazon](http://a.co/5hbnjhv)
* 3x Round Blue Momentary Push Button Switch from [Amazon](http://a.co/7TaxnVT)
* 3x LED Illuminated Pushbutton - 30mm Square from [Adafruit](https://www.adafruit.com/products/491)
* Momentary push button (to access menu)
* Tactile switch (to reset the Raspberry Pi)
* Large Enclosed Piezo Element w/Wires from [Adafruit](https://www.adafruit.com/products/1739)

### Tools and Hardware

* Lots of wires, hand crimped with Dupont connectors
* Crimping Tool
* Screws of many sizes with washers and nuts
* Lexan sheets for the front
* Wood for the enclosure and backing
* Silhouette Portrait vinyl cutter
* Vinyl for the vinyl cutter
* Soldering iron
