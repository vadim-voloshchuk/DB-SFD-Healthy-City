# DB-SFD-Healthy-City
Реализуем кейс от площадки "Цифровой прорыв (ЮФО)".
Кейсосодерждатель - ФГБУ «НМИЦ ТПМ» Минздрава России.

## Описание исходной задачи
Формирование здоровьесберегающей среды является основой Федерального проекта «Укрепление общественного здоровья» в рамках Национального проекта «Демография». Формирование здоровьесберегающей среды – это самый эффективный и экономически целесообразный способ увеличения продолжительности жизни и сохранения трудовых ресурсов. Однако формирование среды является сложным процессом, требующим межсекторального взаимодействия и широкого круга компетенций, не только в вопросах здоровья, но и градостроительства, коммуникаций и др. В России отмечается дефицит как специалистов, так и инструментов в этой области. 
На основе открытых источников (Open Street Map), с применением технологий искусственного интеллекта, участникам хакатона нужно создать MVP в виде веб-приложения для оценки городской инфраструктуры. 
Основной же задачей участников будет формирование рекомендаций по улучшению среды проживания в выбранной зоне (увеличение или уменьшение указанных выше показателей относительно зон-примеров - городов со всего мира, к показателям которых нужно стремиться).  Разработанный продукт (цифровой инструмент) позволит формировать региональные и муниципальные программы укрепления общественного здоровья, включая анализ доступности алкоголя, табака, продуктов питания и возможностей для физической активности.

## Описание решения
В рамках решения предлагается веб-сервис, основанный на RESTful клиент-серверной архитектуре, поддерживаеммый большинством современных браузеров, а также мобильной ОС Android версии ??.
### Аннотация
Реализованный проект предоставит возможность пользователю интерактивную платформу, позволяющую выбрать необходимый для анализа регион и получить краткую и более полную аналитику с точки зрения инфраструктуры. Сервис ориентируется не только на гео- и климатические данные, но также анализирует новостные справки и социальные медиа относительно выбранного региона.
### Архитектура
#### Главные компоненты
```mermaid
graph TD;
    Система-->Frontend;
    Система-->Backend;
    Система-->DB;
    Система-->DevOps;

Frontend-->Мобильное_приложение;
Frontend-->Веб-сервис;
Backend-->Взаимодействие_с_Frontend;
Backend-->ML;
Backend-->Взаимодействие_с_DB;
Backend-->Сбор_данных;
DB-->Хранение_данных;
DevOps-->CI/CD;
DevOps-->Контейнеризация;
ML-->Классификация;
ML-->Регрессия;
Классификация-->Анализ_текстовых_данных;
Классификация-->Анализ_гео-данных;
Регрессия-->Анализ_гео-данных;





```
### Основной функционал
#### Используемые метрики для анализа
### Список открытых источников
- Геоданные:
  - [OSM(Open Street Map)](https://www.openstreetmap.org/#map=3/69.62/-74.90)
  - [Gismeteo](https://www.gismeteo.ru/api/)
- Новостные ресурсы:
  - [ВК API](https://vk.com/feed)
  - [РИА](https://ria.ru/search/?query)
  - [РБК](https://www.rbc.ru/tags/?tag=%D0%A0%D0%91%D0%9A)
  - [RegRu](https://rg.ru/tema/ekonomika)
### Использованные средства разработки
#### IDE/IDLE
- ![vscode](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
- ![vscode](https://img.shields.io/badge/Android_Studio-3DDC84?style=for-the-badge&logo=android-studio&logoColor=white)
#### Описание стека
- ЯП:
  - ![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![TS](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![flutter](https://img.shields.io/badge/Kotlin-0095D5?&style=for-the-badge&logo=kotlin&logoColor=white)
- Фреймворки/технологии:
  - ![react](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![msql](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![grafana](https://img.shields.io/badge/Grafana-F2F4F9?style=for-the-badge&logo=grafana&logoColor=orange&labelColor=F2F4F9)
### Ссылки на исходный код системных компонент
- База данных
- [Серверная часть](https://github.com/iamelnik29/Healthy-City-Back/tree/main)
- Front-end web часть
- Front-end mobile часть
- [UI/UX дизайн](https://www.figma.com/file/T0441FbXWMXjQ24HL5ZhTt/MLS(DBSFD)?type=design&node-id=0%3A1&mode=design&t=Ixji2eeGdy7GpLNj-1)
