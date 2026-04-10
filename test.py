from data import db_session
from data.stories import Stories
from datetime import datetime

db_session.global_init("db/data.db")  # 👈 ВОТ ЭТОГО НЕ ХВАТАЕТ

session = db_session.create_session()

story = Stories(
    title="Тестовая история 2",
    content="Проверка базы2",
    date=datetime.now(),
    author_id=1,
    review_authors_id=1,
    checked=True
)

session.add(story)
session.commit()
session.close()

print("OK")