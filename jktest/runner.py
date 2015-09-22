
import unittest
from jktest.guiIF import GuiIF


class MyTextTestRunner( unittest.TextTestRunner ):

    def run( self, test ):
        # res = ( super( MyTextTestRunner, self ).run( test ) ).wasSuccessful()

        res = ( super( MyTextTestRunner, self ).run( test ) )


        if( res.wasSuccessful() == True ):
            GuiIF().incrTestPass()
        else:
            GuiIF().incrTestFail()

        return res
