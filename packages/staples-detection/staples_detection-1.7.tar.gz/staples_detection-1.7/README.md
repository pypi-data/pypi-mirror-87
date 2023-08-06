# Staples Detection

The first pure-Python library to detect staples in abdominal surgery images. The theoretical basis of this library 
are the following publications:

```
González-Hidalgo M, Munar M, Bibiloni P, Moyà-Alcover G, Craus-Miguel A & Segura-Sampedro JJ (2019)
Detection of infected wounds in abdominal surgery images using fuzzy logic and fuzzy sets
IEEE International Conference on Wireless and Mobile Computing, Networking And Communications (WiMob).
``` 

```
González-Hidalgo M, Munar M, Bibiloni P, Moyà-Alcover G, Craus-Miguel A & Segura-Sampedro JJ (2019)
Detection and Automatic Deletion of Staples in Images of Wound of Abdominal Surgery for m-Health Applications.
VII ECCOMAS Thematic Conference on Computational Vision and Medical Image Processing. 
``` 

```
Munar M., González-Hidalgo M. & Moyà G.(2020).
Entorno de telemedicina para el seguimiento de complicaciones postquirúrgicas en cirugía abdominal para la 
    realización de un estudio clínico
Master's Thesis – Universitat de les Illes Balears
``` 

## Installation

To install the library, simply run the command:
```
pip install staples-detection
```

To use it, import the library:
```
import staples_detection
```

## Example

To be able to detect staples in the image, the StapleDetector object must be initialized, passing the image to be analyzed as a parameter. The library itself contains a method for loading the two demo images provided.

<p align="center">
  <img src="staples_detection/assets/img001.png" height="200">
</p>

For example, to analyse the image above (which corresponds to the image `img001.png`) just execute the following code:

```
detector = StapleDetector(get_example_asset(number=1))

horizontal_staple_detection_result = detector.detect_staples(StapleDetectionMethod.HORIZONTAL_GRADIENT)
vertical_staple_detection_result = detector.detect_staples(StapleDetectionMethod.VERTICAL_GRADIENT)
combined_staple_detection_result = detector.detect_staples(StapleDetectionMethod.COMBINED_GRADIENT)
canny_staple_detection_result = detector.detect_staples(StapleDetectionMethod.CANNY)
```

The function `detect_staples` returns a `GradientStapleDetectionResult` object, containing the time spent in each method and the partial steps (for example, binarization and morphological dilations).

```
Time spent – Horizontal gradient: 1.17761 s
Time spent – Vertical gradient: 1.10948 s
Time spent – Combined gradient: 2.23928 s
Time spent – Canny: 0.2543 s
```

The results obtained are as follows. Applying horizontal gradient:

<p align="center">
  <img src="staples_detection/assets/results_img001/horizontal_result001.png" height="200">
</p>

Applying vertical gradient:

<p align="center">
  <img src="staples_detection/assets/results_img001/vertical_result001.png" height="200">
</p>

Applying combined gradients:

<p align="center">
  <img src="staples_detection/assets/results_img001/combined_result001.png" height="200">
</p>

Applying modified Canny:

<p align="center">
  <img src="staples_detection/assets/results_img001/canny_result001.png" height="200">
</p>