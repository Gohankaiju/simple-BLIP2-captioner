# simple-BLIP2-captioner

## Introduction
simple-BLIP2-captioner generates caption files using BLIP2 on the GUI.

Enter the path to the folder containing the image files, select the model, and run the program to create a caption file in txt file format in the same location as the image folder.

## Installation
Build from source

    git clone https://github.com/Gohankaiju/simple-BLIP2-captioner.git

    python -m venv venv
    .\venv\Scripts\activate

    pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118

    pip install --upgrade -r requirements.txt

    python run.py

## License

[MIT](https://choosealicense.com/licenses/mit/)