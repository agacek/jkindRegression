from .internaldata import InternalData


class XmlProperties( object ):
    '''
    classdocs
    '''
    def __init__( self ):
        '''
        Constructor
        '''
        self.name = ''
        self.source = ''
        self.answer = ''
        self.K = ''


    def toString( self ):
        s = ' \n'
        s += 'Name:   ' + self.name + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Answer: ' + self.answer + '\n'
        s += 'K:      ' + self.K + '\n'
        return s


    def equal( self, arg ):
        if( ( arg.name == self.name ) and ( arg.answer == self.answer ) ):
            return True
        return False


class FileResults( object ):
    '''
    blah blah blah 
    '''
    def __init__( self, filename, argumentString, propertyList ):
        self.filename = filename
        self.argumentString = argumentString

        # Convert the property list to a dictionary, key being the name
        # of the property and the value being the property itself.
        self.resultDict = dict()
        for each in propertyList:
            self.resultDict[each.name] = each


    def toString( self ):
        s = '\n-----------------------\n'
        s += 'Filename:  ' + self.filename + '\n'
        s += 'Arguments: ' + self.argumentString + '\n'
        if ( InternalData().isVerbose() == True ):
            for key in self.resultDict:
                s += self.resultDict[key].toString()

        return s


    def count( self ):
        return len( self.resultDict )


    def dict( self ):
        return self.resultDict


    def equal( self, arg ):

        # Test that the length of the results are the same
        if( ( arg.count() < 1 ) or ( arg.count() != self.count() ) ):
            return False

        # Test that each variable result was the same
        for key in arg.dict():
            if( arg.dict()[key].equal( self.resultDict[key] ) == False ):
                return False

        return True
