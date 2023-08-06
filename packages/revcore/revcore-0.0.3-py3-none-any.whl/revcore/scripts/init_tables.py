#!/usr/bin/env python

from revcore.ddb.models import Model

def init_tables():
    classes = Model.__subclasses__()
    for c in classes:
        if not c.abstract:
            c.init_table()


if __name__ == '__main__':
    init_tables()
