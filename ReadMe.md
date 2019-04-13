Introductions:

I have quite an extensive career in the party scene ranging from local shows/festivals at Rebel/Veld to ungrading my party game to going to EDC Las Vegas and eventually Tomorrowland (2019).  


The Problem:

Since these events have an attendance of 500k over the span of of a weekend, pricing on Hotels are not favourable and can be very difficult to secure ad a reasonable price.


The Fix:

Design a bot that will simulate a user performing a room booking (4 part process):

Important Required Libraries):
    •	Schedule: allows functions (or any other callable) to periodically at pre-determined intervals using a simple, human-friendly syntax.
    •	BeautifulSoup: parser for pulling data out of HTML and XML files.
    •	Money_parser (Price_Str): provides methods to extract price and currency information from the raw string.
    •	Sendgrid: Service that assists businesses with email delivery.
    •	Selenium: web-based automation tool.

Part 1: Login Browser

    1)	Initionalize browser
    2)	Navigate to Hotel Sign In page 
    3)	Enter login and password credentials 
    4)	Confirmation of successful login

Part 2: Search and Parse
    1)	Search for roomtype that matches roomtype you defined
    2)	Collect the price and room's full name
    3)	Check if room title matches any of the booked room titles defined in settings file
    4)	Perform delta check on price listing defined in settings file

Part 3:
    1)	Send email to notify user of delta in price for defined room booking
   