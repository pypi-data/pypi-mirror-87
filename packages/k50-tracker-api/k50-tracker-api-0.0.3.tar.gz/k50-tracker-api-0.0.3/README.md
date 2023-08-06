# K50 tracker ai wrapper

## Installation

Install using `pip`...

    pip install k50-tracker-api
    
### Usage
```python
from k50_tracker import K50Client

k50 = K50Client('<your access_token>')

# get projects
# doc - https://help.k50.ru/tracker-api/api-requests/get-counters-list/
k50.get_projects() # return dict

# get pool list
# doc - https://help.k50.ru/tracker-api/api-requests/get-pool/
k50.get_pool_list(counter_id=123) # optional page: int - default 1, items_per_page: int - default 1000

# get call stats
# doc - https://help.k50.ru/tracker-api/api-requests/get-calls-stat-v2/
k50.get_call_stats(counter=123, dimensions=['dimension1', 'dimension2'], csv=False) # csv True/False by return csv or json

# get order stats
# doc - https://help.k50.ru/tracker-api/api-requests/get-orders-stat-v2/
k50.get_order_stats(counter=123, dimensions=['dimension1', 'dimension2'], csv=False) # csv True/False by return csv or json

# get tags
# doc - https://help.k50.ru/tracker-api/api-requests/get-tags/
k50.get_tags(counter=123)

# get leads
# doc - https://help.k50.ru/tracker-api/api-requests/get-leads/
k50.get_leads(counter=123, dimensions=['dimension1', 'dimension2'], csv=False, is_show_inter_action_chain=False)


# get reports
# doc - https://help.k50.ru/tracker-api/api-requests/get-reports/
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=1)
k50.get_reports(
    counter=123,
    dimensions=['dimension1', 'dimension2'],
    metrics=['metric1'],
    date_from=date_from,
    date_to=date_to,
    limit=1000,
    offset=0,
    csv=False
)

# add call
# doc - https://help.k50.ru/tracker-api/api-requests/add-calls/
k50.add_call(counter=123, call_id=123, start_time=datetime.now(), caller_phone='79379992', called_phone='9389992')

# update_call
# doc - https://help.k50.ru/tracker-api/api-requests/update-calls/
k50.update_call(counter=123, call_id=123, start_time=datetime.now(), caller_phone='79379992', called_phone='9389992')

# add order
# doc - https://help.k50.ru/tracker-api/api-requests/add-orders-stat-v2/
k50.add_order(counter=123, order_id=123, date_time=datetime.now())

# update order
# doc - https://help.k50.ru/tracker-api/api-requests/update-orders-stat-v2/
k50.update_order(counter=123, order_id=123, date_time=(datetime.now() - timedelta(days=1)))

# add tags to call
# dod - https://help.k50.ru/tracker-api/api-requests/add-call-tags/
k50.add_tags_to_calls(counter=123, call_id=123, tags=['list of tags'])


# add tags to call
# dod - https://help.k50.ru/tracker-api/api-requests/add-call-tags/
k50.remove_tags_from_call(counter=123, call_id=123, tags=['list of tags'])
```

### LICENSE
MIT