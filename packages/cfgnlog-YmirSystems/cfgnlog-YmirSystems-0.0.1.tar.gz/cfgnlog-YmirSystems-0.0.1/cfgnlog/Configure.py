#!/usr/bin/python

# Exceptions are to be handled by caller:
#   IOError     - Unable to write to file
#   ValueError  - Malformed configuration file

import os, json
from collections import OrderedDict

def env( var ):
    val = os.getenv( var );
    if( val == None ): return '';
    return val

# XDG Specification Compliance # <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>
DEFAULT_MODE = 0o700
ENV_HOME = env( 'HOME' )
CONFIGURATION_DIRECTORY_XDG = 'XDG_CONFIG_HOME'
CONFIGURATION_DIRECTORY_XDG_DEF = os.path.join( ENV_HOME, '.config' )
DATA_DIRECTORY_XDG = 'XDG_DATA_HOME'
DATA_DIRECTORY_XDG_DEF =  os.path.join( ENV_HOME,  '.local', 'share' )
CACHE_DIRECTORY_XDG = 'XDG_CACHE_HOME'
CACHE_DIRECTORY_XDG_DEF = os.path.join( ENV_HOME, '.cache' )

# Windows Compatibility #
CONFIGURATION_DIRECTORY_WIN = 'LOCALAPPDATA'    #Except XP

DEFAULT_CONFIG_FILE_EXT = '.cfg'

class Configure(  ):
    def __init__( self, app_name, default_configuration_filename = None, config_file = None, log = None, is_partial = False ):
        '''
        app_name - The name of the application is used for keeping your app files separate from other apps.
        default_configuration_filename - This will override the default of "app_name.cfg".
        config_file - Use this if the full path to the configuration file is known or given by the user.
        is_partial - If more than one config file will be used for an application, this will create a directory for them called app_name.
        '''
        self.APP_NAME = app_name
        if( config_file == None ):
            config_file = env( CONFIGURATION_DIRECTORY_XDG )
            if( config_file == '' ): config_file = env( CONFIGURATION_DIRECTORY_WIN );
            if( config_file == '' ): config_file = CONFIGURATION_DIRECTORY_XDG_DEF;
            if( is_partial ): config_file = os.path.join( config_file, self.APP_NAME );
            if not os.path.exists( config_file ):
                if( log ): log.append( 'Creating configuration directory' + ': ' + config_file );
                os.makedirs( config_file, DEFAULT_MODE );
            if default_configuration_filename: config_file = os.path.join( config_file, default_configuration_filename );
            else: config_file = os.path.join( config_file, self.APP_NAME + DEFAULT_CONFIG_FILE_EXT );
        self.config_file = config_file;
        self.actions = {}
        self.dirty = False

    def add_update( self, key, value ):
        if not( self.options[key] == value ):
            self.options[key] = value
            self.dirty = True
            if key in self.actions:
                for trigger in self.actions[key]: trigger( );

    def add_action( self, key, action ):
        if not key in self.actions: self.actions[key] = [];
        self.actions[key].append( action )

    def add_dat( self ):
        ''' Add a data directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( 'DAT' not in self.options ):
            self.options['DAT'] = env( DATA_DIRECTORY_XDG )
            if( self.options['DAT'] == '' ): self.options['DAT'] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.options['DAT'] == '' ): self.options['DAT'] = DATA_DIRECTORY_XDG_DEF;
            self.options['DAT'] = os.path.join( self.options['DAT'], self.APP_NAME )
            self.dirty = True

    def add_log( self, default_log_filename = None, default_use_home = False ):
        ''' Add a log directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( 'LOG' not in self.options ):
            if default_log_filename: self.options['LOG'] = default_log_filename;
            else: self.options['LOG'] = self.APP_NAME + ".log";
            if default_use_home:
                self.options['LOG'] = os.path.join( ENV_HOME, '.'+self.options['LOG'] );
            else: self.options['LOG'] = os.path.join( self.options['DAT'], self.options['LOG'] );
            self.dirty = True

    def add_cache( self ):
        ''' Add a cache directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( 'CACHE' not in self.options ):
            self.options['CACHE'] = env( CACHE_DIRECTORY_XDG )
            if( self.options['CACHE'] == '' ): self.options['CACHE'] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.options['CACHE'] == '' ): self.options['CACHE'] = os.path.join( CACHE_DIRECTORY_XDG_DEF, self.APP_NAME );
            else: self.options['CACHE'] = os.path.join( self.options['CACHE'], self.APP_NAME, 'cache' ); #WINDOWS
            self.dirty = True

    def write( self ):
        fh = open( self.config_file, 'w', DEFAULT_MODE )
        fh.write( json.dumps( self.options, indent=4, separators=(',', ': ') ) )
        fh.close(  )
        self.dirty = False

    def load( self, default_configuration_parameters, log = None ):
        try:
            fh = open( self.config_file )
            self.options = json.loads( fh.read(  ), object_pairs_hook=OrderedDict )
            fh.close(  )
            for key in default_configuration_parameters:
                if( key not in self.options ):
                    self.options[key] = default_configuration_parameters[key]
                    self.dirty = True
        except IOError:
            self.options = default_configuration_parameters
            if log: log.append( 'Creating configuration file: ' + self.config_file );
            self.write(  )
        except ValueError as MalformedFileError:
            MalformedFileError.strerror = "Malformed configuration file"
            MalformedFileError.filename = self.config_file
            MalformedFileError.errno = 1
            raise MalformedFileError


if __name__ == '__main__':
    default_params = { "Testing" : "123" }
    config = Configure( "ConfigureTest", "delete.me" )
    config.load( default_params )
    config.add_dat(  )
    config.add_cache(  )
    config.add_log( default_use_home = True )
    print config.options
