

class ResultList( list ):

    def __eq__( self, other ):

        ok = True

        if isinstance( other, self.__class__ ):

            if( len( self ) != len( other ) ):
                s = '\nMismatch Property Counts'
                try:
                    a = self[0].arguments()
                    b = other[0].arguments()
                    s += ' between: <{} == {}> <{} == {}>'.format( a, len( self ), b, len( other ) )
                except:
                    pass
                print( s )
                ok = False

            else:
                # If we have matching number of property counts then test equality
                for ( x, y ) in zip( self, other ):
                    if( x != y ):
                        ok = False

            return ok

        elif( isinstance( other, type( None ) ) ):
            super.__eq__( self, other )

        else:
            raise AssertionError( 'Invalid class type for equality' )

    def __ne__( self, other ):
        return not self.__eq__( other )

    def copy( self ):
        rv = ResultList()
        for each in self:
            rv.append( each )
        return rv

    def pop( self ):
        rv = self[len( self ) - 1]
        self.__delitem__( len( self ) - 1 )
        return rv


class JKindResult( object ):

    def __init__( self, filename, argString ):
        self.d = dict()
        self.fname = filename
        self.args = argString
        self._equal = False

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
        self._equal = True

        if isinstance( other, self.__class__ ):

            a = self.d.keys()
            b = other.d.keys()

            try:
                if( a != b ):
                    err = 'Unequal number of Properties: {} != {}'.format( len( a ), len( b ) )
                    self._logFailure( err )

                elif( self.d['name'] != self.other.d['name'] ):
                    err = 'Name mismatch:  {} != {}'.format( self.d['name'], self.other.d['name'] )
                    self._logFailure( err )

                elif( self.d['answer'] != self.other.d['answer'] ):
                    if( not ( ( self.d['answer'] == 'unknown' ) or ( self.other.d['answer'] == 'unknown' ) ) ):
                        err = 'Answer mismatch: {} != {}'.format( self.d['answer'], self.other.d['answer'] )
                        self._logFailure( err )

                elif( ( self.d['answer'] == 'falsifiable' ) and ( self.other.d['answer'] == 'falsifiable' ) ):
                    if( self.d['K'] != self.other.d['K'] ):
                        err = 'K mismatch: {} != {}'.format( self.d['K'], self.other.d['K'] )
                        self._logFailure( err )

            except KeyError as e:
                err = 'Key Error Exception: Missing field {}'.format( str( e ) )
                self._logFailure( err )
        else:
            raise AssertionError( 'Invalid class type for equality' )

        return ( self._equal )


    def _logFailure( self, err ):
        s = '{}: <{}> <{}>\n  '.format( self.fname, self.args, self.other.args )
        s += err
        print( s )
        self._equal = False
