
import unittest
from jktest.guiIF import GuiIF


class MyTextTestRunner( unittest.TextTestRunner ):

    def run( self, test ):
        res = ( super( MyTextTestRunner, self ).run( test ) ).wasSuccessful()
        if( res == True ):
            GuiIF().incrTestPass()
        else:
            GuiIF().incrTestFail()

        return res
