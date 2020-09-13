from project.models import *
from project.database import *

init_db()
u = User(name="admin", password="admin")
db_session.add(u)
for i in range(20):
    e = Event(
        histogram='123',
        solved=i%4,
        probability=i/10
    )
    db_session.add(e)
db_session.commit()
