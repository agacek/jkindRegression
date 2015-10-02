'''
This module contains the class definitions for the ResultList and 
the JKindResult.

'''

class ResultList( list ):
    '''
    **Public Class**
    
    This class sub-classes the built-in list class. This was needed so that
    the equal and not-equal methods could be overridden to meet specific
    needs.
    
    .. warning::
    
        Assumes that the list elements are of JKindResult or some other
        sortable type.
    
    .. rubric:: **OBJECT METHOD OVERRIDES**
    
    __eq__( self, other )
        Override of the built-in object equality method.
        
        Checks whether the equality is against a class of this type
        or against the None type. Then checks that the internal list lengths
        match, and if so, will check the equality of the list elements.
        Typically the list elements will be of type JKindResult, but any 
        sortable type will suffice.
        
        Assumes that the lists have been sorted. This means that the 
        internal list elements must implement the __lt__ and __gt__ methods.
        
        Return bool True if equal, otherwise False.
        

    __ne__( self, other ) 
        Negation of the __eq__ method
        
        Return bool True if equal, otherwise False.
        
    '''

    def __eq__( self, other ):

        ok = True  # initialize the equality result

        # First check that the object compared to is the same type as this.
        if isinstance( other, self.__class__ ):

            # Check that the lengths of the internal lists are equal.
            if( len( self ) != len( other ) ):
                s = '\nMismatch Property Counts'
                try:
                    a = self[0].getArguments()
                    b = other[0].getArguments()
                    s += ' between: <{} == {}> <{} == {}>'.format( a, len( self ), b, len( other ) )
                except:
                    pass
                print( s )
                ok = False

            # Lengths match up, so now check the equality of the list elements.
            #
            else:
                # If we have matching number of property counts then test equality.
                # Assumes that the internal list elements implement the less-than
                # and greater-than built-in methods.
                for ( x, y ) in zip( self, other ):
                    if( x != y ):
                        ok = False

            return ok

        # Handles the case of a None type supplied.
        elif( isinstance( other, type( None ) ) ):
            super.__eq__( self, other )

        # Don't know what happened so raise an Exception.
        else:
            raise AssertionError( 'Invalid class type for equality' )


    def __ne__( self, other ):
        return not self.__eq__( other )


    def copy( self ):
        '''
        **Public Method**
        
        Returns a new ResultList object, populated with the internal
        list elements.
        
        :rtype: ResultList
        
        '''
        rv = ResultList()
        for each in self:
            rv.append( each )
        return rv


    def pop( self ):
        '''
        **Public Method**
        
        Override of the Base Class pop method.
        Pops the last item in the internal list.
        
        :rtype: indeterminate
        
        '''
        rv = self[len( self ) - 1]
        self.__delitem__( len( self ) - 1 )
        return rv


class JKindResult( object ):
    '''
    **Public Class**
    
    This class is intended to contain the results of the JKind run. Typically
    the results are read from the output XML file and then used to populate
    an instantiation of this class. Though does not sub-class the built-in dict 
    type, this class implements the __setitem__ and __getitem__ methods so that
    it will act in similar fashion to the dict class. This class is used in 
    lieu of the dict type because the dict does not inherently support sorting
    and we also needed specific equality testing.
    
    To maintain compatibility with the intended usage of the ResultList class,
    the __lt__, __gt__, __eq__ and __ne__ methods are implemented. These allow
    for sorting and comparisons. 
            
    .. note::
        When testing equality, any failures will be printed to stdout.
    
    .. warning::
        When used in the context of the JKind Regression Suite application,
        the assumption is that "name", "answer" and "K" will be set with
        the values read from the XML output file.
        EX:
        
        - jkr = JKindResult( fname, argstr)                
        - jkr['name'] = 'ok1'
        - jkr['answer'] = 'valid'                
        - jkr['K'] = '1'
    
    
    .. rubric:: **OBJECT METHOD OVERRIDES**
    
    __lt__( self, other )
        Implements the less-than method. Compares the "name" items of the
        dict data members
        
        Returns bool
    
    __gt__( self, other )
        Implements the greater-than method. Compares the "name" items of the
        dict data members
        
        Returns bool
    
    __eq__( self, other )
        Implements the equality method for the JKindResult class.
        Tests for equality:
        
        - Each dict data member has the same number of keys, meaning that the
          same number of Property elements were read from the XML output files.
        - The "name" key/value pairs of the dict data members are the same
        - The "answer" key/value pairs of the dict data members are the same.
          If one or both of the values are "unknown" this is considered
          equal (ok).
        - If the "answer" key/value pairs are "falsifiable", checks that the
          "K" key/value pairs are equal.
          
        Returns bool 
            
    __ne__( self, other )
        Negation of the __eq__ method
        
        Returns bool
    
    .. rubric:: **DICT TYPE METHOD IMPLEMENTATIONS**
    
    __setitem__( key, val )
        Allows use of dict type notation to set items.
    
    __getitem__( key )
        Allows use of dict type notation to get items.
        
        Returns the value of the supplied key.     
    
    '''

    def __init__( self, filename, argString ):
        '''
        **Constructor**
        
        :param filename: The filename run to generate these results
        :type filename: str
        :param argString: The arguments run to generate these results
        :type argString: str
        
        '''
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


    def getArguments( self ):
        '''
        **Public Method**
        
        Returns the argument string
        
        :rtype: str
        
        '''
        return self.args


    def _logFailure( self, err ):
        '''
        **Private Method**
        
        Called to log a failure to stdout. String contains the filename,
        arguments of this result class, arguments of the comparison result
        class and the specific error message from the caller.
        
        Sets the equal data member to false.
        
        :param err: Error string to append to report
        :type err: str
        
        :return: n/a:
        
        '''
        s = '{}: <{}> <{}>\n  '.format( self.fname, self.args, self.other.args )
        s += err
        print( s )
        self._equal = False


class ExceptionReport( object ):
    '''
    **Public Class**
    
    This class is just a simple container for Java Exception Text and the
    set of arguments that caused it.
    
    '''

    def __init__( self ):
        '''
        **Constructor**
        
        Sets the public data members.
        
        '''
        self.text = ''
        self.args = ''
