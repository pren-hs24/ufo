# UART Protocol Specification

## Overview

This document defines the UART communication protocol for controlling and monitoring the system.

## General Communication

- **Baud Rate**: 115200
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Endianness**: Little Endian
- **Message Format**:
  - Each message starts with a **command/event identifier** (1 byte)
  - Followed by **payload** (if applicable)
  - End with a **checksum** (1 byte, XOR of all previous bytes)

---

## Command List

### 0x01 - Turn

**Description**: Rotate the vehicle by a specified angle.

**Format**:

```
0x01 [angle (int16)] [snap (uint8)] [checksum]
```

- **angle**: Rotation angle in degrees (-180 (left) to 180 (right))
- **snap**: 0 = No snap, 1 = Snap to angle

### 0x02 - Follow Line

**Description**: Start following the detected line.

**Format**:

```
0x02 [checksum]
```

### 0x03 - Destination Reached

**Description**: Notify that the destination has been reached.

**Format**:

```
0x03 [checksum]
```

### 0x04 - Set Debug Logging

**Description**: Enable or disable debug logging.

**Format**:

```
0x04 [enabled (uint8)] [checksum]
```

- **enabled**: 0 = Disable, 1 = Enable

### 0x05 - Set Speed

**Description**: Set the speed of the vehicle.

**Format**:

```
0x05 [speed (int8)] [checksum]
```

- **speed**: Speed value (-100 to 100)

---

## Event List

### 0x10 - Start

**Description**: Indicates the start of the operation towards a target.

**Format**:

```
0x10 [target (uint8)] [checksum]
```

- **target**: 0 = A, 1 = B, 2 = C

### 0x11 - Point Reached

**Description**: The vehicle has reached an intermediate point.

**Format**:

```
0x11 [checksum]
```

### 0x12 - No Line Found

**Description**: The vehicle failed to detect a line.

**Format**:

```
0x12 [checksum]
```

### 0x13 - Next Point Blocked

**Description**: The next point in the path is obstructed.

**Format**:

```
0x13 [checksum]
```

### 0x14 - Obstacle Detected

**Description**: An obstacle was detected along the path.

**Format**:

```
0x14 [checksum]
```

### 0x15 - Aligned

**Description**: The vehicle has completed an alignment operation.

**Format**:

```
0x15 [checksum]
```

### 0x16 - Returning to Previous Position

**Description**: The vehicle is reversing to its previous location.

**Format**:

```
0x16 [checksum]
```

### 0x17 - Log Message

**Description**: Debug or informational log message.

**Format**:

```
0x17 [message (string)] [checksum]
```

---

## Checksum Calculation

The checksum is calculated as the XOR of all preceding bytes in the message, ensuring basic error detection.

---

## Example Messages

### Example 1: Turn 90 Degrees with Snap

```
0x01 0x5A 0x00 0x01 0x5C
```

- `0x5A 0x00` → 90 (Little Endian)
- `0x01` → Snap enabled
- `0x5C` → Checksum

### Example 2: Start Movement to Target B

```
0x10 0x01 0x11
```

- `0x01` → Target B
- `0x11` → Checksum
