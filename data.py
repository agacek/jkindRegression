

class JKindResults( object ):
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


    def printAttrs( self ):
        print( '\n-------' )
        print( 'Name:   ' + self.name )
        print( 'Source: ' + self.source )
        print( 'Answer: ' + self.answer )
        print( 'K:      ' + self.K )


    def toString( self ):
        s = '------\n'
        s += 'Name:   ' + self.name + '\n'
        s += 'Source: ' + self.source + '\n'
        s += 'Answer: ' + self.answer + '\n'
        s += 'K:      ' + self.K + '\n'
        return s


class FileTest( object ):
    '''
    blah blah blah 
    '''
    def __init__( self, filename = '', argumentString = '', resultList = list() ):
        self.filename = filename
        self.argumentString = argumentString
        self.resultList = resultList


    def toString( self ):
        s = '\n------------\n'
        s += 'Filename:  ' + self.filename + '\n'
        s += 'Arguments: ' + self.argumentString + '\n'
        for each in self.resultList:
            s += each.toString()
        return s


class FileSuite( object ):
    '''
    '''
    def __init__( self ):
        self.testList = list()


    def addFileTest( self, filetest ):
        self.testList.append( filetest )


    def toString( self ):
        s = ''
        for each in self.testList:
            s += each.toString()
        return s


    def validate( self ):
        pass
