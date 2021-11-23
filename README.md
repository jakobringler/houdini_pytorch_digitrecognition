# Houdini + PyTorch Digit Recognition
Simple ML digit recognition in SideFX Houdini using PyTorch and Numpy


### Demo:

![](Houdini_DigitRecognition_PyTorch_v03.gif)

### Dependencies:
- Houdini 19 py3
- Python  3.7.4
- PyTorch 1.10.0 
- Numpy   1.21.3
- Cuda    11.3.1
- cudNN   11.3

### Data:
The digit data gets generated in SOPs within Houdini and doesn't rely on the classical MNIST dataset. There is no real advantage using this approach other than experimenting with procedural data generation and the 'Houdini to PyTorch and back' interface.

### Scripts:
All of the scripts are implemented internally in Houdini's python nodes. The .py files are just for quick code access without having to open Houdini.

### Disclaimer:
There are probably a lot of rookie mistakes and many ways to do things smarter and more efficiently. Keep that in mind when digging into it! =)

### Credits:
[Edmond Boulet-Gilly's video](https://www.youtube.com/watch?v=WNEEokEq-Fg "4 pixel cam AI - Machine Learning in Houdini Tutorial") helped me figure out lots of things!
