# in module ro baraye functionhaye omomi ke ziyad estefade mikonim misazim

def create_random_code(count):
    import random
    return random.randint(10**(count-1),(10**count)-1)

#-------------------------------------------------------------------
# az to internet site kavenegar ro peyda kardam ke ersale sms mikone
# 1. Install kavenegar module    
# 2. copy Python code az kavenegar site

from twilio.rest import Client
def send_sms(mobile_number, active_code):
        try:
                account_sid = '#'
                auth_token = '#'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                        from_='#',
                        body=f'Your Activation Code: {active_code}',
                        to=f'+1{mobile_number}'
                )
                print(message.sid)
        except Exception as error: 
                print (str(error))
                
#-------------------------------------------------------------------
import os
from uuid import uuid4                                                          # uuid4 srtring e random mide. Tekrari nemide.
class FileUpload:
        def __init__(self,dir,secondDir):
                self.dir=dir
                self.secondDir=secondDir
                
        def upload_to(self,instance,filename):
                filename, ext=os.path.splitext(filename)
                # return f"{self.dir}/{self.secondDir}/{uuid4}{ext}"       # baes mishe to db esme hich aksi yeksan nabashe
                return f"media/images/customer/{uuid4}{ext}"               # 
               
#-------------------------------------------------------------------
# in code chon ziyad tekrar shode inja minevisim
def price_by_delivery_tax(price,discount=0):
        delivery=50
        if price>3000:
            delivery=0
        tax= (price+delivery)*0.09                                              # 0.09%
        sum=price+delivery+tax
        sum=sum-(sum*discount/100)
        return int(sum),delivery,int(tax)                                       # int baraye round shodane
