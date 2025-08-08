import googlemaps
import pandas as pd

# Your Google Maps API Key
API_KEY = ''
gmaps = googlemaps.Client(key=API_KEY)

# List of Vancouver attractions
Attractions = ["Stanley Park", "Granville Island", "Vancouver Aquarium", "Museum of Anthropology at UBC",
               "VanDusen Botanical Garden", "Granville Island Public Market", "Queen Elizabeth Park", "Acadia Beach",
               "Vancouver Seawall", "Canada Place", "Science World", "Orpheum", "CF Pacific Centre", "Robson St",
               "Kitsilano Beach", "Bloedel Conservatory", "English Bay Beach", "Marine Building",
               "Vancouver Public Library - Central Library", "Kitsilano Beach Park", "Queen Elizabeth Theatre",
               "Dr. Sun Yat-Sen Classical Chinese Garden", "Rogers Arena", "BC Place", "Totem Poles",
               "Bill Reid Gallery of Northwest Coast Art", "Museum of Vancouver", "Vancouver Art Gallery",
               "False Creek", "Spanish Banks Beach", "Vancouver Convention Centre", "Nitobe Memorial Garden",
               "Jericho Beach Park", "Waterfront Station", "Lions Gate Bridge","Capilano Suspension Bridge Park",
               "Steveston Fisherman's Wharf", "Deer Lake Park", "Central Park", "Vancouver Maritime Museum"]

data = []

for place in Attractions:
    try:
        # Use text_search to find the place
        result = gmaps.places(query=place + ", Vancouver BC")
        if result['results']:
            info = result['results'][0]
            name = info.get('name')
            rating = info.get('rating', 'N/A')
            user_ratings_total = info.get('user_ratings_total', 'N/A')
            address = info.get('formatted_address', 'N/A')
            data.append([name, address, rating, user_ratings_total])
        else:
            data.append([place, "Not Found", "N/A", "N/A"])
    except Exception as e:
        print(f"Error for {place}: {e}")
        data.append([place, "Error", "N/A", "N/A"])

    # time.sleep(0.5) # Add delay to avoid hitting API rate limits

# Change to DataFrame
df = pd.DataFrame(data, columns=["Place_Name", "Address", "Rating", "User_Ratings"])

# Change to numeral
df["Rating"] = pd.to_numeric(df["Rating"], errors='coerce')
df["User_Ratings"] = pd.to_numeric(df["User_Ratings"], errors='coerce')

# Sort the dataset by Rating-First and User Ratings-Second
df_sorted = df.sort_values(by=["Rating", "User_Ratings"], ascending=[False, False])

# Save as CSV
df_sorted.to_csv("vancouver_attractions_sorted.csv", index=False, encoding='utf-8-sig')
print("Finished!")
