## About
This is package is create to interface with COSMED Omnia *(created by ©1996-2024 [COSMED](https://www.cosmed.com/en/) srl)* using OCP (Omnia control protocol) it Could be used to send any command from the OCP and get the result as a python dictionary by first creating the command as an xml send it and receive the response and process it to get a python dictionary to all easy Integration with python.


## to get started with OCP using python follow the following steps:-

1. normally install COSMED Omnia.

2. run the regedit.reg file provided to configure the OCP.

3. then normally start COMSED OMNIA.

4. then you can use the python module ocp.py to send commands to the software.

  
  
### steps to install and use the OCP package:
1. clone the package.
2. run setup.py using (pip install .) while on the same directory as the setup.py.




```
from OCP import OCP #import the OCP main class


ocp = OCP()  # to creates an OCP object
ocp.connect() # to initiate a TCP connection with COSMED Omnia
# to login and notice COSMED omnia needs to be running and replace the username and password with  username and password created on COMED Omnia 
ocp.login("username", "password")




```


you can then send any command and get the result in python as the OCP interface and you can find a
method for every command on the OCP to send that command and receive a response











