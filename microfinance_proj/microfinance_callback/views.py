from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from .config import username,apikey
from .models import Microfinance,session_levels,account
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
				#create an account
				sql16 = account.objects.get(phonenumber=phoneNumber)
				sql11A = account(phonenumber=phoneNumber)
				sql11A.save()

			except account.DoesNotExist as e:

				print("account does not exist")
			try:
						#5. check user in the database
				result = Microfinance.objects.get(phonenumber = phoneNumber)
						#6. check if user is available and serve menu, if not register
				if result and result.city and result.name:
						#7. if user is fully registered, level o and 1 serve the basic menus, the rest allow for financial transaction
						if level == '0' or level == '1':
								#7a.check user typed something
								if userResponse == "":
										if level == '0':
												#7b.Graduate user to next level and serve main menu
												session_level1 = session_levels(session_id= sessionId, phoneNumber = phoneNumber, level='1') 
												session_level1.save() 
												
												#serve the services menu
												response = "CON Welcome to Nerd Microfinance, "+ result.name + " Choose a service.\n"
												response += " 1. Please call me.\n"
												response += " 2. Deposit\n"
												response += " 3. Withdraw\n"
												response += " 4. Send\n"                            
												response += " 5. Buy Airtime\n"
												response += " 6. Repay Loan\n" 
												response += " 7. Account Balance\n" 

												return HttpResponse(response, content_type='text/plain')

								elif userResponse == '0':
											if level == '0':         
														#7b.Graduate user to next level and serve main menu
														session1 = session_levels(session_id= sessionId, phoneNumber = phoneNumber, level=1) 
														session1.save() 
														
														#7c.serve the services menu
														response = "CON Welcome to Nerd Microfinance, "+ result.name + " Choose a service.\n"
														response += " 1. Please call me.\n"
														response += " 2. Deposit\n"
														response += " 3. Withdraw\n"
														response += " 4. Send\n"                            
														response += " 5. Buy Airtime\n"
														response += " 6. Repay Loan\n" 
														response += " 7. Account Balance\n"

														return HttpResponse(response, content_type='text/plain')

								elif userResponse == '1':  
												if level == '1':
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
														 print("Encounted an error when calling:")
													 #print respose so that the gateway can read it  
														 
												return HttpResponse(response, content_type='text/plain')
								elif userResponse == '2':
										if level == '1':
											 #8e. Ask how much and launch Mpesa Checkout to the user
											response = "CON How much are you depositing?\n"
											response += " 1. 19 Shilling.\n"
											response += " 2. 18 Shillings.\n"
											response += " 3. 17 Shillings.\n"        
											 #update to level 9

											session_level9 = session_levels.objects.get(session_id= sessionId)
											session_level9.level = 9
											session_level9.save() 
											
												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								elif userResponse == '3':
										if level == '1':
											 #8e. Ask how much and launch B2C to the user
											response = "CON How much are you Withdrawing?\n"
											response += " 1. 15 Shill'''ing.\n"
											response += " 2. 16 Shillings.\n"
											response += " 3. 17 Shillings.\n"        
											 #update to level 10

											session_level10 = session_levels.objects.get(session_id= sessionId)
											session_level10.level = 10
											session_level10.save() 
													
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								elif userResponse == '4':
										if level == '1':
										 #8e.send another user same money
											response = "CON You can only send 15 Shilling\n"
											response += "Enter a valid phonenumber (like 0722122122)\n"
											#Print the response onto the page so that our gateway can read it
											return HttpResponse(response, content_type='text/plain')
											 #update to level 11

											session_level11 = session_levels.objects.get(session_id= sessionId)
											session_level11.level = 11
											session_level11.save() 
												
											#B2C
											#Find account
											sql10a = account.objects.get(phonenumber= phoneNumber)

											if sql10a:
												# Reduce balance
												newBal = sql10a.balance
												newBal = 15	- newBal			

											if newBal > 0:					    	
												gateway =  AfricasTalkingGateway(username, apiKey)
												productName  = "Nerd Payments"
												currencyCode = "KES"
												 
												recipients  = [{  "phonenumber": phoneNumber,"currencyCode": "KES", "amount": 15,"metadata":{"name": "Clerk","reason": "May Salary"}}
																]
											try :
												responses = gateway.mobilePaymentB2CRequest(productName,recipients) 
											except AfricasTalkingGatewayException as e:
													 print ("Received error response: ") 											    	
														 
											
								elif userResponse == '5':
									
									#Find account

									sql10a = account.objects.get(phonenumber=phoneNumber)

									if sql10a:
										# Reduce balance
										newBal = sql10a.balance
										newBal = newBal-5				

										if newBal > 0:
											#9e. Send user airtime
											response = "END Please wait while we load your airtime account.\n"
											# Print the response onto the page so that our gateway can read it
											return HttpResponse(response, content_type='text/plain')
												
												# Search DB and the Send Airtime
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
												print('Airtime not sent') 
										else: 
											#Alert user of insufficient funds
											response = "END Sorry, you dont have sufficient\n"
											response += " funds in your account \n"	

											# Print the response onto the page so that our gateway can read it
											return HttpResponse(response, content_type='text/plain')

								elif userResponse == '6':
										if level == '1':
										 #9f. Ask how much and launch the Mpesa Checkout to the user
											response = "CON How much are you depositing?\n"
											response += " 4. 15 Shilling.\n"
											response += " 5. 16 Shillings.\n"
											response += "6.  17 Shillings.\n"

						
											 #update to level 12

											session_level11 = session_levels.objects.get(session_id= sessionId)
											session_level11.level = 12
											session_level11.save() 
												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
								elif userResponse == '7':
									if level==1:
											# Find the user in the db

											sql7 = Microfinance.objects.get(phonenumber = phoneNumber)

										# Find the account

											sql7a= account.objects.get(phonenumber=phoneNumber)
											newBal = 0.00
											newLoan = 0.00

											

											if sql7a:
												newBal = sql7a.balance
												newLoan = sql7a.loan						
												#Respond with user Balance
												response = "END Your account statement.\n"
												response += "Nerd Microfinance.\n"
												response += "Name: ".sql7a.name+"\n"	
												response += "City: "+ sql7a.city+"\n"	
												response += "Balance: "+newBal+"\n"	
												response += "Loan: "+newLoan+"\n"																													
												#Print the response onto the page so that our gateway can read it
												return HttpResponse(response, content_type='text/plain')
								else:
										if level == '1':
										 #9g. Return user to Main Menu & Demote user's level
											response = "CON You have to choose a service\n"
											response += " Press 0 to go back.\n"


						
											 #demote
											session_levels.objects.get(session_id=sessionId)
											session_levels.level = 0
											session_levels.save()

												
										 #print respose so that the gateway can read it  
														 
											return HttpResponse(response, content_type='text/plain')
						else: 
							#Financial Services Delivery
							if level == '9':
								#9a. Collect Deposit from user, update db
								if userResponse == '1':
									#Alert user of incoming Mpesa checkout
										response = "END Kindly wait 1 minute for the Checkout.\n"
										return HttpResponse(response, content_type='text/plain')
											#Declare Params
										gateway = AfricasTalkingGateway(username, apikey)
										productName  = "Nerd Payments"
										currencyCode = "KES"
										amount       = 19
										metadata     = {"sacco":"Nerds","productId":"321"}

										try:
											transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
										except AfricasTalkingGatewayException as e:
											print('received an error')	

										return HttpResponse(response, content_type='text/plain')

								elif userResponse == '2':
									response = "END We have sent the MPESA checkout...\n"
									response += "If you dont have a bonga pin, dial \n"
									response += "Dial dial *126*5*1# to create.\n"

									#Declare Params
									gateway = AfricasTalkingGateway(username, apikey)
									productName  = "Nerd Payments"
									currencyCode = "KES"
									amount       = 2
									metadata     = {"sacco":"Nerds","productId":"321"}
									#pass to gateway
									try:
										transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
									
									except AfricasTalkingGatewayException as e:
										 Print("Received error response: ") 		       	

									#Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')
								elif userResponse == '3':
									#Alert user of incoming Mpesa checkout
									response = "END We have sent the MPESA checkout...\n"
									response += "If you dont have a bonga pin, dial \n"
									response += "Dial dial *126*5*1# to create.\n"

									#Declare Params
									gateway =  AfricasTalkingGateway(username, apikey)
									productName  = "Nerd Payments"
									currencyCode = "KES"
									amount       = 3
									metadata     = {"sacco":"Nerds","productId":"321"}
									#pass to gateway
									try:
										transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
									
									except AfricasTalkingGatewayException as e:
										  print ("Received error response: ")		       	

									#Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')	


								else:
									response = "END Apologies, something went wrong... \n"
									# Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')

							elif level == 10:
								if userResponse==1:
								
									#Find account
									sql10a = account.objects.get(phonenumber=phoneNumber)
									
									if sql10a:
										newBal = sql10a.balance
										newBal =  newBal-15
									if Bal > 0:
										#Alert user of incoming Mpesa cash
										response = "END We are sending your withdrawal of\n"
										response += " KES 15/- shortly... \n"

										#Declare Params
										gateway =  AfricasTalkingGateway(username, apiKey)
										productName  = "Nerd Payments"
										currencyCode = "KES"	
										recipients =[{"phoneNumber": phoneNumber,"currencyCode": "KES","amount":1,"metadata":{"name":"Client","reason":"Withdrawal"}
														}]
										#Send B2c
										try: 
											responses = gateway.mobilePaymentB2CRequest(productName, recipients)
										except AfricasTalkingGatewayException as e:
											print("Received error response: ")	
									else:
										#Alert user of insufficient funds
										response = "END Sorry, you dont have sufficient\n"
										response += " funds in your account \n"	

									# Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')

								elif userResponse==2:
									#Find account
									sql10b = account.objects.get(phonenumber = phoneNumber)
									Bal = 100
									if sql10b:
										# Reduce balance
										Bal = sql10b.balance 	
										Bal  = Bal-16	
									if Bal > 0:
										#Alert user of incoming Mpesa cash
										response = "END We are sending your withdrawal of\n"
										response += " KES 2/- shortly... \n"

										#Declare Params
										gateway =  AfricasTalkingGateway(username, apiKey)
										productName  = "Nerd Payments"
										currencyCode = "KES"	
										recipients =[{"phoneNumber": phoneNumber,"currencyCode": "KES","amount":2,"metadata":{"name":"Client","reason":"Withdrawal"}
														}]
										#Send B2c
										try: 
											responses = gateway.mobilePaymentB2CRequest(productName, recipients)
										except AfricasTalkingGatewayException as e:
											print("Received error response: ")	
									else:
										#Alert user of insufficient funds
										response = "END Sorry, you dont have sufficient\n"
										response += " funds in your account \n"	

									# Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')
								elif userResponse ==3:
									sql10c = account.objects.get(phonenumber=phoneNumber)
									Bal = 100
									if sql10c:
										# Reduce balance
										Bal = sql10c.balance	
										Bal =  Bal-17

									if Bal > 0:
										#Alert user of incoming Mpesa cash
										response = "END We are sending your withdrawal of\n"
										response += " KES 17/- shortly... \n"

										#Declare Params
										gateway =  AfricasTalkingGateway(username, apiKey)
										productName  = "Nerd Payments"
										currencyCode = "KES"	
										recipients =[{"phoneNumber": phoneNumber,"currencyCode": "KES","amount":3,"metadata":{"name":"Client","reason":"Withdrawal"}
														}]
										#Send B2c
										try: 
											responses = gateway.mobilePaymentB2CRequest(productName, recipients)
										except AfricasTalkingGatewayException as e:
											print("Received error response: ")	
									else:
										#Alert user of insufficient funds
										response = "END Sorry, you dont have sufficient\n"
										response += " funds in your account \n"	

									# Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')

								else:	
									response = "END Apologies, something went wrong... \n"	
									return HttpResponse(response, content_type='text/plain')

							elif level == 11:
								#11d. Send money to person described
								response = "END We are sending KES 15/- \n"
								response += "to the loanee shortly. \n"

								#Find and update Creditor
								sql11d = account.objects.get(phonenumber=phoneNumber)
								Bal = 100
								if sql11d:
									 # Reduce balance
										Bal = sql11d.balance -15
									#Send loan only if  balance is above 0 
								if Bal > 0:

									#Find and update Debtor
									
									sql11d = account.objects.get(phonenumber=userResponse)
					
									Loan = sql11d.balance+15

									# SMS  Balance
									code = '20880'
									recipients = phoneNumber 
									message    = "We have sent 15/- to"+ userResponse +" If this is a wrong number the transaction will fail.Your  balance is "+ Bal + " Thank you."                                                                                                                                                                                                                                                                                                                                                  
									gateway    =  AfricasTalkingGateway(username, apikey)
									try:
										 results = gateway.sendMessage(recipients, message, code) 
									except AfricasTalkingGatewayException as e: 
										print("Encountered an error while sending: ") 

									
									sql11e = account(phonenumber= phoneNumber)
									sql11e.balance = Bal
									account.save() 

									#11f. Change level to 0
									sql11e = account(loan = Loan, phonenumber=phoneNumber,level=1)
									account.save

									#Declare Params
									gateway =  AfricasTalkingGateway(username, apiKey)
									productName  = "Nerd Payments"
									currencyCode = "KES"
									recipients =[{"phoneNumber": phoneNumber,"currencyCode": "KES","amount":1,"metadata":{"name":"Client","reason":"Withdrawal"}
														}]
									#Send B2c
									try:
										responses = gateway.mobilePaymentB2CRequest(productName, recipients)

									except AfricasTalkingGatewayException as e:
										
										print("Received error response:")	

									#respond
									response = "END We have sent money to"+ userResponse+  "\n"

								else:
										#respond
										response = "END Sorry we could not send the money. \n"	
										response += "Your dont have enough money. \n"

										# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')
							elif level == 12:
								if userResponse == "4":
									#Alert user of incoming Mpesa checkout
									response = "END You are repaying 1/-. We have sent the MPESA checkout...\n"
									response += "If you dont have a bonga pin, dial \n"
									response += "Dial dial *126*5*1# to create.\n"

									#Declare Params
									gateway =  AfricasTalkingGateway(username, apikey)
									productName  = "Nerd Payments"
									currencyCode = "KES"
									amount       = 15
									metadata     = {"Sacco Repayment":"Nerds","productId":"321"}
									#pass to gateway
									try:
									  transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
									
									except AfricasTalkingGatewayException as e:  
											print("Received error response: ")        	

									# Print the response onto the page so that our gateway can read it
									return HttpResponse(response, content_type='text/plain')
								elif userResponse == "5":
									#Alert user of incoming Mpesa checkout
									response = "END You are repaying 2/-. We have sent the MPESA checkout...\n"
									response += "If you dont have a bonga pin, dial \n"
									response += "Dial dial *126*5*1# to create.\n"

									#Declare Params
									gateway =  AfricasTalkingGateway(username, apikey)
									productName  = "Nerd Payments"
									currencyCode = "KES"
									amount       = 15
									metadata     = {"Sacco Repayment": "Nerds","productId": "321"}
									#pass to gateway
									try:
									  transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
									
									except AfricasTalkingGatewayException as e:
										print("Received error response: ")  		       	

									# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')
				else:
						#10. Check that user response is not empty
						if userResponse=="":
							#10a. On receiving a Blank. Advise user to input correctly based on level
							if level == 0:
								
								#10b. Graduate the user to the next level, so you dont serve them the same menu
								

								sql10b = session_levels(session_id = sessionId,phonenumber=phoneNumber,level=1)
								session_levels.save()

								#10c. Insert the phoneNumber, since it comes with the first POST
								

								sql10c = Microfinance(phonenumber = phoneNumber)
								sql10c.save()

								#10d. Serve the menu request for name
								response = "CON Please enter your name"

									# Print the response onto the page so that our gateway can read it
								return HttpResponse(response, content_type='text/plain')
										
									

							elif level ==  1:
								#10e. Request again for name - level has not changed...
								response = "CON Name not supposed to be empty. Please enter your name \n"

								# Print the response onto the page so that our gateway can read it
								return HttpResponse(response, content_type='text/plain')	
								

							elif level ==  2:
								#10f. Request for city again --- level has not changed...
								response = "CON City not supposed to be empty. Please reply with your city \n"

								# Print the response onto the page so that our gateway can read it
								return HttpResponse(response, content_type='text/plain')
									
								

							else:
								#10g. End the session
								response = "END Apologies, something went wrong... \n"

								# Print the response onto the page so that our gateway can read it
								return HttpResponse(response, content_type='text/plain')
						else:
								#11. Update User table based on input to correct level
								
									if level ==  0:
										#10b. Graduate the user to the next level, so you dont serve them the same menu

										sql10b = session_levels(session_id = sessionId,phonenumber=phoneNumber,level=1)
										session_levels.save()
										

										#10c. Insert the phoneNumber, since it comes with the first POST
										sql10c = Microfinance(phonenumber = phoneNumber)
										sql10c.save()

										#10d. Serve the menu request for name
										response = "CON Please enter your name"

										# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')
												
													
									elif level == 1:
										#11b. Update Name, Request for city
										sql11b = Microfinance.objects.get(phonenumber=phoneNumber)
										sql11b.name = userResponse
										sql11b.save()

										#11c. We graduate the user to the city level

										sql11c = session_levels.get(session_id=sessionId)
										sql11c.level =2
										sql11c.save()
										#We request for the city
										response = "CON Please enter your city"

										# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')
												
										
									elif level == 2:
										#11d. Update city
								
										sql11d = Microfinance.objects.get(phonenumber=phoneNumber)
										sql11d.city = userResponse
										sql11d.save()

										#11e. Change level to 0
										

										sql11e = session_levels.get(session_id=sessionId)
										sql11e.level =1
										sql11e.save()

										#11f. Serve the menu request for name
										response = "END You have been successfully registered. Dial *384*303# to choose a service."	        	   	

										# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')
											
																							
									else:
										#11g. Request for city again
										response = "END Apologies, something went wrong... \n"

										# Print the response onto the page so that our gateway can read it
										return HttpResponse(response, content_type='text/plain')

			except Microfinance.DoesNotExist as e:
							print('Microfinance not found')
				
								
							
