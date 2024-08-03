from OCP import OCP 
from time import sleep


ocp = OCP()
ocp.connect()
ocp.login("admin", "hcmlab")
sleep(2)
print(ocp.logout())


