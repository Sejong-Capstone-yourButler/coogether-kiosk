import serial
import requests, json

print('serial ' + serial.__version__)

# Set a PORT Number & baud rate
PORT = 'COM6'
BaudRate = 9600

order = []
ARD= serial.Serial(PORT,BaudRate)

def Decode(A):
    A = A[:-2].decode()
    A = str(A)
    return A
    
def Ardread():
    global order
    temp = []
    if ARD.readable():
        LINE = ARD.readline()
        code=Decode(LINE) 
        print(code)

        if ('.' in code) :
            temp.append(code.split('.'))
            order.append(temp[0][1])

        elif (code == "주문 완료"):
            order_post()
            
        return code
    
    else : 
        print("읽기 실패 from _Ardread_")
        
def orderId_get(dishName):
    URL = 'https://bixby-eats-backend.herokuapp.com/restaurants/1/dishes'
    loginURL = "https://bixby-eats-backend.herokuapp.com/login"

    #owner login
    header = {'Content-Type' : "application/json"}
    data = {"email" : "owner@gmail.com", "password": "12345"}
    response = requests.post(loginURL, data)
    dict_str = response.text
    dict = json.loads(dict_str)    
    token = dict["token"]
    
    headers = {'Content-Type' : "application/json",
           'x-jwt' : token}
    
    response = requests.get(URL, headers=headers)
    #print(response.status_code)
    #print(response.text)
    dict_str = response.text
    dict = json.loads(dict_str)
    dishId = 0
    
    for a in dict["dishes"]:
        if (a["name"] == dishName) :
            dishId = a["id"]
            break
        
    return dishId

def order_post():
    URL = 'https://bixby-eats-backend.herokuapp.com/restaurants/1/'
    loginURL = "https://bixby-eats-backend.herokuapp.com/login"

    #client login
    headers = {'Content-Type' : "application/json"}
    data = {"email" : "client@gmail.com", "password": "12345"}
    response = requests.post(loginURL, data)
    dict_str = response.text
    dict = json.loads(dict_str)    
    token = dict["token"]

    #order
    orderlist = {}
    items = []
    
    for x in order:
        list = {}
        list["dishId"] = orderId_get(x)
        items.append(list)

    orderlist["items"] = items
    
    headers = {'Content-Type' : "application/json",
           'x-jwt' : token}

    response = requests.post(URL, headers=headers, data=json.dumps(orderlist))
    print(response.status_code)
    print(response.text)
    
    order.clear()

while (True):
    Ardread()
