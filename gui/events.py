

class EventTypes( object ):
    '''
    Public Class
    '''
    FILE_UPDATE = 1
    ARG_UPDATE = 2
    RESULT_UPDATE = 3
    TEST_DONE = 4


class Events( object ):
    '''
    Public Class
    '''

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    # _updateMethods = None
    _dict = {
             EventTypes.FILE_UPDATE : list(),
             EventTypes.ARG_UPDATE : list(),
             EventTypes.RESULT_UPDATE : list(),
             EventTypes.TEST_DONE : list()
             }


    def __init__( self ):
        '''
        Constructor
        '''
        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def registerUpdateMethod( self, eventType, method ):
        try:
            self._dict[eventType].append( method )
        except KeyError as key:
            print( 'Invalid Event Key Registration: ' + str( key ) )


    def update( self, eventType ):
        try:
            l = self._dict[eventType]
            for each in l:
                each()
        except KeyError:
            pass
