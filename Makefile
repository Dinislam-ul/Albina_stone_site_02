run:
	poetry run uvicorn stone_site.main:app --reload

.PHONY: help migrate create db-version downgrade reset-db

help:
	@echo "Доступные команды:"
	@echo "  make migrate            - применить все миграции"
	@echo "  make create mes='Название' - создать новую миграцию"
	@echo "  make db-version         - проверить текущую версию БД"
	@echo "  make downgrade          - откатить последнюю миграцию"
	@echo "  make reset-db           - полный сброс БД (ОСТОРОЖНО!)"

migrate:
	@echo "📦 Применение миграций..."
	poetry run alembic upgrade head
	@echo "✅ Миграции применены!"

create:
	@echo "📝 Создание миграции: $(mes)"
	poetry run alembic revision --autogenerate -m "$(mes)"
	@echo "✅ Миграция создана! Проверь файл в migrations/versions/"

db-version:
	@echo "🔍 Текущая версия БД:"
	poetry run alembic current

downgrade:
	@echo "⬇️ Откат на одну миграцию..."
	poetry run alembic downgrade -1
	@echo "✅ Откат выполнен!"

reset-db:
	@echo "⚠️  ВНИМАНИЕ! Это удалит все данные!"
	@read -p "Ты уверена? (y/n) " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		poetry run alembic downgrade base; \
		poetry run alembic upgrade head; \
		echo "✅ БД пересоздана!"; \
	else \
		echo "❌ Отменено"; \
	fi

# для работы с докером 

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f stone_site_app

build:
	docker compose build --no-cache

dev: build up logs