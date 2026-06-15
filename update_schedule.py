#!/usr/bin/env python3
"""
Скрипт обновления расписания богослужений.
Использование: python3 update_schedule.py schedule_data.json
После запуска — автоматически генерирует HTML и пушит на GitHub Pages.
"""

import json
import subprocess
import sys
import os
from datetime import datetime

SCHEDULE_HTML = "/home/agent/khram-site/schedule.html"
REPO_DIR = "/home/agent/khram-site"

def generate_html(data: dict) -> str:
    week_label = data.get("week_label", "")
    days = data.get("days", [])

    rows = []
    for day in days:
        day_name = day["day_name"]
        day_date = day["day_date"]
        saints = day.get("saints", "")
        services = day.get("services", [])
        is_sunday = day.get("sunday", False)
        saint_red = day.get("saint_red", False)

        rowspan = 1 + len(services)
        day_class = 'day sunday' if is_sunday else 'day'
        saint_class = 'saint red' if saint_red else 'saint'

        rows.append(
            f'<tr class="day-start">'
            f'<td class="{day_class}" rowspan="{rowspan}">{day_name} <br>{day_date}</td>'
            f'<td colspan="2" class="{saint_class}"><em>{saints}</em></td>'
            f'</tr>'
        )
        for svc in services:
            time_str = svc["time"]
            svc_text = svc["text"]
            svc_red = svc.get("red", False)
            time_class = 'time red' if svc_red else 'time'
            svc_class = 'svc red' if svc_red else 'svc'
            rows.append(
                f'<tr><td class="{time_class}">{time_str}</td>'
                f'<td class="{svc_class}">{svc_text}</td></tr>'
            )

    table_rows = "\n".join(rows)

    return f"""<!DOCTYPE html><html lang="ru"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>РАСПИСАНИЕ БОГОСЛУЖЕНИЙ 2026 — Храм Рождества Христова</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Times New Roman',serif;background:#f0ebe0;padding:12px}}
.wrap{{max-width:700px;margin:0 auto;background:#fff;border:2px solid #2E6B2E;border-radius:6px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.15)}}
.header{{background:#2E6B2E;color:#fff;display:flex;align-items:center;gap:14px;padding:14px 16px}}
.header-photo{{width:78px;height:78px;min-width:78px;border-radius:50%;overflow:hidden;border:2px solid rgba(255,255,255,.6);box-shadow:0 0 0 3px rgba(255,255,255,.18)}}
.header-photo img{{width:100%;height:100%;object-fit:cover;object-position:center 55%;display:block}}
.header-text{{flex:1;text-align:center}}
.header-cross{{font-size:18px;margin-bottom:2px;opacity:.85}}
.header-church{{font-size:17px;font-weight:bold;letter-spacing:.5px;margin-bottom:4px;line-height:1.25}}
.header-title{{font-size:13px;opacity:.88;margin-bottom:3px;font-style:italic}}
.header-week{{font-size:12px;opacity:.75;font-style:italic}}
.contacts{{background:#245a24;color:#d4f0d4;display:flex;justify-content:center;align-items:center;gap:20px;padding:7px 14px;font-size:12.5px;flex-wrap:wrap}}
.contacts a{{color:#d4f0d4;text-decoration:none}}
.contacts a:hover{{color:#fff}}
table{{width:100%;border-collapse:collapse}}
td{{border:1px solid #c5d9c5;padding:8px 9px;vertical-align:middle}}
td.day{{width:23%;text-align:left;padding:8px 7px;border:1px solid #2E6B2E;font-size:13px;line-height:1.5;font-weight:bold;color:#1a4d1a;vertical-align:middle}}
td.day.sunday{{color:#8B0000;background:#fff9f0}}
td.saint{{border:1px solid #c5d9c5;font-size:12.5px;color:#444;text-align:center;background:#fafff8;padding:7px;font-style:italic}}
td.saint.red{{color:#8B0000;background:#fff8f5}}
td.time{{width:11%;text-align:center;padding:6px 4px;border:1px solid #c5d9c5;font-size:13px;font-weight:bold;color:#1a4d1a;white-space:nowrap}}
td.time.red{{color:#8B0000}}
td.svc{{padding:6px 9px;border:1px solid #c5d9c5;font-size:13px;color:#222}}
td.svc.red{{color:#8B0000;font-weight:bold}}
tr.day-start td{{border-top:2px solid #2E6B2E}}
.footer{{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;font-size:12px;color:#555;border-top:2px solid #2E6B2E;background:#f6faf6;flex-wrap:wrap;gap:4px}}
.footer-church{{font-weight:bold;color:#2E6B2E}}
.btns{{display:flex;gap:10px;justify-content:center;margin:10px auto 2px;flex-wrap:wrap}}
.btn{{padding:7px 20px;border:none;border-radius:4px;font-size:13px;cursor:pointer;font-family:inherit;font-weight:bold}}
.btn-print{{background:#2E6B2E;color:#fff}}
.btn-print:hover{{background:#245a24}}
.btn-share{{background:#fff;color:#2E6B2E;border:2px solid #2E6B2E}}
.btn-share:hover{{background:#f0faf0}}
@media print{{
  body{{background:#fff;padding:0}}
  .wrap{{box-shadow:none;border-radius:0}}
  .btns{{display:none}}
}}
@media(max-width:480px){{
  .header-photo{{width:56px;height:56px;min-width:56px}}
  .header-church{{font-size:14px}}
  .contacts{{gap:10px;font-size:11.5px}}
  td{{padding:5px;font-size:12px}}
}}
</style></head><body>
<div class="wrap">

<div class="header">
  <div class="header-photo">
    <img src="h1.jpg" alt="Храм" onerror="this.style.display='none'">
  </div>
  <div class="header-text">
    <div class="header-cross">✞</div>
    <div class="header-church">Храм Рождества Христова</div>
    <div class="header-title">РАСПИСАНИЕ БОГОСЛУЖЕНИЙ 2026</div>
    <div class="header-week">{week_label}</div>
  </div>
</div>

<div class="contacts">
  <span>⛪ пос. Айхал, Республика Саха (Якутия)</span>
  <span>Настоятель: иерей Иоанн Серкин &nbsp;·&nbsp; <a href="tel:+79244605220">+7 (924) 460-52-20</a></span>
</div>

<table>
{table_rows}
</table>

<div class="footer">
  <span class="footer-church">Храм Рождества Христова</span>
  <span>пос. Айхал</span>
</div>
</div>

<div class="btns">
  <button class="btn btn-print" onclick="window.print()">🖨 Распечатать</button>
  <button class="btn btn-share" onclick="shareSchedule()">📤 Поделиться</button>
</div>

<script>
function shareSchedule() {{
  const url = window.location.href;
  const title = 'Расписание богослужений — Храм Рождества Христова, пос. Айхал';
  if (navigator.share) {{
    navigator.share({{ title, url }}).catch(() => {{}});
  }} else {{
    navigator.clipboard.writeText(url).then(() => {{
      alert('Ссылка скопирована!\\nВставьте её в сообщение.');
    }}).catch(() => {{
      prompt('Скопируйте ссылку:', url);
    }});
  }}
}}
</script>
</body></html>"""


def git_push(week_label: str):
    cmds = [
        ["git", "-C", REPO_DIR, "add", "schedule.html"],
        ["git", "-C", REPO_DIR, "commit", "-m", f"Обновить расписание богослужений: {week_label}"],
        ["git", "-C", REPO_DIR, "push"],
    ]
    for cmd in cmds:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ОШИБКА: {' '.join(cmd)}")
            print(result.stderr)
            sys.exit(1)
        else:
            print(result.stdout.strip() or f"✅ {' '.join(cmd[-2:])}")


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 update_schedule.py schedule_data.json")
        print("Пример файла данных: schedule_TEMPLATE.json")
        sys.exit(1)

    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"Файл не найден: {data_file}")
        sys.exit(1)

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_html(data)

    with open(SCHEDULE_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    week_label = data.get("week_label", datetime.now().strftime("%d.%m.%Y"))
    print(f"✅ schedule.html создан — {week_label}")

    git_push(week_label)
    print(f"\n🎉 Готово! Сайт обновится через 1-2 минуты.")
    print(f"   https://khram-aikhal.github.io/schedule.html")


if __name__ == "__main__":
    main()
