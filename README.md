# Wifi Password Retrieval Tool
A command line tool based on python that is used for retrieval of saved wifi passwords on **Windows or Linux**.  
*OSX support is there but the process is still tedious [Under Development].*  
Many times we wish to know the password of the wifi we are connected to but unfortunately it is a cumbersome task. This tool solves the problem.

## How To Use
```cli
git clone https://github.com/JeeveshN/Retrieve-Wifi-Passwords.git or download the zip file
```
### Retrieve All the passwords together
```cli
python pass.py
```
Or alternatively you can use
- GNU/Linux/OSX: `./pass.py`
- Windows: `pass.py`

![image](https://media.giphy.com/media/hoJvidbWg5vUs/giphy.gif)
### Retrieve Based on Wifi names
#### Selecting one wifi
```cli
python pass.py "wifi name"
```
Or alternatively you can use
- GNU/Linux/OSX: `./pass.py "wifi name"`
- Windows: `pass.py "wifi name"`

![image](https://media.giphy.com/media/1xVcTBzWdBTDa/giphy.gif)

#### Selecting multiple wifi
```cli
python pass.py "wifi name 0" "wifi name 1" "wifi name 2" [...]
```
Or alternatively you can use
- GNU/Linux/OSX: `./pass.py "wifi name 0" "wifi name 1" "wifi name 2" [...]`
- Windows: `pass.py "wifi name 0" "wifi name 1" "wifi name 2" [...]`