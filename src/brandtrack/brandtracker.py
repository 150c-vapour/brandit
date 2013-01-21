#!/usr/local/bin/python2.7
# encoding: utf-8
'''
brandtrack.brandtracker -- shortdesc

brandtrack.brandtracker is a description

It defines classes_and_methods

@author:     user_name
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import praw
import datetime
import time
import sqlite3
import threading

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2013-01-19'
__updated__ = '2013-01-19'

DEBUG = 1
TESTRUN = 0
PROFILE = 0


class BrandTracker(threading.Thread):
    def __init__(self, dbfn):
        threading.Thread.__init__(self)
        
        self.database_file = dbfn


    def run(self):

        dbconn = sqlite3.connect( self.database_file )
              
        self.cursor = dbconn.cursor()
        
        self.dbconn = dbconn
        
        user_agent = "Corporate Karma monitor 1.0 by /u/150c_vapour"
        self.r = praw.Reddit(user_agent=user_agent)
        
        
        login = "memewarri0r"
        password = "fucktacos"
        
        self.r.login(login, password)
        
        while True:
            self.cursor.execute( "SELECT * FROM brands")
            
            rows = self.cursor.fetchall()
            
            for row in rows:
                
                now = datetime.datetime.now()
            
                print 'searching term "' + row[1] + '"'
                
                brand_mentions = self.r.search( row[1], subreddit=None, sort='new', limit=10 )
                        
                for s in brand_mentions:
                    self.cursor.execute( "SELECT COUNT(*) from ignoresubs WHERE (name='" + s.subreddit.url + "')" )
                                 
                    if self.cursor.fetchone()[0] == 0:    
                        """ add it to the brandmentions table if it's a new post """
                        self.cursor.execute( "SELECT COUNT(*) from brandmentions WHERE (id='" + s.id + "')" )
                                     
                        post_tracked = self.cursor.fetchone()[0] > 0;
                        
                        if not post_tracked:
                            self.cursor.executemany( "INSERT INTO brandmentions VALUES( ?, ?, ?, ?, ?, ? )",
                                        [ (s.id, s.author.name, s.title, s.subreddit.url, now, '') ] )
                            
                            self.cursor.executemany( "INSERT INTO posttracking VALUES( ?, ?, ?, ?, ? )",
                                        [ (s.id, now, s.score, s.ups, s.downs) ] )    
                            
                            print  s.subreddit.url + ": " + s.title + ' {:d}'.format(s.score)
                        
                        
                        """ only update the past tracking table when the voting values change """                
                        self.cursor.execute( "SELECT MAX(timestamp),score,ups,downs from posttracking WHERE (id='" + s.id + "')" );
                                            
                        row = self.cursor.next()
                        
                        if row[1] != None and not (row[1] == s.score and row[2] == s.ups and row[3] == s.down):                                            
                            self.cursor.executemany( "INSERT INTO posttracking VALUES( ?, ?, ?, ?, ? )",
                                        [ (s.id, now, s.score, s.ups, s.downs) ] )            
                                                      
                            print ("posttracking updated: " + s.subreddit.url + ": " 
                                   + s.title + " {:d} {:d}/{:d}   delta: {:d} {:d}/{:d}"
                                   .format(s.score, s.ups, s.downs, s.score - row[1], s.ups - row[2], s.downs - row[3])) 
                        
                        self.dbconn.commit()
            
                    else:
                        pass
                    
                time.sleep( 5 )
    
    

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument(dest="paths", help="paths to database [default: %(default)s]", metavar="path", nargs='+')
        
        # Process arguments
        # args = parser.parse_args()
        
        #paths = args.paths
        #verbose = args.verbose
        
        if False > 0:
            print("Verbose mode on")

        tracker =  BrandTracker( 'fucktacos.db' )
        
        tracker.start()
        
        while True:
            pass
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        sys.argv.append("-v")
        sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'brandtrack.brandtracker_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
