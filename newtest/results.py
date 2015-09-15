


class JKindResult( object ):

    def __init__( self, filename, argString ):
        self.d = dict()
        self.fname = filename
        self.args = argString
        self.failures = list()

    def __setitem__( self, key, val ):
        self.d[key] = val

    def __getitem__( self, key ):
        return self.d[key]

    def __eq__( self, other ):
        self.other = other
        self.failures = list()

        if isinstance( other, self.__class__ ):
            a = sorted( self.d.keys() )
            b = sorted( other.d.keys() )
            if( a != b ):
                err = 'Unequal number of Properties: {} != {}'.format( len( a ), len( b ) )
                self._logFailure( err )

            for key in a:
                if( ( self.d[key] != 'unknown' ) and ( other.d[key] != 'unknown' ) ):
                    if( self.d[key] != other.d[key] ):
                        err = 'Key/Value mismatch: {}:{} {}:{}'.format( key,
                                                                        self.d[key],
                                                                        key,
                                                                        other.d[key] )
                        self._logFailure( err )
        else:
            raise AssertionError( 'Invalid class type for equality' )

        return ( len( self.failures ) == 0 )

    def _logFailure( self, err ):
        s = '{}: <{}> <{}>\n  '.format( self.filename(), self.arguments(), self.other.arguments() )
        s += err
        self.failures.append( s )

    def __ne__( self, other ):
        return not self.__eq__( other )

    def filename( self ):
        return self.fname

    def arguments( self ):
        return self.args
