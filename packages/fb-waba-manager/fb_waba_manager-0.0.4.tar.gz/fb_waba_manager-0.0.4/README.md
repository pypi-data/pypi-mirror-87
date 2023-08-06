# Facebook Whatsapp Business Account Manager

Handle some facebook whatsapp business account manager functionalities.

**FYI**: `waba` stands for WhatsApp Business Account

## Usage

### Constructor

```python
from fb_waba_manager import FbWabaManager

access_token = 'my_access_token'
business_id = 'my_business_id'

fwm = FbWabaManager(access_token, business_id)
```

### Methods

The following methods are provided:

Ps.: All methods are **generators**.

#### list_business_wabas

Retrieve a list of all `waba objects` of your `business`

```python
for w in fwm.list_business_wabas():
  print(w)

# Example of a waba object:
# {
#   'id': '21312312321',
#   'name': 'Some name',
#   'currency': 'USD',
#   'timezone_id': '25',
#   'business_type': 'ent',
#   'message_template_namespace': 'gafsdf_2132_213_asd'
# }
```

---

#### list_waba_phone_numbers

Retrieve a list of all `phone number objects` of your `waba`

| Parameters | Type  |
| ---------- | ----- |
| waba_id    | `str` |

```python
waba_id = '1231434'

for pn in fwm.list_waba_phone_numbers(waba_id):
  print(pn)

# Example of a phone number object:
# {
#   'verified_name': 'My number name',
#   'display_phone_number': '+55 73 1234-5678',
#   'quality_rating': 'GREEN',
#   'thread_limit_per_day': 1000,
#   'id': '132354254546'
# }
```

---

#### list_business_phone_numbers

Retrieve a list of all `phone number objects` of all `wabas` of your `business`

| Parameters | Type              |
| ---------- | ----------------- |
| wabas      | `list` (optional) |

```python

for pn in fwm.list_business_phone_numbers():
  print(pn)

# You can pass a list of wabas
# the objects must have at least the id key

my_wabas = [
  {
    'id': '12342443'
  },
  {
    'id': '56355465'
  }
]

for pn in fwm.list_business_phone_numbers(my_wabas):
  print(pn)
```

### Reference

The `waba`, `business`, `phone number` definition and properties can be found at [Facebook's oficial documentation](https://developers.facebook.com/docs/whatsapp/business-management-api)
