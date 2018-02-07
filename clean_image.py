#!/usr/bin/python
# -*- coding: UTF-8 -*-
print "\n"
print "╔══════════════════════════════ ♡ ═ ♫ ♫ ♫ ═ ♡ ═══════════════════════════════╗"
print "║                                                                            ║"
print "║            _______                       _      _  _                       ║"
print "║            (_______)                     | |    | |(_)                     ║"
print "║             _____     ____   ____  ____  | |  _ | | _  ____                ║"
print "║            |  ___)   / ___) / _  ||  _ \ | | / )| || ||  _ \               ║"
print "║            | |      | |    ( ( | || | | || |< ( | || || | | |              ║"
print "║            |_|      |_|     \_||_||_| |_||_| \_)|_||_||_| |_|              ║"
print "║                                                                            ║"
print "║                                                                            ║"
print "║                Docker images clear tool. Author: Franklin                  ║"
print "║                                                                            ║"
print "╚══════════════════════════════ ♡ ═ ♫ ♫ ♫ ═ ♡ ═══════════════════════════════╝"

import sys, os, json, httplib, urllib, base64, socket, commands
retained_num = 3;
print "\nBegin to list all the docker images..."
(status, image_list) = commands.getstatusoutput("docker images --digests")
#print status
if status != 0:
  print "Error: error code='%s' " % status
else:
  obsolete_images = []
  latestImageDic = {}
  list = image_list.split('\n')
  for row in list:
    #print row
    column = row.split( )
    repository = column[0]
    if(repository == 'REPOSITORY'):
      continue
    tag = column[1]
    digest = column[2]
    if(latestImageDic.has_key(repository)):
      num = latestImageDic[repository];
      if( num < retained_num ):
        num += 1;
        latestImageDic[repository] = num;
        print "Retain %s:%s" % (repository, tag)
      else:
        if (digest == '<none>'):
          obsolete_images.append("%s:%s" % (repository, tag))
          print "Prepare to delete %s:%s" % (repository, tag)
        else:
          obsolete_images.append("%s@%s" % (repository, digest))
          print "Prepare to delete %s@%s" % (repository, digest)
    else:
      latestImageDic[repository] = 1;
      print "Retain %s:%s" % (repository, tag)

  print "------------------------\n"
  print "Begin to delete images..."
  for image in obsolete_images:
    #print image
    os.system("docker rmi %s" % image)

  print "Complete to delete obsoleted images."
