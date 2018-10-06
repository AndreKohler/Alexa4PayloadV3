#
#   https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/smart-home-skill-api-reference
#
import uuid
from datetime import datetime

action_func_registry = []

# action-func decorator
def alexa(action_name, directive_type, response_type, namespace ):
    def store_metadata(func):
        func.alexa_action_name = action_name
        func.alexa_directive_type = directive_type
        func.alexa_response_type = response_type
        func.alexa_namespace = namespace
        

        action_func_registry.append( func )
        return func
    return store_metadata


class AlexaActions(object):
    def __init__(self, sh, logger, devices):
        self.actions = {}
        self.actions_by_directive = {}

        for func in action_func_registry:
            logger.debug("Alexa: initializing action {}".format(func.alexa_action_name))
            action = AlexaAction(sh, logger, devices, func, func.alexa_action_name, func.alexa_directive_type, func.alexa_response_type,func.alexa_namespace)
            self.actions[action.name] = action
            self.actions_by_directive[action.directive_type] = action

    def by_name(self, name):
        return self.actions[name] if name in self.actions else None

    def for_directive(self, directive):
        return self.actions_by_directive[directive] if directive in self.actions_by_directive else None
    
    

class AlexaAction(object):
    def __init__(self, sh, logger, devices, func, action_name, directive_type, response_type, namespace):
        self.sh = sh
        self.logger = logger
        self.devices = devices
        self.func = func
        self.name = action_name
        self.directive_type = directive_type
        self.response_type = response_type
        #P3 Properties
        self.namespace = namespace
        self.response_Value = None

    def __call__(self, payload):
        return self.func(self, payload)

    def items(self, device_id):
        device = self.devices.get(device_id)
        return device.items_for_action(self.name) if device else []

    def item_range(self, item, default=None):
        return item.alexa_range if hasattr(item, 'alexa_range') else default

    def header(self, name=None):
        return {
            'messageId': uuid.uuid4().hex,
            'name': name if name else self.response_type,
            'namespace': 'Alexa.ConnectedHome.Control',
            'payloadVersion': '2'
        }

    def respond(self, payload={}):
        return {
            'header': self.header(),
            'payload': payload
        }
    # find Value for Key in Json-structure
    # needed for Alexa Payload V3
    def search(self,p, strsearch):
        if type(p) is dict:  # im Dictionary nach 'language' suchen
            if strsearch in p:
                tokenvalue = p[strsearch]
                if not tokenvalue is None:
                 return tokenvalue
            else:
                for i in p:
                    tokenvalue = self.search(p[i], strsearch)  # in den anderen Elementen weiter suchen
                    if not tokenvalue is None:
                        return tokenvalue
    def replace(self,p, strsearch, newValue):
        if type(p) is dict:  # im Dictionary nach 'language' suchen
            if strsearch in p:
                tokenvalue = p[strsearch]
                p[strsearch] = newValue
                if not tokenvalue is None:
                 return tokenvalue
            else:
                for i in p:
                    tokenvalue = self.search(p[i], strsearch)  # in den anderen Elementen weiter suchen
                    if not tokenvalue is None:
                        return tokenvalue
    
    def p3_respond(self, Request):
        myEndpoint = self.search(Request,'endpoint')
        myScope = self.search(Request,'scope')
        myEndPointID = self.search(Request,'endpointId')
        myHeader = self.search(Request,'header')
        now = datetime.now().isoformat()
        myTimeStamp = now[0:22]+'Z'
        self.replace(myHeader,'messageId',uuid.uuid4().hex)
        self.replace(myHeader,'name','Response')
        self.replace(myHeader,'namespace','Alexa')
        
        
        myReponse = {
          "context": {
            "properties": [ {
              "namespace": self.namespace,
              "name": self.response_type,
              "value": self.response_Value,
              "timeOfSample": myTimeStamp,
              "uncertaintyInMilliseconds": 5000
            } ]
          },
          "event": {
              "header": myHeader
                   ,
          "endpoint" : {
                        "scope": myScope,
                        "endpointId": myEndPointID 
                       },
          "payload": {}
                    }
          }
 
        return myReponse 
    
def p3_reportstate(self, Request, Properties=[]):
        myEndpoint = self.search(Request,'endpoint')
        myScope = self.search(Request,'scope')
        myEndPointID = self.search(Request,'endpointId')
        myHeader = self.search(Request,'header')
        now = datetime.now().isoformat()
        myTimeStamp = now[0:22]+'Z'
        self.replace(myHeader,'messageId',uuid.uuid4().hex)
        self.replace(myHeader,'name','StateReport')
        self.replace(myHeader,'namespace','Alexa')
        
        
        myReponse = {
          "context": {
            "properties": [ Properties ]
          },
          "event": {
              "header": myHeader
                   ,
          "endpoint" : {
                        "scope": myScope,
                        "endpointId": myEndPointID 
                       },
          "payload": {}
                    }
          }
 
        return myReponse         
# https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/smart-home-skill-api-reference#error-messages
def error(self, error_type, payload={}):
        return {
            'header': self.header(error_type),
            'payload': payload
        }
