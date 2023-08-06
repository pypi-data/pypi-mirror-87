# Fingerprint-Feature-Extraction-Python
    extracts the minutiae features from fingerprint images.
	Features that are extracted:
	a) Terminations: These are the minutiae end points --> associated feature includes location of the minutiae point(LocX, LocY), and "theta", the angle of the ridge
	b) Bifurcations: These are points where one ridge gets splits into two --> associated feature includes location of the minutiae point(LocX, LocY), and "theta1", "theta2", "theta3", the three angles of the ridges
	

## Quickstart
    This library extracts fingerprint minutiae features which is necessary in biometric recognition systems applications.

## Installation

    To install, run:
    ```
    pip install fingerprint-feature-extractor
    ```

## Usage:
	```Python
	import fingerprint_feature_extractor
	
	img = cv2.imread('image_path', 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
	FeaturesTerminations, FeaturesBifurcations = fingerprint_feature_extractor.extract_minutiae_features(img, showResult=True)
	```
	As easy as that!