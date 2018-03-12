# Score Scan
 
 ## Introduction
Score Scan is a score scanner based on image processing algorithms and convolutional neural networks for optical music recognition.
It processes pdf and png files to create a MusicXML file.

It was a master project of seven students of Hochschule Kempten - University of Applied Sciences in winter semester 2017/18. We published this project in github to inspire other people. Maybe there are people which are interested to work on this project.

## Dependencies
To-Do

## Usage
`A update how you can train cnn model will come later! So you get a error at the moment because you have no trained model!`

To run this application you have to run the `main.py` file. If you would like to digitize a other score than you have to set in `config.json` the attribute `pathToClassifiactionImage` to a other file:

  "Input": {
    ...,
    "pathToClassifiactionImage": "./Input_Component\\Input\\clear_basic_15.pdf"
  },
