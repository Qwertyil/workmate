# Coffee Consumption Report

CLI-скрипт строит отчёт `median-coffee` по одному или нескольким CSV-файлам и считает медиану `coffee_spent` по каждому студенту с сортировкой по убыванию. Для быстрого ревью в репозитории есть примеры входных данных в `examples/` и отдельный пример реального запуска в `docs/run_example.txt`.

Примеры запуска:

```bash
poetry run python main.py --files examples/math.csv --report median-coffee
poetry run python main.py --files examples/math.csv examples/physics.csv examples/programming.csv --report median-coffee
```

В проекте логика отчётов отделена от CLI, поэтому новые отчёты можно добавлять через реестр в `coffee_reports/reports/registry.py`. Основной функционал и ключевые error-сценарии покрыты тестами на `pytest`.
