# fwdproject

## To execute the project from starting to end follow these steps

1. Create a App in fyers api
2. Get User Credentials and add it in UserCred.json file
3. install all the dependencies from requirements.txt
4. Run the script generate_access_token_and_auth_code in 
Tokens directory
5. this will give you a link go on that link and from the 
url copy the auth code
then past the auth code where input is prompted
6. This will give you the access code and refresh token that will
be directly added to the access_token.txt and refresh_token.txt
7. this access_token expires the next day but refresh token is valid 
for 15 days
8. To start with checking whether everything is working smooth
you can run the script testing_candle_daily.py if it is giving the LTP
of SBI then everything is perfect if not then you are missing something
9. Suppose today you finished your work now tomorrow you wish to do
and, you are working with same access_token of yesterdays this will
not work because Every day at the start you need to generate new access
token
10. To generate new access token you can use the new_access_token_using_refresh_token.py
script in Tokens directory to generate a new one using refresh token
11. once you get the new access token copy that and paste it in 
access_token.txt and save it, then you are good to go. To check everything
is fine run the testing_candle_daily.py
12. Add whatever stocks you wish to add in utils.py in scripts
13. First script to run will be D45_cycle.py enter there the 
FROM_DATE and TO_DATE, you wish to find the fib prices and run the script
this will create a new csv file in csv_files directory "D45_cycle.csv"
14. Run the 2nd script for 15 days as same
15. Run the next script called merge_and_highlight_fibonacci.py, This script has
2 functions the first is merger_and_add_ltp this will concat the 2 csv files created and add a column 
there at index 1 named 'ltp' and will also add
the LTP's starting from cell B3. The ltp is fetched from the get_LTP_from_here.py this script 
returns the ltp of all stock in utils. the instance of this function is created below as latest_ltp.
The added ltp column and the added LTP of each stock will be saved as merged_data_with_ltp.xlsx
16. The last function is for highlighting the matching fib level prices, using column mapping
the values are checked with key values, if any same are found than both cells are colored yellow
and the file is saved as merged_data_and_highlighted_with_ltp.xlsx
17. This Script has to be executed only once in start. you can do some manual changes as well in Excel
you can merge the header for 45 days and 15 days, draw borders, make headers bold etc. The changes you make 
will be permanent, and will be used further.
18. The Next script to run is main_scanner, everytime if you need to update it just run this script