import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as urlRequest

#Classes
class HouseCollection:
    def __init__(self):
        self.houses = []      
    
    def add(self, obj):
        if (isinstance(obj, House) == False):
            print("Object isn't of the type 'House'")
            return
        else:
            self.houses.append(obj)

    #what kinda sort am i gonna use bubble, merge, quick or whut
    #not bubble nor quick
    
    #returns house object at some position
    def getHouse(self, obj, position):
        return self.houses[position]
    
    #returns entire collection
    def getCollection(self):
        return self.houses

    
    def mergeSort(self, arr):
        if len(arr) > 1:
            mid = len(arr)//2
            
            L = arr[:mid]
            R = arr[mid:]

            self.mergeSort(L)
            self.mergeSort(R)

        
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i+=1
                else:
                    arr[k] = R[j]
                    j+=1
                k+=1

            #finds the spares.
            while i < len(L):
                arr[k] = L[i]
                i+=1
                k+=1
            while j < len(R):
                arr[k] = R[j]
                j+=1
                k+=1

    
    def mortgageMerge(self, arr):
        if len(arr) > 1:
            mid = len(arr)//2
            
            L = arr[:mid]
            R = arr[mid:]

            self.mergeSort(L)
            self.mergeSort(R)

        
            i = j = k = 0
            while i < len(L) and j < len(R):
                
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i+=1
                else:
                    arr[k] = R[j]
                    j+=1
                k+=1

            #finds the spares.
            while i < len(L):
                arr[k] = L[i]
                i+=1
                k+=1
            while j < len(R):
                arr[k] = R[j]
                j+=1
                k+=1
    #this the one to call in main
    def mSortPrices(self):
        self.mergeSort(self.houses)

    def mSortMortgage(self):
        self.mortgageMerge(self.houses)
        
class House:

    address = ""
    size =""
    price = 0
    mortgage = ""
    link = ""
    def __init__(self, address, size, price, mortgage, link):
        self.address = address
        self.size = size
        price = price.replace(",","").replace("$","")
        #price = price
        self.price = int(price)
        self.mortgage = self.findMortgage(mortgage)
        self.link = link


    def findMortgage(self, mort):
        #print("mort entered")
        temp = ""
        for letter in mort:
            if letter.isdigit():
                temp += letter
        #print(temp, "OOOOOOOOOOOOOOOO")
        return temp

    def __cmp__(self, other):
        if (isinstance(other, House) == True):
            if (other.price > self.price):
                return -1 #negative will be if this object is smaller than the other
            elif (other.price < self.price):
                return 1 #postitve will be if this object is larger than the other
            else:
                return 0 #objects are equal

    def __lt__(self, other):
        if (isinstance(other, House) == True):
            return self.price < other.price
    
    #k gonna use LE SPECIFICALLY TO COMPARE MORTGAGES AND ONLY MORTGAGES use LT for PRICES 
    def __le__(self, other):
        if (isinstance(other, House) == True):
            return int(self.mortgage) <= int(other.mortgage)
    #comparable methods are dunder - eq, lt, gt, ge, le, cmp
    #gonna use cmp
#End Classes-------------------------------------------------------------------------------

def getMortgage(base_website, full_house_link):
    if isinstance(base_website, str) and isinstance(full_house_link, str):
        #print(base_website + full_house_link)
        full_house_site = urlRequest(base_website + full_house_link)
        full_house_html = full_house_site.read()
        full_house_site.close()

        full_soup = soup(full_house_html, "html5lib")
        full_a_links = full_soup.find_all("div","Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 bjqKkI SummaryMortgageInfo__EstimatedMortgageText-sc-1os1zgj-0 LRvbQ")
        #print(full_a_links[0].text)

        return full_a_links[0].text
    
#making this a def so that I can code other part easier kinda
#def is gonna need soup that's already found, and collection i think?
def makeCollection(cards_found, house_collection):
    for card in cards_found:
        #print(card.find("div","Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 keMYfJ").text)
        prop_details = card.find_all("div","Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 dZyoXR")
        
        #checkers to see if the parts of the "House" object are prepared to be stored
        price_found = False
        size_found = False
        address_found = False
        
        try:
            prop_price = card.find("div", "Text__TextBase-sc-1cait9d-0-div Text__TextContainerBase-sc-1cait9d-1 keMYfJ").text
            price_found = True
        except:
            print("Price not found")

        try:
            prop_size = str(prop_details[0].text)
            size_found = True
        except:
            print("Size not found")

        try:
            prop_address = str(prop_details[1].text) + " " + str(prop_details[2].text)
            address_found = True
        except:
            print("Address not found")
        

        if (price_found and size_found and address_found):
            try:
                links_to_parse = card.find_all("a","PropertyCard__StyledLink-m1ur0x-3 dgzfOv")
                mortgage_string = getMortgage("https://www.trulia.com", str(links_to_parse[0]["href"]))
                house_collection.add(House(prop_address, prop_size, prop_price, mortgage_string, ("https://www.trulia.com" + str(links_to_parse[0]["href"]))))
                #print(prop_address, getMortgage("https://www.trulia.com", str(links_to_parse[0]["href"])))
            except:
                print("Link not found, House object not made")
    
def makeHtml(link):
    try:
        client = urlRequest(link)
        html = client.read()
        client.close()
        return html
    except:
        print("Something went wrong in makeHtml, check the link that was passed to it.")



def parsePages(link, max_pages):
#this is made specifically for trulia, no other realtor site
    houses_collection = HouseCollection()
    
    for count in range(max_pages) : 
        realtor_link = link + str(count+1) + "_p/" #searching homes in bridgeport ct
        print(realtor_link)
        realtor_html = makeHtml(realtor_link)
        realtor_soup = soup(realtor_html, "html5lib")
        property_cards = realtor_soup.find_all("div","Padding-sc-1tki7vp-0 kRVDgw")

        
        makeCollection(property_cards, houses_collection)
        print("Page:", str(count+1), "out of", str(max_pages), "complete.")

    houses_collection.mSortPrices()
    city_state_base = realtor_link.split("/")
    city_state = city_state_base[4] + "_" + city_state_base[3]
    print(city_state)
    fileName = "realty_for_trulia_" + city_state + ".csv"
    headers = "Location, Size, Price, Mortgage (Monthly), , , Listing Link\n"
    csv_for_realty = open(fileName,"w")
    csv_for_realty.write(headers)
    for i in range(len(houses_collection.getCollection())):
        house = houses_collection.getCollection()[i]
        csv_for_realty.write(house.address.replace(",", " ") + "," + house.size.replace(",", " ") + "," + "$"+str(house.price).replace(",", " ") + "," + str(house.mortgage) + "," + "," +"," + str(house.link) + "\n")
    csv_for_realty.close()

        
bridgeport_ct = "https://www.trulia.com/CT/Bridgeport/"
houston_tx = "https://www.trulia.com/TX/Houston/"
parsePages(houston_tx, 305)

