from .internaldata import ConfigData


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
        # self.K = ''


    def equal( self, arg ):
        if( ( arg.name == self.name ) and ( arg.answer == self.answer ) ):
            return True
        return False


class RunResult( object ):
    '''
    blah blah blah 
    '''
    def __init__( self, filename, argumentString, propertyList ):
        self._filename = filename
        self._argumentString = argumentString

        # Convert the property list to a dictionary, key being the name
        # of the property and the value being the property itself.
        self.resultDict = dict()
        for each in propertyList:
            self.resultDict[each.name] = each


    def argumentStr( self ):
        return self._argumentString


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
