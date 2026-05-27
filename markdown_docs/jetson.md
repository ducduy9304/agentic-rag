<!-- page-marker:1 -->
![NVIDIA Logo](nvidia_logo.png)

# Jetson Orin Nano Developer Kit Carrier Board

## Specification

SP-11324-001_v1.3 | December 2024

---

<!-- page-marker:2 -->
# Document History

SP-11324-001_v1.3

| Version | Date | Description of Change |
|---|---|---|
| 1.0 | March 20, 2023 | Initial release |
| 1.1 | May 17, 2023 | > Updated Note in Chapter 1: Introduction with VDD_IN related information.<br> > Updated Pin #13 in Table 2-5: DisplayPort Connector Pin Description – J8.<br> > Updated Pin #55 and Pin #57 in Table 2-6: M.2 Key E Expansion Slot Pin Description – J10.<br> > Added developer kit weight.<br> > Updated Figure 5-1: Power Diagram.<br> > Updated VDD_5V_SYS in Table 5-2: Interface Supply Current Capabilities.<br> > Updated Table 5-3: Supply Current Capabilities per Connector per Supply; replaced VDD_IN with VDD_5V_SYS. |
| 1.2 | April 12, 2024 | > Updated Figure 1-4. Jetson Orin Nano Carrier Board Placement – Top View: corrected Pin 1 location on J20 and J21 camera connectors |
| 1.3 | December 20, 2024 | > Introduction: updated note - Orin NX 40W (MAXN_SUPER) is NOT supported on the developer kit carrier board.<br> > Jetson Orin Nano Module Feature List: updated Memory to reflect MAXN_SUPER performance<br> > CAN Bus Header: corrected typo; reference to a 2.45 mm pitch header (J17) was corrected to say 2.54 mm pitch header (J17) |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | ii

---

<!-- page-marker:3 -->
Table of Contents

Chapter 1. Introduction........................................................................... 1
1.1 Jetson Orin Nano Module Feature List............................................. 2
1.2 Carrier Board Feature List ............................................................. 2
1.3 Jetson Orin Nano Carrier Board Block Diagram ................................... 3

Chapter 2. Jetson Nano Carrier Board Standard Connectors......................... 7
2.1 USB Ports ..................................................................................... 7
2.2 Gigabit Ethernet ............................................................................ 10
2.3 DisplayPort.................................................................................... 11
2.4 M.2 Key E Expansion Slot ................................................................ 12
2.5 M.2 Key M Expansion Slot ................................................................ 14

Chapter 3. Carrier Board Custom Expansion IF Connections....................... 18
3.1 Jetson Orin Nano Module Connector................................................ 18
3.2 Camera Connector ........................................................................... 18
3.3 40-Pin Expansion Header .................................................................. 21
3.4 Button Header ................................................................................ 24
3.5 Optional CAN Bus Header ................................................................ 25
3.6 Fan Connector ................................................................................ 25
3.7 Optional Battery Back-up Coin Cell Holder ........................................... 26
3.8 DC Power Jack ............................................................................... 26
3.9 Optional Power-Over Ethernet and Backpower Headers............................ 27

Chapter 4. Mechanical Specification .......................................................... 29

Chapter 5. Interface Power ........................................................................ 31

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | iii

---

<!-- page-marker:4 -->
# List of Figures

Figure 1-1. Jetson Orin Nano Block Diagram........................................... 4
Figure 1-2. Jetson Orin Nano – Top View (Envelope)..................................... 4
Figure 1-3. Jetson Orin Nano – Bottom View (Envelope).................................. 5
Figure 1-4. Jetson Orin Nano Carrier Board Placement – Top View ....................... 5
Figure 1-5. Jetson Orin Nano Carrier Board Placement – Bottom View.................... 6
Figure 3-1. Expansion Header Connections .............................................. 21
Figure 3-2. Jack Connector ............................................................. 26
Figure 3-3. PoE Alternative Power Input................................................ 27
Figure 4-1. Developer Kit Carrier Board Mechanical Dimensions.......................... 29
Figure 4-2. Developer Kit Mechanical Dimensions........................................ 30
Figure 5-1. Power Diagram.............................................................. 31

# List of Tables

Table 2-1. USB 3.2 Type C Connector Pin Description – J5............................... 7
Table 2-2. USB 3.2 Type A Connector Pin Descriptions – J6............................... 8
Table 2-3. USB 3.2 Type A Connector Pin Description – J7............................... 9
Table 2-4. Ethernet RJ45 Connector Pin Description – J15............................... 10
Table 2-5. DisplayPort Connector Pin Description – J8.................................. 11
Table 2-6. M.2 Key E Expansion Slot Pin Description – J10............................... 12
Table 2-7. M.2 Key M Expansion Slot Pin Description – J11 (x4 PCIe).................... 14
Table 2-8. M.2 Key M Expansion Slot Pin Description – J24 (x2 PCIe).................... 16
Table 3-1. Camera #0 Connector Pin Description – J20................................... 19
Table 3-2. Camera #1 Connector Pin Description – J21................................... 20
Table 3-3. Expansion Header Pin Description – J12...................................... 22
Table 3-4. Button Header Description – J14............................................. 24
Table 3-5. Optional CAN Header Pin Description – J17................................... 25
Table 3-6. Fan Connector Pin Description – J13.......................................... 25
Table 3-7. RTC Backup Batter Connector Pin Description – J3............................ 26
Table 3-8. DC Jack Pin Description – J16................................................ 27
Table 3-9. PoE Header – J19............................................................. 27
Table 3-10. PoE Backpower Header – J18.................................................. 28
Table 5-1. Interface Power Supply Allocation........................................... 32
Table 5-2. Interface Supply Current Capabilities....................................... 32
Table 5-3. Supply Current Capabilities per Connector per Supply....................... 33

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | iv

---

<!-- page-marker:5 -->
# Chapter 1. Introduction

This specification contains recommendations and guidelines for engineers to follow to create modules for the expansion connectors on the NVIDIA® Jetson Orin™ Nano carrier board. As well as understand the capabilities of the other dedicated interface connectors and associated power solutions on the platform.

The Jetson Orin Nano carrier board is ideal for software development within the Linux environment. Standard connectors are used to access Jetson Orin Nano features and interfaces, enabling a highly flexible and extensible development platform. Go to https://developer.nvidia.com/embedded/develop or r contact your NVIDIA representative for access to software updates and the developer SDK supporting the OS image and host development platform that you want to use. The developer SDK includes an OS image that you will load onto your Jetson Orin Nano device, supporting documentation, and code samples to help you get started.

The Jetson Orin Nano carrier board supports all the Jetson Orin Nano Series and Jetson Orin NX Series modules.

> **Caution**: ALWAYS CONNECT JETSON ORIN NANO and ALL EXTERNAL PERIPHERAL DEVICES BEFORE CONNECTING THE POWER SUPPLY TO THE AC POWER JACK. Connecting a device while powered on may damage the developer kit carrier board, Jetson Orin Nano, or peripheral device. In addition, the carrier board should be powered down and the power removed before plugging or unplugging devices or add-on modules into the headers. Wait for the red power VDD_IN LED to turn off or wait for 5 minutes if your system does not have a power LED. This includes the Jetson Orin Nano module, the camera connector, the M.2 connector, and the other expansion headers.

The Jetson Orin Nano developer board contains ESD-sensitive parts. Always use appropriate anti-static and grounding techniques when working with the system. Failure to do so can result in ESD discharge to sensitive pins, and irreparably damage your Jetson Orin Nano board. NVIDIA will not replace units that have been damaged due to ESD discharge.

> **Note**: The developer kit carrier board has been modified to only support 5V to the module. The MODULE_ID signal is not pulled up on the carrier board. This means that regardless of the capability of the module, VDD_IN will be 5V only. Custom carrier boards can still be designed to support 5V and 19V and use the MODULE_ID to identify a 5V vs. 19V Input. Orin NX 40W (MAXN_SUPER) is NOT supported on the developer kit carrier board.

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 1

---

<!-- page-marker:6 -->
Introduction

1.1 Jetson Orin Nano Module Feature List

The following is a list of features for the Jetson Orin Nano module.

> Applications processor (AP)
> - NVIDIA Orin™
> Memory
> - 8 GB 128-bit wide LPDDR5 DRAM (up to 68 GB/s; 102GB/s MAXN_SUPER)
> - Micro SD card socket (UHS-1)
> Networking
> - 10/100/1000 BASE-T Ethernet
> Advanced power management (APM)
> Dynamic voltage and frequency scaling
> Multiple clock and power domains

1.2 Carrier Board Feature List

The following is a list of features for the carrier board.

> Connection to Jetson Orin Nano
> - 260-pin SO-DIMM connector
> USB
> - USBC: Supports Recovery Mode
> - USB 3.2 (Gen2x1) Hub to 4x Type A (host only)
> Wired network
> - Gigabit Ethernet (RJ45 connector with LEDs and optional PoE header)
> Display
> - VESA® DisplayPort™ (DP v1.2 (+MST) and eDP v1.4)
> Camera connectors
> - 2x 22-position flex connectors
> - CSI (2.5 Gbps per pair): 1, x2 or x4 and 1, x2
> - Camera CLK, I2C, and control
> M.2 Key E connector
> - PCIe (Gen3) x1 Lane, USB 2.0
> - I2S, UART, I2C
> - Control

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 2

---

<!-- page-marker:7 -->
Introduction

> M.2 Key M connector (x2)
> - #1) PCIe (Gen3) x4 lane, control
> - #2) PCIe (Gen3) x2 lane, control
> Expansion header
> - 40-pin (2x20) header
> - I2C (x2), SPI (x2), UART
> - I2S, audio clock, GPIOs, PWMs
> UI and indicators
> - Button header: Power, reset, force recovery, debug UART, Auto-Power-On disable
> - LEDs: Power
> Miscellaneous
> - Fan connector: 5V, PWM, and tach
> - Optional RTC back-up connector
> - Optional CAN header
> Power
> - DC Jack: 9-20 V (19V supply provided)
> - Optional Ethernet PoE and back power headers
> - Main 5.0 V Pre-regulator: GS9230 (or A0Z2264)
> - Provides VDD_IN to module
> - Main 3.3V supply: GS9230 (or A0Z2264)
> - Main 1.8V supply: GS71 16S5
> - 3.3V AO (always on) supply: GS71 16S5
> - USB VBUS load switches: AP22811AW5-7 (x2)
> - DP 3.3V power switch: APL3552ABI-TRG
> Developer kit operating temperature range
> - 0°C to 35°C

1.3 Jetson Orin Nano Carrier Board Block Diagram

Figure 1-1 through Figure 1-5 show the block diagram and various placement views for Jetson Orin Nano and the carrier board.

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 3

---

<!-- page-marker:8 -->
Introduction

Figure 1-1. Jetson Orin Nano Block Diagram

![Jetson Orin Nano Block Diagram](image)

Jetson Orin Nano Carrier Board

Jetson Orin Nano

DC Jack 19.5V → PWR & Ctrl → 5V → VDD_IN → Power Subsystem → PCIe#1, Lane 0 → M.2, Key E Socket
→ WiFi DataIF
→ BT Audio
→ BTIF
→ WIFI/BT Control

RJ45 → MDI → GbE PHY (PCIe) → USB 2.0 #2 → I2S #1 → UART#0 → GPIOs

USB Type C → Mux → DPO_x (USBSS1) → PCIe#0, Lanes [3:0] → M.2, Key M Socket → PCIe IF

USB SS Type A x2 → USB 3.1 Hub → USB1 (USB 2.0) → USBSS0 → PCIe#2, Lanes [1:0] → M.2, Key M Socket → PCIe IF

Camera Conn (2-lane) → CSI0/CSI1/CLK1 → MCLK/CTRL → AUD_MCLK → I2S #0 → Level Shifters → Audio Expansion Connector

Camera Conn (2/4-lane) → CSI2/CSI3/CLK2 → MCLK/CTRL → I2C #0 & #1 → SPI #0 & #1 → UART#1 → GPIOs → CtrlIfs → GPIOs

DisplayPort → DPO_TXDx → DPO_AUX → DPO_HPD → LP DDR5, 8GB → QSP IROM (Boot) → PWM & TACH → Fan Conn

SoC

UART#2 → SYS_RESET* → FORCE_RECOVER → SLEEP/WAKE* → Button Header

Figure 1-2. Jetson Orin Nano – Top View (Envelope)

![Jetson Orin Nano – Top View (Envelope)](image)

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 4

---

<!-- page-marker:9 -->
Introduction

Figure 1-3. Jetson Orin Nano – Bottom View (Envelope)

![Jetson Orin Nano – Bottom View (Envelope)](image)

Figure 1-4. Jetson Orin Nano Carrier Board Placement – Top View

![Jetson Orin Nano Carrier Board Placement – Top View](image)

Button Header [J14] — [J17] Optional CAN Bus Header
Camera Conn. #0 [J20] — [J13] Fan Header
Camera Conn. #1 [J21] — [J12] 40-pin Exp Header
Optional PoE Backpower Header — [J2] SODIMM Conn.
USB 3.0 Type A (x2 Stacked) — [J19] Optional PoE Header
DP Connector — [J15] Ethernet Jack
Power Jack — [DS1] Power LED
— [J5] USB Type C

J2 Jetson Orin Nano Conn. (SODIMM, 260-pin) J15 RJ45 Ethernet Socket, 18-pins, RA, Female
J5 USB Type C J16 Power Jack
J6 USB Type A Dual Stacked Connector J17 Optional: CAN Bus Header (1x4, 2.54 mm pitch, RA)
J7 USB Type A Dual Stacked Connector J18 Optional: PoE Backpower Header (1x2, 2.54 mm pitch)
J8 DisplayPort Connector J19 Optional: PoE Header (1x4, 2.54 mm pitch)
J12 40-pin Expansion Header (2x20, 2.54 mm pitch) J20 Camera (#0) Connector (22 pos, 0.5 mm pitch)
J13 Fan Header (4-pin, 1.25 mm pitch) J21 Camera (#1) Connector (22 pos, 0.5 mm pitch)
J14 Button Header (1x12, 2.54 mm pitch, RA) DS1 Power LED (Green)

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 5

---

<!-- page-marker:10 -->
Introduction

Figure 1-5. Jetson Orin Nano Carrier Board Placement – Bottom View

![Jetson Orin Nano Carrier Board Placement – Bottom View](image)

M.2, Key E Socket [J10] —————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

---

<!-- page-marker:11 -->
# Chapter 2. Jetson Nano Carrier Board Standard Connectors

The Jetson Orin Nano carrier board provides several connectors with industry standard pinouts to support additional functionality beyond what is integrated on the main platform board. This includes:

- USB 3.2: Type C connector
- USB 3.2: 2 x Type A stacked connectors
- Gigabit Ethernet: RJ45 connector
- DisplayPort connector
- M.2, Key E socket
- M.2, Key M socket (4-lane PCIe)
- M.2, Key M socket (2-lane PCIe)

## 2.1 USB Ports

The carrier board supports five USB connectors. One is a USB 3.2 Type C connector (J5) supporting host, device, and USB Recovery. In addition, there are two, dual stacked USB 3.2 Type A connectors (J6 and J7). Each connector supports host mode only. A load switch supplying VBUS is provided for each of the USB 3.2 ports per stack and is limited to 3A of output current.

### Table 2-1. USB 3.2 Type C Connector Pin Description – J5

| Pin # | Connector Pin Name | Associated Module Pin Name (See Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
|-------|--------------------|----------------------------------------------|--------------|-------------------|----------|
| A1    | GND_A              | –                                            | –            | Ground            | Ground   |
| A2    | TX1_P              | USBSS1_TX_P                                 | G23          | USB 3.2 #1 Transmit 1 from mux | Output   |
| A3    | TX1_N              | USBSS1_TX_N                                 | G22          |                   | Output   |
| A4    | –                  | –                                           | –            | USB VBUS_A Power  | Power    |
| A5    | CC1                | –                                           | –            | CC 1 from CC Controller | Output   |
| A6    | D1_P               | USB0_D_P                                    | F12          | USB 2.0 #0 Data 1  | Bidir    |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 7

---

<!-- page-marker:12 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Connector Pin Name | Associated Module Pin Name (See Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A7 | D1_N | USB0_D_N | F13 |  |  |
| A8 | SBU1 | – | – | Unconnected | – |
| A9 | – | – | – | USB VBUS_A Power | Power |
| A10 | RX2_N | USBSS1_RX_P | C22 | USB 3.2 #1 Receive 2 from mux | Input |
| A11 | RX2_P | USBSS1_RX_N | C23 |  |  |
| A12 | GND_A | – | – | Ground | Ground |
| B1 | GND_B | – | – | Ground | Ground |
| B2 | TX2_P | USBSS1_TX_P | G23 | USB 3.2 #1 Transmit 2 from mux | Output |
| B3 | TX2_N | USBSS1_TX_N | G22 |  |  |
| B4 | – | – | – | USB VBUS_A Power | Power |
| B5 | CC2 | – | – | CC 2 from CC Controller | Output |
| B6 | D2_P | USB0_D_P | F12 |  |  |
| B7 | D2_N | USB0_D_N | F13 | USB 2.0 #0 Data 2 | Bidir |
| B8 | SBU2 | – | – | Unconnected | – |
| B9 | – | – | – | USB VBUS_A Power | Power |
| B10 | RX1_N | USBSS1_RX_P | C22 | USB 3.2 #1 Receive 1 from mux | Input |
| B11 | RX1_P | USBSS1_RX_N | C23 |  |  |
| B12 | GND_B | – | – | Ground | Ground |

Notes:
1. USB 3.2 module pin names are using the Orin NX and Orin Nano function names.
2. The module pins for the USB 3.2 ports are not directly connected to the USB connector pins but are routed through a multiplexer.
3. In the Type/Dir column, Output is to USB connectors. Input is from USB connectors. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

Table 2-2. USB 3.2 Type A Connector Pin Descriptions – J6

| Pin # | Module Pin Name (see Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
| :--- | :--- | :--- | :--- | :--- |
| USB 3.0 Type A (2) |  |  |  |  |
| 1 | – | – | VBUS Supply | Power |
| 2 | USB1_D_N |  | USB 2.0 #2 Data from hub | Bidir |
| 3 | USB1_D_P |  |  |  |
| 4 | – | – | Ground | Ground |
| 5 | USBSS0_RX_N | 161 | USB 3.1 Receive #2 Data from hub | Input |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 8

---

<!-- page-marker:13 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name (see Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
|-------|------------------------------------|--------------|-------------------|----------|
| 6     | USBSSO_RX_P                       | 163          |                   |          |
| 7     | –                                  | –            | Ground            | Ground   |
| 8     | USBSSO_TX_N                       | 166          |                   |          |
| 9     | USBSSO_TX_P                       | 168          | USB 3.1 Transmit #2 Data from hub | Output |
|       | **USB 3.0 Type A (1)**             |              |                   |          |
| 10    | –                                  | –            | VBUS Supply       | Power    |
| 11    | USB1_D_N                          | 115          | USB 2.0 Data #1 Data from hub | Bidir |
| 12    | USB1_D_P                          | 117          |                   |          |
| 13    | –                                  | –            | Ground            | Ground   |
| 14    | USBSSO_RX_N                       | 161          | USB 3.1 Receive #1 Data from hub | Input |
| 15    | USBSSO_RX_P                       | 163          |                   |          |
| 16    | –                                  | –            | Ground            | Ground   |
| 17    | USBSSO_TX_N                       | 166          |                   |          |
| 18    | USBSSO_TX_P                       | 168          | USB 3.1 Transmit #1 Data from hub | Output |

Notes:
1. USB 3.2 module pin names are using the Orin NX and Orin Nano function names.
2. The module pin names not directly connected to the USB connector pins but are routed to the input of the USB hub.
3. In the Type/Dir column, Output is to USB connectors. Input is from USB connectors. Bidir is for bidirectional signals.

Legend
| Ground | Power | Reserved |

Table 2-3. USB 3.2 Type A Connector Pin Description – J7

| Pin # | Module Pin Name (see Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
|-------|------------------------------------|--------------|-------------------|----------|
|       | **USB 3.0 Type A (2)**             |              |                   |          |
| 1     | –                                  | –            | VBUS Supply       | Power    |
| 2     | USB1_D_N                          | 115          | USB 2.0 #4 Data from hub | Bidir |
| 3     | USB1_D_P                          | 117          |                   |          |
| 4     | –                                  | –            | Ground            | Ground   |
| 5     | USBSSO_RX_N                       | 161          | USB 3.1 Receive #4 Data from hub | Input |
| 6     | USBSSO_RX_P                       | 163          |                   |          |
| 7     | –                                  | –            | Ground            | Ground   |
| 8     | USBSSO_TX_N                       | 166          |                   |          |
| 9     | USBSSO_TX_P                       | 168          | USB 3.1 Transmit #4 Data from hub | Output |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 9

---

<!-- page-marker:14 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name (see Note 1 and 2) | Module Pin # | Usage/Description | Type/Dir |
|---|---|---|---|---|
| USB 3.0 Type A (1) | | | | |
| 10 | – | – | VBUS Supply | Power |
| 11 | USB1_D_N | 115 | USB 2.0 Data #3 Data from hub | Bidir |
| 12 | USB1_D_P | 117 | | |
| 13 | – | – | Ground | Ground |
| 14 | USBSSO_RX_N | 161 | USB 3.1 Receive #3 Data from hub | Input |
| 15 | USBSSO_RX_P | 163 | | |
| 16 | – | – | Ground | Ground |
| 17 | USBSSO_TX_N | 166 | | |
| 18 | USBSSO_TX_P | 168 | USB 3.1 Transmit #3 Data from hub | Output |

Notes:
1. USB 3.2 module pin names are using the Orin NX and Orin Nano function names.
2. The module pin names not directly connected to the USB connector pins but are routed to the input of the USB hub.
3. In the Type/Dir column, Output is to USB connectors. Input is from USB connectors. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

2.2 Gigabit Ethernet

The carrier board implements an RJ45 connector (J15) along with the necessary magnetics device.

Table 2-4. Ethernet RJ45 Connector Pin Description – J15

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|---|---|---|---|---|
| 1 | GPE_MDIO_P | 186 | Gigabit Ethernet MDI 0+ | Bidir |
| 2 | GPE_MDIO_N | 184 | Gigabit Ethernet MDI 0– | Bidir |
| 3 | GPE_MD1_P | 192 | Gigabit Ethernet MDI 1+ | Bidir |
| 4 | – | – | MCT | – |
| 5 | – | – | MCT | – |
| 6 | GPE_MD1_N | 190 | Gigabit Ethernet MDI 1– | Bidir |
| 7 | GPE_MD2_P | 198 | Gigabit Ethernet MDI 2+ | Bidir |
| 8 | GPE_MD2_N | 196 | Gigabit Ethernet MDI 2– | Bidir |
| 9 | GPE_MD3_P | 204 | Gigabit Ethernet MDI 3+ | Bidir |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 10

---

<!-- page-marker:15 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|
| 10    | GPE_MDI3_N      | 202          | Gigabit Ethernet MDI 3- | Bidir |
| 11    |                 |              |                   |          |
| 12    |                 |              | Power-Over-Ethernet | Power |
| 13    |                 |              |                   |          |
| 14    |                 |              |                   |          |
| 15    |                 |              | Green LED Anode | Input |
| 16    | GBE_LED_LINK    | 188          | Green LED Cathode. On for 1,000 Mbps link. Off for 10/100Mbps. | Output |
| 17    |                 |              | Yellow LED Anode | Input |
| 18    | GBE_LED_ACT     | 194          | Yellow LED Cathode. On indicates activity. | Output |
| 19    |                 |              | Shield Ground | Ground |
| 20    |                 |              |                   |          |

Note: In the Type/Dir column, Output is to RJ45 connector. Input is from RJ45 connector. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

2.3 DisplayPort

A DisplayPort (DP) connector (J8) is provided. Dual mode is supported.

Table 2-5. DisplayPort Connector Pin Description – J8

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|
| 1     | DPO_TXD0_P      | 41           | DP Lane 0+ | Output |
| 2     |                 |              | Ground | Ground |
| 3     | DPO_TXD0_N      | 39           | DP Lane 0- | Output |
| 4     | DPO_TXD1_P      | 47           | DP Lane 1+ | Output |
| 5     |                 |              | Ground | Ground |
| 6     | DPO_TXD1_N      | 45           | DP Lane 1- | Output |
| 7     | DPO_TXD2_P      | 53           | DP Lane 2+ | Output |
| 8     |                 |              | Ground | Ground |
| 9     | DPO_TXD2_N      | 51           | DP Lane 2- | Output |
| 10    | DPO_TXD3_P      | 59           | DP Lane 3+ | Output |
| 11    |                 |              | Ground | Ground |
| 12    | DPO_TXD3_N      | 57           | DP Lane 3- | Output |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 11

---

<!-- page-marker:16 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|
| 13    | -               | -            | MODE to support Dual-role mode. Connects from DP connector to PI3AUX221ZTAEX device to select between DP or HDMI mode. | Input |
| 14    | -               | -            | CEC_DP: Not used – pulled to GND through 1 Mohm resistor | Unused |
| 15    | DPO_AUX_N       | 90           | DisplayPort Auxiliary Channel 0- | Bidir |
| 16    | -               | -            | Ground | Ground |
| 17    | DPO_AUX_P       | 92           | DisplayPort Auxiliary Channel 0+ | Bidir |
| 18    | DPO_HPD         | 88           | HDMI™ Hot Plug Detect | Input |
| 19    | -               | -            | Power Return (Ground) | Ground |
| 20    | -               | -            | +3.3 V | Power |

Note: In the Type/Dir column, Output is to DP connector. Input is from DP connector. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

2.4 M.2 Key E Expansion Slot

The Jetson Orin Nano carrier board includes a M.2, Key E Slot Mini-PCIe Expansion slot (J10). This includes interface options for WiFi/BT including PCIe (x1), USB 2.0, UART, I2S, and I2C optional.

Notes:
> The Jetson Orin Nano Developer Kit carrier board will only support single sided M.2 Key E modules.
> Stuffing resistors for connecting I2C2 to pins 58 and 60 of the M.2 Key E connector are not installed by default. If I2C is required, 0Ω resistors can be installed at locations R106 and R107. Care should be taken as some M.2 cards can cause conflicts with other devices connected to the I2C interface.

Table 2-6. M.2 Key E Expansion Slot Pin Description – J10

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|-------|-----------------|--------------|-------------------|----------|
| 1     | -               | -            | Ground | Ground | -     | -               | -            | No Pin | - |
| 3     | USB2_D_P        | 123          | USB 2.0 Data | Bidir | 2     | -               | -            | Main 3.3V Supply | Power |
| 5     | USB2_D_N        | 121          | USB 2.0 Data | Bidir | 4     | -               | -            | - | - |
| 7     | -               | -            | Ground | Ground | 6     | -               | -            | Unused | Unused |
| 9     | -               | -            | Unused | Unused | 8     | I2S1_CLK        | 226          | I2S #1 Clock | Bidir, 1.8V |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 12

---

<!-- page-marker:17 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|-------|-----------------|--------------|-------------------|----------|
| 11    |                 |              |                   |          | 10    | I2S1_FS         | 224           | I2S #1 Left/Right Clock | Bidir, 1.8V |
| 13    |                 |              |                   |          | 12    | I2S1_DIN        | 222           | I2S #1 Data In    | Input, 1.8V |
| 15    |                 |              |                   |          | 14    | I2S1_DOUT       | 220           | I2S #1 Data Out   | Bidir, 1.8V |
| 17    |                 |              |                   |          | 16    | -               | -             | Unused            | Unused   |
| 19    |                 |              |                   |          | 18    | -               | -             | Ground            | Ground   |
| 21    |                 |              |                   |          | 20    | GPIO02          | 124           | Bluetooth #2 Wake AP | Input, 3.3V |
| 23    |                 |              |                   |          | 22    | UART0_RXD       | 101           | UART #0 Receive   | Input, 1.8V |
| 25    |                 |              |                   |          | 24    |                 |               |                   |          |
| 27    |                 |              |                   |          | 26    |                 |               |                   |          |
| 29    | -               | -            | Key               | Unused   | 28    | -               | -             | Key               | Unused   |
| 31    |                 |              |                   |          | 30    |                 |               |                   |          |
| 33    | -               | -            | Ground            | Ground   | 32    | UART0_TXD       | 99            | UART #0 Transmit  | Output, 1.8V |
| 35    | PEX1_TXO_P      | 174          | PCIe #1 Transmit Lane 0 | Output | 34    | UART0_CTS*      | 105           | UART #0 Clear to Send | Input, 1.8V |
| 37    | PEX1_TXO_N      | 172          |                   |          | 36    | UART0_RTS*      | 103           | UART #0 Request to Send | Output, 1.8V |
| 39    | -               | -            | Ground            | Ground   | 38    |                 |               |                   |          |
| 41    | PEX1_RXO_P      | 169          | PCIe #1 Receive Lane 0 | Input | 40    |                 |               |                   |          |
| 43    | PEX1_RXO_N      | 167          |                   |          | 42    |                 |               |                   |          |
| 45    | -               | -            | Ground            | Ground   | 44    |                 |               |                   |          |
| 47    | PEX1_CLK_P      | 175          | PCIe #1 Reference clock | Output | 46    |                 |               |                   |          |
| 49    | PEX1_CLK_N      | 173          |                   |          | 48    |                 |               |                   |          |
| 51    | -               | -            | Ground            | Ground   | 50    | CLK_32K_OUT     | 210           | Suspend Clock (32 KHz) | Output, 3.3V |
| 53    | PEX1_CLKRE Q*   | 182          | PCIe #1 Clock Request | Bidir, 3.3V | 52    | PEX0_RST*       | 183           | PCIe #0 Reset     | Output, 3.3V |
| 55    | PEX_WAKE*       | 179          | PCIe Wake         | Input, 3.3V | 54    | GPIO3           | 126           | BT Enable         | Output, 3.3V |
| 57    | -               | -            | Ground            | Ground   | 56    | GPIO5           | 128           | Wi-Fi Disable     | Output, 3.3V |
| 59    | -               | -            | Unused            | Unused   | 58    | I2C2_SDA        | 234           | General I2C #2    | Bidir/OD, 1.8V |
| 61    |                 |              |                   |          | 60    | I2C2_SCL        | 232           | (optional)        |          |
| 63    | -               | -            | Ground            | Ground   | 62    | GPIO10          | 212           | M.2, Key E Connector Alert | Input, 1.8V |

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 13

---

<!-- page-marker:18 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|-------|-----------------|--------------|-------------------|----------|
| 65    | -               | -            | Unused            | Unused   | 64    | -               | -            | Unused            | Unused   |
| 67    | -               | -            | Ground            | Ground   | 66    | -               | -            | Unused            | Unused   |
| 69    | -               | -            | Ground            | Ground   | 68    | -               | -            | Unused            | Unused   |
| 71    | -               | -            | Unused            | Unused   | 70    | -               | -            | Unused            | Unused   |
| 73    | -               | -            | Unused            | Unused   | 72    | -               | -            | Main 3.3V Supply  | Power    |
| 75    | -               | -            | Ground            | Ground   | 74    | -               | -            | Main 3.3V Supply  | Power    |

Note: In the Type/Dir column, Output is to M.2 module. Input is from M.2 module. Bidir is for bidirectional signals.

Legend
| Ground | Power | Reserved |

## 2.5 M.2 Key M Expansion Slot

The carrier board includes two M.2, Key M Slots for NVMe storage (J11 and J24). The M.2, Key M slot J11 supports PCIe (x4), Gen4. The M.2, Key M slot J24 supports PCIe (x2), Gen4.

Notes:
> Jetson Orin Nano modules supports only up to Gen3 PCIe, and Jetson Orin NX modules support up to Gen4 PCIe
> The Jetson Orin Nano Developer Kit carrier board will only support single sided M.2 Key M modules.

Table 2-7. M.2 Key M Expansion Slot Pin Description – J11 (x4 PCIe)

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|-------|-----------------|--------------|-------------------|------------------|
| 1     | -               | -            | Ground            | Ground           | 2     | -               | -            | Main 3.3V Supply  | Power            |
| 3     | -               | -            | Ground            | Ground           | 4     | -               | -            | Main 3.3V Supply  | Power            |
| 5     | PCIe0_RX3_N     | 155          | PCIe IF #0 Lane 3 Receive | Input           | 6     | -               | -            | Unused            | Unused           |
| 7     | PCIe0_RX3_P     | 157          | Receive           | Input            | 8     | -               | -            | Unused            | Unused           |
| 9     | -               | -            | Ground            | Ground           | 10    | -               | -            | Unused            | Unused           |
| 11    | PCIe0_TX3_N     | 154          | PCIe IF #0 Lane 3 Transmit | Output         | 12    | -               | -            | Main 3.3V Supply  | Power            |
| 13    | PCIe0_TX3_P     | 156          | Transmit          | Output           | 14    | -               | -            | Main 3.3V Supply  | Power            |
| 15    | -               | -            | Ground            | Ground           | 16    | -               | -            | Main 3.3V Supply  | Power            |
| 17    | PCIe0_RX2_N     | 149          | PCIe IF #0 Lane 2 Receive | Input           | 18    | -               | -            | Unused            | Unused           |
| 19    | PCIe0_RX2_P     | 151          | Receive           | Input            | 20    | -               | -            | Unused            | Unused           |

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 14

---

<!-- page-marker:19 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|-------|-----------------|--------------|-------------------|------------------|
| 21    | –               | –            | Ground            | Ground           | 22    | –               | –            | –                 | –                |
| 23    | PCIE0_TX2_N     | 148          | PCIe IF #0 Lane 2 Transmit | Output       | 24    | –               | –            | –                 | –                |
| 25    | PCIE0_TX2_P     | 150          | Transmit          | Output           | 26    | –               | –            | –                 | –                |
| 27    | –               | –            | Ground            | Ground           | 28    | –               | –            | –                 | –                |
| 29    | PCIE0_RX1_N     | 137          | PCIe IF #0 Lane 1 Receive | Input        | 30    | –               | –            | –                 | –                |
| 31    | PCIE0_RX1_P     | 139          | Receive           | Input            | 32    | –               | –            | –                 | –                |
| 33    | –               | –            | Ground            | Ground           | 34    | –               | –            | –                 | –                |
| 35    | PCIE0_TX1_N     | 140          | PCIe IF #0 Lane 1 Transmit | Output       | 36    | –               | –            | –                 | –                |
| 37    | PCIE0_TX1_P     | 142          | Transmit          | Output           | 38    | –               | –            | –                 | –                |
| 39    | –               | –            | Ground            | Ground           | 40    | –               | –            | Unused            | Unused           |
| 41    | PCIE0_RX0_N     | 131          | PCIe IF #0 Lane 0 Receive | Input        | 42    | –               | –            | –                 | –                |
| 43    | PCIE0_RX0_P     | 133          | Receive           | Input            | 44    | GPIO10          | 212          | M.2 Key M Alert   | Input, 1.8V      |
| 45    | –               | –            | Ground            | Ground           | 46    | –               | –            | Unused            | Unused           |
| 47    | PCIE0_TX0_N     | 134          | PCIe IF #0 Lane 0 Transmit | Output       | 48    | –               | –            | –                 | –                |
| 49    | PCIE0_TX0_P     | 136          | Transmit          | Output           | 50    | PEX0_RST*       | 181          | PCIe IF #0 Reset  | Output, 3.3V     |
| 51    | –               | –            | Ground            | Ground           | 52    | PEX0_CLKREQ*    | 180          | PCIe IF #0 Clock Request | Input, 3.3V     |
| 53    | PCIE0_CLK_N     | 160          | PCIe IF #0 Reference Clock | Output       | 54    | PEX_WAKE*       | 179          | PCIe Wake (Level Shifted from 3.3V to 1.8V) | Input, 3.3V     |
| 55    | PCIE0_CLK_P     | 162          | Clock             | Output           | 56    | –               | –            | Unused            | Unused           |
| 57    | –               | –            | Ground            | Ground           | 58    | –               | –            | –                 | –                |
| 59    | –               | –            | Unused (Key)      | Unused           | 60    | –               | –            | –                 | –                |
| 61    | –               | –            | Unused (Key)      | Unused           | 62    | –               | –            | –                 | –                |
| 63    | –               | –            | –                 | –                | 64    | –               | –            | –                 | –                |
| 65    | –               | –            | –                 | –                | 66    | –               | –            | –                 | –                |
| 67    | –               | –            | Unused            | Unused           | 68    | –               | –            | 32 KHz Suspend Clock | Output, 3.3V     |
| 69    | –               | –            | –                 | –                | 70    | –               | –            | –                 | –                |
| 71    | –               | –            | –                 | –                | 72    | –               | –            | Main 3.3V Supply  | Power            |
| 73    | –               | –            | Ground            | Ground           | 74    | –               | –            | –                 | –                |
| 75    | –               | –            | No Pin            | –                | –     | –               | –            | –                 | –                |

Note: In the Type/Dir column, Output is to M.2 module. Input is from M.2 Module. Bidir is for bidirectional signals.

Legend
| Ground | Power | Reserved |

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 15

---

<!-- page-marker:20 -->
Jetson Nano Carrier Board Standard Connectors

Table 2-8. M.2 Key M Expansion Slot Pin Description – J24 (x2 PCIe)

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|-------|-----------------|--------------|-------------------|------------------|
| 1     |                 |              | Ground            | Ground           | 2     |                 |              | Main 3.3V Supply   | Power            |
| 3     |                 |              | Ground            | Ground           | 4     |                 |              | Main 3.3V Supply   | Power            |
| 5     |                 |              | Unused            | Unused           | 6     |                 |              | Unused            | Unused           |
| 7     |                 |              | Unused            | Unused           | 8     |                 |              | Unused            | Unused           |
| 9     |                 |              | Ground            | Ground           | 10    |                 |              | Unused            | Unused           |
| 11    |                 |              | Unused            | Unused           | 12    |                 |              | Main 3.3V Supply   | Power            |
| 13    |                 |              | Ground            | Ground           | 14    |                 |              | Main 3.3V Supply   | Power            |
| 15    |                 |              | Ground            | Ground           | 16    |                 |              | Unused            | Unused           |
| 17    |                 |              | Unused            | Unused           | 18    |                 |              | Unused            | Unused           |
| 19    |                 |              | Ground            | Ground           | 20    |                 |              | Unused            | Unused           |
| 21    |                 |              | Ground            | Ground           | 22    |                 |              | Unused            | Unused           |
| 23    |                 |              | Unused            | Unused           | 24    |                 |              | Unused            | Unused           |
| 25    |                 |              | Ground            | Ground           | 26    |                 |              | Unused            | Unused           |
| 27    |                 |              | Ground            | Ground           | 28    |                 |              | Unused            | Unused           |
| 29    | PCIe2_RX1_N     | 58           | PCIe IF #2 Lane 1 | Input            | 30    |                 |              | Unused            | Unused           |
| 31    | PCIe2_RX1_P     | 60           | Receive           | Input            | 32    |                 |              | Unused            | Unused           |
| 33    |                 |              | Ground            | Ground           | 34    |                 |              | Unused            | Unused           |
| 35    | PCIe2_TX1_N     | 64           | PCIe IF #2 Lane 1 | Output           | 36    |                 |              | Unused            | Unused           |
| 37    | PCIe2_TX1_P     | 66           | Transmit          | Output           | 38    |                 |              | Unused            | Unused           |
| 39    |                 |              | Ground            | Ground           | 40    |                 |              | Unused            | Unused           |
| 41    | PCIe2_RX0_N     | 40           | PCIe IF #2 Lane 0 | Input            | 42    |                 |              | Unused            | Unused           |
| 43    | PCIe2_RX0_P     | 42           | Receive           | Input            | 44    | GPIO10           | 212           | M.2 Key M Alert    | Input, 1.8V      |
| 45    |                 |              | Ground            | Ground           | 46    |                 |              | Unused            | Unused           |
| 47    | PCIe2_TX0_N     | 46           | PCIe IF #2 Lane 0 | Output           | 48    |                 |              | Unused            | Unused           |
| 49    | PCIe2_TX0_P     | 48           | Transmit          | Output           | 50    | PEX2_RST*        | 219           | PCIe IF #0 Reset   | Output, 3.3V     |
| 51    |                 |              | Ground            | Ground           | 52    | PEX2_CLKREQ*     | 221           | PCIe IF #0 Clock Request | Input, 3.3V     |
| 53    | PCIe2_CLK_N     | 52           | PCIe IF #2 Reference Clock | Output | 54    | PEX_WAKE*        | 179           | PCIe Wake (Level Shifted from 3.3V to 1.8V) | Input, 3.3V     |
| 55    | PCIe2_CLK_P     | 54           |                   |                   | 56    |                 |              | Unused            | Unused           |
| 57    |                 |              | Ground            | Ground           | 58    |                 |              | Unused (Key)      | Unused           |
| 59    |                 |              | Unused (Key)      | Unused           | 60    |                 |              | Unused (Key)      | Unused           |

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 16

---

<!-- page-marker:21 -->
Jetson Nano Carrier Board Standard Connectors

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default | Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|-------|-----------------|--------------|-------------------|------------------|
| 61    |                 |              |                   |                  | 62    |                 |              |                   |                  |
| 63    |                 |              |                   |                  | 64    |                 |              |                   |                  |
| 65    |                 |              |                   |                  | 66    |                 |              |                   |                  |
| 67    | -               | -            | Unused            | Unused           | 68    | -               | -            | 32 KHz Suspend Clock | Output, 3.3V     |
| 69    |                 |              |                   |                  | 70    |                 |              |                   |                  |
| 71    |                 |              |                   |                  | 72    | -               | -            | Main 3.3V Supply   | Power            |
| 73    | -               | -            | Ground            | Ground           | 74    |                 |              |                   |                  |
| 75    |                 |              |                   |                  | 76    | -               | -            | -No Pin            | -                |

Notes:
1. PCIe 2 module pin names are using the Orin NX and Orin Nano function names.
2. In the Type/Dir column, Output is to M.2 module. Input is from M.2 Module. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 17

---

<!-- page-marker:22 -->
# Chapter 3. Carrier Board Custom Expansion IF Connections

The Jetson Orin Nano carrier board supports several expansion headers and connectors that have custom pinouts. The following lists the headers and connectors that have custom pinouts.

- Jetson Orin Nano Module Connector, 260-pin, SO-DIMM, 1.27 mm pitch
- Camera Connectors (x2), 22 position, Flex Connector, 0.5 mm pitch
- 40-Pin Expansion Header, 2x20, 2.54 mm pitch
- Button Header, 2x4, 2.54 mm pitch
- Optional CAN Bus header
- Fan Connector, 4-pin, 1.25 mm pitch
- Optional real-time-clock (RTC) back-up connector
- DC Power Jack
- Optional Power-over Ethernet (PoE) header, 1x4, 2.54 mm pitch
- Optional PoE backpower header, 1x, 2.54 mm pitch

## 3.1 Jetson Orin Nano Module Connector

The carrier board interfaces to the Jetson Orin Nano module using a 260-pin SODIMM connector (J2). The carrier board has a TE Connectivity 2309413-1 connector. This interfaces with the Jetson Orin Nano edge fingers. The connector pinout can be found in the Jetson Orin Nano Product Design Guide.

## 3.2 Camera Connector

The Jetson Orin Nano carrier board includes two 22-position flex (0.5 mm pitch) camera connectors (J20 and J219). The connector used on the carrier board is a Molex Japan Part #54548-2272.

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 18

---

<!-- page-marker:23 -->
Carrier Board Custom Expansion IF Connections

The connectors support the following.
> J20: CSI 1 x2 lane
> J21: CSI 1 x2 lane or 1 x4 lane
> Both J20/J21: C
- CAM_I2C, clock, and control GPIOs for the camera
- 3.3V Supply

Table 3-1. Camera #0 Connector Pin Description – J20

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|
| 1 | – | – | +3.3V | Power |
| 2 | CAM_I2C_SDA | 215 | Camera I2C. 2.2 kΩ pull-ups on module. The module CAM_I2C pins connect to an I2C mux. The camera connector #0 (J20) receives the I2C from the mux (first output). The I2C signals on the camera side of the mux have 1 kΩ pull-ups. | Bidir, 3.3V |
| 3 | CAM_I2C_SCL | 213 |  | Output, 3.3V |
| 4 | – | – | Ground | Ground |
| 5 | CAM0_MCLK | 116 | Camera #0 Primary Clock | Output, 1.8V |
| 6 | CAM0_PWDN | 114 | Camera #0 Power-down | Output, 1.8V |
| 7 | – | – | Ground | Ground |
| 8 | CSI0_D1_P | 18 | CSI 0 Data 1 | Input |
| 9 | CSI0_D1_N | 16 |  |  |
| 10 | – | – | Ground | Ground |
| 11 | CSI0_DO_P | 6 | CSI 0 Data 0 | Input |
| 12 | CSI0_DO_N | 4 |  |  |
| 13 | – | – | Ground | Ground |
| 14 | CSI1_CLK_P | 11 | CSI 0 Clock | Input |
| 15 | CSI1_CLK_N | 9 |  |  |
| 16 | – | – | Ground | Ground |
| 17 | CSI1_D1_P | 17 | CSI 1 Data 1 | Input |
| 18 | CSI1_D1_N | 15 |  |  |
| 19 | – | – | Ground | Ground |
| 20 | CSI1_DO_P | 5 | CSI 1 Data 0 | Input |
| 21 | CSI1_DO_N | 3 |  |  |
| 22 | – | – | Ground | Ground |

Note: In the Type/Dir column, Output is to camera module. Input is from camera module. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 19

---

<!-- page-marker:24 -->
Carrier Board Custom Expansion IF Connections

Table 3-2. Camera #1 Connector Pin Description – J21

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
|-------|-----------------|--------------|-------------------|----------|
| 1 | – | – | +3.3V | Power |
| 2 | CAM_I2C_SDA | 215 | Camera I2C. 2.2 kΩ pull-ups on module. The module CAM_I2C pins connect to an I2C mux. The camera connector #1 (J21) receives the I2C from the mux (second output). The I2C signals on the camera side of the mux have 1 kΩ pull-ups. | Bidir, 3.3V |
| 3 | CAM_I2C_SCL | 213 |  | Output, 3.3V |
| 4 | – | – | Ground | Ground |
| 5 | CAM1_MCLK | 122 | Camera #0 Primary Clock | Output, 1.8V |
| 6 | CAM1_PWDN | 120 | Camera #0 Power-down | Output, 1.8V |
| 7 | – | – | Ground | Ground |
| 8 | CSI3_D1_P | 35 | CSI 3 Data 1 | Input |
| 9 | CSI3_D1_N | 33 |  | Input |
| 10 | – | – | Ground | Ground |
| 11 | CSI3_DO_P | 23 | CSI 3 Data 0 | Input |
| 12 | CSI3_DO_N | 21 |  | Input |
| 13 | – | – | Ground | Ground |
| 14 | CSI2_CLK_P | 30 | CSI 2 Clock | Input |
| 15 | CSI2_CLK_N | 28 |  | Input |
| 16 | – | – | Ground | Ground |
| 17 | CSI2_D1_P | 36 | CSI 2 Data 1 | Input |
| 18 | CSI2_D1_N | 34 |  | Input |
| 19 | – | – | Ground | Ground |
| 20 | CSI2_DO_P | 24 | CSI 2 Data 0 | Input |
| 21 | CSI2_DO_N | 22 |  | Input |
| 22 | – | – | Ground | Ground |

Note: In the Type/Dir column, Output is to camera module. Input is from camera module. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 20

---

<!-- page-marker:25 -->
Carrier Board Custom Expansion IF Connections

## 3.3 40-Pin Expansion Header

The Jetson Orin Nano carrier board includes a 40-pin (2x20, 2.54 mm pitch) expansion header (J12). The connector used on the carrier board is an Astron Technology (Part # 27-0169H-220-1G-H).

The expansion connector includes various audio and control interfaces including:

- I2S
- Audio (AU) clock
- I2C (x2)
- SPI (x2)
- UART
- GPIOs (x3 – See notes)

> Notes:
> - All the signals on the expansion header use 3.3V levels.
> - All the interface signal pins (I2S, I2C, SPI, UART, and AU clock) can also be configured as GPIOs.
> - Any pull-up or pull-down resistors on the signals (except I2C) must be weak (limited to >50 kΩ).

Figure 3-1. Expansion Header Connections

| Pin | Signal | Pin | Signal |
|-----|--------|-----|--------|
| 1 | 3.3V | 2 | 5.0V |
| 3 | I2C1_SDA | 4 | 5.0V |
| 5 | I2C1_SCL | 6 | GND |
| 7 | GPIO09 | 8 | UART1_TXD |
| 9 | GND | 10 | UART1_RXD |
| 11 | UART1_RTS* | 12 | I2S0_SCLK |
| 13 | SPI1_SCK | 14 | GND |
| 15 | GPIO12 | 16 | SPI1_CS1* |
| 17 | 3.3V | 18 | SPI1_CS0* |
| 19 | SPI0_MOSI | 20 | GND |
| 21 | SPI0_MISO | 22 | SPI0_MISO |
| 23 | SPI0_SCK | 24 | SPI0_CS0* |
| 25 | GND | 26 | SPI0_CS1* |
| 27 | I2C0_SDA | 28 | I2C0_SCL |
| 29 | GPIO01 | 30 | GND |
| 31 | GPIO11 | 32 | GPIO07 |
| 33 | GPIO13 | 34 | GND |
| 35 | I2S0_FS | 36 | UART1_CTS* |
| 37 | SPI1_MOSI | 38 | I2S0_DIN |
| 39 | GND | 40 | I2S0_DOUT |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 21

---

<!-- page-marker:26 -->
Carrier Board Custom Expansion IF Connections

Table 3-3. Expansion Header Pin Description – J12

| Header Pin # | Module Pin Name | Module Pin # | SoC Pin Name | Default Usage / Description | Alternate Functionality | Type/ Dir | Pin Drive or Power Pin Max Current | SoC GPIO Port # | Power-on Default | PU/PD on Default Module | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | – | – | – | Main 3.3V Supply | – | Power (input) | 1A | – | – | – | 1 |
| 2 | – | – | – | Main 5.0V Supply | – | Power (input/output) | 1A | – | – | – | 1 |
| 3 | I2C1_SDA | 191 | GP16_I2C8_DAT | I2C #1 Data | – | Bidir OD | ±2 mA | PDD.02 | z | 2.2KΩ PU | 2 |
| 4 | – | – | – | Main 5.0V Supply | – | Power | 1A | – | – | – | – |
| 5 | I2C1_SCL | 189 | GP15_I2C8_CLK | I2C #1 Clock | – | Bidir OD | ±2 mA | PDD.01 | z | 2.2KΩ PU | 2 |
| 6 | – | – | – | Ground | – | Ground | – | – | – | – | – |
| 7 | GPIO09 | 211 | GP167 | GPIO | Audio Primary Clock | Bidir/Output | ±20uA | PAC.06 | pd | – | 3 |
| 8 | UART1_TXD | 203 | GP70_UART1_T XD_BOOT2_STR AP | UART #1 Transmit | GPIO | Output/Bidir | ±20uA | PR.02 | pd | – | 3 |
| 9 | – | – | – | Ground | – | Ground | – | – | – | – | – |
| 10 | UART1_RXD | 205 | GP71_UART1_R XD | UART #1 Receive | GPIO | Input/Bidir | ±20uA | PR.03 | pd | – | 3 |
| 11 | UART1_RTS* | 207 | GP72_UART1_ RTS_N | GPIO | UART #2 Request to Send | Bidir/Output | ±20uA | PR.04 | pd | – | 3 |
| 12 | I2S0_SCLK | 199 | GP122 | GPIO | Audio I2S #0 Clock | Bidir | ±20uA | PH.07 | pd | – | 3 |
| 13 | SPI1_SCK | 106 | GP36_SPI1_CLK | GPIO | SPI #1 Shift Clock | Bidir/Output | ±20uA | PY.00 | pd | – | 3 |
| 14 | – | – | – | Ground | – | Ground | – | – | – | – | – |
| 15 | GPIO12 | 218 | GP88_PWM1 | GPIO | – | Bidir | ±20uA | PN.01 | z | – | 3 |
| 16 | SPI1_CS1* | 112 | GP40_SPI3_CS1 _N | GPIO | SPI #1 Chip Select #1 | Bidir/Output | ±20uA | PY.04 | z | – | 3 |
| 17 | – | – | – | Main 3.3V Supply | – | Power | 1A | – | – | – | 1 |
| 18 | SPI1_CS0* | 110 | GP39_SPI3_CS0 _N | GPIO | SPI #0 Chip Select #0 | Bidir/Output | ±20uA | PZ.06 | z | – | 3 |
| 19 | SPI0_MOSI | 89 | GP49_SPI1_MO SI | GPIO | SPI #0 Primary Out/Secondary In | Bidir/Output | ±20uA | PZ.05 | pd | – | 3 |
| 20 | – | – | – | Ground | – | Ground | – | – | – | – | – |
| 21 | SPI0_MISO | 93 | GP48_SPI1_MIS O | GPIO | SPI #0 Primary In/Secondary Out | Bidir/Input | ±20uA | PZ.04 | pd | – | 3 |
| 22 | SPI1_MISO | 108 | GP37_SPI3_MIS O | GPIO | SPI #1 Primary In/Secondary Out | Bidir/Input | ±20uA | PY.01 | pd | – | 3 |
| 23 | SPI0_SCK | 91 | GP47_SPI1_CLK | GPIO | SPI #0 Shift Clock | Bidir/Output | ±20uA | PZ.03 | pd | – | 3 |
| 24 | SPI0_CS0* | 95 | GP50_SPI1_CS0 _N | GPIO | SPI #0 Chip Select #0 | Bidir/Output | ±20uA | PZ.06 | z | – | 3 |

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 22

---

<!-- page-marker:27 -->
Carrier Board Custom Expansion IF Connections

| Header Pin # | Module Pin Name | Module Pin # | SoC Pin Name | Default Usage / Description | Alternate Functionality | Type / Dir | Pin Drive or Power Pin Max Current | SoC GPIO Port # | Power-on Default | PU/PD on Default Module | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | - | - | - | Ground | - | Ground | - | - | - | - | - |
| 26 | SPI0_CS1* | 97 | GP51_SPI1_CS1_N | GPIO | SPI #0 Chip Select #1 | Bidir/Output | ±20uA | PZ.07 | pu | 3 |
| 27 | I2C0_SDA | 187 | GP14_I2C2_DAT | I2C #0 Data | GPIO | Bidir OD/Bidir | ±2 mA | PDD.00 | z | 1.5KΩ PU | 2 |
| 28 | I2C0_SCL | 185 | GP13_I2C2_CLK | I2C #0 Clock | GPIO | Bidir OD/Bidir | ±2 mA | PCC.07 | z | 1.5KΩ PU | 2 |
| 29 | GPIO01 | 118 | GP65 | GPIO | General Purpose Clock #0 | Bidir/Output | ±20uA | PQ.05 | pd | 3 |
| 30 | - | - | - | Ground | - | Ground | - | - | - | - | - |
| 31 | GPIO11 | 216 | GP66 | GPIO | General Purpose Clock #1 | Bidir/Output | ±20uA | PQ.06 | pd | 3 |
| 32 | GPIO07 | 206 | GP113_PWM7 | GPIO | PWM | Bidir/Output | ±20uA | PG.06 | z | 3 |
| 33 | GPIO13 | 228 | GP115 | GPIO | PWM | Bidir/Output | ±20uA | PH.00 | z | 3 |
| 34 | - | - | - | Ground | - | Ground | - | - | - | - | - |
| 35 | I2S0_FS | 197 | GP125 | GPIO | Audio I2S #0 Field Select | Bidir | ±20uA | PI.02 | pd | 3 |
| 36 | UART1_CTS* | 209 | GP73_UART1_CTS_N | GPIO | UART #1 Clear to Send | Bidir/Input | ±20uA | PR.05 | pd | 3 |
| 37 | SPI1_MOSI | 104 | GP38_SPI3_MO SI | GPIO | SPI #1 Primary Out/Secondary In | Bidir/Output | ±20uA | PY.02 | pd | 3 |
| 38 | I2S0_DIN | 195 | GP124 | GPIO | Audio I2S #0 Data in | Bidir/Input | ±20uA | PI.01 | pd | 3 |
| 39 | - | - | - | Ground | - | Ground | - | - | - | - | - |
| 40 | I2S0_DOUT | 193 | GP123 | GPIO | Audio I2S #0 Data Out | Bidir/Output | ±20uA | PI.00 | pd | 3 |

Notes:
1. This is current capability per power pin.
2. These pins are connected to the SoC directly. They are open-drain (either pulled up or driven low by the SoC when configured as outputs). The max drive that meets the data sheet VOL is ±2 mA.
3. These pins connect to TI TXB0108 level translators. Due to the design of these devices, the output drivers are very weak, so they can be overdriven by another connected device output for bidirectional support.
4. In the Type/Dir column, output is to expansion header. Input is from expansion header. Bidir is for bidirectional signals. Where two directions are shown, the first is for the primary function (mostly GPIOs) and the second is for the alternate function.
5. Where the signal direction is input or output in this table (Table 3-3), this matches the typical special function usage (for example, SPI, I2S, and so on). The direction is bidirectional if these are configured as GPIOs.
6. All signals on the 40-pin header are 3.3V levels.

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification
SP-11324-001_v1.3 | 23

---

<!-- page-marker:28 -->
Carrier Board Custom Expansion IF Connections

3.4 Button Header

The Jetson Orin Nano carrier board brings several system signals (power, reset, and force recovery), UART, and Sleep/Wake LED-related signals to a pair of standard 0.254 mm pitch header. The button header is J14.

Table 3-4. Button Header Description – J14

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
| :--- | :--- | :--- | :--- | :--- |
| 1 | – | – | PC_LED-: Connects to LED Cathode to indicate System Sleep/Wake (Off when system in sleep mode) | Input, 5V |
| 2 | – | – | PC_LED+: Connects to LED Anode (see Pin 1) | Output |
| 3 | UART2_RXD (DEBUG) | 238 | UART #2 Receive | Input, 3.3V |
| 4 | UART2_TXD (DEBUG) | 236 | UART #2 Transmit | Output, 3.3V |
| 5 | – | – | AC OK: Connect pins 5 and 6 to disable Auto-Power-On and require power button press. | Input, 3.3V |
| 6 | – | – | Auto Power-on disable: Pulled to GND. See Pin 5. | Not applicable |
| 7 | – | – | Ground | Ground |
| 8 | SYS_RESET* | 239 | Temporarily connect pins 7 and 8 to reset system | Input, 1.8V |
| 9 | – | – | Ground | Ground |
| 10 | FORCE_RECOVERY* | 214 | Connect pins 9 and 10 during power-on to put system in USB Force Recovery mode. | Input, 1.8V |
| 11 | – | – | Ground | Ground |
| 12 | SLEEP/WAKE* | 240 | Connect pins 11 and 12 to initiate power-on if Auto-Power-On disabled (Pins 5 and 6 connected). | Input, 5V |

Note: In the Type/Dir column, Output is to button header. Input is from button header. Bidir is for bidirectional signals.

Legend
Ground | Power | Reserved

---

<!-- page-marker:29 -->
Carrier Board Custom Expansion IF Connections

3.5 Optional CAN Bus Header

The Jetson Orin Nano carrier board includes the footprint for a 4-pin, 2.54 mm pitch header (J17) which supports a CAN bus interface.

Table 3-5. Optional CAN Header Pin Description – J17

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|
| 1     | CAN_TX          | 145          | CAN Bus transmit  | Output, 3.3V     |
| 2     | CAN_RX          | 143          | CAN Bus receive   | Input, 3.3V      |
| 3     | -               | -            | Ground            | Ground           |
| 4     | -               | -            | Main 3.3V Supply  | Power            |

Note: In the Type/Dir column, Output is to CAN connector. Input is from CAN connector. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

3.6 Fan Connector

The Jetson Orin Nano carrier board includes a 4-pin fan header (J13). The connector used is a Singatron Enterprise Co., Ltd., Part # 2WBA2542WVC-F-04PNLBT1N00G.

Table 3-6. Fan Connector Pin Description – J13

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
|-------|-----------------|--------------|-------------------|------------------|
| 1     | -               | -            | Ground            | Ground           |
| 2     | -               | -            | Main 5.0V Supply  | Power            |
| 3     | GPIO08          | 208          | Fan Tachometer signal | Input, 5V      |
| 4     | GPIO14          | 230          | Fan Pulse Width Modulation signal | Output, 5V |

Note: In the Type/Dir column, Output is to fan connector. Input is from fan connector. Bidir is for bidirectional signals.

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 25

---

<!-- page-marker:30 -->
Carrier Board Custom Expansion IF Connections

3.7 Optional Battery Back-up Coin Cell Holder

The Jetson carrier board has a connector where an RTC backup battery can be connected. This connector (J3) is commonly used on laptop designs. The connector used is a Wieson Technologies AC2651-0011-003-HH, 2-pin, 1.25 mm pitch connector.

Table 3-7. RTC Backup Batter Connector Pin Description – J3

| Pin # | Associated Module Pin Name | Module Pin # | Usage/Description | Type/Dir |
| :--- | :--- | :--- | :--- | :--- |
| 1 | PM IC_BBAT | 235 | RTC backup battery supply | Power |
| 2 | - | - | Ground | Ground |

Legend
Ground Power Reserved

3.8 DC Power Jack

The Jetson Orin Nano carrier board uses a DC power jack (J16) to bring in the power from the included DC power supply. The jack used on the carrier board is a Singatron Enterprise part (part #: 2DC-0005D206F). The mating barrel jack connector dimensions are:

- Barrel length: 9.5 mm
- Barrel diameter: 5.5 mm
- Pin receptacle: Accepts 2.5 mm jack pin
- The center pin is positive (+V)
- Max current supported is 3.5 A

Figure 3-2. Jack Connector

![Jack Connector](image)

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 26

---

<!-- page-marker:31 -->
Carrier Board Custom Expansion IF Connections

Table 3-8. DC Jack Pin Description – J16

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
| :--- | :--- | :--- | :--- | :--- |
| 1 | – | – | Main DC input supplying DC jack input (9-20 V) | Power |
| 2 | – | – | Ground | Ground |
| 3 | – | – | Ground | Ground |

Legend
Ground Power Reserved

3.9 Optional Power-Over Ethernet and Backpower Headers

The Jetson Orin Nano carrier board provides an option for an alternate main power input (besides the DC power jack). A 4-pin Power over Ethernet (PoE) header (J19 – 1x4 male, 2.54 mm pitch) brings out the VC power pins of the Ethernet connector. In addition, a 2-pin Backpower header (J18 – 1x2 male, 2.54 mm pitch) provides an alternate path for the input voltage (3 A max). To use this alternate PoE power mechanism, the design will require a power converter to take the high-voltage PoE supply (38 V-60 V) and convert it to the 5 V-20 V input the carrier board requires.

Figure 3-3. PoE Alternative Power Input

![PoE Alternative Power Input](image)

Table 3-9. PoE Header – J19

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
| :--- | :--- | :--- | :--- | :--- |
| 1 | – | – | Ethernet RG45 connector PoE VC1 power | Power |
| 2 | – | – | Ethernet RG45 connector PoE VC2 power | Power |
| 3 | – | – | Ethernet RG45 connector PoE VC3 power | Power |
| 4 | – | – | Ethernet RG45 connector PoE VC4 power | Power |

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 27

---

<!-- page-marker:32 -->
Carrier Board Custom Expansion IF Connections

Table 3-10. PoE Backpower Header – J18

| Pin # | Module Pin Name | Module Pin # | Usage/Description | Type/Dir Default |
| :--- | :--- | :--- | :--- | :--- |
| 1 | – | – | Main DC input supplying DC jack input (9 V–20 V). 3 A max. | Power |
| 2 | – | – | Ground | Ground |

Legend
Ground Power Reserved

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 28

---

<!-- page-marker:33 -->
# Chapter 4. Mechanical Specification

Figure 4-1 and Figure 4-2 show the mechanical dimensions for the carrier board and the developer kit.
The Developer Kit Weighs 0.175kg

## Figure 4-1. Developer Kit Carrier Board Mechanical Dimensions

![Developer Kit Carrier Board Mechanical Dimensions](image)

1.57 ± 0.16 mm

100.00 ± 0.13 mm

79.00 ± 0.13 mm

16.70 mm Max

4.30 mm Max

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 29

---

<!-- page-marker:34 -->
Mechanical Specification

Figure 4-2. Developer Kit Mechanical Dimensions

![Developer Kit Mechanical Dimensions](image)

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 30

---

<!-- page-marker:35 -->
# Chapter 5. Interface Power

## Figure 5-1. Power Diagram

**Note:** Jetson Orin Nano DevKit Carrier Board has pull-up on MODULE_ID removed. Only 5V mode (VDD_5V_SYS) supported regardless of module type.

```plaintext
MODULE_ID
- Low selects VDD_5V_SYS
- High selects VDD_HV
```

![Power Diagram](image)

Jetson Orin Nano

USB Type C CC Controller

USB Type C Mux

USB 3.2 Type C

USB HUB

USB 3.2 Type A

USB 3.2 Type A

USB 3.2 Type A

USB 3.2 Type A

Fan

Expansion Connector

DP

M.2 Key E Socket

M.2 Key M Skt #1

M.2 Key M Skt #2

Gbit LAN LEDs

Camera Connector

CAM_I2C Mux

Power Button Ctrl

Power LED

Level Shifters/Misc.

CAN Conn. (opt.)
```

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 31

---

<!-- page-marker:36 -->
Interface Power

The following tables show the allocation of supplies to the connectors on the Jetson
Orin Nano carrier board and current capabilities.

Table 5-1. Interface Power Supply Allocation

| Power Rails | Usage | (V) | Power Supply or Gate | Source | Enable |
| --- | --- | --- | --- | --- | --- |
| DC_IN | Main power input from DC Adapter | 19.5 | AONR21357025 Power mux | DC Adapter |  |
| VDD_5V_SYS | Main 5.0V supply | 5.0 | GS9230NVTQ-R | VDD_CVB (DC_IN after Power FET) | VDD_CVB |
| VDD_3V3_SYS | Main 3.3V supply | 3.3 | GS9230NVTQ-R | VDD_CVB | SYS_RESET_IN* |
| 3V3_AO | Button MCU | 3.3 | GS7116S5-ADJ-R LDO | VDD_5V_SYS | VDD_5V_SYS regulator power good |
| VDD_1V8 | Main 1.8V supply | 1.8 | AP2127K-1.8TRG1 | VDD_3V3_SYS | 3.3V_IO_PG |
| VDD_AV10_HUB | USB hub | 1.1 | GS7303ACTD-R | VDD_5V_SYS | VDD_3V3_SYS regulator power good |
| USBC_VBUS | 5V VBUS for USB Type C connector | 5.0 | AP22811AW5-7 | VDD_5V_SYS | ID from USB Type C CC controller |
| USB_VBUS_A | 5V VBUS for dual stacked 3.0 Type A connector | 5.0 | AP22811AW5-7 Load Switch | VDD_5V_SYS | From USB Hub |
| USB_VBUS_B | 5V VBUS for dual stacked 3.0 Type A connector | 5.0 | AP22811AW5-7 Load Switch | VDD_5V_SYS | From USB Hub |
| VDD_3V3_DP | 3.3V rail for DP connector | 5.0 | GS7612S5MC-R Load Switch | VDD_3V3_SYS | VDD_3V3_SYS regulator power good |

Table 5-2. Interface Supply Current Capabilities

| Power Rails | Usage | (V) | Max Current (A) |
| --- | --- | --- | --- |
| DCJ_IN | Main power input from DC Adapter | 19.0 | 4.2 |
| VDD_5V_SYS | Main 5.0V supply | 5.0 | 7.8 |
| VDD_3V3_SYS | Main 3.3V supply | 3.3 | 5.4 |
| VDD_1V8 | Main 1.8V supply | 1.8 | 0.0002 |
| 3V3_AO | 3.3V Always-on supply | 3.3 | 0.200 |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 32

---

<!-- page-marker:37 -->
Interface Power

Table 5-3. Supply Current Capabilities per Connector per Supply

| Power Rails | Connector | (V) | Max Current (A) |
| --- | --- | --- | --- |
| VDD_5V_SYS | SO-DIMM (VDD_IN) | 5.0 | 5.0 |
|  | 40-pin header |  | 0.5 |
|  | Fan connector |  | 0.15 |
| VDD_3V3_DP | DP connector |  | 0.5 |
| USBC_VBUS | USB Type C |  | 0.5 |
| USB_VBUS_A/B | USB 3.2 type A (x4) |  | 0.5 |
| VDD_3V3_SYS | 40-pin header | 3.3 | 0.1 |
|  | M.2 Key E socket |  | 0.8 |
|  | M.2 Key M sockets (x2) |  | 2.1 |
|  | Camera connectors (x2) |  | 0.26 |

Jetson Orin Nano Developer Kit Carrier Board Specification SP-11324-001_v1.3 | 33

---

<!-- page-marker:38 -->
Notice

This document is provided for information purposes only and shall not be regarded as a warranty of a certain functionality, condition, or quality of a product. NVIDIA Corporation ("NVIDIA") makes no representations or warranties, expressed or implied, as to the accuracy or completeness of the information contained in this document and assumes no responsibility for any errors contained herein. NVIDIA shall have no liability for the consequences or use of such information or for any infringement of patents or other rights of third parties that may result from its use.

This document is not a commitment to develop, release, or deliver any Material (defined below), code, or functionality.

NVIDIA reserves the right to make corrections, modifications, enhancements, improvements, and any other changes to this document, at any time without notice.

Customer should obtain the latest relevant information before placing orders and should verify that such information is current and complete.

NVIDIA products are sold subject to the NVIDIA standard terms and conditions of sale supplied at the time of order acknowledgement, unless otherwise agreed in an individual sales agreement signed by authorized representatives of NVIDIA and customer ("Terms of Sale"). NVIDIA hereby expressly objects to applying any customer general terms and conditions with regards to the purchase of the NVIDIA product referenced in this document. No contractual obligations are formed either directly or indirectly by this document.

Unless specifically agreed in writing by NVIDIA, NVIDIA products are not designed, authorized, or warranted to be suitable for use in medical, military, aircraft, space, or life support equipment, nor in applications where failure or malfunction of the NVIDIA product can reasonably be expected to result in personal injury, death, or property or environmental damage. NVIDIA accepts no liability for inclusion and/or use of NVIDIA products in such equipment or applications and therefore such inclusion and/or use is at customer's own risk.

NVIDIA makes no representation or warranty that products based on this document will be suitable for any specified use. Testing of all parameters of each product is not necessarily performed by NVIDIA. It is customer's sole responsibility to evaluate and determine the applicability of any information contained in this document, ensure the product is suitable and fit for the application planned by customer, and perform the necessary testing for the application in order to avoid a default of the application or the product. Weaknesses in customer's product designs may affect the quality and reliability of the NVIDIA product and may result in additional or different conditions and/or requirements beyond those contained in this document. NVIDIA accepts no liability related to any default, damage, costs, or problem which may be based on or attributable to: (i) the use of the NVIDIA product in any manner that is contrary to this document or (ii) customer product designs.

No license, either expressed or implied, is granted any NVIDIA patent right, copyright, or other NVIDIA intellectual property right under this document. Information published by NVIDIA regarding third-party products or services does not constitute a license from NVIDIA to use such products or services or a warranty or endorsement thereof. Use of such information may require a license from a third party under the patents or other intellectual property rights of the third party, or a license from NVIDIA under the patents or other intellectual property rights of NVIDIA.

Reproduction of information in this document is permissible only if approved in advance by NVIDIA in writing, reproduced without alteration and in full compliance with all applicable export laws and regulations, and accompanied by all associated conditions, limitations, and notices.

THIS DOCUMENT AND ALL NVIDIA DESIGN SPECIFICATIONS, REFERENCE BOARDS, FILES, DRAWINGS, DIAGNOSTICS, LISTS, AND OTHER DOCUMENTS (TOGETHER AND SEPARATELY, "MATERIALS") ARE BEING PROVIDED "AS IS." NVIDIA MAKES NO WARRANTIES, EXPRESSED, IMPLIED, STATUTORY, OR OTHERWISE WITH RESPECT TO THE MATERIALS, AND EXPRESSLY DISCLAIMS ALL IMPLIED WARRANTIES OF NONINFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE. TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL NVIDIA BE LIABLE FOR ANY DAMAGES, INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, ARISING OUT OF ANY USE OF THIS DOCUMENT, EVEN IF NVIDIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES. Notwithstanding any damages that customer might incur for any reason whatsoever, NVIDIA's aggregate and cumulative liability towards customer for the products described herein shall be limited in accordance with the Terms of Sale for the product.

Trademarks

NVIDIA, the NVIDIA logo, Jetson, Jetson Orin Nano, and NVIDIA Orin are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries. Other company and product names may be trademarks of the respective companies with which they are associated.

VESA DisplayPort

DisplayPort and DisplayPort Compliance Logo, DisplayPort Compliance Logo for Dual-mode Sources, and DisplayPort Compliance Logo for Active Cables are trademarks owned by the Video Electronics Standards Association in the United States and other countries.

HDMI

HDMI, the HDMI logo, and High-Definition Multimedia Interface are trademarks or registered trademarks of HDMI Licensing LLC.

Copyright

© 2023 NVIDIA Corporation. All rights reserved.

NVIDIA Corporation | 2788 San Tomas Expressway, Santa Clara, CA 95051
http://www.nvidia.com

![NVIDIA Logo](nvidia_logo.png)