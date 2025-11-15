# generate_data.py
import os
import csv

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Hotels sample (city, name, price_per_night, rating, lat, lon, image, link)
hotels = [
    ["city", "name", "price", "rating", "Address" ],
    # ---------------------- London ----------------------
    ["London", "Parkside Inn", 95, 3.7, "12 Park Lane, London"],
    ["London", "London Grand Hotel", 220, 4.6, "88 Westminster Rd, London"],
    ["London", "Budget Stay London", 60, 3.2, "4 Baker St, London"],
    ["London", "Thames Riverside Hotel", 180, 4.4, "210 Riverside Walk, London"],
    ["London", "The Royal Suites", 260, 4.8, "1 Royal Crescent, London"],
    ["London", "Central Hostel London", 45, 2.9, "6 Oxford Rd, London"],
    ["London", "The Blue Orchid Inn", 120, 4.1, "14 Kensington Ave, London"],
    ["London", "London Luxe Palace", 320, 4.9, "5 Regent St, London"],
    ["London", "City Comfort Hotel", 110, 4.0, "72 Piccadilly St, London"],
    ["London", "Green Gardens Hotel", 130, 4.3, "33 Hyde Park Rd, London"],
    ["London", "Urban Budget Inn", 55, 3.0, "9 Camden St, London"],
    ["London", "Heritage Plaza", 200, 4.5, "18 Victoria St, London"],
    ["London", "The Traveller's Nest", 70, 3.4, "22 Soho Lane, London"],
    ["London", "The Comfort Suites", 140, 4.2, "31 Marble Arch Rd, London"],
    ["London", "Riverside Boutique Hotel", 175, 4.6, "3 Thames Blvd, London"],

    # ---------------------- Paris ----------------------
    ["Paris", "Hotel Lumiere", 150, 4.5, "7 Rue de Lyon, Paris"],
    ["Paris", "Paris Budget Stay", 65, 3.1, "15 Rue Claude, Paris"],
    ["Paris", "Eiffel View Hotel", 210, 4.7, "9 Rue Tour Eiffel, Paris"],
    ["Paris", "Champs Elysees Retreat", 260, 4.8, "80 Avenue des Champs-Élysées, Paris"],
    ["Paris", "Cosy Corner Inn", 90, 3.8, "3 Rue Lafayette, Paris"],
    ["Paris", "Hotel de Belleville", 120, 4.0, "33 Rue Belleville, Paris"],
    ["Paris", "Royal Paris Suites", 310, 4.9, "5 Rue Royale, Paris"],
    ["Paris", "Paris Garden Hotel", 130, 4.2, "21 Rue du Jardin, Paris"],
    ["Paris", "The French Escape", 160, 4.3, "18 Rue Provence, Paris"],
    ["Paris", "Urban Stay Paris", 75, 3.4, "11 Rue Montmartre, Paris"],
    ["Paris", "Hotel Opera House", 185, 4.4, "10 Rue Opera, Paris"],
    ["Paris", "Paris Central Inn", 100, 3.9, "17 Rue Paris Nord, Paris"],
    ["Paris", "Vintage Paris Hotel", 140, 4.1, "4 Rue Vieux Paris, Paris"],
    ["Paris", "Paris Emerald Suites", 270, 4.7, "8 Rue du Louvre, Paris"],
    ["Paris", "Hotel Montparnasse", 155, 4.2, "12 Avenue Montparnasse, Paris"],

    # ---------------------- New York ----------------------
    ["New York", "Times Square Central", 200, 4.4, "44 Broadway, NY"],
    ["New York", "NY Budget Lodge", 75, 3.0, "88 8th Ave, NY"],
    ["New York", "Empire Luxury Suites", 330, 4.8, "12 Empire Blvd, NY"],
    ["New York", "Central Park Hotel", 250, 4.6, "5 Central Park West, NY"],
    ["New York", "SoHo Urban Stay", 150, 4.2, "77 SoHo Street, NY"],
    ["New York", "Manhattan Riverside", 230, 4.5, "9 Riverside Dr, NY"],
    ["New York", "Queens Comfort Inn", 90, 3.5, "11 Queens St, NY"],
    ["New York", "Brooklyn Grand Hotel", 160, 4.0, "15 Brooklyn Avenue, NY"],
    ["New York", "Harlem Budget Inn", 70, 3.1, "22 Harlem Rd, NY"],
    ["New York", "5th Avenue Plaza", 310, 4.7, "2 Fifth Avenue, NY"],
    ["New York", "Times Boutique Suites", 270, 4.6, "6 Times Square, NY"],
    ["New York", "CityLights Hotel", 190, 4.3, "9 Madison Ave, NY"],
    ["New York", "The Manhattan Palace", 350, 4.9, "1 Manhattan Tower, NY"],
    ["New York", "NY Classic Stay", 140, 4.1, "14 Park Avenue, NY"],
    ["New York", "UrbanView NY", 120, 3.9, "31 Lexington St, NY"],

    # ---------------------- Tokyo ----------------------
    ["Tokyo", "Shinjuku Plaza Hotel", 140, 4.2, "11 Shinjuku St, Tokyo"],
    ["Tokyo", "Tokyo Capsule Stay", 45, 3.3, "3 Akihabara St, Tokyo"],
    ["Tokyo", "Imperial Tokyo Suites", 300, 4.8, "2 Chiyoda Palace, Tokyo"],
    ["Tokyo", "Tokyo Bay Resort", 220, 4.6, "19 Tokyo Bay Rd, Tokyo"],
    ["Tokyo", "Ueno Garden Hotel", 100, 4.0, "66 Ueno Park Ave, Tokyo"],
    ["Tokyo", "Shibuya Central Inn", 95, 3.9, "7 Shibuya Crossing, Tokyo"],
    ["Tokyo", "Tokyo Metro Hotel", 130, 4.1, "20 Metro Line Blvd, Tokyo"],
    ["Tokyo", "Sakura Blossom Inn", 160, 4.4, "13 Sakura St, Tokyo"],
    ["Tokyo", "Ginza Exclusive Suites", 320, 4.9, "4 Ginza Avenue, Tokyo"],
    ["Tokyo", "Budget Stay Tokyo", 55, 3.0, "21 Asakusa Rd, Tokyo"],
    ["Tokyo", "Tokyo Tower View Hotel", 180, 4.5, "3 Tower Lane, Tokyo"],
    ["Tokyo", "Shinagawa Comfort Hotel", 120, 4.1, "5 Shinagawa St, Tokyo"],
    ["Tokyo", "Urban Tokyo Hotel", 110, 3.8, "9 Minato Rd, Tokyo"],
    ["Tokyo", "Cherry Blossom Hotel", 200, 4.6, "12 Sakura Ave, Tokyo"],
    ["Tokyo", "Hotel Kiyoshi", 90, 3.7, "16 Kyoto Rd, Tokyo"],

    # ---------------------- Dubai ----------------------
    ["Dubai", "Dubai Marina Hotel", 180, 4.5, "22 Marina Walk, Dubai"],
    ["Dubai", "Budget Sands Inn", 65, 3.2, "3 Deira St, Dubai"],
    ["Dubai", "Palm Island Resort", 420, 4.9, "1 Palm Jumeirah, Dubai"],
    ["Dubai", "Desert Mirage Hotel", 250, 4.6, "19 Al Sahara Rd, Dubai"],
    ["Dubai", "Gold Souk Stay", 110, 4.0, "7 Souk St, Dubai"],
    ["Dubai", "Dubai Skyline Suites", 330, 4.8, "10 Sheikh Zayed Rd, Dubai"],
    ["Dubai", "Dubai Creek Inn", 140, 4.2, "5 Creek Road, Dubai"],
    ["Dubai", "Oasis Comfort Hotel", 130, 4.1, "11 Oasis Ave, Dubai"],
    ["Dubai", "Palm View Suites", 350, 4.7, "2 Crescent Rd, Dubai"],
    ["Dubai", "UrbanStay Dubai", 95, 3.7, "6 Downtown Blvd, Dubai"],
    ["Dubai", "Dubai Royal Palace", 500, 5.0, "1 Royal District, Dubai"],
    ["Dubai", "The Burj Vista Hotel", 390, 4.9, "1 Burj Lane, Dubai"],
    ["Dubai", "Dubai Modern Inn", 120, 4.0, "8 Future St, Dubai"],
    ["Dubai", "Creekside Boutique Hotel", 150, 4.3, "21 Creekside Rd, Dubai"],
    ["Dubai", "Desert Budget Stay", 55, 2.9, "34 Sand Road, Dubai"],

    # ---------------------- Sydney ----------------------
    ["Sydney", "Harbour View Hotel", 190, 4.4, "5 Harbour Rd, Sydney"],
    ["Sydney", "Sydney Budget Inn", 70, 3.1, "10 George St, Sydney"],
    ["Sydney", "Opera House Suites", 260, 4.8, "1 Opera House Lane, Sydney"],
    ["Sydney", "Bondi Beach Resort", 220, 4.6, "8 Bondi Beach Rd, Sydney"],
    ["Sydney", "Downtown Comfort Hotel", 120, 4.0, "17 Pitt St, Sydney"],
    ["Sydney", "Darling Harbour Plaza", 240, 4.5, "9 Darling Rd, Sydney"],
    ["Sydney", "UrbanStay Sydney", 110, 3.8, "25 Oxford St, Sydney"],
    ["Sydney", "Sydney Skyline Suites", 280, 4.7, "3 Skyline Ave, Sydney"],
    ["Sydney", "Southern Cross Hotel", 160, 4.2, "13 Cross Rd, Sydney"],
    ["Sydney", "Harbour Budget Stay", 60, 3.0, "7 Wharf Rd, Sydney"],
    ["Sydney", "Sydney Central Lodge", 140, 4.1, "22 Kent St, Sydney"],
    ["Sydney", "Emerald Bay Hotel", 210, 4.4, "12 Bayview Rd, Sydney"],
    ["Sydney", "Sydney Luxe Palace", 350, 4.9, "2 Royal Ave, Sydney"],
    ["Sydney", "Opera View Inn", 180, 4.3, "19 Opera St, Sydney"],
    ["Sydney", "Pacific Breeze Hotel", 150, 4.2, "3 Pacific Rd, Sydney"],

    # ---------------------- Toronto ----------------------
    ["Toronto", "Downtown Toronto Inn", 130, 4.1, "17 Queen St, Toronto"],
    ["Toronto", "Maple Budget Stay", 65, 3.0, "22 Maple Rd, Toronto"],
    ["Toronto", "CN Tower View Hotel", 210, 4.6, "1 SkyDome Blvd, Toronto"],
    ["Toronto", "Toronto Grand Suites", 280, 4.7, "9 King St, Toronto"],
    ["Toronto", "Lakeside Comfort Inn", 150, 4.2, "4 Lakeshore Dr, Toronto"],
    ["Toronto", "UrbanStay Toronto", 95, 3.6, "77 College St, Toronto"],
    ["Toronto", "Royal Ontario Hotel", 310, 4.8, "11 Royal Ave, Toronto"],
    ["Toronto", "Toronto Midtown Hotel", 170, 4.3, "32 Yonge St, Toronto"],
    ["Toronto", "Budget Toronto Lodge", 55, 3.1, "6 Bloor St, Toronto"],
    ["Toronto", "The Maple Leaf Suites", 260, 4.7, "10 Maple Leaf Rd, Toronto"],
    ["Toronto", "CityCenter Toronto", 140, 4.0, "15 Dundas St, Toronto"],
    ["Toronto", "Harbourfront Inn", 180, 4.4, "2 Harbourfront Rd, Toronto"],
    ["Toronto", "The Toronto Palace", 320, 4.9, "3 Palace Rd, Toronto"],
    ["Toronto", "SkyView Toronto Hotel", 230, 4.5, "12 SkyView Ave, Toronto"],
    ["Toronto", "Toronto Urban Inn", 100, 3.8, "29 Lawrence Ave, Toronto"]
]



# Restaurants sample (city,name,cuisine,price_per_person,rating,address,lat,lon,image,link)
restaurants = [
    ["city","name","cuisine","price","rating","address"],

    # ---------------------- LONDON ----------------------
    ["London","Tokyo Garden","Japanese",35,4.5,"12 Sakura St, London"],
    ["London","Samurai Grill","Japanese",28,4.2,"88 Shinjuku Rd, London"],
    ["London","Ramen Central","Japanese",15,3.9,"4 Udon Lane, London"],
    ["London","Sushi Palace","Japanese",42,4.7,"21 Sushi Ave, London"],
    ["London","Ninja Noodles","Japanese",18,4.0,"16 Kyoto Rd, London"],
    ["London","Koi Bento House","Japanese",22,4.1,"33 Tokyo Blvd, London"],

    ["London","Roma Bella","Italian",30,4.3,"19 Roma St, London"],
    ["London","Pasta Veloce","Italian",18,4.0,"7 Veneto Rd, London"],
    ["London","Venice Dine","Italian",40,4.6,"1 Venetian Walk, London"],
    ["London","Trattoria Milano","Italian",28,4.2,"3 Milano Ln, London"],
    ["London","Mamma Mia Cafe","Italian",20,3.8,"11 Napoli St, London"],
    ["London","Bella Italia House","Italian",33,4.4,"8 Tuscany Rd, London"],

    ["London","Turkish Flame","Turkish",27,4.2,"6 Istanbul St, London"],
    ["London","Sultans Grill","Turkish",35,4.5,"22 Ottoman Rd, London"],
    ["London","Kebab House London","Turkish",15,3.9,"3 Kebab Ln, London"],
    ["London","Ankara Delight","Turkish",30,4.3,"12 Ankara Ave, London"],
    ["London","Mediterranean Meze","Turkish",24,4.1,"5 Bosphorus Rd, London"],
    ["London","Golden Baklava","Turkish",18,4.0,"9 Marmara St, London"],

    ["London","Royal English Kitchen","English",25,4.1,"17 Thames St, London"],
    ["London","London Fry House","English",14,3.7,"3 Pavilion Rd, London"],
    ["London","The British Roast","English",22,4.3,"6 Kensington St, London"],
    ["London","Ye Olde Tavern","English",35,4.5,"77 King St, London"],
    ["London","Fish & Chips Corner","English",12,3.8,"1 Dockside Ln, London"],
    ["London","The English Plate","English",28,4.2,"10 Victoria Rd, London"],

    ["London","Spice of India","Indian",20,4.1,"33 Curry Ave, London"],
    ["London","Bombay Palace","Indian",32,4.6,"9 Bombay St, London"],
    ["London","Masala Street","Indian",18,3.9,"6 Masala Ln, London"],
    ["London","Delhi Flavours","Indian",25,4.3,"14 Delhi Rd, London"],
    ["London","Tandoori Nights","Indian",28,4.4,"2 Punjab Ave, London"],
    ["London","Curry House London","Indian",15,3.8,"21 Spice Rd, London"],


    # ---------------------- PARIS ----------------------
    ["Paris","Sakura Blossom","Japanese",32,4.4,"10 Rue Sakura, Paris"],
    ["Paris","Ninja Ramen","Japanese",20,3.9,"4 Rue Tokyo, Paris"],
    ["Paris","Kyoto Sushi Bar","Japanese",38,4.6,"18 Rue Kyoto, Paris"],
    ["Paris","Bento Street Paris","Japanese",16,3.8,"2 Rue Osaka, Paris"],
    ["Paris","Shogun Grill","Japanese",28,4.2,"11 Rue Samurai, Paris"],
    ["Paris","Ginza Fresh","Japanese",34,4.3,"7 Rue Ginza, Paris"],

    ["Paris","Bella Roma Paris","Italian",30,4.2,"19 Rue Roma, Paris"],
    ["Paris","Pasta Du Jour","Italian",22,4.1,"9 Rue Pasta, Paris"],
    ["Paris","Trattoria Parisienne","Italian",40,4.7,"3 Rue Milano, Paris"],
    ["Paris","Veneto Bistro","Italian",27,4.0,"14 Rue Veneto, Paris"],
    ["Paris","Napoli Maison","Italian",35,4.5,"8 Rue Napoli, Paris"],
    ["Paris","Tuscany Table","Italian",31,4.3,"22 Rue Tuscany, Paris"],

    ["Paris","Istanbul Magic","Turkish",26,4.1,"17 Rue Istanbul, Paris"],
    ["Paris","Ottoman Grill Paris","Turkish",33,4.4,"2 Rue Sultan, Paris"],
    ["Paris","Meze House Paris","Turkish",20,3.8,"9 Rue Meze, Paris"],
    ["Paris","Ankara Flame","Turkish",28,4.2,"6 Rue Ankara, Paris"],
    ["Paris","Turkish Delight Cafe","Turkish",18,3.9,"11 Rue Marmara, Paris"],
    ["Paris","Golden Kebab","Turkish",15,3.7,"5 Rue Antalya, Paris"],

    ["Paris","French-English Bistro","English",29,4.1,"25 Rue London, Paris"],
    ["Paris","Traditional Roast House","English",34,4.4,"7 Rue Royale, Paris"],
    ["Paris","Fish & Chips Paris","English",17,3.8,"2 Rue Britannia, Paris"],
    ["Paris","The English Manor","English",40,4.7,"11 Rue Windsor, Paris"],
    ["Paris","British Brunch Cafe","English",22,4.0,"12 Rue Cambridge, Paris"],
    ["Paris","London Pie House","English",15,3.6,"8 Rue Scotland, Paris"],

    ["Paris","Curry Palace Paris","Indian",27,4.2,"6 Rue Curry, Paris"],
    ["Paris","Delhi House Paris","Indian",22,4.0,"2 Rue Delhi, Paris"],
    ["Paris","Bombay Spice","Indian",18,3.7,"3 Rue Bombay, Paris"],
    ["Paris","Tandoori Garden","Indian",32,4.5,"16 Rue Punjab, Paris"],
    ["Paris","Indian Flavour Street","Indian",20,3.9,"7 Rue India, Paris"],
    ["Paris","Masala Time Paris","Indian",25,4.3,"9 Rue Masala, Paris"],


    # ---------------------- NEW YORK ----------------------
    ["New York","Samurai NY","Japanese",38,4.6,"5 Tokyo St, NY"],
    ["New York","Ramen Hub NY","Japanese",14,3.8,"2 Ramen Rd, NY"],
    ["New York","Sushi Empire Manhattan","Japanese",48,4.7,"1 Shibuya Ave, NY"],
    ["New York","Bento Express","Japanese",19,4.0,"8 Bento Ln, NY"],
    ["New York","Kyoto Flame","Japanese",29,4.3,"11 Kyoto Blvd, NY"],
    ["New York","Ginza Street NY","Japanese",33,4.2,"4 Ginza Rd, NY"],

    ["New York","Italiano Metro","Italian",32,4.3,"9 Rome Ave, NY"],
    ["New York","Pasta Republic","Italian",20,4.0,"3 Pasta St, NY"],
    ["New York","Napoli Grande","Italian",45,4.6,"12 Napoli Ave, NY"],
    ["New York","Milano Chef","Italian",28,4.2,"7 Milano Blvd, NY"],
    ["New York","Tuscan Table NY","Italian",38,4.5,"2 Tuscany Ln, NY"],
    ["New York","Venice Piazza","Italian",41,4.7,"18 Venice Rd, NY"],

    ["New York","Istanbul Grill NY","Turkish",29,4.2,"4 Istanbul Rd, NY"],
    ["New York","Sultan Palace NY","Turkish",36,4.5,"15 Ottoman Ave, NY"],
    ["New York","Kebab Brothers","Turkish",16,3.7,"6 Kebab St, NY"],
    ["New York","Turkish Meze Bar","Turkish",24,4.1,"11 Meze Ln, NY"],
    ["New York","Ankara Kitchen","Turkish",30,4.3,"19 Ankara Blvd, NY"],
    ["New York","Golden Baklava NY","Turkish",21,4.0,"8 Marmara Rd, NY"],

    ["New York","NY English Diner","English",21,4.0,"17 British St, NY"],
    ["New York","Big Apple Roast House","English",38,4.6,"3 Regent Ave, NY"],
    ["New York","Fish & Chips Manhattan","English",16,3.7,"7 Dock Rd, NY"],
    ["New York","Empire English Pub","English",29,4.3,"11 Windsor Blvd, NY"],
    ["New York","The Royal Plate NY","English",34,4.5,"1 Crown Ln, NY"],
    ["New York","English Corner NY","English",19,3.8,"9 London Rd, NY"],

    ["New York","Curry Town NY","Indian",23,4.1,"3 Curry St, NY"],
    ["New York","Bombay Bistro NY","Indian",32,4.4,"12 Bombay Ln, NY"],
    ["New York","Delhi Street Kitchen","Indian",20,3.9,"1 Delhi Ave, NY"],
    ["New York","Tandoori Grill NY","Indian",30,4.5,"5 Punjab St, NY"],
    ["New York","Masala Fusion","Indian",18,3.8,"7 Spices Rd, NY"],
    ["New York","Indian Paradise NY","Indian",28,4.3,"14 Curry Hill, NY"],


    # ---------------------- TOKYO ----------------------
    ["Tokyo","Sakura Sky Restaurant","Japanese",42,4.7,"3 Shinjuku Rd, Tokyo"],
    ["Tokyo","Ramen Masters","Japanese",12,3.8,"6 Udon St, Tokyo"],
    ["Tokyo","Sushi Ginza Tokyo","Japanese",50,4.9,"1 Ginza Blvd, Tokyo"],
    ["Tokyo","Bento Craft","Japanese",18,4.1,"9 Osaka Rd, Tokyo"],
    ["Tokyo","Kyoto Eats","Japanese",25,4.3,"4 Kyoto Ave, Tokyo"],
    ["Tokyo","Shogun Sushi House","Japanese",35,4.5,"8 Samurai St, Tokyo"],

    ["Tokyo","Italian Sky","Italian",29,4.3,"10 Roma St, Tokyo"],
    ["Tokyo","Tokyo Pasta House","Italian",19,4.0,"3 Milano Rd, Tokyo"],
    ["Tokyo","La Cucina Tokyo","Italian",40,4.6,"2 Napoli Blvd, Tokyo"],
    ["Tokyo","Veneto Garden","Italian",28,4.1,"6 Veneto Ln, Tokyo"],
    ["Tokyo","Tuscany Tokyo","Italian",32,4.4,"12 Tuscany Ave, Tokyo"],
    ["Tokyo","Italian Fusion Tokyo","Italian",36,4.5,"14 Italian Blvd, Tokyo"],

    ["Tokyo","Ankara Tokyo","Turkish",27,4.1,"7 Ankara Rd, Tokyo"],
    ["Tokyo","Sultan Tokyo Grill","Turkish",33,4.4,"3 Sultan St, Tokyo"],
    ["Tokyo","Meze Tokyo Kitchen","Turkish",21,3.9,"6 Meze Ln, Tokyo"],
    ["Tokyo","Istanbul Tokyo Cafe","Turkish",25,4.0,"9 Istanbul Blvd, Tokyo"],
    ["Tokyo","Kebab Tokyo Express","Turkish",15,3.6,"2 Kebab Rd, Tokyo"],
    ["Tokyo","Turkish Aroma Tokyo","Turkish",29,4.2,"5 Ottoman Ave, Tokyo"],

    ["Tokyo","English Tea House Tokyo","English",22,4.1,"8 London Rd, Tokyo"],
    ["Tokyo","Tokyo British Kitchen","English",30,4.3,"5 Regent Ln, Tokyo"],
    ["Tokyo","Tower Roast Tokyo","English",35,4.5,"11 Tower Ave, Tokyo"],
    ["Tokyo","Fish & Chips Tokyo","English",18,3.8,"3 Dockside Rd, Tokyo"],
    ["Tokyo","The British Spoon","English",26,4.2,"14 Windsor Ln, Tokyo"],
    ["Tokyo","English Tavern Tokyo","English",32,4.4,"2 Crown Rd, Tokyo"],

    ["Tokyo","Curry Tokyo House","Indian",21,4.0,"6 Curry Ave, Tokyo"],
    ["Tokyo","Delhi Tokyo Diner","Indian",27,4.2,"1 Delhi Rd, Tokyo"],
    ["Tokyo","Bombay Express Tokyo","Indian",19,3.9,"3 Bombay Ln, Tokyo"],
    ["Tokyo","Tandoori Tokyo","Indian",33,4.6,"9 Punjab Ave, Tokyo"],
    ["Tokyo","Masala Tokyo Cafe","Indian",16,3.7,"5 Masala Rd, Tokyo"],
    ["Tokyo","Indian Feast Tokyo","Indian",30,4.4,"8 Spice St, Tokyo"],


    # ---------------------- DUBAI ----------------------
    ["Dubai","Sakura Marina","Japanese",37,4.4,"11 Marina Rd, Dubai"],
    ["Dubai","Ramen Dubai Hub","Japanese",17,3.9,"3 Ramen Ln, Dubai"],
    ["Dubai","Ginza Luxury Dubai","Japanese",65,4.9,"1 Ginza Ave, Dubai"],
    ["Dubai","Samurai Palace Dubai","Japanese",55,4.7,"5 Tokyo Bay Rd, Dubai"],
    ["Dubai","Bento Box Dubai","Japanese",20,4.1,"8 Sushi Rd, Dubai"],
    ["Dubai","Kyoto Grill Dubai","Japanese",29,4.3,"12 Kyoto St, Dubai"],

    ["Dubai","Roma Dubai","Italian",35,4.3,"2 Roma Rd, Dubai"],
    ["Dubai","Pasta Bella Dubai","Italian",22,4.0,"11 Pasta Rd, Dubai"],
    ["Dubai","Italia Royale Dubai","Italian",50,4.8,"3 Milano Ave, Dubai"],
    ["Dubai","Tuscan Breeze Dubai","Italian",33,4.2,"9 Tuscany Ln, Dubai"],
    ["Dubai","Venice Cove Dubai","Italian",45,4.7,"6 Venice Blvd, Dubai"],
    ["Dubai","Napoli Vista Dubai","Italian",38,4.5,"8 Napoli St, Dubai"],

    ["Dubai","Sultan Dubai Grill","Turkish",32,4.3,"12 Ottoman St, Dubai"],
    ["Dubai","Istanbul Bay Dubai","Turkish",28,4.1,"3 Istanbul Ln, Dubai"],
    ["Dubai","Dubai Kebab House","Turkish",18,3.8,"7 Kebab Rd, Dubai"],
    ["Dubai","Ankara Royal Dubai","Turkish",40,4.6,"1 Ankara Blvd, Dubai"],
    ["Dubai","Turkish Meze Dubai","Turkish",23,3.9,"5 Bosphorus Rd, Dubai"],
    ["Dubai","Golden Baklava Dubai","Turkish",20,4.0,"10 Marmara St, Dubai"],

    ["Dubai","Dubai English Kitchen","English",26,4.2,"14 London Rd, Dubai"],
    ["Dubai","Royal Roast Dubai","English",39,4.6,"7 Crown Ave, Dubai"],
    ["Dubai","Dubai Fry House","English",17,3.8,"2 Dockside Ln, Dubai"],
    ["Dubai","The English Palace Dubai","English",45,4.7,"9 Windsor Rd, Dubai"],
    ["Dubai","British Corner Dubai","English",22,4.0,"11 Regent St, Dubai"],
    ["Dubai","London Taste Dubai","English",19,3.7,"5 Oxford Ln, Dubai"],

    ["Dubai","Spice Route Dubai","Indian",24,4.1,"8 Curry Rd, Dubai"],
    ["Dubai","Bombay Elite Dubai","Indian",38,4.6,"3 Bombay Blvd, Dubai"],
    ["Dubai","Delhi Royal Dubai","Indian",30,4.4,"1 Delhi Ave, Dubai"],
    ["Dubai","Punjab Grill Dubai","Indian",42,4.8,"11 Punjab St, Dubai"],
    ["Dubai","Masala Dubai Diner","Indian",18,3.7,"7 Masala Ln, Dubai"],
    ["Dubai","Indian Haveli Dubai","Indian",26,4.2,"6 Spice St, Dubai"],


    # ---------------------- SYDNEY ----------------------
    ["Sydney","Sakura Cove","Japanese",30,4.2,"3 Sakura Rd, Sydney"],
    ["Sydney","Ramen Harbour","Japanese",14,3.8,"10 Udon Ln, Sydney"],
    ["Sydney","Tokyo Dining Sydney","Japanese",40,4.5,"1 Tokyo Blvd, Sydney"],
    ["Sydney","Sushi Bay","Japanese",22,4.1,"11 Bayview Rd, Sydney"],
    ["Sydney","Kyoto House Sydney","Japanese",28,4.3,"4 Kyoto Ave, Sydney"],
    ["Sydney","Shogun Sydney Grill","Japanese",35,4.4,"8 Samurai St, Sydney"],

    ["Sydney","Italian Harbour","Italian",27,4.2,"9 Harbour Rd, Sydney"],
    ["Sydney","Pasta Station Sydney","Italian",20,4.0,"3 Pasta Ln, Sydney"],
    ["Sydney","Venice Pearl Sydney","Italian",45,4.7,"12 Venice Ave, Sydney"],
    ["Sydney","Napoli Street Sydney","Italian",32,4.3,"17 Napoli Rd, Sydney"],
    ["Sydney","Tuscany Breeze Sydney","Italian",36,4.4,"8 Tuscany Ln, Sydney"],
    ["Sydney","Milano Cove Sydney","Italian",40,4.6,"22 Milano St, Sydney"],

    ["Sydney","Istanbul Harbour Sydney","Turkish",28,4.1,"6 Istanbul Rd, Sydney"],
    ["Sydney","Sultan Grill Sydney","Turkish",35,4.5,"3 Sultan St, Sydney"],
    ["Sydney","Kebab Sydney House","Turkish",17,3.8,"12 Kebab Rd, Sydney"],
    ["Sydney","Ankara Sydney House","Turkish",29,4.2,"11 Ankara Blvd, Sydney"],
    ["Sydney","Meze Harbour Sydney","Turkish",23,3.9,"7 Meze Ln, Sydney"],
    ["Sydney","Turkish Delight Sydney","Turkish",19,3.7,"14 Marmara St, Sydney"],

    ["Sydney","Sydney English Grill","English",24,4.0,"2 London Ln, Sydney"],
    ["Sydney","Harbour Roast Sydney","English",38,4.6,"7 Windsor Ave, Sydney"],
    ["Sydney","Sydney Fish & Chips","English",15,3.6,"10 Dock Rd, Sydney"],
    ["Sydney","Royal English Table","English",34,4.4,"9 Regent St, Sydney"],
    ["Sydney","British Crown Sydney","English",29,4.3,"4 Crown Ave, Sydney"],
    ["Sydney","English Kitchen Sydney","English",20,3.9,"5 Queen St, Sydney"],

    ["Sydney","Curry House Sydney","Indian",23,4.1,"5 Curry Ave, Sydney"],
    ["Sydney","Bombay Harbour Sydney","Indian",37,4.6,"10 Bombay Ln, Sydney"],
    ["Sydney","Delhi Street Sydney","Indian",21,3.9,"8 Delhi Rd, Sydney"],
    ["Sydney","Punjab Kitchen Sydney","Indian",33,4.5,"14 Punjab Blvd, Sydney"],
    ["Sydney","Masala Cove Sydney","Indian",17,3.7,"6 Masala Ln, Sydney"],
    ["Sydney","Indian Spices Sydney","Indian",26,4.2,"7 Spice St, Sydney"],


    # ---------------------- TORONTO ----------------------
    ["Toronto","Tokyo Leaf Toronto","Japanese",29,4.2,"3 Sakura St, Toronto"],
    ["Toronto","Ramen North Toronto","Japanese",13,3.8,"10 Noodle Rd, Toronto"],
    ["Toronto","Ginza West Toronto","Japanese",45,4.6,"1 Ginza Ln, Toronto"],
    ["Toronto","Samurai Spot Toronto","Japanese",26,4.1,"6 Samurai Ave, Toronto"],
    ["Toronto","Kyoto Centre Toronto","Japanese",32,4.3,"17 Kyoto Rd, Toronto"],
    ["Toronto","Bento Spot Toronto","Japanese",18,3.9,"14 Bento Rd, Toronto"],

    ["Toronto","Roma Central Toronto","Italian",28,4.1,"22 Roma St, Toronto"],
    ["Toronto","Pasta Hub Toronto","Italian",19,4.0,"3 Pasta Ln, Toronto"],
    ["Toronto","Venice View Toronto","Italian",40,4.5,"11 Venice Rd, Toronto"],
    ["Toronto","Napoli North Toronto","Italian",31,4.3,"8 Napoli Ave, Toronto"],
    ["Toronto","Tuscany Hill Toronto","Italian",35,4.4,"6 Tuscany Blvd, Toronto"],
    ["Toronto","Milano House Toronto","Italian",38,4.6,"17 Milano Ln, Toronto"],

    ["Toronto","Istanbul Eats Toronto","Turkish",24,4.0,"3 Istanbul Rd, Toronto"],
    ["Toronto","Ottoman House Toronto","Turkish",34,4.5,"1 Ottoman St, Toronto"],
    ["Toronto","Kebab Kitchen Toronto","Turkish",16,3.6,"8 Kebab Ln, Toronto"],
    ["Toronto","Ankara Bistro Toronto","Turkish",28,4.2,"12 Ankara Ave, Toronto"],
    ["Toronto","Golden Meze Toronto","Turkish",22,3.9,"6 Meze St, Toronto"],
    ["Toronto","Turkish Palace Toronto","Turkish",30,4.3,"10 Sultan Rd, Toronto"],

    ["Toronto","English Manor Toronto","English",25,4.1,"4 London Rd, Toronto"],
    ["Toronto","Toronto Roast House","English",37,4.5,"11 Windsor Ave, Toronto"],
    ["Toronto","Fish & Chips Toronto","English",14,3.7,"6 Dock Ln, Toronto"],
    ["Toronto","British Plate Toronto","English",29,4.2,"3 Regent St, Toronto"],
    ["Toronto","Royal English Grill TO","English",33,4.4,"9 Queen St, Toronto"],
    ["Toronto","The English Table TO","English",21,3.9,"14 Oxford St, Toronto"],

    ["Toronto","Curry Toronto Kitchen","Indian",22,4.0,"7 Curry Rd, Toronto"],
    ["Toronto","Bombay Grill Toronto","Indian",35,4.6,"3 Bombay Ave, Toronto"],
    ["Toronto","Delhi North Toronto","Indian",20,3.9,"11 Delhi Blvd, Toronto"],
    ["Toronto","Punjab Spice Toronto","Indian",30,4.4,"5 Punjab Ln, Toronto"],
    ["Toronto","Masala Toronto House","Indian",18,3.7,"9 Masala Lane, Toronto"],
    ["Toronto","Indian Express Toronto","Indian",27,4.2,"12 Spice St, Toronto"],
]


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print("Wrote:", path)

write_csv(os.path.join(DATA_DIR, "hotels_1.csv"), hotels)
write_csv(os.path.join(DATA_DIR, "restaurants_1.csv"), restaurants)

print("Dataset creation complete. Files in ./data/")
