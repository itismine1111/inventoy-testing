import math, random

def generateOTP() :
 
    # Declare a string variable 
    # which stores all string
    string = '0123456789'
    OTP = ""
    length = len(string)
    for i in range(4) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP
 
# Driver code
if __name__ == "__main__" :
     
    print("OTP of length 4:", generateOTP())