from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, creation_date, status):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.status = status

    def __str__(self):
        return f"{self.task_id},{self.title},{self.description},{self.creation_date},{self.status}\n"


def load_tasks(file_path):
    tasks = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                task_data = line.strip().split(",")
                if len(task_data) == 5:
                    task_id = int(task_data[0])
                    title = task_data[1]
                    description = task_data[2]
                    creation_date = task_data[3]
                    status = task_data[4]
                    task = Task(task_id, title, description, creation_date, status)
                    tasks.append(task)
    except FileNotFoundError:
        print("Plik z zadaniami nie istnieje. Tworzony będzie nowy plik.")
        with open(file_path, "w"):
            pass
    except Exception as e:
        print(f"Błąd podczas wczytywania zadań: {e}")
    return tasks


def save_tasks(tasks, file_path):
    try:
        with open(file_path, "w") as file:
            for task in tasks:
                file.write(str(task))
    except Exception as e:
        print(f"Błąd podczas zapisywania zadań: {e}")


def add_task(tasks, title, description, file_path):
    if title.strip():
        last_task_id = max(task.task_id for task in tasks) if tasks else 0
        task_id = last_task_id + 1
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Do zrobienia"
        task = Task(task_id, title, description, creation_date, status)
        tasks.append(task)
        print("Zadanie dodane pomyślnie.")
        save_tasks(tasks, file_path)
    else:
        print("Tytuł zadania nie może być pusty.")


def display_tasks(tasks, status_filter=None):
    if not tasks:
        print("Brak zadań do wyświetlenia.")
        return

    filtered_tasks = []
    if status_filter:
        for task in tasks:
            if task.status.lower() == status_filter.lower():
                filtered_tasks.append(task)
    else:
        filtered_tasks = tasks

    if not filtered_tasks:
        print("Brak zadań pasujących do wybranego filtru.")
        return

    for task in filtered_tasks:
        print("=" * 30)
        print(f"ID: {task.task_id}")
        print(f"Tytuł: {task.title}")
        print(f"Opis: {task.description}")
        print(f"Data utworzenia: {task.creation_date}")
        print(f"Status: {task.status}")
        print()


def get_task_by_id(tasks, task_id):
    for task in tasks:
        if task.task_id == task_id:
            return task
    return None


def edit_task(tasks, task_id, file_path):
    task = get_task_by_id(tasks, task_id)
    if task:
        print("Edytuj zadanie:")
        print("1. Tytuł")
        print("2. Opis")
        print("3. Status")
        choice = input("Wybierz atrybut do edycji: ")

        if choice == "1":
            title = input("Nowy tytuł zadania: ")
            if title.strip():
                task.title = title
                print("Tytuł zadania zaktualizowany pomyślnie.")
                save_tasks(tasks, file_path)
            else:
                print("Tytuł zadania nie może być pusty.")
        elif choice == "2":
            description = input("Nowy opis zadania: ")
            task.description = description
            print("Opis zadania zaktualizowany pomyślnie.")
            save_tasks(tasks, file_path)
        elif choice == "3":
            status = input("Nowy status zadania (Do zrobienia/W trakcie/Zrealizowane): ").capitalize()
            if status in ["Do zrobienia", "W trakcie", "Zrealizowane"]:
                task.status = status
                print("Status zadania zaktualizowany pomyślnie.")
                save_tasks(tasks, file_path)
            else:
                print("Nieprawidłowy status. Dostępne opcje to: Do zrobienia, W trakcie, Zrealizowane.")
        else:
            print("Nieprawidłowy wybór atrybutu.")

    else:
        print("Nie znaleziono zadania o podanym ID.")


def delete_task(tasks, task_id, file_path):
    task = get_task_by_id(tasks, task_id)
    if task:
        tasks.remove(task)
        print("Zadanie usunięte pomyślnie.")
        save_tasks(tasks, file_path)
    else:
        print("Nie znaleziono zadania o podanym ID.")



file_path = "tasks.txt"
tasks = load_tasks(file_path)

while True:
    print("\n===== MENU =====")
    print("1. Dodaj zadanie")
    print("2. Wyświetl wszystkie zadania")
    print("3. Wyświetl zadania według statusu")
    print("4. Edytuj zadanie")
    print("5. Usuń zadanie")
    print("6. Wyjście")
    choice = input("Wybierz opcję: ")

    if choice == "1":
        title = input("Podaj tytuł zadania: ")
        description = input("Podaj opis zadania: ")
        add_task(tasks, title, description, file_path)

    elif choice == "2":
        display_tasks(tasks)

    elif choice == "3":
        status_filter = input("Podaj status zadania (Do zrobienia/W trakcie/Zrealizowane): ").capitalize()
        if status_filter in ["Do zrobienia", "W trakcie", "Zrealizowane"]:
            display_tasks(tasks, status_filter)
        else:
            print("Nieprawidłowy status. Dostępne opcje to: Do zrobienia, W trakcie, Zrealizowane.")

    elif choice == "4":
        task_id = int(input("Podaj ID zadania do edycji: "))
        edit_task(tasks, task_id, file_path)

    elif choice == "5":
        task_id = int(input("Podaj ID zadania do usunięcia: "))
        delete_task(tasks, task_id, file_path)

    elif choice == "6":
        print("Wyjście z programu.")
        break

    else:
        print("Nieprawidłowa opcja. Wybierz ponownie.")

