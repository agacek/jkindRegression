
import xml.dom.minidom
from xml.dom.minidom import Node


doc = xml.dom.minidom.parse( 'c:/temp/pre.lus.xml' )

props = doc.getElementsByTagName( 'Property' )

for each in props:
    print( each.getAttribute( 'name' ) )
    
# Get the first Property Attribute
ok2 = props[0]
ok2_name = ok2.getAttribute( 'name' )

# Get the Answer attribute from the Property
ok2_answer = ok2.getElementsByTagName( 'Answer' )[0]
ok2_valid = ok2_answer.firstChild.data  # get the data, valid or not
ok2_source = ok2_answer.getAttribute( 'source' )  # get the source (i.e. k-induction)

# Get the K attribute from the Property
ok2_k = ok2.getElementsByTagName( 'K' )[0]
ok2_k_num = ok2_k.firstChild.data  # get the k number

# Print the results
print( '------' )
print( ok2_name )
print( ok2_source )
print( ok2_valid )
print( ok2_k_num )

