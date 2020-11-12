# Extract multiple archieves.
This program extract all the archieves in the input folder with a specific format, writing the results in the output folder.<br>
It requires several dependencies, that you can install using this bash command:
```bash
pip3 install argparse zipfile progressbar termcolor
```
To run the program, you need to type for example this command on bash:
```bash
python3 extract_all.py -i ../folder_in -o ../folder_out -f jpg
```
where **../folder_in** is the input folder, **../folder_out** is the output folder, **-f zip** is used to specify the image extension (e.g. *zip* in this case). If **-o** option is not specified, by default the output folder is the input folder.<br>
Type the following bash command for help about the argument parameters:
```bash
python3 extract_all.py -h
```