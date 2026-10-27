#!/bin/bash
# Быстрый пуш расписания на сайт.
# Если файл schedule.html уже отредактирован — просто запустить: bash push_schedule.sh

cd /home/agent/khram-site

if ! git diff --quiet schedule.html; then
    echo "📋 Найдены изменения в schedule.html — пушу на сайт..."
    git add schedule.html
    git commit -m "Обновить расписание богослужений: $(date +'%d.%m.%Y')"
    git push
    echo ""
    echo "✅ Готово! Сайт обновится через 1-2 минуты."
    echo "   https://khram-aikhal.github.io/schedule.html"
else
    echo "ℹ️  Изменений в schedule.html нет. Обновление не нужно."
fi
