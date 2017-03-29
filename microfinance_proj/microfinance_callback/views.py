from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from .config import username,apikey
from .models import Microfinance,session_levels
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def callback(request):


	if request.method == 'POST'and request.POST:

			sessionId = request.POST.get('sessionId', None)
			serviceCode=request.POST.get('serviceCode',None)
			phoneNumber=request.POST.get('phoneNumber',None)
			text=request.POST.get('text',None)

			textList = text.split('*') #1.converting the string into a list
			userResponse = textList[-1].split() #2.removing whitespace and getting last element of the array
			level = 0 #3.set default level of user
			try:
								#4. Check the level of the user from the DB and retain default level if none is found for this session
					session = session_levels.objects.get(session_id = sessionId)
					level = session.level

			except session_levels.DoesNotExist as e:
								
								print('session_levels not found')
			
			try:
						#5. check user in the database
				 result = Microfinance.objects.get(phonenumber = phoneNumber)
						#6. check if user is available and serve menu, if not register
				 if result and result.city and result.name:
						#7. if user is fully registered, level o and 1 serve the basic menus, the rest allow for financial transaction
						if level == 0 or level == 1:
								#7a.check user typed something
								if userResponse == "":
										if level == 0:
												#7b.Graduate user to next level and serve main menu
												session_level1 = session_levels(session_id= sessionId, phoneNumber = phoneNumber, level=1) 
												session_level1.save() 
												
												#serve the services menu
												response = "CON Welcome to Nerd Microfinance, "+ result.name + " Choose a service.\n"
												response += " 1. Please call me.\n"
												response += " 2. Deposit Money\n"
												response += " 3. Withdraw Money\n"
												response += " 4. Send Money\n"                            
												response += " 5. Buy Airtime\n"
												response += " 6. Repay Loan\n"  

												return HttpResponse(response, content_type='text/plain')

								elif userResponse == 0:
											if level == 0:         
														#7b.Graduate user to next level and serve main menu
														session1 = session_levels(session_id= sessionId, phoneNumber = phoneNumber, level=1) 
														session1.save() 
														
														#7c.serve the services menu
														response = "CON Welcome to Nerd Microfinance, "+ result.name + " Choose a service.\n"
														response += " 1. Please call me.\n"
														response += " 2. Deposit Money\n"
														response += " 3. Withdraw Money\n"
														response += " 4. Send Money\n"                            
														response += " 5. Buy Airtime\n"
														response += " 6. Repay Loan\n" 

														return HttpResponse(response, content_type='text/plain')

								elif userResponse == 1:  
												if level == 1:
													 #8d. call the user and bridge to a sales person
													response = "END Please wait while we place your call.\n"
													 #make a call
													from_= "+254711082300"
													to_ = phoneNumber
													 #create a new instance of our awesome gateway class
													gateway = AfricasTalkingGateway(username,apikey)
													try:
														gateway.call(from_,to_)
													except AfricasTalkingGatewayException as e:
														 print("Encounted an error when calling:" + e.getMessage())
													 #print respose so that the gateway can read it  
														 
												return HttpResponse(response, content_type='text/plain')
								elif userResponse == 2:
										if level == 1:
											 #8e. Ask how much and launch Mpesa Checkout to the user
											response = "CON How much are you depositing?\n"
											response += " 1. 1 Shilling.\n"
											response += " 2. 2 Shillings.\n"
											response += " 3. 3 Shillings.\n"        
											 #update to level 9

											session_level9 = session_levels.objects.get(session_id= sessionId)
											session_level9.level = 9
											session_level9.save() 
											
												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								elif userResponse == 3:
										if level == 1:
											 #8e. Ask how much and launch B2C to the user
											response = "CON How much are you Withdrawing?\n"
											response += " 1. 1 Shilling.\n"
											response += " 2. 2 Shillings.\n"
											response += " 3. 3 Shillings.\n"        
											 #update to level 10

											session_level10 = session_levels.objects.get(session_id= sessionId)
											session_level10.level = 10
											session_level10.save() 
													
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								elif userResponse == 4:
										if level == 1:
										 #8e.send another user same money
											response = "CON You can only send 1 Shilling\n"
											response += "Enter a valid phonenumber (like 0722122122)\n"
						
											 #update to level 11

											session_level11 = session_levels.objects.get(session_id= sessionId)
											session_level11.level = 11
											session_level11.save() 
												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')

								elif userResponse == 5:
										if level==1:
											#9e. send user airtime
											response = "END Please wait while we load your account.\n"
											#search db and send airtime
											recipients=[ {'phonenumber': phoneNumber,'amount': 'KES 5'}
								      								#can add more numbers
									      							]
											#JSON encode
											recipientStringFormat = JsonResponse(recipients)
											#Create an instance of ourawesome gateway class, pass your credentials
											gateway = AfricasTalkingGateway(username, apiKey)
											try:
												results = gateway.sendAirtime(recipientStringFormat)  
											except AfricasTalkingGatewayException as e:
												print(e.getMessage()) 
											#print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')

								elif userResponse == 6:
										if level == 1:
										 #9f. Ask how much and launch the Mpesa Checkout to the user
											response = "CON How much are you depositing?\n"
											response += " 4. 1 Shilling.\n"
											response += " 5. 2 Shillings.\n"
											response += "6.  3 Shillings.\n"

						
											 #update to level 12

											session_level11 = session_levels.objects.get(session_id= sessionId)
											session_level11.level = 12
											session_level11.save() 
												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								else:
										if level == 1:
										 #9g. Return user to Main Menu & Demote user's level
											response = "CON How much are you depositing?\n"
											response += " Press 0 to go back.\n"


						
											 #demote
											session_levels.objects.filter(session_id=sessionId).update(level=0)

												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
											
			except Microfinance.DoesNotExist as e:
								print('Microfinance not found')
				
