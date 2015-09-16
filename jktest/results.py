


class JKindResult( object ):

    def __init__( self, filename, argString ):
        self.d = dict()
        self.fname = filename
        self.args = argString
        self.failLog = list()

    def __setitem__( self, key, val ):
        self.d[key] = val

    def __getitem__( self, key ):
        return self.d[key]

    def __lt__( self, other ):
        return self.d['name'] < other.d['name']

    def __ne__( self, other ):
        return not self.__eq__( other )

    def __eq__( self, other ):
        self.other = other
        # self.failLog = list()

        if isinstance( other, self.__class__ ):

            # if( self.d != other.d ):
            #    self._logFailure( 'd doesnt match' )

            a = self.d.keys()
            b = other.d.keys()

            if( a != b ):
                err = 'Unequal number of Properties: {} != {}'.format( len( a ), len( b ) )
                self._logFailure( err )

            for key in a:
                try:
                    if( ( self.d[key] != 'unknown' ) and ( other.d[key] != 'unknown' ) ):
                        if( self.d[key] != other.d[key] ):
                            err = 'Key/Value mismatch: {}:{} {}:{}'.format( key,
                                                                            self.d[key],
                                                                            key,
                                                                            other.d[key] )
                            self._logFailure( err )
                except KeyError as e:
                    err = 'Missing field {}'.format( str( e ) )
                    self._logFailure( err )
        else:
            raise AssertionError( 'Invalid class type for equality' )

        return ( len( self.failLog ) == 0 )


    def _logFailure( self, err ):
        s = '{}: <{}> <{}>\n  '.format( self.filename(), self.arguments(), self.other.arguments() )
        s += err
        self.failLog.append( s )

    def failures( self ):
        return self.failLog

    def filename( self ):
        return self.fname

    def arguments( self ):
        return self.args
