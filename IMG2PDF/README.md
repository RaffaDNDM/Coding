# Creates pdf using a set of images.
This program can work in two different ways:
<details><summary><b>-r</b> <i>option</i></summary>
the application is going to analyse all the subfolders of the input folder. For each of them, it will create a pdf composed by all the images inside of it.<br>
To run the program, you need to type for example this command on bash:
```bash
python3 img2pdf.py -d ../folder -f jpg -r
```
where <b>../folder</b> is the input folder, <b>-f jpg</b> is used to specify the image extension (e.g. <i>jpg</i> in this case).
</details>
<details><summary><i>no</i> <b>-r</b> <i>option</i></summary>
the application will create a pdf composed by all the images inside the input folder.<br>
To run the program, you need to type for example this command on bash:
```bash
python3 img2pdf.py -d ../folder -f jpg
```
where <b>../folder</b> is the input folder, <b>-f jpg</b> is used to specify the image extension (e.g. <i>jpg</i> in this case).
</details>
It requires several dependencies, that you can install using this bash command:
```bash
pip3 install argparse zipfile progressbar termcolor
```
Type the following bash command for help about the argument parameters:
```bash
python3 img2pdf.py -h
```