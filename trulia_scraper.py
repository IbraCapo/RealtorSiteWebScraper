from requests_html import HTML, HTMLSession, AsyncHTMLSession
from Houses import House, HouseCollection
import time #gonna keep track of the time that each run takes based off my modifications


#Function to get and store links
def get_links(link):
    #basically loading the page that will be scraped
    s = HTMLSession()
    start_session = s.get(link)
    site = start_session.html
    
    #finds the sites that brings you to the page of all the houses that are for sale, not all the links on the page
    site_links = site.absolute_links 
    for linked_site in site_links:
        if (linked_site in links) == False:
            if linked_site.find("/p/ct/bridgeport") > 0:
                links.append(linked_site)
        else:
            print("There was a duplicate file out here man")
    

#finds how many pages are going to be gone through based off of .../x_p/ available from the bottom of the page that the program sees, not that I see
def get_max_pages(main_link):
    s = HTMLSession()
    html_session = s.get(main_link)
    this_site = html_session.html
    max_pages = int(this_site.find(".SearchResultsPagination__PageLinkList-jwrszk-1", first=True).find("li")[6].text)
    print("There's a max of ", str(max_pages), "pages.")

    return max_pages

def fetchData(): #House object needs address, price, mortgage, size, and the link
    s = HTMLSession()
    count = 0
    for link in links:
        count+= 1
        
        #print("ran through", count, "times")
        site = s.get(link).html
        #this one is for the side that has the address, beds, baths, and size
        success = success2 = success3 = False
        try:
            property_info = site.find(".kzUlfS",first=True)
            house_info = property_info.find("span")
            size = property_info.find("li")[2].text.replace(",","").replace(" sqft","")
            address = house_info[0].text.replace(", ", " ").replace(",", "") + " " + house_info[1].text.replace(", ", " ").replace(",","")
            success = True
            #print(address)
            #print(address, size)
        except:
            print("Couldn't find address or size")
        
        try:
            pricing_info = site.find(".eMsDQ")[1]
            price = pricing_info.find("h3", first=True).text.replace("$","").replace(",","")
            #print(price)
            success2 = True
        except:
            print("price not found")
        
        try:
            mortgage = ""
            for letter in pricing_info.find(".LRvbQ",first=True).text.split(" ")[2]:
                if letter.isdigit():
                    mortgage += letter

            #print(mortgage)
            success3 = True
            if success == success2 == success3 == True:
                
                
                houses.add(House(address, int(price), int(mortgage), int(size), link))
                
            if count%100 == 0:
                print(count, " times looped in fetch_data")
            else: print("Couldn't make a house object from",link)
        except:
            print("mortgage not found")


def main():
    website = "https://www.trulia.com/CT/Bridgeport/"#input("Enter the trulia website link that has the city and state on it: ")
    max_pages = get_max_pages(website)
    for i in range(max_pages):
        get_links(website + str(i+1) + "_p/")
        print("Completed", str(i+1), "pages out of", max_pages)

    fetchData()

    print(len(links))
    web_split = website.split("/")
    file_city = web_split[3]
    file_state = web_split[4]
    links_file = open("trulia_" + file_city + "_" + file_state + ".csv", "w") #every time the program is ran it SHOULD remove any houses that are no longer on the website
    headers = "Address, Price, Est Mortgage, Size, Website\n"
    links_file.write(headers)
    for x in houses.getCollection():
        links_file.write(x.address + "," + "$" + str(x.price) + "," + "$" + str(x.mortgage) + "," + str(x.size) + "sq. ft" + "," + x.link + "," + "\n")
    links_file.close()

startTime = time.perf_counter()
houses = HouseCollection()
links = []
main()
finalTime = time.perf_counter() - startTime

print("Program completed in", str(finalTime), "seconds.")