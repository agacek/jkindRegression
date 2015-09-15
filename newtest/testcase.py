
from newtest.testdata import TestData



def testFunction():
    fname = TestData().popFile()
    print( fname )

    for each in TestData()._argsList:
        print( each )




def mySetUp():
    pass


def myTearDown():
    pass
