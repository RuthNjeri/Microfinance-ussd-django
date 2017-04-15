from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from microfinance_callback.config import username,apikey
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import datetime
from microfinance_callback.models import session_levels
from microfinance_callback.models import Microfinance
from microfinance_callback.models import account

# Create your views here.
@csrf_exempt

def menu(request):
    if request.method == POST  and request.POST:
    #1. Receive POST from AT
      isActive  = request.POST.get('isActive')
      callerNumber =request.POST.get('callerNumber')
      dtmfDigits = request.POST.get('dtmfDigits')
      sessionId = request.POST.get('sessionId')

      #2. Check if isActive=1 to act on the call or isActive=='0' to store the result
    if isActive =='1':
                  
          if dtmfDigits == "0":
              #2b. Compose response - talk to sales...
            response  = '<?xml version="1.0" encoding="UTF-8"?>'
            response += '<Response>'
            response += '<Say>Please hold while we connect you to Sales.</Say>'     
            response += '<Dial phoneNumbers="880.welovenerds@ke.sip.africastalking.com" ringbackTone="http:#62.12.117.25:8010/media/SautiFinaleMoney.mp3"/>'
            response += '</Response>'
             
            # Print the response onto the page so that our gateway can read it
            return HttpResponse(response, content_type='text/plain') 
              
          if dtmfDigits == "1":
                  #2c. Compose response - talk to support...
                response  = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<Say>Please hold while we connect you to Support.</Say>'     
                response += '<Dial phoneNumbers="880.welovenerds@ke.sip.africastalking.com" ringbackTone="http:#62.12.117.25:8010/media/SautiFinaleMoney.mp3"/>'
                response += '</Response>'
                 
                # Print the response onto the page so that our gateway can read it
                return HttpResponse(response, content_type='text/plain') 
                  
          if dtmfDigits == "2":
                  #2d. Redirect to the main IVR...
                response  = '<?xml version="1.0" encoding="UTF-8"?>'
                response += '<Response>'
                response += '<Redirect>http:#62.12.117.25/MF-Ussd-Live/voiceCall.php</Redirect>'
                response += '</Response>'

                # Print the response onto the page so that our gateway can read it
                return HttpResponse(response, content_type='text/plain') 
               
              
          else:
                #2e. By default talk to support
              response  = '<?xml version="1.0" encoding="UTF-8"?>'
              response += '<Response>'
              response += '<Say>Please hold while we connect you to Support.</Say>'     
              response += '<Dial phoneNumbers="880.welovenerds@ke.sip.africastalking.com" ringbackTone="http:#62.12.117.25:8010/media/SautiFinaleMoney.mp3"/>'
              response += '</Response>'
               
              # Print the response onto the page so that our gateway can read it
              return HttpResponse(response, content_type='text/plain')   
        

    else:
        #3. Store the data from the POST
          durationInSeconds=request.POST.get('durationInSeconds')
          direction=request.POST.get('direction')
          amount=request.POST.get('amount')
          callerNumber=request.POST.get('callerNumber')
          destinationNumber=request.POST.get('destinationNumber')
          sessionId=request.POST.get('sessionId')
          callStartTime=request.POST.get('callStartTime')
          isActive=request.POST.get('isActive')
          currencyCode=request.POST.get('currencyCode')
          status=request.POST.get('status')

        #3a. Store the data, write your SQL statements here...
  

