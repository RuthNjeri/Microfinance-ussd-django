from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from microfinance_callback.config import username,apikey
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import datetime
from microfinance_callback.models import session_levels
from microfinance_callback.models import Microfinance
from microfinance_callback.models import account



@csrf_exempt


def voice(request):
		
		try:
			 




				if request.method == 'POST':
					# # This is a unique ID generated for this call
					
					sessionId = request.POST.get('sessionId')
					isActive = request.POST.get('isActive')




					if isActive == '1': #make the call when isActive is 1
							 
								callerNumber = request.POST.get('callerNumber')

								# Compose the response
								response  = '<?xml version="1.0" encoding="UTF-8"?>'
								response += '<Response>'
								response += '<GetDigits timeout="30" finishOnKey="#" callbackUrl="http://7a255c6d.ngrok.io/index/menu">'
								response += '<Say>Thank you for calling Press 0 to talk to sales, 1 to talk to support or 2 to hear this message again</Say>'
								response += '</GetDigits>'
								response += '<Say>Thank you for calling Good bye!</Say>'
								response += '</Response>'
								# Print the response onto the page so that our gateway can read it
								return HttpResponse(response, content_type='application/xml')

					else: 
						
					#       # Read in call details (duration, cost)+ This flag is set once the call is completed+
					#       # Note that the gateway does not expect a response in thie case
								
								duration     = request.POST.get('durationInSeconds')
								currencyCode = request.POST.get('currencyCode')
								amount       = request.POST.get('amount')
								
								# You can then store this information in the database for your records
					
		except Exception as e:
			print('exception',duration)






