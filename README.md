# Google-Maps-Scraper

Collects business listing information for a given keyword and region from Google Maps Places API.

Some notes:
1. Google only provides 60 listings per request, that is why the program sends multiple requests for small areas.
2. In most cases requests returns duplicate listings, I included a duplicate checker function that runs right before requesting further information from API about a spesific listing.
3. API is not consistant and also didnt allow multiple requests at a given time in my experiments, that is why I used time.sleep() wherever I needed. 
4. Since results from API are not consistant, the program runs multiple times to gather more listings. 
5. Results are written to a CSV file.
