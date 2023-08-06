# Color detection with OpenCV

Python module for detecting the color of a OpenCV frame.

## Installation

```bash
> pip install jdla-color-detection
```

## Usage

```python
from color_detection.detect import Mask
import numpy as np
import cv2

# Get dominant color
image = cv2.imread("img/blue.jpg")
color = Mask.detect_dominant(image)
print(color)

# Detect color
my_mask = Mask("Blue", [90, 60, 0], [121, 255, 255])
detected_mask = Mask.detect(color, [my_mask])
print(detected_mask.name)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgments

This module uses [ColorThief](https://github.com/fengsp/color-thief-py) for grabbing the most dominant color of a contour.
