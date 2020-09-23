import requests, json, time, csv, sys

#   Covers entire northern virginia
    # 38.837211,-77.412990 3 mi
    # 38.916717,-77.503911  4mi
    # 38.915541,-77.404331 3.5 mi
    # 39.025810,-77.393600 4 mi
    # 38.921594,-77.248507 4 mi
    # 38.843642,-77.284189 3.7 mi
    # 38.845399,-77.107912 4 mi
    # 38.756228,-77.477422 4.3 mi
    # 38.654806,-77.261290 8 mi
    # 38.758395,-77.139508 3.7mi
    # 38.826382,-77.660691 5 mi
    # 39.105553,-77.564537 6 mi
    # 38.828603, -77.455112 16 mi


businessList = []
apiKey = "YOURMAPSAPI"


coordinates = ["38.837211,-77.412990", "38.916717,-77.503911", "38.915541,-77.404331" , "39.025810,-77.393600"
                , "38.921594,-77.248507", "38.843642,-77.284189", "38.845399,-77.107912", "38.756228,-77.477422"
                , "38.654806,-77.261290", "38.758395,-77.139508", "38.826382,-77.660691", "39.105553,-77.564537"
                , "38.828603,-77.455112"]
radiusList = ["4800", "6400", "5600", "6400", "6400", "5950", "6400", "6900", "12800", "5950", "8000", "9600", "25000"]
numOfBusinesses = 0
duplicates = 0
searchType = ["nearbysearch", "textsearch"]
keyword = ["remodel", "kitchen+bath", "kitchen+cabinets", "kitchen+and+bath"]

def main():
    global numOfBusinesses
    global duplicates
    global keyword
    global searchType

    for k in range(len(keyword)):
        for z in range(2):
            print("Running turn: " + str(z))
            print("Search Type: " + searchType[z % 2])
            print("Keyword: " + keyword[k])
            start = time.time()

            businessFinder(searchType[z % 2], keyword[k])

            end = time.time()
            print("Total of " + str(numOfBusinesses) +" businesses found")
            print("Dublicates found: " + str(duplicates))
            print("New records: " + str(numOfBusinesses - duplicates))
            print("Took " + str(end - start) + "seconds")
            duplicates = 0
            time.sleep(10)
    
    print("Searching process completed.")
    print("Duplicates found: " + str(duplicates))
    print("Writing to file...")
    writeToFile(businessList)
    print("Writing Completed.")
    print("Done")

def businessFinder(sType, sWord):
    global numOfBusinesses
    numOfBusinesses = 0
    for k in range(len(radiusList)):
        response = requests.get("https://maps.googleapis.com/maps/api/place/"+ sType + "/json?" 
            + "location=" + coordinates[k]
            + "&radius=" + radiusList[k]
            + "&keyword=" + sWord # KEYWORD
            + "&query=" + sWord # KEYWORD
            + "&key=" + apiKey)

        while True:   
            result = response.json() 
            bList = result["results"] 

            if len(bList) == 0:
                print("PROBLEM DETECTED: " + result)
                break

            # iterate trough businesses
            for i in range(len(bList)):
                # Convert dict to JSON then JSON to Python dict
                info = json.dumps(bList[i])
                info = json.loads(info)
                numOfBusinesses += 1
                infoReader(info, numOfBusinesses)
            
            if "next_page_token" in result:
                response.close()
                time.sleep(5)
                response = requests.get("https://maps.googleapis.com/maps/api/place/"+ sType + "/json?" 
                    + "pagetoken=" + result["next_page_token"] # next page
                    + "&key=" + apiKey)  
            else:
                time.sleep(5)
                print("exited")
                break


def infoReader(info, k):
    print('.', end='', flush=True)
    if dublicateChecker(info):
        time.sleep(1)
        getter = requests.get("https://maps.googleapis.com/maps/api/place/details/json?"
            + "place_id=" + info["place_id"]
            + "&fields=name,website,formatted_phone_number,url"
            + "&key=" + apiKey)  
        result = getter.json() # creates json object
        result = result["result"]
        result = json.dumps(result)
        result = json.loads(result)

        business = {
            "place_id": info["place_id"],
            "name": info["name"],
        }
        if "address" in info:
            business["address"] = info["formatted_address"]
        if "formatted_phone_number" in result:
            business["phone"] = result["formatted_phone_number"]
        if "website" in result:
            business["website"] = result["website"]
        if "url" in result:
            business["google"] = result["url"]

        businessList.append(business)


def dublicateChecker(info):
    for i in range(len(businessList)):
        if info["place_id"] == businessList[i]["place_id"]:
            global duplicates
            duplicates += 1
            return False
    return True

def writeToFile(bList):
    keys = bList[0].keys()
    with open('test.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(bList)


if __name__ == "__main__":
    main()