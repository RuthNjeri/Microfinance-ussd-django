from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from .config import username,apikey
from .models import Microfinance,session_levels
from django.http import HttpResponse

# Create your views here.

def callback(request):
	if request.method == 'POST'and request.POST:

        sessionId = request.POST.get('sessionId', None)
    	serviceCode=request.POST.get('serviceCode',None)
    	phoneNumber=request.POST.get('phoneNumber',None)
    	text=request.POST.get('text',None)

    	textList = text.split('*') #1.converting the string into a list
    	userResponse = text.textList[-1].split() #2.removing whitespace and getting last element of the array
    	level = 0 #3.set default level of user
        
        try:
            #4. Check the level of the user from the DB and retain default level if none is found for this session
          session = session_levels.objects.filter(session_id = sessionId)
          level = session.level

        except session_levels.DoesNotExist as e:
                print('Session does not exist')
    	
        try:
            #5. check user in the database
         result = Microfinance.objects.get(phoneNumber = phoneNumber)
            #6. check if user is available and serve menu, if not register
         if result and result.city and result.name:
            #7. if user is fully registered, level o and 1 serve the basic menus, the rest allow for financial transaction
            if level == 0 or level == 1
                #check user typed something
                if userResponse:
                    if level == 0:
                        
                        def caseLevelZero:

                            def caseEmpty:
                            return response   

                            def caseZero:
                            return response  
                              
                        return response

                    elif level == 1:
                         def caseLevelOne:
                        


                
        except Microfinance.DoesNotExist as e:
               print('Microfinance does not exist')
        
