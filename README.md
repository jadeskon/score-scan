# Score Scan
 
 ## Introduction
Score Scan is a score scanner based on image processing algorithms and convolutional neural networks for optical music recognition.
It processes pdf and png files to create a MusicXML file.

It was a master project of seven students of Hochschule Kempten - University of Applied Sciences in winter semester 2017/18. We published this project in github to inspire other people. Maybe there are people which are interested to work on this project.

## Dependencies

### Integration of ImageMagick in Python

1. Download and run ImageMagick Vers. 6

2. You have to check followed boxes:

   ![Setup - ImageMagick 6.9.9 Q8](https://github.com/jadeskon/score-scan/blob/master/sources/images/readme_md/SelectAdditionalTasks.jpg "Setup - ImageMagick 6.9.9 Q8")

3. Set a new System Environment Variable "MAGICK_HOME". The value have to be the installation directory of ImageMagick-6.9.9-Q8:

   ![System variables](https://github.com/jadeskon/score-scan/blob/master/sources/images/readme_md/EditSystemVariables.jpg "System variables")

4. Download and install ghostscript:
https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs922/gs922w64.exe

5. Now you have to install Wand about pip install:
`pip install Wand`

6. Now you are Ready. To check if your installation works try this in python: 

   ![Wand Header](https://github.com/jadeskon/score-scan/blob/master/sources/images/readme_md/Wand_Header.jpg "Wand Header")

Reference to integrate ImageMagick: http://docs.wand-py.org/en/0.4.4/guide/install.html#install-imagemagick-windows

### Other dependencies
Other dependencies are OpenCV and Tensorflow. This dependencies can you install also about pip:
`pip install opencv-python`
`pip install tensorflow`

## Usage
`A update how you can train cnn model will come later! So you get a error at the moment because you have no trained model!`

To run this application you have to run the `main.py` file. If you would like to digitize a other score than you have to set in `config.json` the attribute `pathToClassifiactionImage` to a other file:

  "Input": {
    ...,
    "pathToClassifiactionImage": "./Input_Component\\Input\\clear_basic_15.pdf"
  },
