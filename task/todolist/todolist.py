from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Table(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class Menu:
    def __init__(self, table_name, engine):
        self.__table_name = table_name
        self.__engine = engine

        Session = sessionmaker(bind=engine)
        self.__session = Session()

    def start(self):
        self.__show_menu()

    def __show_menu(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")

        self.__accept_input()

    def __accept_input(self):
        cmd = input()
        command = -1
        if cmd.isnumeric():
            command = int(cmd)

        if command == 0:
            print("Bye!")
            return
        elif command == 1:
            self.__show_today_tasks()
        elif command == 2:
            self.__show_weeks_tasks()
        elif command == 3:
            self.__show_all_tasks()
        elif command == 4:
            self.__show_missed_tasks()
        elif command == 5:
            self.__add_task()
        elif command == 6:
            self.__delete_task()
        else:
            print("Wrong input! Try again.")

        print()
        self.__show_menu()

    def __get_tasks_by_date(self, date):
        return self.__session.query(Table).filter(Table.deadline == date.date()).all()

    def __show_today_tasks(self):
        today = datetime.today()
        print(f"Today {today.day} {today.strftime('%B')[:3]}:")

        tasks = self.__get_tasks_by_date(today)
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            num = 1
            for task in tasks:
                print(f"{num}. {task.task}")
                num += 1

    def __show_weeks_tasks(self):
        today = datetime.today()
        day = today

        for i in range(7):
            print(f"{day.strftime('%A')} {day.day} {day.strftime('%B')[:3]}:")
            tasks = self.__get_tasks_by_date(day)
            if len(tasks) == 0:
                print("Nothing to do!")
            else:
                num = 1
                for task in tasks:
                    print(f"{num}. {task.task}")
                    num += 1

            day += timedelta(days=1)
            print()

    def __show_all_tasks(self):
        print("All tasks:")
        rows = self.__session.query(Table).order_by(Table.deadline).all()

        if len(rows) == 0:
            print("Nothing to do!")
        else:
            num = 1
            for row in rows:
                print(f"{num}. {row}. {row.deadline.day} {row.deadline.strftime('%B')[:3]}")
                num += 1

    def __add_task(self):
        print("Enter task")
        task = input()

        print("Enter deadline")
        date = datetime.strptime(input(), "%Y-%m-%d")

        new_row = Table(task=task, deadline=date)
        self.__session.add(new_row)
        self.__session.commit()
        print("The task has been added!")

    def __show_missed_tasks(self):
        print("Missed tasks:")

        today = datetime.today()
        tasks = self.__session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()

        if len(tasks) == 0:
            print("Nothing is missed!")
        else:
            num = 1
            for task in tasks:
                print(f"{num}. {task}. {task.deadline.day} {task.deadline.strftime('%B')[:3]}")
                num += 1

    def __delete_task(self):
        print("Choose the number of the task you want to delete:")
        rows = self.__session.query(Table).order_by(Table.deadline).all()

        num = 1
        for row in rows:
            print(f"{num}. {row}. {row.deadline.day} {row.deadline.strftime('%B')[:3]}")
            num += 1

        ind = int(input()) - 1
        task = rows[ind]
        self.__session.delete(task)
        self.__session.commit()

        print("The task has been deleted!")

def make_database(database_file):
    engine = create_engine(f"sqlite:///{database_file}?check_same_thread=False")
    Base.metadata.create_all(engine)
    return engine


def main():
    database_file = "todo.db"
    table_name = "task"

    engine = make_database(database_file)
    menu = Menu(table_name, engine)
    menu.start()


main()
