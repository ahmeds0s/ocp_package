to get started with OCP using python follow the following steps:- 


1. normally install COSMED Omnia.
2. run the regedit.reg file provided to configure the OCP.
3. then normally start COMSED OMNIA.
4. then you can use the python module ocp.py to send commands to the software.


# you can just import OCP using 
 
from OCP import OCP

commander
# first create a client using
 
client = Client(host="127.0.0.1", port=44444)


# then create a  object using
com = commander()

# get the command to be sent
command = com.login() # in that case provide the username and password


# then give send the command using 
response = client.send_xml(command) # you would recieve a python dictionary with the response with same structure as the result 









