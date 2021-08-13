class House: #I want the house collection to be able to sort by Price, Mortgage, or Size, that's why they're integers initialized at 0.

    def __init__(self, address, price, mortgage, size, link):
        
        self.address = address
        self.price = price
        self.mortgage = mortgage
        self.size = size
        self.link = link

#getters and setters, though most likely not needed
    def getAddress(self):
        return address
    
    def getPrice(self):
        return price

    def getMortgage(self):
        return mortgage
    
    def getSize(self):
        return size

    def getLink(self):
        return link
    
    def setAddress(self, address):
        self.address = address
    
    def setPrice(self, price):
        self.price = price

    def setMortgage(self, mortgage):
        self.mortgage = mortgage
    
    def setSize(self, size):
        self.size = size

    def setLink(self, link):
        self.link = link

    def __eq__(self, obj):
        return self.address == obj.address
    
    def __lt__(self, obj):
        return self.price < obj.price
    
    def __le__(self, obj):
        return self.price <= obj.price
    
    def __gt__(self, obj):
        return self.price > obj.price

    def __ge__(self, obj):
        return self.price >= obj.price

    def __str__(self):
        result = address
        result += "\nSelling for: " + str(price)
        result += "\nEstimated Mortgage: " + str(mortgage)
        result += "\nSize (sqft): " + str(size)
        return result

class HouseCollection:
    def __init__(self):
        self.collection = []
    
    def add(self, house):
        if isinstance(house, House) == True:
            self.collection.append(house)
             
    #using merge sort algorithm
    def sort(self, arr, l, r):
        if len(arr) >1:
            mid = int(len(self.collection) / 2)
            L = self.collection[:mid]
            R = self.collection[mid:]

            sort(arr, L, R)
        
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i+=1
                k+=1
            else:
                arr[k] = R[j]
                j+=1
                k+=1
        
        #to catch the rest
        while i < len(L):
            arr[k] = L[i]
            i+=1
            k+=1
        
        while j < len(R):
            arr[k] = R[j]
            j+=1
            k+=1

    def getCollection(self):
        return self.collection
