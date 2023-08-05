# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['investments',
 'investments.data_providers',
 'investments.ibtax',
 'investments.report_parsers']

package_data = \
{'': ['*']}

install_requires = \
['aiomoex>=1.2.2,<2.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['ibtax = investments.ibtax.ibtax:main']}

setup_kwargs = {
    'name': 'investments',
    'version': '0.1.24',
    'description': 'Analysis of Interactive Brokers reports for tax reporting in Russia',
    'long_description': '# Investments\nБиблиотека для анализа брокерских отчетов + утилита для подготовки налоговой отчетности\n\n![Tests status](https://github.com/cdump/investments/workflows/tests/badge.svg)\n\n## Установка/обновление\n```\n$ pip install investments --upgrade --user\n```\nили с помощью [poetry](https://python-poetry.org/)\n\n## Утилита ibtax\nРасчет прибыли Interactive Brokers для уплаты налогов для резидентов РФ\n\n- расчет сделок по методу ФИФО, учет даты расчетов (settle date)\n- конвертация по курсу ЦБ\n- раздельный результат сделок по акциям и опционам + дивиденды\n- учёт начисленных процентов на остаток по счету\n- учитывает комисии по сделкам\n- пока **НЕ** поддерживаются сделки в валютах, отличных от USD\n- пока **НЕ** поддерживаются сплиты\n- пока **НЕ** поддерживаются сделки Forex, сделка пропускается и выводится сообщение о том, что это может повлиять на итоговый отчет\n\n*Пример отчета:*\n![ibtax report example](./images/ibtax_2020.jpg)\n\n\n### Запуск\nЗапустить `ibtax` указав в `--activity-reports-dir` и `--confirmation-reports-dir` директории отчетами в формате `.csv` (см. *Подготовка отчетов Interactive Brokers*)\n\nВажно, чтобы csv-отчеты `activity` и `confirmation` были в разных директориях!\n\n### Подготовка отчетов Interactive Brokers\nДля работы нужно выгрузить из [личного кабинета](https://www.interactivebrokers.co.uk/sso/Login) два типа отчетов: *Activity statement* (сделки, дивиденды, информация по инструментам и т.п.) и *Trade Confirmation* (settlement date, необходимая для правильной конвертации сумм по курсу ЦБ)\n\n#### Activity statement\nДля загрузки нужно перейти в **Reports / Tax Docs** > **Default Statements** > **Activity**\n\nВыбрать `Format: CSV` и скачать данные за все доступное время (`Perioid: Annual` для прошлых лет + `Period: Year to Date` для текущего года)\n\n**Обязательно выгрузите отчеты за все время существования вашего счета!**\n\n![Activity Statement](./images/ib_report_activity.jpg)\n\n#### Trade Confirmation\n\nДля загрузки нужно перейти в **Reports / Tax Docs** > **Flex Queries** > **Trade Confirmation Flex Query** и создать новый тип отчетов, выбрав в **Sections** > **Trade Confirmation** все пункты в группе **Executions**, остальные настройки - как на скриншоте:\n\n![Trade Confirmation Flex Query](./images/ib_trade_confirmation_settings.jpg)\n\nПосле этого в **Reports / Tax Docs** > **Custom Statements** выгрузите отчеты **за все время существования вашего счета**, используя `Custom date range` периодами по 1 году (больше IB поставить не дает):\n\n\n![Trade Confirmation Statement](./images/ib_report_trade_confirmation.jpg)\n\n\n## Разворачивание проекта для внесения изменений\n\n- Install [poetry](https://python-poetry.org/docs/#installation)\n- Clone & modify & run\n\n```\n$ git clone https://github.com/cdump/investments\n\n$ cd investments\n\n$ poetry install\n$ poetry run ibtax\nusage: ibtax [-h] --activity-reports-dir ACTIVITY_REPORTS_DIR --confirmation-reports-dir CONFIRMATION_REPORTS_DIR [--cache-dir CACHE_DIR] [--years YEARS] [--verbose]\nibtax: error: the following arguments are required: --activity-reports-dir, --confirmation-reports-dir\n\n$ vim investments/ibtax/ibtax.py # edit main file for example\n\n$ poetry run ibtax # run updated version\n```',
    'author': 'Maxim Andreev',
    'author_email': 'andreevmaxim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cdump/investments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
