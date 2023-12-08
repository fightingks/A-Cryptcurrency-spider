"""
A cryptcurrency spider, get the data from CoinUnited.io

Methods:

Profit() --Use your authorization to get your account information, including profit, coin numbers.(In Developer Tools of Chrome/Edge, if you login into Coinunited.io and stay at the main page, you can find your tokens sent for "https://cu-api.com/newcuuser/api/private/margin/marginInfo?crypto=USDT&calcCoins=BTCUSDT")

Monitor() -- Set a maximun or/and minimun, and the function will monitor the market (default for BTCUSDT). If the price reach what you set, a messagebox will mention you.

main() -- The core function in this program. Search for the price of a certain currency, refer to the list in "crypt_list.txt".

realtime() -- Show the price (default for BTCUSDT) in real-time.
"""
import time
import requests
from tkinter import messagebox
import json
#import argparse

coinunited="https://cu-api.com/cumarket/api/market/getAllPriceInfo"

def Profit():
    headers = {"platform":"`web`",'Content-Type':'application/json',
    'X-authorization': '`Bearer <Your tokens after `Bearer>','Connection':'close'
    }  
    url="https://cu-api.com/newcuuser/api/private/margin/marginInfo?crypto=USDT&calcCoins=BTCUSDT"
    html=requests.get(headers=headers,url=url)
    coin_data=json.loads(html.text)
    Profit=coin_data["data"]["c11"]-coin_data["data"]["c12"]
    time.sleep(5)
    """Coins={}
    for coin in coin_data["data"]["coins"]:
        if coin["c34"]==0:
            continue
        Coins[coin["c20"]]={"Price":coin["collateralPrice"],"Num":coin["c34"]}"""
        #print(f"{coin['c20']}: {coin['collateralPrice']} * {coin['c34']}")      
    return Profit

"""
"Coins":[c20:{"Price":,"Num":c34}]
"""

def main(crypto_cur="BTCUSDT"):
    coin_http=requests.get(coinunited,headers={'Connection':'close'})
    if coin_http.status_code != 200:
        messagebox.showinfo("Attention",f"Connect failed: Status {coin_http.status_code}")
        exit()
    coin_inf=json.loads(coin_http.text)
    for coin in coin_inf:
        if coin["p"]==crypto_cur:
            val=coin["a"]
    return val,crypto_cur

def monitor(high_level=0,low_level=0,crypto_cur="BTCUSDT"):
    monitor= True
    print("Monitoring...")
    while monitor:
        val,crypto_cur=main(crypto_cur)
        if high_level!=0 and val> high_level:
            messagebox.showinfo("Attention",f"{crypto_cur} is higher than {high_level},Now {val}!")
            monitor = False
        if low_level!=0 and val< low_level:
            messagebox.showinfo("Attention",f"{crypto_cur} is lower than {low_level},Now {val}!")
            monitor = False
        time.sleep(3)


def realtime():
    val,crypto_cur=main()
    print(f"{crypto_cur}: {val}")
    time.sleep(20)

args= input("Please input m, p or r.\n")
if args == "m":
    print("######################################")
    print("#### Crypt-currency Price Monitor ####")
    print("######################################")
    while True:
        highlevel= input("High level:")
        lowlevel= input("Low level:")
        print("\n")
        if highlevel=="":
            highlevel="0"
        elif lowlevel=="":
            lowlevel="0"
        monitor(int(highlevel),int(lowlevel))
elif args == "p":
    print("######################################")
    print("############ Your Profit #############")
    print("######################################")
    while True:
        profit=Profit()
        print('%.2f'%profit)
elif args == "r":
    print("######################################")
    print("### Crypt-currency real-time Price ###")
    print("######################################")
    while True:
        realtime()

"""

#######################
### Aborted Program ###
#######################

#############################
### Use in Command Prompt ###
#############################
parser = argparse.ArgumentParser(description='Start earn money.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
parser.add_argument('function', choices=["-m","-p","-r",""],help='Choose functions: -m: monitor, -p: profit, -r: realtime')
args = parser.parse_args()
if args.function == "monitor":
    while True:
        monitor()
elif args.function == "profit":
    while True:
        Profit()
elif args.function == "realtime":
    while True:
        realtime()
"""

"""
    with open("./crypt_list.txt","r") as f:
        crypt_list=f.readlines() # To create a list to choose
"""
