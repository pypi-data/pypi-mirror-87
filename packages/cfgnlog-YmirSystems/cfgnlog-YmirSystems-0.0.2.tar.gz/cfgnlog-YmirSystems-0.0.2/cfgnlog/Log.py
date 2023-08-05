#!/usr/bin/python

from datetime import datetime

class Log( ):
    def __init__( self ):
        self.logfile = None
        self.backlog = []
    def append( self, mesg ):
        mesg = '{:%Y-%m-%dT%H:%M:%SZ}'.format(datetime.utcnow()) + ' ' + mesg + '\n'
        print( mesg )
        if( self.logfile ):
            try:
                fh = open( self.logfile, 'a' )
                fh.write( mesg )
            except IOError as e:
                print( "\nERROR: Unable to append mesg to logfile" )
                print( "\n\tLogfile: " + self.logfile )
                print( "\n\t" + e.strerror )
        else: self.backlog.append( mesg );
    def setfile( self, filename ):
        try:
            fh = open( filename, "a+" );
            for mesg in self.backlog: fh.write( mesg );
            fh.close()
        except IOError as e:
            print( "\nError: " + e.strerror + ": " + filename )
            return
        self.backlog = []
        self.logfile = filename
