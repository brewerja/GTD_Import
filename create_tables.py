#!/usr/bin/python

import os
import sys
import csv
import psycopg2

from settings import DATABASE, USER

countries_file = open('data/countries', 'r')
regions_file = open('data/regions', 'r')
alternatives = open('data/alternatives', 'r')
attack_types = open('data/attack_types', 'r')
target_types = open('data/target_types', 'r')
claim_modes = open('data/claim_modes', 'r')
weapon_types = open('data/weapon_types', 'r')
weapon_subtypes = open('data/weapon_subtypes', 'r')
damage = open('data/damage', 'r')
hostage_outcomes = open('data/hostage_outcomes', 'r')

con = None

try:
    # Connect to the database.
    con = psycopg2.connect(database=DATABASE, user=USER)
    cur = con.cursor()

    # Create the alternatives table and populate it.
    cur.execute('CREATE TABLE alternatives(id INT PRIMARY KEY, name '
                'VARCHAR(35))')
    for type in alternatives:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO alternatives VALUES(%s, '%s')" % (n, name))
    alternatives.close()

    # Create the hostage outcomes table and populate it.
    cur.execute('CREATE TABLE hostage_outcomes(id INT PRIMARY KEY, name '
                'VARCHAR(50))')
    for type in hostage_outcomes:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO hostage_outcomes VALUES(%s, '%s')" %
                    (n, name))
    hostage_outcomes.close()

    # Create the damage table and populate it.
    cur.execute('CREATE TABLE damage(id INT PRIMARY KEY, name VARCHAR(50))')
    for type in damage:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO damage VALUES(%s, '%s')" % (n, name))
    damage.close()

    # Create the weapon subtypes table and populate it.
    cur.execute('CREATE TABLE weapon_subtypes(id INT PRIMARY KEY, name '
                'VARCHAR(50))')
    for type in weapon_subtypes:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO weapon_subtypes VALUES(%s, '%s')" % (n, name))
    weapon_subtypes.close()

    # Create the weapon types table and populate it.
    cur.execute('CREATE TABLE weapon_types(id INT PRIMARY KEY, name '
                'VARCHAR(50))')
    for type in weapon_types:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO weapon_types VALUES(%s, '%s')" % (n, name))
    weapon_types.close()

    # Create the claim modes table and populate it.
    cur.execute('CREATE TABLE claim_modes(id INT PRIMARY KEY, name '
                'VARCHAR(35))')
    for mode in claim_modes:
        n = mode.split('=')[0].strip()
        name = mode.split('=')[1].strip()
        cur.execute("INSERT INTO claim_modes VALUES(%s, '%s')" % (n, name))
    claim_modes.close()

    # Create the target types table and populate it.
    cur.execute('CREATE TABLE target_types(id INT PRIMARY KEY, name '
                'VARCHAR(35))')
    for type in target_types:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO target_types VALUES(%s, '%s')" % (n, name))
    target_types.close()

    # Create the attack types table and populate it.
    cur.execute('CREATE TABLE attack_types(id INT PRIMARY KEY, name '
                'VARCHAR(35))')
    for type in attack_types:
        n = type.split('=')[0].strip()
        name = type.split('=')[1].strip()
        cur.execute("INSERT INTO attack_types VALUES(%s, '%s')" % (n, name))
    attack_types.close()

    # Create the countries table and populate it.
    cur.execute('CREATE TABLE countries(id INT PRIMARY KEY, name VARCHAR(35))')
    for country in countries_file:
        n = country.split('=')[0].strip()
        name = country.split('=')[1].strip()
        cur.execute("INSERT INTO countries VALUES(%s, '%s')" % (n, name))
    countries_file.close()

    # Create the regions table and populate it.
    cur.execute('CREATE TABLE regions(id INT PRIMARY KEY, name VARCHAR(45))')
    for region in regions_file:
        n = region.split('=')[0].strip()
        name = region.split('=')[1].strip()
        cur.execute("INSERT INTO regions VALUES(%s, '%s')" % (n, name))
    regions_file.close()

    # Create the master 'gtd' table in preparation for inserting data.
    stmt = open('create_gtd_table.sql', 'rb').read()
    cur.execute(stmt)
    cur.execute('ALTER TABLE gtd OWNER TO %s' % USER)

    con.commit()

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
