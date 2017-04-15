from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from microfinance_callback.config import username,apikey
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from microfinance_callback.models import session_levels
from microfinance_callback.models import Microfinance
from microfinance_callback.models import account
from microfinance_callback.models import checkout

# Create your views here.
@csrf_exempt
def callback(request):



   if request.method == 'POST'and request.POST:

         sessionId = request.POST.get('sessionId')
         serviceCode=request.POST.get('serviceCode')
         phoneNumber=request.POST.get('phoneNumber')
         text=request.POST.get('text')
         now = datetime.datetime.now()
       

         
         
         textList= text.split('*')
         userResponse= textList[-1].strip()
         

         
         
         try:
                              #4. Check the level of the user from the DB and retain default level if none is found for this session
               session = Microfinance.objects.get(phonenumber = phoneNumber)
               level = session.level


         except Microfinance.DoesNotExist as e:
                  level=0     
               

         

         try:
            #create an account
            sql11A = account.objects.get(phonenumber=phoneNumber)
           

         except account.DoesNotExist as e:

            money=20.00

            sqlb = account(phonenumber=phoneNumber,balance=money)
            sqlb.save()
         try:

            result,created = Microfinance.objects.get_or_create(phonenumber=phoneNumber)
            if created:
               result.save()

         
         
            
                     #6. check if user is available and serve menu, if not register
            if result and result.name and result.city:
                     
                     #7. if user is fully registered, level 0 and 1 serve the basic menus, the rest allow for financial transaction
                     if level == 0 or level == 1:
                           #7a.check user typed something
                           if userResponse == "":
                                 if level == 0:
                                       #7b.Graduate user to next level and serve main menu
                                       session_level1 = Microfinance.objects.get(phonenumber = phoneNumber) 
                                       session_level1.level=1
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
                                       

                           if userResponse == '0':
                                    if level == 0:         
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
                                             
                           if userResponse == "":
                                 if level == 1:
                                       #7b.Graduate user to next level and serve main menu
                                       session_level1 = Microfinance.objects.get(phonenumber = phoneNumber) 
                                       session_level1.level=1
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
                                       

                           if userResponse == '1':
                                       
                                       if level == 1:
                                           
                                           #8d. call the user and bridge to a sales person
                                          response = "END Please wait while we place your call.\n"
                                           #make a call
                                          callFrom = "+254711082733"
                                          callTo   = phoneNumber
                                           #create a new instance of our awesome gateway class
                                          gateway = AfricasTalkingGateway(username,apikey)


                                          try:
                                             
                                             gateway.call(callFrom,callTo)
                                          except AfricasTalkingGatewayException as e:
                                              print("Encounted an error when calling:",e)
                                           #print respose so that the gateway can read it 
                                          
                                              
                                          return HttpResponse(response, content_type='text/plain')
                                          
                           if userResponse == '2':
                                 if level == 1:
                                     #8e. Ask how much and launch Mpesa Checkout to the user
                                    response = "CON How much are you depositing?\n"
                                    response += " 1. 19 Shilling.\n"
                                    response += " 2. 18 Shillings.\n"
                                    response += " 3. 17 Shillings.\n"        
                                     #update to level 9

                                    session_level9 = Microfinance.objects.get(phonenumber= phoneNumber)
                                    session_level9.level = 9
                                    session_level9.save() 
                                    
                                       
                                  #print respose so that the gateway can read it  
                                              
                                    return HttpResponse(response, content_type='text/plain')
                                    
                           if userResponse == '3':
                                 if level == 1:
                                     #8e. Ask how much and launch B2C to the user
                                    response = "CON How much are you Withdrawing?\n"
                                    response += " 1. 15 Shillings.\n"
                                    response += " 2. 16 Shillings.\n"
                                    response += " 3. 17 Shillings.\n"        
                                     #update to level 10

                                    session_level10 = Microfinance.objects.get(phonenumber= phoneNumber)
                                    session_level10.level = 10
                                    session_level10.save() 
                                          
                                  #print respose so that the gateway can read it  
                                              
                                    return HttpResponse(response, content_type='text/plain')
                                    
                           if userResponse == '4':
                                 if level == 1:
                                     #8e.send another user same money
                                    response = "CON You can only send 15 Shilling\n"
                                    response += "Enter a valid phonenumber (like 0722122122)\n"
                                    #Print the response onto the page so that our gateway can read it
                                    session_level11 = Microfinance.objects.get(phonenumber= phoneNumber)
                                    session_level11.level = 11
                                    session_level11.save() 
                                    level = session_level11.level
                                    return HttpResponse(response, content_type='text/plain')
                                    
                           if userResponse == '5':
                              
                              #Find account

                              sql10a = account.objects.get(phonenumber=phoneNumber)

                              if sql10a:
                                 # Reduce balance
                                 newBal = sql10a.balance
                                 newBal = newBal-5          

                                 if newBal > 0:
                                    
                                    #Print the response onto the page so that our gateway can read it
                                    response = "END Please wait while we load your airtime account.\n"

                                       # Search DB and the Send Airtime
                                    recipients=[ {"phoneNumber": phoneNumber ,"amount": "KES 5"}
                                                                  
                                                ]

                                    # #JSON encode
                                    # json_data = json.dumps(recipients)
                                  
                                    #Create an instance of ourawesome gateway class, pass your credentials
                                    
                                    try:
                                       results = AfricasTalkingGateway(username,apikey)
                                       results.sendAirtime(recipients) 
                                       #9e. Send user airtime
                                    

                                    except AfricasTalkingGatewayException as e:
                                       print('Airtime not sent')
                                    

                                    return HttpResponse(response, content_type='text/plain')
                                 else: 
                                    #Alert user of insufficient funds
                                    response = "END Sorry, you dont have sufficient\n"
                                    response += " funds in your account \n"   

                                    # Print the response onto the page so that our gateway can read it
                                    return HttpResponse(response, content_type='text/plain')
                                    


                           if userResponse == '6':
                                 if level == 1:
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
                                    
                           if userResponse == '7':
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
                                       response += "Name: "+sql7.name+"\n"   
                                       response += "City: "+ sql7.city+"\n"  
                                       response += "Balance: "+str(newBal)+"\n" 
                                       response += "Loan: "+str(newLoan)+"\n"                                                                                       
                                       #Print the response onto the page so that our gateway can read it
                                       return HttpResponse(response, content_type='text/plain')
                                                                
                     if level == 9:
                           session = Microfinance.objects.get(phonenumber = phoneNumber)
                           session.level = 0
                           session.save()


                           #9a. Collect Deposit from user, update db
                           if userResponse == '1':
                              #Alert user of incoming Mpesa checkout
                                 response = "END Kindly wait 1 minute for the Checkout.\n"
                                 
                                    #Declare Params
                                 gateway = AfricasTalkingGateway(username, apikey)
                                 productName  = "walk"
                                 currencyCode = "KES"
                                 amount       = 19
                                 metadata     = {"sacco":"walk","productId":"1060"}
                                 sqlz = checkout(status= 'pending', amount=amount,phonenumber=phoneNumber)
                                 sqlz.save()

                                 try:
                                    transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
                                 except AfricasTalkingGatewayException as e:
                                    print('received an error',e) 

                                 return HttpResponse(response, content_type='text/plain')
                                 

                           if userResponse == '2':
                              response = "END We have sent the MPESA checkout...\n"
                              response += "If you dont have a bonga pin, dial \n"
                              response += "Dial dial *126*5*1# to create.\n"

                              #Declare Params
                              gateway = AfricasTalkingGateway(username, apikey)
                              productName  = "walk"
                              currencyCode = "KES"
                              amount       = 18
                              metadata     = {"sacco":"walk","productId":"1060"}
                              #pass to gateway
                              sqlz = checkout(status= 'pending', amount=amount,phonenumber=phoneNumber)
                              sqlz.save()
                              try:
                                 transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
                              
                              except AfricasTalkingGatewayException as e:
                                  print("Received error response: ",e)       

                              #Print the response onto the page so that our gateway can read it
                              return HttpResponse(response, content_type='text/plain')
                              
                           if userResponse == '3':
                              #Alert user of incoming Mpesa checkout
                              response = "END We have sent the MPESA checkout...\n"
                              response += "If you dont have a bonga pin, dial \n"
                              response += "Dial dial *126*5*1# to create.\n"

                              #Declare Params
                              gateway =  AfricasTalkingGateway(username, apikey)
                              productName  = "walk"
                              currencyCode = "KES"
                              amount       = 3
                              metadata     = {"sacco":"walk","productId":"1060"}
                              #pass to gateway
                              sqlz = checkout(status= 'pending', amount=amount,phonenumber=phoneNumber)
                              sqlz.save()
                              try:
                                 transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
                              
                              except AfricasTalkingGatewayException as e:
                                 print ("Received error response: ",e)    

                              #Print the response onto the page so that our gateway can read it
                              return HttpResponse(response, content_type='text/plain') 
                             


                           else:
                              response = "END Apologies, something went wrong... \n"
                              # Print the response onto the page so that our gateway can read it
                              return HttpResponse(response, content_type='text/plain')
                              

                     if level == 10:
                           session = Microfinance.objects.get(phonenumber = phoneNumber)
                           session.level = 0
                           session.save()
                           if userResponse=='1':
                           
                              #Find account
                              sql10a = account.objects.get(phonenumber=phoneNumber)
                              
                              if sql10a:
                                 newBal = sql10a.balance
                                 newBal =  newBal-15
                              if newBal > 0:
                                 #Alert user of incoming Mpesa cash
                                 response = "END We are sending your withdrawal of\n"
                                 response += " KES 15/- shortly... \n"

                                 #Declare Params
                                 gateway =  AfricasTalkingGateway(username, apikey)
                                 productName  = "walk"
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
                              
                           if userResponse=='2':
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
                                 gateway =  AfricasTalkingGateway(username, apikey)
                                 productName  = "walk"
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
                              
                           if userResponse =='3':
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
                                 gateway =  AfricasTalkingGateway(username, apikey)
                                 productName  = "walk"
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
                              

                     if level == 11:
                          
                           session = Microfinance.objects.get(phonenumber = phoneNumber)
                           session.level = 0
                           session.save()

                           phone=userResponse

                           #11d. Send money to person described
                           response = "END We are sending KES 15/- \n"
                           response += "to the loanee shortly. \n"

                           #Find and update Creditor
                           sql11d = account.objects.get(phonenumber=phoneNumber)
                           Bal = 0
                           figure = 15
                           if sql11d:
                              
                               # Reduce balance
                              Bal = sql11d.balance - figure
                              #Send loan only if  balance is above 0 
                           if Bal > 0:
                             
                              Loan = sql11d.balance + figure
                              
                              Bal = 0

                              #create and update Debtor
                              
                              sql11d = account(phonenumber=userResponse,balance = Bal ,loan=Loan)
                              sql11d.save()
                  
                              

                              # SMS  Balance
                              code = '20880'
                              recipients = phoneNumber 
                              
                              message    = "We have sent 15/- to"+" "+ userResponse +" If this is a wrong number the transaction will fail.Your  balance is "+ str(Bal) + " Thank you."
      
                              
                              try:
                                 
                                 results = AfricasTalkingGateway(username,apikey)
                                 
                                 results.sendMessage(recipients,message) 
                                
                              except AfricasTalkingGatewayException as e: 
                                 print("Encountered an error while sending: ",e)  

                            

                              #Declare Params
                              
                              productName  = "walk"
                              currencyCode = "KES"
                              recipients =[{"phoneNumber": phoneNumber,"currencyCode": "KES","amount":1,"metadata":{"name":"Client","reason":"Withdrawal"}
                                             }]
                              #Send B2c
                              try:
                                 responses = AfricasTalkingGateway(username,apikey)
                                 responses.mobilePaymentB2CRequest(productName, recipients)

                              except AfricasTalkingGatewayException as e:
                                 
                                 print("Received error response:",e)   

                              #respond
                              response = "END We have sent money to"+ userResponse+  "\n"
                              

                              return HttpResponse(response,content_type='text/plain')

                           else:
                                 #respond
                                 response = "END Sorry we could not send the money. \n"   
                                 response += "Your dont have enough money. \n"

                                 # Print the response onto the page so that our gateway can read it
                                 
                                 return HttpResponse(response, content_type='text/plain')
                                 
                     if level == 12:
                           if userResponse == "4":
                              #Alert user of incoming Mpesa checkout
                              response = "END You are repaying 1/-. We have sent the MPESA checkout...\n"
                              response += "If you dont have a bonga pin, dial \n"
                              response += "Dial dial *126*5*1# to create.\n"

                              #Declare Params
                              gateway =  AfricasTalkingGateway(username, apikey)
                              productName  = "walk"
                              currencyCode = "KES"
                              amount       = 15
                              metadata     = {"sacco":"walk","productId":"1060"}
                              #pass to gateway
                              try:
                                transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
                              
                              except AfricasTalkingGatewayException as e:  
                                    print("Received error response: ",e)           

                              # Print the response onto the page so that our gateway can read it
                              return HttpResponse(response, content_type='text/plain')
                              
                           elif userResponse == "5":
                              #Alert user of incoming Mpesa checkout
                              response = "END You are repaying 2/-. We have sent the MPESA checkout...\n"
                              response += "If you dont have a bonga pin, dial \n"
                              response += "Dial dial *126*5*1# to create.\n"

                              #Declare Params
                              gateway =  AfricasTalkingGateway(username, apikey)
                              productName  = "walk"
                              currencyCode = "KES"
                              amount       = 15
                              metadata     = {"sacco":"walk","productId":"1060"}
                              #pass to gateway
                              try:
                                transactionId = gateway.initiateMobilePaymentCheckout(productName,phoneNumber,currencyCode,amount,metadata)
                              
                              except AfricasTalkingGatewayException as e:
                                 print("Received error response: ",e)                 

                              # Print the response onto the page so that our gateway can read it
                                 return HttpResponse(response, content_type='text/plain')
                                 
                                 
            else: #registering the user

                     

                     if created: #chek if user is in the microfinance tabe
                        
                        result.save()#save the user in the microfinance table
                        response= "CON Please enter your name"
                        
      
                        return HttpResponse(response, content_type='text/plain')
                     if not created:
                        if not result.name:
                           #save the name
                           result.name = userResponse
                           result.save()

                        
                           response= "CON Please enter your city"
                         
                           return HttpResponse(response, content_type='text/plain')
                     if not result.city:
                         #save the city
                           result.city = userResponse
                           result.level=1
                           result.save()

                        
                           response ="END You have successfully been registered"
                           return HttpResponse(response, content_type='text/plain')
                  
                        
                     

         except Exception as e:

                     print('exception', e)
          

                     #11g. Request for city again
                     response = "END Apologies, something is wrong... \n"

                     # Print the response onto the page so that our gateway can read it
                     return HttpResponse(response, content_type='text/plain')
                     









 
      
            
                        
                     
