db_representatives = []


def db_recorder(cls):
    db_representatives.append(cls())


if '__main__' == __name__:
    print(db_representatives)
