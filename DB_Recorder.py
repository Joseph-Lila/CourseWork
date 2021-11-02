db_representatives = []


def db_recorder(cls):
    db_representatives.append(cls())


@db_recorder
class Hello:
    def __init__(self):
        print('object Hello was created')

    def say(self):
        print('say hello')


@db_recorder
class Bye:
    def __init__(self):
        print('bye')

    def say(self):
        print('say goodbye')


def main():
    print(db_representatives)


if '__main__' == __name__:
    main()
