#!/usr/bin/python

import psycopg2
import sys
import os


def add_counts_col(fkey_table, fkey, col_name):
    con = psycopg2.connect(database=DATABASE, user=USER)
    cur = con.cursor()

    cur.execute("ALTER TABLE {fkt} ADD COLUMN {cn} "
                "INTEGER".format(fkt=fkey_table, cn=col_name))

    cur.execute("SELECT {fkt}.id, count(*) FROM {fkt} JOIN gtd ON (gtd.{fk} = "
                "{fkt}.id) GROUP BY {fkt}.id ORDER BY {fkt}.id".format(
                    fkt=fkey_table, fk=fkey))

    d = {}
    for p in cur.fetchall():
        d[p[0]] = int(p[1])

    cur.execute("SELECT id from {fkt}".format(fkt=fkey_table))
    ids = cur.fetchall()
    for id in ids:
        if id[0] in d:
            cur.execute("UPDATE {fkt} SET {cn}={c} WHERE "
                        "id={idno}".format(fkt=fkey_table, c=d[id[0]],
                                           idno=id[0], cn=col_name))
        else:
            cur.execute("UPDATE {fkt} SET {cn}=0 WHERE "
                        "id={idno}".format(fkt=fkey_table, idno=id[0],
                                           cn=col_name))

    con.commit()
    print "Column added to the {} table".format(fkey_table)


def add_cum_counts_col(fkey_table, col_name, cols_to_sum):
    con = psycopg2.connect(database=DATABASE, user=USER)
    cur = con.cursor()

    cur.execute("ALTER TABLE {fkt} ADD COLUMN {cn} "
                "INTEGER".format(fkt=fkey_table, cn=col_name))

    eqId = '={fkt}.id'.format(fkt=fkey_table)
    sum_str = (eqId + ' or ').join(cols_to_sum) + eqId
    query_str = "SELECT count(*) from gtd where {sum}".format(sum=sum_str)
    print query_str
    cur.execute("UPDATE {fkt} SET {cn}=({query})".format(fkt=fkey_table,
                                                     cn=col_name,
                                                     query=query_str))
    con.commit()
    print "Column added to the {} table".format(fkey_table)


if __name__ == '__main__':

    DATABASE = sys.argv[1]
    USER = os.getenv('USER')

    col_name = 'num_attacks'

    # Create a faux foreign key table for the years and populate it.
    con = psycopg2.connect(database=DATABASE, user=USER)
    cur = con.cursor()
    cur.execute("CREATE TABLE years (id INTEGER PRIMARY KEY)")
    cur.execute("INSERT INTO years (id) SELECT year FROM gtd GROUP BY year "
                "ORDER BY year")
    con.commit()
    fkey_table = 'years'
    fkey = 'year'
    add_counts_col(fkey_table, fkey, col_name)
    cur.execute("ALTER TABLE years RENAME COLUMN id TO name")
    con.commit()

    fkey_table = 'regions'
    fkey = 'region'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'countries'
    fkey = 'country'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'dbsources'
    fkey = 'dbsource'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'alternatives'
    fkey = 'alternative'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'hostage_outcomes'
    fkey = 'hostkidoutcome'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'damage'
    fkey = 'propextent'
    add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'weapon_types'
    cols_to_sum = []
    for i in range(1, 5):
        fkey = 'weaptype%d' % i
        col_name = 'num_attacks' + '_' + fkey
        cols_to_sum.append(fkey)
        add_counts_col(fkey_table, fkey, col_name)
    add_cum_counts_col(fkey_table, 'num_attacks', cols_to_sum)

    fkey_table = 'weapon_subtypes'
    cols_to_sum = []
    for i in range(1, 5):
        fkey = 'weapsubtype%d' % i
        col_name = 'num_attacks' + '_' + fkey
        cols_to_sum.append(fkey)
        add_counts_col(fkey_table, fkey, col_name)
    add_cum_counts_col(fkey_table, 'num_attacks', cols_to_sum)

    fkey_table = 'target_types'
    cols_to_sum = []
    for i in range(1, 4):
        fkey = 'targtype%d' % i
        col_name = 'num_attacks' + '_' + fkey
        cols_to_sum.append(fkey)
        add_counts_col(fkey_table, fkey, col_name)
    add_cum_counts_col(fkey_table, 'num_attacks', cols_to_sum)

    fkey_table = 'countries'
    for i in range(1, 4):
        fkey = 'natlty%d' % i
        col_name = 'num_attacks' + '_' + fkey
        add_counts_col(fkey_table, fkey, col_name)

    fkey_table = 'attack_types'
    cols_to_sum = []
    for i in range(1, 4):
        fkey = 'attacktype%d' % i
        col_name = 'num_attacks' + '_' + fkey
        cols_to_sum.append(fkey)
        add_counts_col(fkey_table, fkey, col_name)
    add_cum_counts_col(fkey_table, 'num_attacks', cols_to_sum)

    fkey_table = 'claim_modes'
    cols_to_sum = []
    fkey = 'claimmode'
    col_name = 'num_attacks' + '_' + fkey
    cols_to_sum.append(fkey)
    add_counts_col(fkey_table, fkey, col_name)
    for i in range(2, 4):
        fkey = 'claimmode%d' % i
        col_name = 'num_attacks' + '_' + fkey
        cols_to_sum.append(fkey)
        add_counts_col(fkey_table, fkey, col_name)
    add_cum_counts_col(fkey_table, 'num_attacks', cols_to_sum)
