from project.models import *
from project.database import *
import json
import random


init_db()
u = User(name="admin", password="admin")
db_session.add(u)
with open("polygons.json") as file:
    # polyes = json.loads(file.readline())
    events = json.loads(file.readline())
    for event in events:
        # poly = [" ".join([str(y) for y in x]) for x in polyes[0]]
        e = Event(
            histogram='123',
            solved=0,
            probability=random.randint(6000, 10000) / 10000,
            polygons=json.dumps(event)
        )
        db_session.add(e)
db_session.commit()
