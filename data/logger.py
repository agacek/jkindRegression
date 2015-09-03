

class Logger( object ):

    # Define the shared state - Borg DP
    __we_are_the_borg_we_are_one = {}



    def __init__( self ):

        # Set the shared state - Borg DP
        self.__dict__ = self.__we_are_the_borg_we_are_one


    def initializeLogger( self ):
        pass


    def log( self, logstr ):

        print( logstr )
