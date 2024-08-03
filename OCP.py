import sys
import xml.etree.ElementTree as ET
import socket                    # used for tcp communication
import xmltodict                 # used to convert xml recieved from omnia to dict
# used to convert python dictionary to xml to be sent to omnia server
from dicttoxml2 import dicttoxml
# to create delay between different commands to allow the command to be executed properly
from time import sleep
from functools import wraps

#  class commander to create commands in xml format
# then send it via the client


class Commander:
    """ 
        the commander class is mostly intended to convert dictionary commands into xml
        and then it uses the client to send the command to omnia server
    """

    def __init__(self, root_node="OmniaXB"):
        """
            the root_node is the root xml tag by default it is OmniaXB
            the IP and Port by default 127.0.0.1, 44444
        """
        self.root_node = root_node
        # the main body of the system command to be used to send
        # every system command and the same thing was done for every set of  commands(archive, system, Realtime)
        self.sys_body = {
            root_node: {
                "System": {}
            }
        }
        self.arch_body = {
            root_node: {
                "Archive": {}
            }
        }
        self.RT_body = {

            root_node: {
                "RealTime": {}
            }
        }

    def to_xml(self, dict):
        """convert python dictionary to XML format (bytes)"""
        return dicttoxml(dict, root=False, attr_type=False)

    @staticmethod
    def _send_and_recieve(method):
        @wraps(method)
        def func(self, *args, **kwargs):
            xml = method(self, *args, **kwargs)
            return self.send_xml(xml)
        return func
    def _create_main_sys_body(self, child):
        """Create the main XML structure for system messages"""
        body = self.sys_body.copy()
        body[self.root_node]["System"] = child
        return body

    def _create_main_arch_body(self, child):
        """Create the main XML structure for archive messages"""
        body = self.sys_body.copy()
        body[self.root_node]["Archive"] = child
        return body

    def _create_main_RT_body(self, child):
        """Create the main XML structure for RealTime messages"""
        body = self.RT_body.copy()
        body[self.root_node]["RealTime"] = child
        return body
    @_send_and_recieve
    def CreateCommand(self, command: dict):
        """Creates a command given a dictionary"""
        return dicttoxml(command, root=False, attr_type=False)

    # creating Subsystem: System commands
    @_send_and_recieve
    def closeApp(self):
        return self.to_xml(self._create_main_sys_body({"CloseApplication": ""}))

    @_send_and_recieve
    def createSessionKey(self):
        return self.to_xml(self._create_main_sys_body({"CreateSessionKey": ""}))

    @_send_and_recieve
    def enableRealTimeInfo(self):
        return self.to_xml(self._create_main_sys_body({"EnableRealTimeInformation": {"Enabled": "1"}}))

    @_send_and_recieve
    def getCurrentUser(self):
        return self.to_xml(self._create_main_sys_body({"GetCurrentUser": ""}))

    @_send_and_recieve
    def getLoginToken(self, username: str, password: str, domain_name=""):
        return self.to_xml(self._create_main_sys_body({"GetLoginToken": {"Username": username, "Password": password, "Domain": domain_name}}))

    @_send_and_recieve
    def getPermissionLevel(self):
        return self.to_xml(self._create_main_sys_body({"GetPermissionLevel": ""}))

    @_send_and_recieve
    def getProtocolLevel(self):
        return self.to_xml(self._create_main_sys_body({"GetProtocolLevel": ""}))

    @_send_and_recieve
    def login(self, username, password, secure=False):
        if secure:
            return self.to_xml(self._create_main_sys_body({"Login": {"Username": username, "SecurePassword": password}}))

        return self.to_xml(self._create_main_sys_body({"Login": {"Username": username, "Password": password}}))

    @_send_and_recieve
    def logout(self):
        return self.to_xml(self._create_main_sys_body({"Logout": ""}))

    @_send_and_recieve
    def selectScreen(self, num: str):
        return self.to_xml(self._create_main_sys_body({"SelectScreen": {"ScreenNumber": "0"}}))

    @_send_and_recieve
    def setBackground(self):
        return self.to_xml(self._create_main_sys_body({"SetBackground": ""}))

    @_send_and_recieve
    def setForeground(self):
        return self.to_xml(self._create_main_sys_body({"SetForeground": ""}))

    @_send_and_recieve
    def showDebugMonitor(self):
        return self.to_xml(self._create_main_sys_body({"ShowDebugMonitor": ""}))

    @_send_and_recieve
    def showMessage(self, text="Hello!", ok_text="do it", cancel_text="don't", time_out='20'):
        return self.to_xml(self._create_main_sys_body({"ShowMessage": {"Text": text, "OK": ok_text, "Cancel": cancel_text, "Timeout": time_out, "DefautCancel": ""}}))

    @_send_and_recieve
    def showOCPButton(self, num='1'):
        return self.to_xml(self._create_main_sys_body({"ShowOCPButton": {"Show": "1"}}))

    @_send_and_recieve
    def testSessionkey(self, key: str):
        return self.to_xml(self._create_main_sys_body({"TestSessionKey": {"Text": key}}))

    # ---- Archive commands ----  #
    @_send_and_recieve
    def ChangeSubject(self, record_id, data: dict):
        data["RecordID"] = record_id
        return self.to_xml(self._create_main_arch_body({"ChangeSubject": data}))

    @_send_and_recieve
    def ChangeVisit(self, record_id, data: dict):
        data["RecordID"] = record_id
        return self.to_xml(self._create_main_arch_body({"ChangeVisit": data}))

    @_send_and_recieve
    def createSubject(self, data: dict):
        return self.to_xml(self._create_main_arch_body({"CreateSubject": data}))

    @_send_and_recieve
    def deleteSubject(self, record_id):
        return self.to_xml(self._create_main_arch_body({"DeleteVisit": {"RecordID": record_id}}))

    @_send_and_recieve
    def exportData(self, type: str, record_id: str, filepath: str):
        return self.to_xml(self._create_main_arch_body({"ExportData": {"Type": type, "RecordID": record_id, "Filename": filepath}}))

    @_send_and_recieve
    def exportReport(self, record_id: str, filepath: str, non_best: str):
        # to be modified to have editional records that could be add
        return self.to_xml(self._create_main_arch_body({"ExportReport": {"RecordID": record_id, "Filename": filepath, "NonBest": non_best}}))

    @_send_and_recieve
    def exportXls(self, record_id: str, filepath: str):
        return self.to_xml(self._create_main_arch_body({"ExportXls": {"RecordID": record_id, "Filename": filepath}}))

    @_send_and_recieve
    def getLastTest(self):
        return self.to_xml(self._create_main_arch_body({"GetLastTest": ""}))

    @_send_and_recieve
    def getSubjectList(self, filepath: str):
        return self.to_xml(self._create_main_arch_body({"GetSubjectList": {"Filename": filepath}}))

    @_send_and_recieve
    def getSubjectVisitList(self, record_id):
        return self.to_xml(self._create_main_arch_body({"GetSubjectVisitList": {"RecordID": record_id}}))

    @_send_and_recieve
    def getTestInfo(self, record_id: str):
        return self.to_xml(self._create_main_arch_body({"GetTestInfo": {"RecordID": record_id}}))

    @_send_and_recieve
    def getTestParameters(self, record_id: str, filepath: str):
        return self.to_xml(self._create_main_arch_body({"GetTestParameters": {"RecordID": record_id, "Filename": filepath}}))

    @_send_and_recieve
    def getVisitTestList(self, record_id):
        return self.to_xml(self._create_main_arch_body({"GetVisitTestList": {"RecordID": record_id}}))

    @_send_and_recieve
    def mergeSubjects(self, source: str, target: str):
        return self.to_xml(self._create_main_arch_body({"MergeSubjects": {"Source": source, "Target": target}}))

    @_send_and_recieve
    def searchId(self, id: str, query: dict):
        return self.to_xml(self._create_main_arch_body({"SearchID": {"ID1": id, **query}}))

    @_send_and_recieve
    def searchOrder(self, order: str, query: dict):
        return self.to_xml(self._create_main_arch_body({"SearchOrder": {"Order": order, **query}}))

    @_send_and_recieve
    def searchSubject(self, last_name: str, query: dict):
        return self.to_xml(self._create_main_arch_body({"SearchSubject": {"LastName": last_name, **query}}))

    @_send_and_recieve
    def selectCreateSubject(self, data: dict):
        return self.to_xml(self._create_main_arch_body({"SelectCreateSubject": data}))

    @_send_and_recieve
    def selectSubject(self, record_id):
        return self.to_xml(self._create_main_arch_body({"SelectSubject": {"RecordID": record_id}}))

    @_send_and_recieve
    def selectVisit(self, record_id):
        return self.to_xml(self._create_main_arch_body({"SelectVisit": {"RecordID": record_id}}))

    @_send_and_recieve
    def showTest(self, record_id):
        return self.to_xml(self._create_main_arch_body({"ShowTest": {"RecordID": record_id}}))

    # --- RealTime Commands --- #

    @_send_and_recieve
    def abortTest(self):
        return self.to_xml(self._create_main_RT_body({"AbortTest": {"AutoConfirm": "10"}}))

    @_send_and_recieve
    def endTest(self, test_type, data):
        return self.to_xml(self._create_main_RT_body({"ExecuteTest": {"TestType": test_type, **data}}))

    @_send_and_recieve
    def exitTest(self):
        return self.to_xml(self._create_main_RT_body({"ExitTest": ""}))

    @_send_and_recieve
    def getErgometerInfo(self, tags):
        return self.to_xml(self._create_main_RT_body({"GetErgometerInfo": tags}))

    @_send_and_recieve
    def pauseProtocol(self, num: str):
        return self.to_xml(self._create_main_RT_body({"PauseProtocol": {"Pause": num}}))

    @_send_and_recieve
    def pauseTest(self, num: str):
        return self.to_xml(self._create_main_RT_body({"PauseTest": {"Pause": num}}))

    @_send_and_recieve
    def protocolNext(self):
        return self.to_xml(self._create_main_RT_body({"ProtocolNext": ""}))

    @_send_and_recieve
    def setEndTestPostData(self, manufacturer_id, ecg_link):
        return self.to_xml(self._create_main_RT_body({"SetEndTestPostData": {"Manufacturer": id, "ECGLink": ecg_link}}))

    @_send_and_recieve
    def setLoad(self, loads: dict):
        return self.to_xml(self._create_main_RT_body({"SetLoad": loads}))

    @_send_and_recieve
    def setMarker(self):
        return self.to_xml(self._create_main_RT_body({"Label": ""}))

    @_send_and_recieve
    def setPhase(self, phase):
        return self.to_xml(self._create_main_RT_body({"SetPhase": {"Phase": phase}}))

    @_send_and_recieve
    def setRealTimeInfo(self, info: dict):
        return self.to_xml(self._create_main_RT_body({"SetRealTimeInfo": info}))

    @_send_and_recieve
    def startErgoRecording(self):
        return self.to_xml(self._create_main_RT_body({"StartErgoRecording": ""}))

    @_send_and_recieve
    def startRecoveryPhase(self):
        return self.to_xml(self._create_main_RT_body({"StartRecoveryPhase": ""}))

    @_send_and_recieve
    def startTest(self):
        return self.to_xml(self._create_main_RT_body({"StartTest": ""}))

    @_send_and_recieve
    def testEvent(self, event_type):
        return self.to_xml(self._create_main_RT_body({"TestEvent": {"EventType": event_type}}))
    



# to carry out the tcp connection and send and recieve data
class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        self.socket.close()

    def send_xml(self, xml_data):
        self.socket.sendall(xml_data)
        response = self.receive_response()
        return response

    @staticmethod
    def _receive_as_dict(recieve):
        """a decorator that return a list of messages"""
        @wraps(recieve)
        def func(self):
            response = recieve(self).split(
                '<?xml version="1.0" encoding="utf-8" standalone="no"?>')
            if response[0] == '':
                response.remove('')
            if len(response) == 0 :
                return []
            elif response[0] == 'TimeOUT':
                return []

            messages = []
            for message in response:
                try:
                    messages.append(xmltodict.parse(message))
                except Exception as E:
                    print("recieved:", response, "end")
                    print(E)
                    print(response)
            return messages
        return func

    @_receive_as_dict
    def receive_response(self):
        """Receives a response with one or more messsages"""
        response = b""
        try:
            while True:
                part = self.socket.recv(1024)
                response += part

                if len(part) < 1024:
                    break

        except TimeoutError:
            return "TimeOUT"
        return response.decode("utf-8")


class OCP(Commander, Client):
    """Creates an OCP object that could be used to send commands and recieve response"""
    # Merge Commander and Client Class
    def __init__(self, root_node="OmniaXB", ip_address="127.0.0.1", port=44444):
        Commander.__init__(self, root_node=root_node)
        Client.__init__(self, host=ip_address, port=port)



if __name__ == "__main__":
    try:
        c = OCP(ip_address="127.0.0.1", port=44444, root_node="OmniaXB")
        c.connect()
        c.login("admin",'hcmlab')
        sleep(1)
        print(c.receive_response())
        sleep(5)
        print(c.enableRealTimeInfo())
        print(c.showOCPButton())
        for _ in range(100):
            print(c.receive_response())
    except:
        c.disconnect()
