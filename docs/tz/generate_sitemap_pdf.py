#!/usr/bin/env python3
"""Генерація PDF-карти сайту Kupolla за ТЗ замовниці."""

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).parent / "Kupolla_карта_сайту.pdf"

FONT_CANDIDATES = [
  "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
  "/System/Library/Fonts/Supplemental/Arial.ttf",
  "/Library/Fonts/Arial Unicode.ttf",
  "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def register_font() -> str:
  for path in FONT_CANDIDATES:
    if Path(path).exists():
      pdfmetrics.registerFont(TTFont("SiteFont", path))
      pdfmetrics.registerFont(TTFont("SiteFont-Bold", path))
      return "SiteFont"
  raise FileNotFoundError("Не знайдено шрифт із підтримкою кирилиці")


def p(text: str, style) -> Paragraph:
  return Paragraph(text.replace("\n", "<br/>"), style)


def build_styles(base_font: str):
  styles = getSampleStyleSheet()
  return {
    "title": ParagraphStyle(
      "title",
      fontName=base_font,
      fontSize=22,
      leading=28,
      alignment=TA_CENTER,
      spaceAfter=6,
      textColor=colors.HexColor("#1a3a2f"),
    ),
    "subtitle": ParagraphStyle(
      "subtitle",
      fontName=base_font,
      fontSize=11,
      leading=14,
      alignment=TA_CENTER,
      spaceAfter=16,
      textColor=colors.HexColor("#4a6358"),
    ),
    "h1": ParagraphStyle(
      "h1",
      fontName=base_font,
      fontSize=15,
      leading=20,
      spaceBefore=14,
      spaceAfter=8,
      textColor=colors.HexColor("#1a3a2f"),
    ),
    "h2": ParagraphStyle(
      "h2",
      fontName=base_font,
      fontSize=12,
      leading=16,
      spaceBefore=10,
      spaceAfter=6,
      textColor=colors.HexColor("#2d5a47"),
    ),
    "body": ParagraphStyle(
      "body",
      fontName=base_font,
      fontSize=9.5,
      leading=13,
      spaceAfter=4,
      alignment=TA_LEFT,
      textColor=colors.HexColor("#222222"),
    ),
    "bullet": ParagraphStyle(
      "bullet",
      fontName=base_font,
      fontSize=9.5,
      leading=13,
      leftIndent=14,
      spaceAfter=2,
      bulletIndent=0,
      textColor=colors.HexColor("#222222"),
    ),
    "mono": ParagraphStyle(
      "mono",
      fontName=base_font,
      fontSize=9,
      leading=12,
      leftIndent=10,
      textColor=colors.HexColor("#1f4d3a"),
      backColor=colors.HexColor("#f4f7f5"),
      spaceAfter=3,
    ),
    "footer": ParagraphStyle(
      "footer",
      fontName=base_font,
      fontSize=8,
      leading=10,
      alignment=TA_CENTER,
      textColor=colors.HexColor("#888888"),
    ),
    "cell": ParagraphStyle(
      "cell",
      fontName=base_font,
      fontSize=8.5,
      leading=11,
      alignment=TA_LEFT,
      textColor=colors.HexColor("#222222"),
      wordWrap="CJK",
    ),
    "cell_header": ParagraphStyle(
      "cell_header",
      fontName=base_font,
      fontSize=8.5,
      leading=11,
      alignment=TA_LEFT,
      textColor=colors.HexColor("#1a3a2f"),
      wordWrap="CJK",
    ),
  }


def _cell(text, style, header: bool = False) -> Paragraph:
  safe = (
    str(text)
    .replace("&", "&amp;")
    .replace("<", "&lt;")
    .replace(">", "&gt;")
  )
  if header:
    safe = f"<b>{safe}</b>"
  return Paragraph(safe, style)


def tree_table(rows, col_widths, styles):
  cell_style = styles["cell"]
  header_style = styles["cell_header"]

  wrapped = []
  for row_idx, row in enumerate(rows):
    wrapped_row = []
    for cell in row:
      style = header_style if row_idx == 0 else cell_style
      if isinstance(cell, Paragraph):
        wrapped_row.append(cell)
      else:
        wrapped_row.append(_cell(cell, style, header=row_idx == 0))
    wrapped.append(wrapped_row)

  table = Table(wrapped, colWidths=col_widths, hAlign="LEFT", repeatRows=1)
  table.setStyle(
    TableStyle(
      [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f0ec")),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8d8d0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fafcfa")]),
      ]
    )
  )
  return table


def main():
  font = register_font()
  s = build_styles(font)

  doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=1.8 * cm,
    rightMargin=1.8 * cm,
    topMargin=1.6 * cm,
    bottomMargin=1.6 * cm,
    title="Kupolla — карта сайту",
    author="PrometeyLabs",
  )

  story = []

  # Титул
  story.append(p("KUPOLLA", s["title"]))
  story.append(p("Карта сайту (Sitemap)", s["title"]))
  story.append(Spacer(1, 4))
  story.append(
    p(
      f"Технічне завдання · Виробництво купольних будинків<br/>"
      f"Дата: {date.today().strftime('%d.%m.%Y')}",
      s["subtitle"],
    )
  )
  story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2d5a47")))
  story.append(Spacer(1, 8))

  # 1. Мета та аудиторія
  story.append(p("1. Контекст проєкту", s["h1"]))
  story.append(
    p(
      "<b>Мета сайту:</b> презентація компанії та продукту; отримання заявок; "
      "демонстрація модельного ряду; формування довіри до бренду.",
      s["body"],
    )
  )
  story.append(
    p(
      "<b>Цільова аудиторія:</b> власники земельних ділянок; інвестори; глемпінги та "
      "бази відпочинку; девелопери туристичних комплексів; готелі, що розширюються.",
      s["body"],
    )
  )
  story.append(
    p(
      "<b>Дизайн:</b> преміальний, мінімалістичний, сучасний; акцент на екологічності "
      "та інноваційності. Референси: move-homes.com, oodhouse.com.",
      s["body"],
    )
  )

  # 2. Ієрархія
  story.append(p("2. Ієрархія сторінок (відповідно до п.3 ТЗ)", s["h1"]))
  hierarchy = [
    ["Рівень", "Сторінка", "URL (приклад)", "Примітка"],
    ["0", "Головна", "/{lang}/", "Перший екран, переваги, моделі, технології, форма"],
    ["1", "Про компанію", "/{lang}/about/", "Історія, місія, команда, цінності"],
    ["1", "Модельний ряд", "/{lang}/models/", "Каталог усіх моделей"],
    ["2", "Сторінка моделі", "/{lang}/models/{slug}/", "Окрема сторінка кожної моделі"],
    ["1", "Конфігуратор", "/{lang}/configurator/", "Підбір конфігурації куполу"],
    ["1", "Технології та матеріали", "/{lang}/technologies/", "Матеріали, етапи виробництва"],
    ["1", "Галерея", "/{lang}/gallery/", "Фото реалізованих об'єктів"],
    ["1", "Блог", "/{lang}/blog/", "Список статей"],
    ["2", "Стаття блогу", "/{lang}/blog/{slug}/", "Окрема публікація"],
    ["1", "FAQ", "/{lang}/faq/", "Часті запитання"],
    ["1", "Контакти", "/{lang}/contacts/", "Контакти, карта, форма"],
    ["—", "Адмін-панель", "/admin/", "Керування контентом (п.7 ТЗ)"],
  ]
  story.append(tree_table(hierarchy, [1.1 * cm, 3.6 * cm, 4.8 * cm, 7.9 * cm], s))

  story.append(PageBreak())

  # 3. Головна
  story.append(p("3. Головна сторінка — структура блоків (п.4 ТЗ)", s["h1"]))
  home_blocks = [
    ["№", "Блок", "Зміст", "CTA / елементи"],
    ["3.1", "Перший екран (Hero)", "Візуалізація купольного будинку; короткий опис переваг", "Кнопка «Отримати консультацію» → форма / модальне вікно"],
    ["3.2", "Блок переваг", "Енергоефективність · Екологічність · Швидкий монтаж · Довговічність", "4 картки з іконками"],
    ["3.3", "Блок моделей", "Прев'ю модельного ряду (фото, площа, ціна від)", "Посилання на /models/ та окремі моделі"],
    ["3.4", "Блок технологій", "Короткий огляд технологій та матеріалів", "Посилання на /technologies/"],
    ["3.5", "Форма заявки", "Ім'я, телефон, email, коментар, згода на обробку даних", "Відправка → CRM / email"],
    ["3.6", "Глобальні елементи", "Шапка, футер, перемикач мов, навігація", "Меню з усіх розділів п.3 ТЗ"],
  ]
  story.append(tree_table(home_blocks, [0.9 * cm, 3.2 * cm, 6.8 * cm, 6.5 * cm], s))

  # 4. Сторінка моделі
  story.append(p("4. Сторінка моделі — структура (п.5 ТЗ)", s["h1"]))
  model_blocks = [
    ["№", "Секція", "Опис"],
    ["4.1", "Назва моделі", "H1, slug для URL"],
    ["4.2", "Площа", "Загальна площа, м²"],
    ["4.3", "Планування", "План поверху, схема зонування"],
    ["4.4", "Візуалізації", "Галерея рендерів / фото (слайдер)"],
    ["4.5", "Технічні характеристики", "Діаметр, висота, утеплення, вікна, фундамент тощо"],
    ["4.6", "Комплектації", "Базова / стандарт / преміум (таблиця порівняння)"],
    ["4.7", "Ціна", "Вартість від … (за комплектацією)"],
    ["4.8", "Форма заявки", "Заявка на консультацію / розрахунок по моделі"],
    ["4.9", "Додатково", "Хлібні крихти, схожі моделі, CTA «Налаштувати в конфігураторі»"],
  ]
  story.append(tree_table(model_blocks, [0.9 * cm, 3.8 * cm, 12.7 * cm], s))

  # 5. Інші сторінки
  story.append(p("5. Деталізація інших розділів", s["h1"]))

  story.append(p("5.1 Про компанію", s["h2"]))
  for item in [
    "Про бренд Kupolla та сферу діяльності",
    "Місія, цінності (екологічність, інновації)",
    "Етапи співпраці з клієнтом",
    "Переваги для цільових сегментів (інвестори, глемпінги, девелопери)",
    "Форма зворотного зв'язку / CTA",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.2 Модельний ряд", s["h2"]))
  for item in [
    "Фільтри: площа, призначення (проживання / глемпінг / комерція), ціна",
    "Сітка карток моделей",
    "Перехід на сторінку моделі та конфігуратор",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.3 Конфігуратор", s["h2"]))
  for item in [
    "Вибір базової моделі",
    "Параметри: діаметр, комплектація, опції (вікна, тераса, інженерія)",
    "Попередній розрахунок вартості",
    "Візуальний прев'ю конфігурації",
    "Форма заявки з переданими параметрами конфігурації",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.4 Технології та матеріали", s["h2"]))
  for item in [
    "Опис конструктиву купола",
    "Матеріали (екологічність, довговічність)",
    "Енергоефективність та утеплення",
    "Етапи виробництва та монтажу",
    "Сертифікати / гарантії (за наявності)",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.5 Галерея", s["h2"]))
  for item in [
    "Фото реалізованих об'єктів",
    "Фільтр за типом проєкту (глемпінг, житло, комерція)",
    "Lightbox-перегляд",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.6 Блог", s["h2"]))
  for item in [
    "Список статей з прев'ю, датою, категорією",
    "Сторінка статті: заголовок, контент, медіа, SEO",
    "Категорії / теги",
    "Пов'язані статті",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.7 FAQ", s["h2"]))
  for item in [
    "Акордеон із питаннями та відповідями",
    "Групування за темами (монтаж, ціна, дозвіл, експлуатація)",
    "CTA «Не знайшли відповідь?» → форма / контакти",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(p("5.8 Контакти", s["h2"]))
  for item in [
    "Адреса, телефон, email, месенджери",
    "Карта (Google Maps / аналог)",
    "Графік роботи",
    "Форма зворотного зв'язку",
    "Реквізити компанії",
  ]:
    story.append(p(f"• {item}", s["bullet"]))

  story.append(PageBreak())

  # 6. Функціонал
  story.append(p("6. Функціональні вимоги (п.6 ТЗ)", s["h1"]))
  func_rows = [
    ["Вимога", "Реалізація на карті сайту"],
    ["Адаптивність", "Усі публічні сторінки: desktop / tablet / mobile (iOS Safari)"],
    ["Форми зворотного зв'язку", "Головна, модель, конфігуратор, контакти, FAQ, модальні CTA"],
    ["Google Analytics", "GA4 на всіх сторінках, події: form_submit, cta_click, configurator_step"],
    ["Інтеграція CRM", "Webhook / API при відправці всіх форм (обов'язково)"],
    ["Багатомовність", "Префікс /{lang}/; перемикач у шапці та футері"],
  ]
  story.append(tree_table(func_rows, [4.2 * cm, 13.2 * cm], s))

  story.append(Spacer(1, 8))
  story.append(p("6.1 Підтримувані мови", s["h2"]))
  langs = [
    ["Код", "Мова", "Статус"],
    ["uk", "Українська", "Основна"],
    ["en", "Англійська", "Запуск"],
    ["sk", "Словацька", "Запуск"],
    ["cs", "Чеська", "Запуск"],
    ["nl", "Нідерландська", "Запуск"],
    ["ru", "Російська", "Запуск"],
    ["es", "Іспанська", "Запуск"],
    ["fr", "Французька", "Запуск"],
  ]
  story.append(tree_table(langs, [1.8 * cm, 4.8 * cm, 10.8 * cm], s))

  # 7. Адмін
  story.append(p("7. Адміністративна панель (п.7 ТЗ)", s["h1"]))
  admin_rows = [
    ["Модуль", "Можливості"],
    ["Моделі", "Додавання / редагування / видалення моделей, характеристик, цін, медіа"],
    ["Контент сторінок", "Редагування текстів усіх статичних розділів"],
    ["Медіа", "Завантаження фото (галерея, моделі, блог)"],
    ["Блог", "Створення, редагування, публікація / зняття статей"],
    ["FAQ", "Керування питаннями та відповідями"],
    ["Заявки", "Перегляд заявок з форм сайту"],
    ["Налаштування", "Мови, контакти, інтеграції (GA, CRM)"],
  ]
  story.append(tree_table(admin_rows, [3.8 * cm, 13.6 * cm], s))

  # 8. Дерево URL
  story.append(p("8. Повне дерево URL (Sitemap Tree)", s["h1"]))
  tree_lines = [
    "kupolla.com/",
    "├── {lang}/                          ← uk | en | sk | cs | nl | ru | es | fr",
    "│   ├── /                            Головна",
    "│   ├── about/                       Про компанію",
    "│   ├── models/                      Модельний ряд",
    "│   │   └── {model-slug}/            Сторінка моделі (×N)",
    "│   ├── configurator/                Конфігуратор",
    "│   ├── technologies/                Технології та матеріали",
    "│   ├── gallery/                     Галерея",
    "│   ├── blog/                        Блог",
    "│   │   └── {post-slug}/             Стаття (×N)",
    "│   ├── faq/                         FAQ",
    "│   └── contacts/                    Контакти",
    "├── admin/                           Адмін-панель",
    "├── api/",
    "│   ├── forms/                       Прийом заявок",
    "│   └── configurator/                Розрахунок конфігурації",
    "├── sitemap.xml                      SEO-карта",
    "└── robots.txt",
  ]
  for line in tree_lines:
    story.append(p(line.replace(" ", "&nbsp;"), s["mono"]))

  # 9. Форми
  story.append(p("9. Карта форм та точок конверсії", s["h1"]))
  forms = [
    ["Форма", "Розташування", "Поля (мінімум)"],
    ["Консультація (Hero)", "Головна — перший екран", "Ім'я, телефон, email"],
    ["Заявка (нижня)", "Головна — блок форми", "Ім'я, телефон, email, коментар, згода GDPR"],
    ["Заявка на модель", "Сторінка моделі", "Ім'я, телефон, email, модель (hidden), комплектація"],
    ["Конфігуратор", "Сторінка конфігуратора", "Параметри конфігурації + контакти"],
    ["Контакти", "Сторінка контактів", "Ім'я, email, телефон, повідомлення"],
    ["FAQ fallback", "FAQ", "Коротке питання + контакти"],
  ]
  story.append(tree_table(forms, [3.5 * cm, 4.6 * cm, 9.3 * cm], s))

  # 10. Навігація
  story.append(p("10. Глобальна навігація", s["h1"]))
  story.append(
    p(
      "<b>Шапка (Header):</b> Логотип · Про компанію · Модельний ряд · Конфігуратор · "
      "Технології · Галерея · Блог · FAQ · Контакти · [Мова] · [Отримати консультацію]",
      s["body"],
    )
  )
  story.append(
    p(
      "<b>Футер (Footer):</b> Навігація · Контакти · Соцмережі · Політика конфіденційності · "
      "Умови використання · © Kupolla · Перемикач мов",
      s["body"],
    )
  )
  story.append(
    p(
      "<b>Мобільне меню:</b> бургер-меню, sticky CTA «Консультація», адаптація під iOS Safari "
      "(safe-area, фіксовані елементи, touch-target ≥ 44px).",
      s["body"],
    )
  )

  story.append(Spacer(1, 20))
  story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc")))
  story.append(
    p(
      "Документ сформовано на основі ТЗ замовниці. Усі сторінки з п.3 ТЗ включені. "
      "Динамічні сторінки моделей та статей блогу масштабуються через адмін-панель.",
      s["footer"],
    )
  )

  doc.build(story)
  print(f"PDF створено: {OUTPUT}")


if __name__ == "__main__":
  main()
