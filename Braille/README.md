# Braille
The program encodes a string with Braille symbols.
It requires several dependencies, that you can install using this bash command:
```bash
pip3 install colorama termcolor
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
**-it** only to type the string on stdin and see the results