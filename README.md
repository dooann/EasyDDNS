# EasyDDNS

An easy use DDNS script implemented by using Aliyun SDK. 

# How to use

## Step 1
Install Aliyun SDK for python.

``` shell
cd EasyDDNS

pip3 install -r requirements.txt
```

## Step 2
Sign up an Aliyun account and create AccessKey. Then fill the corresponding fields in ```config.json```. 

``` json
    "access_key": "<access_key>",
    "access_key_secret": "<access_key_secret>",
```

## Step 3
Edit ```config.json``` with your domains infomation.

This is a simple example below.

### Example 
``` json
{
    "access_key": "abcdefghijklmn",
    "access_key_secret": "oprstuvwxyz",
    "domains": [
        {
            "domain_name": "example.com",
            "subdomain_name": "ipv6",
            "type": "AAAA"
        }
    ], 
    "period": 600
}
```
It will execute the record update task for ```ipv6.example.com``` every 600 seconds until you stop it.

**Note**: 
- Only the ```"domain_name"``` field is necessary for every single domain. 
- If there is no ```"type"``` field, "AAAA" (IPv6) is assumed. You must specify the ```"type"``` field with the value of "A" if you want to update the record with IPv4 address.
- If there is no ```"subdomain_name"``` field, "@" is assumed.
- If you want to use another scheduled task program to execute update task periodic, just remove the ```"period"``` field.
- You can add multiple domain into ```"domains"``` field. It will update the record for every domain you added.
- You can also add a ```"query_url"``` field for every single domain to specify a custom API which returns plain text data of your ip address for query.

## Step 4
Just run it.
``` shell
python3 EasyDDNS.py
```
