'''
Created by Toyu#0001
https://github.com/ToyuAU/shopifymonitor

!!!Please Dont Delete This!!!
!!!DONT be a scum, Credit Owner!!!
'''
import requests
import colorama
from utility import *
from termcolor import *
import datetime
import time
import threading
import json
from discord_webhook import *
import random
colorama.init()
import ctypes

class Shopify:
    def __init__(self):
        self.first_run = True
        self.products = []
        self.proxies = Data().loadProxies('proxies.txt')
        self.sites = [
            #Add Sites Here! Either do base url without / or a collection without the / 
            #For example "https://www.culturekings.com.au/collections/nike"
            "Site1",
            "etc"
        ]
        self.in_stock = {}
        self.run_number = 0

    def LOG(self, stats, text, color):
        print(colored(f"[{datetime.datetime.now()}] [{stats}] {text}", color))
    
    def update_status(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Shopify Monitor | https://github.com/ToyuAU/shopifymonitor | Run: {str(self.run_number)} | Items In Stock: {len(self.in_stock.keys())}")
    
    def alert(self, title, url, image_url, sizes, site, price):
        webhook = DiscordWebhook(url="WEBHOOK URL", username="Trinity Monitors")
        embed = DiscordEmbed(title=str(title), color="00FF00", url=url)
        embed.set_author(name=str(site), url=str(site))
        embed.add_embed_field(name="**Price**", value=str(price), inline=False)
        embed.add_embed_field(name="**Sizes**", value="".join(sizes), inline=False)
        embed.set_timestamp()
        embed.set_thumbnail(url=image_url)
        embed.set_footer(text="Trinity Monitors | Version Beta")
        webhook.add_embed(embed)
    def pick_proxy(self):
        proxies = random.choice(self.proxies)
        return proxies

    def check_stock(self, site):
        keywords = [
            "jordan 1",
            "jordan 2",
            "jordan 3", 
            "jordan 4", 
            "jordan 5", 
            "jordan 6", 
            "jordan 7",
            "jordan 8"
            "jordan 9", 
            "jordan 10", 
            "jordan 11", 
            "jordan 12", 
            "jordan 13", 
            "yeezy", 
            "dunk",
            "dunk low",
            "dunk high",
            "2002r",
            "550",
            "sacai"
        ]

        site_stripped = site.split("/")
        site_stripped = "https://"+site_stripped[2]
        try:
            headers = {
                'method': 'GET',
                'scheme': 'https',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
            }
            r = requests.get(site+"/products.json?limit=300", headers=headers, timeout=10, proxies=self.pick_proxy())
        except Exception as e:
            self.LOG("REQUESTS", "Failed to get Site.... Error {}".format(e), "red")
            time.sleep(5)
            return
        
        if r.status_code == 200:
            try:
                json_data = json.loads(r.text)
            except:
                self.LOG("JSON", "Failed to create JSON....", "red")
                time.sleep(5)
                return

            current_stock = []
            for product in json_data["products"]:
                sizes = []
                for keyword in keywords:
                    if keyword.lower() in product["title"].lower():
                        current_stock.append(product["id"])
                        if product['id'] not in self.in_stock.keys():
                            self.in_stock.update({product['id']:site})
                            if self.first_run == False:
                                self.LOG("CHECKER", f"New Product! Name: {product['title']}", "green")
                                for variant in product["variants"]:
                                    if variant["available"] == True:
                                        sizes.append(f'{variant["title"]} | **[ATC]({site_stripped}/cart/{variant["id"]}:1)**\n')
                                if sizes:
                                    price = product["variants"][0]["price"]
                                    self.alert(product["title"], f"{site_stripped}/products/"+product["handle"], product["images"][0]["src"], sizes, site_stripped, str(price))
            for product in list(self.in_stock.keys()):
                if product not in current_stock:
                    if self.in_stock[product] == site:
                        self.LOG("PRODUCT", "Removed product: "+str(product),'red')
                        self.in_stock.pop(product)

        else:
            self.LOG("REQUESTS", f"Failed to get site: {site} | Text: {r.content} | Response: {str(r.status_code)}", "red")
            time.sleep(10)
            return
                
    def monitor(self):
        while True:
            self.run_number += 1
            start = time.time()
            self.LOG("CHECKER", "Checking Stock...", "yellow")
            self.update_status()
            threads = []
            for site in self.sites:
                t = threading.Thread(target=self.check_stock, args=(str(site),))
                threads.append(t)
            
            for t in threads:
                t.start()
            
            for t in threads:
                t.join()
            self.first_run = False
            finish = time.time()

            self.LOG("CHECKER", f"No Stock! Run Time: {str(round(finish - start))}s", "red")
            current = ",".join(str(i) for i in self.in_stock)
            #Remove Sleep if you want but if you dont have proxies set to 10 if you have little set to 1
            time.sleep(1)

Shopify().monitor()
