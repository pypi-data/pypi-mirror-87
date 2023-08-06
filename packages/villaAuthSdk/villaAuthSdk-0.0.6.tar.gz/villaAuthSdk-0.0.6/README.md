# villaAuthSdk
> interact with villa authentication backend


## Install

`pip install villaAuthSdk`

## How to use

create an auth object

```
from villaAuthSdk.auth import AuthSdk
from nicHelper.dictUtil import printDict
```

```
sdk=AuthSdk(user=None,pw=None,region='ap-southeast-1')
## user and pw here are the aws key/secret for your client
```

## Create cashier

```
sdk.createCashier({
  'user': 'nic1',
  'phone': '+66816684442',
  'pw': '12345678',
  'name': 'nic',
  'cashierId': '001'
})
```




    {'success': True,
     'user': 'nic1',
     'phone': '+66816684442',
     'pw': '12345678',
     'name': 'nic',
     'cashierId': '001'}



## login

```
result = sdk.auth(user='nic1',pw='12345678')
printDict(result)
```

# Confirm
confirm phone/email

```
result=sdk.confirm(user='nic1', code= '123')
printDict(result)
```

## Get Profile

```
result=sdk.getProfile('nic1')
printDict(result)
```

## update Profile

```
result = sdk.updateProfile(
  user= 'nic1',
  attributes= {
    'custom:cashierCode': '1234'
  })
printDict(result)
```

## set password

```
sdk.setPassword(user='nic1',pw='12345678')
```

## Unauth
get unauthenticated credentials

```
result = sdk.unauth()
printDict(result)
```
