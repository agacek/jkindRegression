
import xml.dom.minidom


def getArguments():

    argsList = list()

    doc = xml.dom.minidom.parse( 'test_config.xml' )
    # doc = xml.dom.minidom.parse( r'C:\Users\prmarti1\smaccm\jkind_test\test_workspace\jkindRegression\test_config.xml' )

    groups = doc.getElementsByTagName( 'ArgumentGroup' )

    for eachGroup in groups:
        args = eachGroup.getElementsByTagName( 'arg' )
        l = list()

        for eachArg in args:
            try:
                l.append( eachArg.firstChild.data )
            except AttributeError:
                l.append( '' )

        argsList.append( l )

    return argsList
