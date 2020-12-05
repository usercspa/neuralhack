import imaplib 
import email 
from email.header import decode_header 
import webbrowser 
import os 
import csv  
filename = " "
  

username = ""  
  

password = " "  
  
imap = imaplib.IMAP4_SSL("imap.gmail.com") 
  

result = imap.login(username, password) 
 
imap.select('"[Gmail]/All Mail"',readonly = True)  fields = ['index', 'MESSAGE-ID', 'RAW MESSAGE'] 
  
response, messages = imap.search(None,'UnSeen') 
messages = messages[0].split() 
  
with open(filename, 'w') as csvfile:   
    cwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cwriter.writerow(fields)  
latest = int(messages[-1]) 
 
oldest = int(messages[0]) 
  
for i in range(latest, latest-20, -1): 
    
    res, msg = imap.fetch(str(i), "(RFC822)") 
      
                   
    with open(filename, 'w') as csvfile: 
       
        cwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1]) 
                new_row =[i,msg["MESSAGE-ID"],msg["Subject"]] 
            cwriter.writerow(new_row)
            
            
  
    for part in msg.walk(): 
        if part.get_content_type() == "text / plain": 
            
            body = part.get_payload(decode = True) 
            print(f'Body: {body.decode("UTF-8")}', ) 
