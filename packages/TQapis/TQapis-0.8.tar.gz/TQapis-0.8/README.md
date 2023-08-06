<p><img src="https://github.com/treasuryquants/examples/raw/main/assets/MainPic2.png" width="1100"></p>

***
# TQapis Package

The Package contains four modules:

| Files | Description |
| ------ | ----------- |
| TQConnection| Contains the class Connection responsible for sending requests and receiving responses.  |
| TQRequests| Complete set of requests builders for all our APIs to be sent to our server using TQConnection  |
| TQResponse| It is the response xml object |
| TQTest| Runner for functional testing|

A set of examples on how this package is used and some explanation can be found on GitHub: https://github.com/treasuryquants/TQPython

## TQConnetion

This module has two classes:

| Class | Description |
| ------ | ----------- |
| Message| A simple utility class helper for result status and messaging |
| Connection| Contains the class Connection responsible for sending requests and receiving responses as well as parsing the response xml and consuming the results.  |

### Message Class
Usage:

    message=Message(status, content)

- status [Boolean] : Indicate the status of the call 
- content [dictionary] : all results/error messages originating from the call 
 
### Connection Class
Below are the relevant list of interfaces of the class

|Interface | Description |
|---------- | ----------- |
|response | Contains the last xml response|
|email | Your email|
|url | The target URL of the server|
|token | Most recent updated token. it is automatically updated.|
|expiry | How long (in minutes) before the expiry of the token.|
|cost | The cost of last api call |
|balance | Current balance in your account|
|client_id | Your ID with us|
|source_id | Your public IP|
|is_post | 'True' means use 'POST' and false means use 'GET' (unsecure) HTTP protocol.|


Creation Usage:

    connection = TQConnection.Connection(email, is_post):


- email is the email you have with us
- is_post [Boolean]: 'True' means use 'POST' and 'False' means use 'GET' (unsecure) HTTP protocol. 


#### The 'send' Interface 

A straight forward usage to send requests: 

```
request_dictionary = TQRequests.request_name_of_request(arguments) # see TQRequests section for the list of all requests 
message = connection.send(request_dictionary)
if not message.is_OK:
   process_error(message.content) # or return message
# cary on .... 
```
Before you send a request, you need to make sure your IP is already registered with your account. Otherwise, the server will return an error.

Here is an example of checking to see if the server recognises your IP before you start

```
request_ip_return = TQRequests.request_ip_return()
message = connection.send(request_ip_return)
if not message.is_OK:
    print(message.is_OK, message.content) #printing the dictionary object and not its content
    exit()
```


Here is a more interesting example: Pricing an FX forward
```
market_fx_forward = TQRequests.request_function_price_fx_forward(
    asof=20201022
    , type='fx_forward'
    , trade_date=20201022
    , trade_expiry=20201222
    , pay_amount=1000000
    , pay_currency='gbp'
    , receive_amount=1000000
    , receive_currency='usd'
)
message = connection.send(market_fx_forward)
print("\nresult status:{}\ncost:{}\nbalance:{}\ncontent:{}".format(message.is_OK,connection.cost,connection.balance, message.content))
```

***
## TQRequests
The module provides request generators for two objectives:

### 1) Account Life Cycle APIs
These APIs are predominantly used when you are not a client but an intermediary making requests on behalf of a user. 
They are meant to cover the APIs to deal with all the functionalities of an account life cycle
The are:
* request_account_create(email, password , ip , callback_url, is_test=False)
    * *Creates a new account. The account will be created but disabled until it is activated.*
* request_account_send_activation_key(email, callback_url="", is_test=False)
    * *Send and activation key for activating a new account or resetting the password.*
* request_account_activate(email, activation_key, is_test=False)
    * *Activates a the newly created account using the activation key that was send via email.*
* request_account_password_change(email, password,new_password, is_test=False)
    * *Changes the password.* 
* request_account_ip_change(email, password,new_ip, is_test=False)
    * *Changes the IP associated with the account. This IP is the only IP where the requests for this account is accepted.* 
* request_account_password_reset(email, activation_key,new_password, is_test=False)
    * *Resets the password using the activation key that was send via email.*
    
    
In above, 
* email: the email associated with the account 
* password: the password to be associated with the account
* ip: The IP associated with the account. (not necessarily yours)
* callback_url: The url of the site where you expect it to be activated from the welcome email. It will be in include in the activation key email as url/?email=...&activation_key=...
* is_test: a boolean that allows you to run the API under testing. This would allow you to activate a account that is already activated. Or create an account that is already created etc.  


### 2) List of Remaining Request Generators
The following APIs cover all our current services. They will return a dictionary that would then be fed into the "send" function of the Connection object described above.
They are:  
* request_account_token_create(email)
    * *All tokens have an associated expiry and you need to refresh them. If you are using TQConnection it is done for you.*
* request_function_describe(item_name="")
    * *Describes all the APIs available on the server with their name and a small description*
    * *If any of them is selected and returned as argument, the result would be the description of that API*
* request_function_show_available(item_name="")
    * *It provides all the configuration options available such as business dates, daycounts, etc.*    
    * *If any of them is selected and returned as argument, the result would be all the options for that element.*
* request_function_workspace_show_files()
    * *Lists all the files that have been saved under your account.*
* request_function_workspace_delete_file(file_name)
    * *Deletes a file under your account.*
* request_function_market_swap_rates(asof, currency)
    * *It provides the market implied swap rates for a given currency and a given date*
* request_function_market_fx_rates(asof, to_date, base_currency)
    * *It provides all available the market implied fx forward rates for a given base currency and give business date and a forward date*
    * *If the asof date is the same as the to_date, then the results would be FX spot values*
* request_function_price_vanilla_swap( asof, type, notional, trade_date, trade_maturity, index_id, discount_id, floating_leg_period, fixed_leg_period, floating_leg_daycount, fixed_leg_daycount, fixed_rate, is_payer, spread, business_day_rule, business_centres, spot_lag_days, save_as="")
    * *Prices a vanilla swap. *
    * *You can use the discounting to be the same as the libor curve *
    * *The argument save_as is optional and it saves the trade (if successfully priced) in your account.*
* request_function_price_fx_forward(asof, type, trade_date, trade_expiry, pay_amount, pay_currency, receive_amount, receive_currency, save_as="")
    * *Prices a vanilla FX Forward*
    * *The argument save_as is optional and it saves the trade (if successfully priced) in your account.*
* request_function_price(asof, load_as) 
    * *Prices any trade that was saved in your account*
* request_function_risk_ladder(asof, load_as)
    * *Performs linear spot and ladder sensitivities on the swap and FX forward. *
* request_function_pnl_predict(load_as, from_date, to_date) 
    * *Performs a PnL predict calculation for a saved trade between two dates* 
* request_function_pnl_attribute(load_as, from_date, to_date)
    * *Performs a PnL attribution for a saved trade between two dates* 
 
***
## TQTest
This module provides a minimal functionalities for a lightweight functional testing platform.

* Each test file should be marked with an extension ".request". 
* The result for each test is generated with an extension ".result"
* If a test has no associated result file (".result"), then the test will generate one for you and marks it as successful.
* If a test has an associated result file in the same folder, then the module will compare the results:
    * If the new results match the result file content, the test is marked as success.
    * If the new results does not match the result file content, the test is marked as failure and a new file with the extension ".result_new" is generated.   
* run_test_all(folder, email, is_post)
    * runs all the tests in  given folder
* run_test_single(root_folder, file_name,email,is_post)
    * runs a single test file_name inside the folder root_folder.

The platform does not have an overall pass/fail status. Instead, it returns a report of the dictionary type
- key=file_name
- value=OK (or error) 

    
### Anatomy of a Test File
Each test corresponds to one file with ".request" extension. Inside this file there maybe multiple tests, each marked as 
'[test]' with a dictionary of the associated APIs. The format of the test *tag* is as follows:

    [test]: description  

In the format above "description can be any string". This description would then show up in the result file, so you would know which result would correspond to which test.

Here is an example of a test that obtains market fx forward

```
[test]: fx forwards
function_name=market_fx_rates
to_date=20211023  # as integer
asof = "20201023" #as string
base_currency=eur
```

This file will generate a result file similar to

```
[result]:fx forwards
chf=1.068745311999
eur=1.000000000000
gbp=0.911476020717
jpy=124.749323243691
usd=1.192655865299
```

As explained above, there maybe multiple tests in one file. The advantage of this is that one can place all relevant tests in one file. 

<a name="what_can_we_do_better"></a>
## What can we do better?
Any comments, feedback, question? just drop us a line.

<p align="left"><a href="https://www.treasuryquants.com/"> <img src="https://github.com/treasuryquants/examples/raw/main/assets/logoBlackSmall.png" width="300"></a></p>
<p align="left"></p>
<p>Email: <a href="mailto:contact@treasuryquants.com">contact@treasuryquants.com</a></p>
<p>Website: <a href="https://www.treasuryquants.com/" target="_blank">TreasuryQuants.com</a></p>
<p align="left"><a href="https://www.linkedin.com/company/treasury-quants/"><img src="https://github.com/treasuryquants/examples/raw/main/assets/linkedIn.png" width="35"></a></p>
