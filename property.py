'''
Created on Sep 2, 2015

@author: prmarti1
'''

class Property( object ):
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
