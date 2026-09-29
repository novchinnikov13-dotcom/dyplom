from app.database import engine
from app.models import Base

print("Начинаю создание таблиц...")
Base.metadata.create_all(bind=engine)
print("Готово! Все таблицы созданы.")