## Personal Access Tokens

Starting with release 3.13, SMARTdiagnostics provides the capability to create Personal Access Tokens (PAT) that can be used as a Bearer token to authorize API requests.  These access tokens are connected to the user that created them, acting on behalf of that SD user. Currently, the tokens are long living with no expiration date,. In the future, however, we do plan institute lifetimes to these tokens.

To use the new Python SDK to access SMARTdiagnostics APIs, you must first create a Personal Access Token (PAT).  There is currently NO interface withing the SMARTdiagnostics UI to create PATs. Therefore, you will need to create one through the API after you have logged into SD in a browser. The easiest way to create tokens at this time is through our Swagger UI interface.

Finally, you will only be given the actual token one time, as part of the response from the CREATE request. There is no other way to retrieve the token through other APIs. Although it is long-living, you only have one time to copy and use the token. If you lose the token, another one will have to be created.

To create a PAT:

1. Log into SD
2. Access the [Swagger UI](https://sd.kcftech.com/swagger/index.html?urls.primaryName=SmartDiagnostics%20Internal%20API%20V3) controls and look for the Users APIs near the bottom, specifically the POST to `Users/CurrentUser/tokens`
3. Expand this API and click on the "Try it Out" button
4. The POST request only requires one property, the "description" which will be shown to you in SMARTdiagnostics in the future and (currently) when you request a list of PATs through the API. Use the description to note what application this PAT is used for or why you created it.
5. Click the blue "Execute" button and then look for the response. The `token` property is your new PAT and it must be copied and saved for use later. For the purposes of this example, we will save this token to a file that will be read by the Python script.

### Overview of the SMARTdiagnostics Python SDK

The Python SDK provides access to all APIs exposed through the Internal APIs as well as their REQUEST and RESPONSE models. We've chosen to provide an SDK specifically for this set of Internal APIs so that we can be intentional about exposing helpful APIs that we can commit to supporting long-term. If an API is not exposed through the Internal list, then it should be considered Private, not supported outside of the KCF Development team and subject to change. 

There are two main advantages to using the SDK:

1. All web request logic is handled internally. There is no need to create additional methods for handling this request/response logic.
2. All models necessary to both make requests (POST/PUT) and to consume responses (GET) are provided. You do not have to create a set of objects/classes to hold this data.

### Dependencies

We currently use an application called AutoREST to create the SDK for Python. One of dependencies of the SDK that allows it to manage the requests is `msrest`. This must be installed before using the SDK.

`pip install msrest`

### Parameter Usage

If you examine the API documentation through Swagger UI, most GET requests that allow paging take at least four standard request parameters:

- `Filter`: This is a string that specifies the properties to refine the response
- `Page`: when a response has more than one page of items, request additional pages of data by incrementing this value
- `PageLimit`: The number of items to include on page. Default is 10. Max is 2,000 items per page. In most cases, it will be more efficient to request the maximum so that fewer requests are made. YMMV.
- `OrderBy`: Which property to sort the response by.

In general Python fashion, these request parameters are translated to their lowercase, underline separated variant which is shown in the example script (eg. "page_limit", "order_by")

### Settings.ini file

The script variables, including the PAT are stored in an external file called `settings.ini`.  The format of this file matches that of the `configparser` module.

```python
[SDAPI]
base_url = https://sd.kcftech.com
token = 0123456789+abcdefghijk/kcf
corporation_id = 00000000-0000-0000-0000-000000000001
```

### Example script

For this simple example, we will list all of the Locations for a given Corporation. For this example, we assume that the response provides more than one page of results to show one possible way to page the results.

```python
from smartdiagnostics_sdk import SmartDiagnosticsApi, models
import configparser

# Get configuration
configuration = configparser.ConfigParser()
configuration.read("settings.ini")

# Prod base_url example: https://sd.kcftech.com
base_url = configuration["SDAPI"]["base_url"]
bearer_token = configuration["SDAPI"]["token"]
corporation_id = configuration["SDAPI"]["corporation_id"]

# instantiate client and add token for requests
sd_client = SmartDiagnosticsApi(base_url=base_url)
sd_client.config.headers["Authorization"] = "bearer " + bearer_token

# call the locations GET API
corporation_filter = "CorporationId eq '{}'".format(corporation_id)
location_response = sd_client.get_locations(filter=corporation_filter) 

total_pages = location_response.total_pages

# Print some details for each location
print("LOCATIONS:")
for i in range(1, total_pages + 1):
    location_response = sd_client.get_locations(filter=corporation_filter,page=i, page_limit=10)
    for location in location_response.result:
        print(location.name)
        print("Id: {}".format(location.id))
        print("Abbreviation: {}".format(location.abbreviation))
        print("CorporationId: {}".format(location.corporation.corporation_id))
        print("Settings: {}".format(location.settings))
```