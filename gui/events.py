'''
This file contains the classes to trigger "events" to the tk GUI.
These really aren't true events, but rather a layer between the JKind tests
and the tk GUI. In most cases these are kinda recursive in that the "event"
calls a registered GUI method and that GUI method in turn calls in to the
JKind test modules to get data.
'''

class EventTypes( object ):
    '''
    **Public Class**
    
    This class defines the "Constants" for the update types.
    The GUI will use these definitions to register an update method.
    The JKind test modules use these to trigger the registered GUI methods.
    
    .. note::
        The constants are defined as class variables so that they may be
        accessed without instantiating this class.
        
    .. warning::
        Do not change the values of these "Constants". Doing so will break
        the registration scheme between the events and the GUI.
         
    '''

    ARG_UPDATE = 1
    FILE_UPDATE = 2
    RESULT_UPDATE = 3
    TEST_DONE = 4


class Events( object ):
    '''
    **Public Class**
    
    This class provides the mechanism to register methods to be called when
    triggered with an update for a particular event.
    
    This class implements the **Borg** Design Pattern. This DP is similar to a 
    Singleton, except that it is explicitly instantiated and contains shared
    data. Each instantiation is a unique object but all objects share the internal
    __dict__ and thus all share the data.
    
    '''

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}

    # Define shared data
    _dict = {
             EventTypes.FILE_UPDATE : list(),
             EventTypes.ARG_UPDATE : list(),
             EventTypes.RESULT_UPDATE : list(),
             EventTypes.TEST_DONE : list()
             }


    def __init__( self ):
        '''
        **Constructor**
        
        Sets the shared state per the Borg Design Pattern.
        
        '''
        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def registerUpdateMethod( self, eventType, method ):
        '''
        **Public Method**
        
        Registers a method to be called with the desired event type
        enumeration. Allows for multiple methods to be registered with each
        individual event type.
        
        :param eventType: The desired event type for the method. Typically use
                          the EventType class enumerations.
        :type eventType: int
        :param method: The class-method (or individual function) to call when
                       triggered by this class's update method.
        :type method: method *or* function
        
        :return: n/a:
        
        '''
        try:
            self._dict[eventType].append( method )
        except KeyError as key:
            print( 'Invalid Event Key Registration: ' + str( key ) )


    def update( self, eventType ):
        '''
        **Public Method**
        
        Given an event type will call any methods previously registered with
        this event type. Does nothing if no methods are registered to the
        event type.
        
        :param eventType: The desired event type for the method. Typically use
                          the EventType class enumerations.
        :type eventType: int
        
        :return: n/a:
        
        '''
        try:
            l = self._dict[eventType]
            for each in l:
                each()
        except KeyError:
            pass
