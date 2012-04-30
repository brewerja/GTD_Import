#!/usr/bin/python

import os
import sys
import csv
import psycopg2

from settings import DATABASE, USER


def pstr(string):
    """Processing for a varchar or text column. Returns any text in UTF-8."""
    if not string:
        return 'NULL'
    else:
        string = string.decode('latin-1').replace("'", "''")
        return "'" + string + "'"


def intgr(integer):
    """Processsing for an integer column."""
    if not integer or integer == '0' or integer == '-9' or integer == '-99':
        return 'NULL'
    else:
        return int(integer)


def floatr(number):
    """Processsing for a real (float) column."""
    if not number or number == '-9' or number == '-99':
        return 'NULL'
    else:
        return float(number)


def bools(value):
    """Processing for a boolean column. Returns "'0'" or "'1'" or 'NULL'"""
    # See 20000225007 claimed = '2'
    if value != '0' and value != '1':
        return 'NULL'
    else:
        return repr(value)


os.chdir('data')
os.system('tar xzvf gtd.tgz')
os.chdir('..')
reader = csv.reader(open('data/gtd.csv', 'rb'))
months = range(1, 13)
days = range(1, 32)

con = None

try:
    # Connect to the database.
    con = psycopg2.connect(database=DATABASE, user=USER)
    cur = con.cursor()

    cur.execute('SELECT * FROM dbsources')
    dbsources = {}
    for p in cur.fetchall():
        dbsources[str(p[1])] = p[0]

    # Traverse the csv file one line at a time.
    for l in reader:

        # I. GTD ID
        id = int(l[0])
        cur.execute("INSERT INTO gtd(id) VALUES(%s)" % id)
        print id

        # II. Incident Date
        year, month, day = intgr(l[1]), intgr(l[2]), intgr(l[3])
        stmt = ("UPDATE gtd SET year=%s, month=%s, day=%s where id=%s" %
                    (year, month, day, id))
        cur.execute(stmt)

        if month in months and day in days:  # Unknowns are '0'
            date = '%d-%02d-%02d' % (year, month, day)
            cur.execute("UPDATE gtd SET date='%s' where id=%s" % (date, id))

        approxdate, extended = pstr(l[4]), bools(l[5])
        resolution = l[6].strip().split('/')
        if len(resolution) == 3:
            month, day, year = resolution
            resolution = '%d-%02d-%02d' % (int(year), int(month), int(day))
            cur.execute("UPDATE gtd SET resolution='%s' where id=%s" %
                        (date, id))

        # III. Incident Location
        country, region = l[7], l[9]
        provstate, city = pstr(l[11]), pstr(l[12])
        vicinity, location = bools(l[13]), pstr(l[14])
        stmt = ("UPDATE gtd SET country=%s, region=%s, provstate=%s, "
                "city=%s, vicinity=%s, location=%s where id=%s" %
                (country, region, provstate, city, vicinity, location, id))
        cur.execute(stmt)

        # IV. Incident Information
        (summary, crit1, crit2, crit3, doubtterr, alternative, multiple,
        conflict) = (pstr(l[15]), bools(l[16]), bools(l[17]), bools(l[18]),
                     bools(l[19]), intgr(l[20]), bools(l[22]), bools(l[23]))
        stmt = ("UPDATE gtd SET summary=%s, crit1=%s, crit2=%s, crit3=%s, "
                "doubtterr=%s, alternative=%s, multiple=%s, conflict=%s where "
                "id=%s" % (summary, crit1, crit2, crit3, doubtterr,
                           alternative, multiple, conflict, id))
        cur.execute(stmt)

        # V. Attack Information
        success, suicide = bools(l[24]), bools(l[25])
        attacktype1, attacktype2, attacktype3 = (intgr(l[26]), intgr(l[28]),
                                                 intgr(l[30]))
        stmt = ("UPDATE gtd SET success=%s, suicide=%s, attacktype1=%s, "
                "attacktype2=%s, attacktype3=%s where id=%s" %
                (success, suicide, attacktype1, attacktype2, attacktype3, id))
        cur.execute(stmt)

        # VI. Target/Victim Information
        targtype1, corp1, target1, natlty1 = (intgr(l[32]), pstr(l[34]),
                                              pstr(l[35]), intgr(l[36]))
        targtype2, corp2, target2, natlty2 = (intgr(l[38]), pstr(l[40]),
                                              pstr(l[41]), intgr(l[42]))
        targtype3, corp3, target3, natlty3 = (intgr(l[44]), pstr(l[46]),
                                              pstr(l[47]), intgr(l[48]))
        stmt = ("UPDATE gtd SET targtype1=%s, corp1=%s, target1=%s, "
                "natlty1=%s, targtype2=%s, corp2=%s, target2=%s, "
                "natlty2=%s, targtype3=%s, corp3=%s, target3=%s, "
                "natlty3=%s where id=%s" % (targtype1, corp1, target1, natlty1,
                                            targtype2, corp2, target2, natlty2,
                                            targtype3, corp3, target3, natlty3,
                                            id))
        cur.execute(stmt)

        # VII. Perpetrator Information
        gname, gsubname = pstr(l[50]), pstr(l[51])
        gname2, gsubname2 = pstr(l[52]), pstr(l[53])
        gname3, gsubname3 = pstr(l[54]), pstr(l[55])
        motive = pstr(l[56])
        guncertain1, guncertain2, guncertain3 = (bools(l[57]), bools(l[58]),
                                                 bools(l[59]))
        stmt = ("UPDATE gtd SET gname=%s, gsubname=%s, gname2=%s, "
                "gsubname2=%s, gname3=%s, gsubname3=%s, motive=%s, "
                "guncertain1=%s, guncertain2=%s, guncertain3=%s where id=%s" %
                (gname, gsubname, gname2, gsubname2, gname3, gsubname3, motive,
                guncertain1, guncertain2, guncertain3, id))
        cur.execute(stmt)

        # VIII. Perpetrator Statistics
        # nperps -99 or Unknown when not reported
        nperps, nperpcap = intgr(l[60]), intgr(l[61])
        stmt = ("UPDATE gtd SET nperps=%s, nperpcap=%s where id=%s" %
                (nperps, nperpcap, id))
        cur.execute(stmt)

        # IX. Perpetrator Claim of Responsibility
        claimed, claimmode, claimconf = (bools(l[62]), intgr(l[63]),
                                         bools(l[65]))
        claim2, claimmode2, claimconf2 = (bools(l[66]), intgr(l[67]),
                                          bools(l[69]))
        claim3, claimmode3, claimconf3 = (bools(l[70]), intgr(l[71]),
                                          bools(l[73]))
        compclaim = bools(l[74])
        stmt = ("UPDATE gtd SET claimed=%s, claimmode=%s, claimconf=%s, "
                "claim2=%s, claimmode2=%s, claimconf2=%s, claim3=%s, "
                "claimmode3=%s, claimconf3=%s where id=%s" %
                (claimed, claimmode, claimconf, claim2, claimmode2, claimconf2,
                 claim3, claimmode3, claimconf3, id))
        cur.execute(stmt)

        # X. Weapon Information
        weaptype1, weapsubtype1 = intgr(l[75]), intgr(l[77])
        weaptype2, weapsubtype2 = intgr(l[79]), intgr(l[81])
        weaptype3, weapsubtype3 = intgr(l[83]), intgr(l[85])
        weaptype4, weapsubtype4 = intgr(l[87]), intgr(l[89])
        weapdetail = pstr(l[91])
        stmt = ("UPDATE gtd SET weaptype1=%s, weapsubtype1=%s, weaptype2=%s, "
                "weapsubtype2=%s, weaptype3=%s, weapsubtype3=%s, "
                "weaptype4=%s, weapsubtype4=%s, weapdetail=%s where id=%s" %
                (weaptype1, weapsubtype1, weaptype2, weapsubtype2, weaptype3,
                 weapsubtype3, weaptype4, weapsubtype4, weapdetail, id))
        cur.execute(stmt)

        # XI. Casualty Information
        nkill, nkillus, nkillter = floatr(l[92]), floatr(l[93]), floatr(l[94])
        nwound, nwoundus, nwoundter = (floatr(l[95]), floatr(l[96]),
                                       floatr(l[97]))
        stmt = ("UPDATE gtd SET nkill=%s, nkillus=%s, nkillter=%s, nwound=%s, "
                "nwoundus=%s, nwoundter=%s where id=%s" %
                (nkill, nkillus, nkillter, nwound, nwoundus, nwoundter, id))
        cur.execute(stmt)

        # XII. Consequences
        property, propextent, propvalue, propcomment = \
                (bools(l[98]), intgr(l[99]), floatr(l[101]), pstr(l[102]))
        stmt = ("UPDATE gtd SET property=%s, propextent=%s, propvalue=%s, "
                "propcomment=%s where id=%s" % (property, propextent,
                                                propvalue,  propcomment, id))
        cur.execute(stmt)

        # XIII. Hostage/Kidnapping Additional Information
        (ishostkid, nhostkid, nhostkidus, nhours, ndays, divert,
        kidhijcountry, ransom, ransomamt, ransomamtus, ransompaid,
        ransompaidus, ransomnote, hostkidoutcome, nreleased) = \
        (bools(l[103]), floatr(l[104]), floatr(l[105]), floatr(l[106]),
         intgr(l[107]), pstr(l[108]), pstr(l[109]), bools(l[110]),
         floatr(l[111]), floatr(l[112]), floatr(l[113]), floatr(l[114]),
         pstr(l[115]), intgr(l[116]), floatr(l[118]))
        stmt = ("UPDATE gtd SET ishostkid=%s, nhostkid=%s, nhostkidus=%s, "
                "nhours=%s, ndays=%s, divert=%s, kidhijcountry=%s, ransom=%s, "
                "ransomamt=%s, ransomamtus=%s, ransompaid=%s, ransompaidus=%s,"
                "ransomnote=%s, hostkidoutcome=%s, nreleased=%s where id=%s" %
                (ishostkid, nhostkid, nhostkidus, nhours, ndays, divert,
                 kidhijcountry, ransom, ransomamt, ransomamtus, ransompaid,
                 ransompaidus, ransomnote, hostkidoutcome, nreleased, id))
        cur.execute(stmt)

        # XIV. Additional Information
        addnotes = pstr(l[119])

        # XV. Source Information
        scite1, scite2, scite3, dbsource = (pstr(l[120]), pstr(l[121]),
                                            pstr(l[122]), l[123])
        stmt = ("UPDATE gtd SET addnotes=%s, scite1=%s, scite2=%s, scite3=%s, "
                "dbsource=%s where id=%s" % (addnotes, scite1, scite2, scite3,
                                             dbsources[dbsource], id))
        cur.execute(stmt)

    con.commit()

    # Create cities table, populate gtd table with that data, then drop it.
    os.system('tar xzvf cities.tgz')
    os.system('psql -d %s -U %s -f cities.sql' % (DATABASE, USER))
    cur.execute('update gtd set lat=cities.lat, lon=cities.lon from cities'
                ' where cities.id=gtd.id')
    cur.execute('drop table cities')
    con.commit()

    os.system('rm cities.sql')
    os.system('rm data/gtd.csv')

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
