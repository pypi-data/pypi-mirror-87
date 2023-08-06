# hns_chargebee_api
Performs common task on chargebee

## Installation
`pip install hns-chargebee-api`

## Usage
```python
from hns_chargebee_api import ChargebeeAPI

cb = ChargebeeAPI('test_api_key', 'test_site')

# Perform the tasks
# Retrieves a subscription
cb.retrieve('subs_id')
```