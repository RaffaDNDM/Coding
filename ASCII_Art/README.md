# Braille
The program generates an ASCII art from an image.
It requires several dependencies, that you can install using this bash command:
```bash
pip3 install colorama termcolor Pillow
```
or<br>
```bash
pip3 install -r requirements.txt
```
To run the server in a Docker container, you need to type the following commands on terminal:
```bash
docker build -t username/app .
docker run -it username/app
```
with:<br>
**-t tagname** to specify a tagname to identify the container<br>
**-it** only to type the path of the image (e.g. porsche.jpg) on stdin and see the results on the terminal