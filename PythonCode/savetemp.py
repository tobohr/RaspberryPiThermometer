#!/usr/bin/env python

import MySQLdb

def gettemp(id):
  try:
    mytemp = ''
    f = open('/sys/bus/w1/devices/' + id + '/w1_slave', 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 99999
    f.close()

    return int(mytemp[1])

  except:
    return 99999

id_Outside = '28-0214631ea0ff'
id_Inside = '28-04146a7a1cff'
tempOutside = gettemp(id_Outside)/float(1000)
tempInside = gettemp(id_Inside)/float(1000)

if id_Outside != 99999:
   print "Temp : " + '{:.3f}'.format(tempInside)
   print "Temp : " + '{:.3f}'.format(tempOutside)

   db = MySQLdb.connect("localhost", "user", "pass", "temp")
   curs=db.cursor()
   try:
       curs.execute ("INSERT INTO Data(temp,time,location_id) values(" + repr(tempOutside) + ",NOW(),0)")
       curs.execute ("INSERT INTO Data(temp,time,location_id) values(" + repr(tempInside) + ",NOW(),1)")
       db.commit()
       print "Data committed"
   except:
       print "Error: the database is being rolled back"
       db.rollback()
else:
   print "couldn't read temp  "
