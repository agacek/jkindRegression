'''
This file contains the classes to trigger "events" to the tk GUI.
These really aren't true events, but rather a layer between the JKind tests
and the tk GUI. In most cases these are kinda recursive in that the "event"
calls a registered GUI method and that GUI method in turn calls in to the
JKind test modules to get data.
'''

class EventTypes( object ):
    '''
    Public Class
    
    This class defines the "Constants" for the update types.
    The GUI will use these definitions to register an update method.
    The JKind test modules use these to trigger the registered GUI methods.
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
