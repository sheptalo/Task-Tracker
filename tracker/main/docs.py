register_user_post = "Метод регистрации пользователя"

task_status_post = "Создает статусы задач, возвращает их id"
task_status_get = "Возвращает id, name статусов задач"

task_priority_get = "Возвращает id, name приоритетов задач"
task_priority_post = "Создает приоритеты задач, возвращает их id"

user_project_assignment_get = """
Список всех пользователей назначенных на какой-либо проект с отображением роли
доступные фильтры:
 - project - фильтр про id проекта
"""

user_project_assignment_post = """
Добавление пользователя в проект
при добавлении пользователю приходит письмо на почту и websocket уведомление
"""

comments_get = """
Возвращает список комментариев, ?task=int будет возвращать комментарии для определенной задачи
"""
comments_post = """
Создает новую задачу и отправляет клиенту WebSocket уведомление
"""


roles_get = "Возвращает существующие роли"

roles_post = "Создает новую роль"

projects_get = """
Возвращает список проектов, доступны Параметры строки: 
order - позволяет вернуть в нужном порядке
mode - режим фильтрации дат
 - created_at - по умолчанию "по дате создания"
 - updated_at - фильтрация по дате последнего обновления задачи
start_date - минимальная дата заданного режима см. режимы фильтрации задачи формат дд.мм.гггг
end_date - максимальная дата заданного режима см. режимы фильтрации задачи формат дд.мм.гггг
"""

tasks_get = """
Возвращает список задач 

фильтры:
status - Фильтр по статусу, в качестве значения передается id статуса
priority - Фильтр по приоритетности, значение также как и в статусе
assignee - Фильтр по исполнителю, параметр - id пользователя
tester - фильтр по тестеру см. assignee

order - параметр по которому ведется сортировка, передается название требуемого параметрa

mode - режим фильтрации дат
 - created_at - по умолчанию "по дате создания"
 - updated_at - фильтрация по дате последнего обновления задачи
start_date - минимальная дата создания задача формат дд.мм.гггг
end_date - максимальная дата создания задачи формат дд.мм.гггг
"""


users_get = """
Получения списка пользователя, есть возможность поставить порядок
по любому из доступных пользователю параметров
 - project - сортировка пользователей про id проекта
"""

history_get = """
Возвращает историю проектов пользователя
фильтры:
  - user - id пользователя
"""

history_post = """
Создание записи о участии пользователя в проекте, история идет по названию проекта
"""

export = """
Получить задачи проекта в формате pdf, csv
обязательный параметр ?project_id - id проекта с которого беруться задачи
?formatter - либо csv либо pdf - в каком формате вернуть ответ
Возвращает id таска 
"""

export_result = """
Возвращает результаты таска по его id, если таковы имеются либо статус задачи
"""
