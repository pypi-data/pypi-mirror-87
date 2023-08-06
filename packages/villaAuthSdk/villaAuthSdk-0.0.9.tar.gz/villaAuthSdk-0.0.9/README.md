# villaAuthSdk
> interact with villa authentication backend


## Install

`pip install villaAuthSdk`

## How to use

create an auth object

```python
from villaAuthSdk.auth import AuthSdk
from nicHelper.dictUtil import printDict
```

```python
sdk=AuthSdk(user=None,pw=None,region='ap-southeast-1')
## user and pw here are the aws key/secret for your client
```

## Create cashier

```python
sdk.createCashier({
  'user': 'nic1',
  'phone': '+66816684442',
  'pw': '12345678',
  'name': 'nic',
  'cashierCode': '001',
  'email': 'test@gmail.com'
})
```




    {'success': True,
     'user': 'nic1',
     'phone': '+66816684442',
     'pw': '12345678',
     'name': 'nic',
     'cashierCode': '001',
     'email': 'test@gmail.com',
     'body': '{"Username":"nic1","UserAttributes":{"sub":"f5aa60ba-0f65-45f3-b8f7-2a064e7e5311","email_verified":"false","name":"nic","custom:cashierCode":"001","phone_number_verified":"true","phone_number":"+66816684442","email":"test@gmail.com"},"UserCreateDate":1606995525.734,"UserLastModifiedDate":1606995525.988,"Enabled":true,"UserStatus":"CONFIRMED","ResponseMetadata":{"RequestId":"6b2010b5-aabc-4d36-8e3e-0234da56f3ab","HTTPStatusCode":200,"HTTPHeaders":{"date":"Thu, 03 Dec 2020 11:38:46 GMT","content-type":"application\\/x-amz-json-1.1","content-length":"467","connection":"keep-alive","x-amzn-requestid":"6b2010b5-aabc-4d36-8e3e-0234da56f3ab"},"RetryAttempts":0}}',
     'statusCode': 200,
     'headers': {'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': '*'}}



## login

```python
result = sdk.auth(user='nic1',pw='12345678')
printDict(result)
```

    AccessKeyId : ASIAVX4Z5T
    SecretKey : zTt7RyFFji
    SessionToken : IQoJb3JpZ2
    Expiration : 1606999129.0
    AccessToken : eyJraWQiOi
    ExpiresIn : 3600
    TokenType : Bearer
    RefreshToken : eyJjdHkiOi
    IdToken : eyJraWQiOi
    NewDeviceMetadata
     DeviceKey : ap-southea
     DeviceGroupKey : -lt0cpemm
    userInfo
     Username : nic1
     UserCreateDate : 1606995525.734
     UserLastModifiedDate : 1606995525.988
     Enabled : True
     UserStatus : CONFIRMED
     ResponseMetadata
      RequestId : 44425d05-8
      HTTPStatusCode : 200
      HTTPHeaders
       date : Thu, 03 De
       content-type : applicatio
       content-length : 467
       connection : keep-alive
       x-amzn-requestid : 44425d05-8
      RetryAttempts : 0
    kwUserAttrib
     sub : f5aa60ba-0
     email_verified : false
     name : nic
     custom:cashierCode : 001
     phone_number_verified : true
     phone_number : +668166844
     email : test@gmail


# Confirm
confirm phone/email

```python
result=sdk.confirm(user='nic1', code= '123')
printDict(result)
```

    error
     pickledb64string : gASVTQUAAA
     error : confirmati


## Get Profile

```python
result=sdk.getProfile('nic1')
printDict(result)
```

    Username : nic1
    UserAttributes
     sub : f5aa60ba-0
     email_verified : false
     name : nic
     custom:cashierCode : 001
     phone_number_verified : true
     phone_number : +668166844
     email : test@gmail
    UserCreateDate : 1606995525.734
    UserLastModifiedDate : 1606995525.988
    Enabled : True
    UserStatus : CONFIRMED
    ResponseMetadata
     RequestId : 85a734ac-2
     HTTPStatusCode : 200
     HTTPHeaders
      date : Thu, 03 De
      content-type : applicatio
      content-length : 467
      connection : keep-alive
      x-amzn-requestid : 85a734ac-2
     RetryAttempts : 0


## update Profile

```python
result = sdk.updateProfile(
  user= 'nic1',
  attributes= {
    'custom:cashierCode': '1234'
  })
printDict(result)
```

    Username : nic1
    UserAttributes
     sub : f5aa60ba-0
     email_verified : false
     name : nic
     custom:cashierCode : 1234
     phone_number_verified : true
     phone_number : +668166844
     email : test@gmail
    UserCreateDate : 1606995525.734
    UserLastModifiedDate : 1606995533.461
    Enabled : True
    UserStatus : CONFIRMED
    ResponseMetadata
     RequestId : ec6ffad2-1
     HTTPStatusCode : 200
     HTTPHeaders
      date : Thu, 03 De
      content-type : applicatio
      content-length : 468
      connection : keep-alive
      x-amzn-requestid : ec6ffad2-1
     RetryAttempts : 0


## set password

```python
sdk.setPassword(user='nic1',pw='12345678')
```




    {'ResponseMetadata': {'RequestId': 'e878f2d6-d1de-487c-8a0a-484072b82309',
      'HTTPStatusCode': 200,
      'HTTPHeaders': {'date': 'Thu, 03 Dec 2020 11:38:54 GMT',
       'content-type': 'application/x-amz-json-1.1',
       'content-length': '2',
       'connection': 'keep-alive',
       'x-amzn-requestid': 'e878f2d6-d1de-487c-8a0a-484072b82309'},
      'RetryAttempts': 0}}



## Unauth
get unauthenticated credentials

```python
result = sdk.unauth()
printDict(result)
```

    AccessKeyId : ASIAVX4Z5T
    SecretKey : UbsJ2mlM3z
    SessionToken : IQoJb3JpZ2
    Expiration : 1606999136.0


## DeleteUser

```python
result = sdk.deleteUser(user='nic1')
printDict(result)
```

    ResponseMetadata
     RequestId : 7e3fc4ac-5
     HTTPStatusCode : 200
     HTTPHeaders
      date : Thu, 03 De
      content-type : applicatio
      content-length : 0
      connection : keep-alive
      x-amzn-requestid : 7e3fc4ac-5
     RetryAttempts : 0

