'''
Created on Sep 2, 2015

@author: prmarti1
'''

class Property( object ):
    '''
    classdocs
    '''
    def __init__( self, params ):
        '''
        Constructor
        '''
        self.name = ''
        self.source = ''
        self.answer = ''
        self.K = ''
        
        
    def printAttrs( self ):
        print( 'Name:   ' + self.name )
        print( 'Source: ' + self.source )
        print( 'Answer: ' + self.answer )
        print( 'K:      ' + self.K )
