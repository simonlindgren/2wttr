# 2wittr
Get tweets from the v2 Twitter API, using Academic access.

Current functionality:

- Collect tweets from the **full archive search** endpoint.

### 2wittr_fas.py

Full archive search. Academic access allows for 10M tweets to be collected per month. Keep track on the [developer portal](https://developer.twitter.com/en/portal/dashboard).

1. Provide your bearer token in `bt.txt`.
2. Set parameters in `qp_fas.py`.
3. `$python3 2wttr_fas.py`.

Requests will be done in batches of 100 tweets per page, and paginate until no more tweets are returned.
