#!/usr/bin/env python

import os, random, shutil, stat, time

starttime = time.time()

randomuuid = str(random.randrange(1000000000, 9999999999)).decode('utf-8')

COLLECT_DIR=u'collected-scores-files'
COLLECT_DIR_FFN=os.path.join(u'..', COLLECT_DIR)
os.mkdir(COLLECT_DIR_FFN)

for dirp, dirfns, fns in os.walk(u'.'):
     for fn in fns:
         if fn.startswith(u'scores'):
             ffn = os.path.join(dirp, fn)
             ftime = os.stat(ffn)[stat.ST_MTIME]
             if ftime < (starttime - 4):
                 targfname = u'scores-'+randomuuid+'-'+os.path.basename(dirp)+fn
                 shutil.copy2(ffn, os.path.join(COLLECT_DIR_FFN, targfname))
