# Описание проекта
Система для автоматического отслеживания активности окон пользователя с сохранением статистики в базу данных ClickHouse. Проект состоит из двух компонентов:
1. Серверная часть (Ubuntu Server)
Docker-контейнер с ClickHouse 23.3

2. Клиентская часть (Windows)
Python-скрипт для мониторинга активных окон и записи в БД

# Технологический стек
1. ClickHouse - колоночная СУБД для аналитики
2. Docker - контейнеризация базы данных
3. Python + pyautogui - отслеживание активности
3. Ubuntu Server 24.04 - серверная платформа
4. Oracle VirtualBox - виртуализация
5. DBeaver 24.2.3 - универсальный графический клиент для работы с БД.

# Серверная часть (Ubuntu Server)
## Создание контейнера ClickHouse на Ubuntu Server 24.04
В Oracle VirtualBox создаем виртуальную машину из образа ubuntu-24.04-live-server-amd64.iso
Добавить 2 сетевых адаптера (первый для выхода в интернет, второй для связи с хостом)

### Обновление пакетов
sudo apt update
sudo apt upgrade -y

### Установка необходимых пакетов
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

### Добавление Docker репозитория
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

### Установка Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

В папке /opt добавить закрепленную в проетке папку clickhouse

### Запуск контейнера
cd /opt/clickhouse
docker-compose up -d

# Клиентская часть (Windows)
Python-скрипт для автоматического отслеживания активности окон пользователя. Он мониторит смену активных приложений, вычисляет время работы в каждом окне и сохраняет данные (дата, название окна, продолжительность) в базу данных ClickHouse для последующего анализа продуктивности.

