import jwt
from datetime import datetime, timedelta, timezone

encoded = jwt.encode(
    {'some': 'payload', 'exp': datetime.now(timezone.utc) + timedelta(seconds=30)},
    'secret',
    algorithm='HS256'
)
print(encoded)

decoded = jwt.decode(encoded, 'secret', algorithms=['HS256'])
print(decoded)
