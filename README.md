Capital City Time API

API Token

All secure endpoints require a bearer token.

Token: feather987oak

Include this in the request header:

Authorization: Bearer feather987oak

Endpoints
1. /api/hello

- Method: GET  
- Public route  
- Response:
  {
    "message": "Hello, world!"
  }

2. /api/secure-data

- Method: GET  
- Protected route (requires token)  
- Response:
  {
    "secret": "This is protected info!"
  }

3. /api/time

- Method: GET  
- Protected route (requires token)  
- Query parameter: city  
- Example:
  GET /api/time?city=London  
  Header: Authorization: Bearer feather987oak  
- Response:
  {
    "city": "London",
    "local_time": "2025-04-21 22:30:12",
    "utc_offset": "+01:00"
  }
