# Wifi Password Retrieval Tool
A command line tool based on python that is used for retrieval of saved wifi passwords on **Windows or Linux**.  
*OSX support is there but the process is still tedious [Under Development].*  
Many times we wish to know the password of the wifi we are connected to but unfortunately it is a cumbersome task. This tool solves the problem.

## How To Use As Library/Utility

### Importing the class
```python
from PassRetrievalTool import PassRetrievalTool # Import the class

class PassRetrievalTool_test:

    def __init__(self):
        wifi_password_dictionary = PassRetrievalTool.get_wifi_password_dictionary() # Call the static method get_wifi_password_dictionary() and save it
        
        PassRetrievalTool.print_passwords(wifi_password_dictionary) # Print them or do whatever you want.

if __name__ == "__main__":
    test = PassRetrievalTool_test()
```
A test.py is available.
## How To Use As Command Line
```
git clone https://github.com/JeeveshN/Retrieve-Wifi-Passwords.git or download the zip file
```
### Retrieve All the passwords together
```bash
python pass.py
```
![image](https://media.giphy.com/media/hoJvidbWg5vUs/giphy.gif)
### Retrieve in JSON format
```bash
python pass.py --json
```
Example of output:
```json
{
  "Example-Wifi-SSID" : "WifiPassword1234",
  "WifiSSID2" : "p4$$w0rD"
}

```


### Retrieve Based on Wifi Name 
Retrieve the password bases on the SSID name. This can also be combined with --json parameter.
```bash
python pass.py "Name of Wifi"
```
```bash
python pass.py "Name of Wifi" --json
```
![image](https://media.giphy.com/media/1xVcTBzWdBTDa/giphy.gif)

