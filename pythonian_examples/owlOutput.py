"""
Exporting Nextkb to OWL
"""

from pythonian import *
import logging
import time
import xml.dom
from xml.dom.minidom import parse, parseString
from io import *
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

# temporary:
p1 = 'C:/qrg/fire/flat-files/owl/test2.owl'

logger = logging.getLogger('OwlAgent')

global owl_agent  # a global for testing in a python shell

class OwlAgent(Pythonian):
    name = "OwlAgent" # This is the name of the agent to register with

    def __init__(self, **kwargs):
        super(OwlAgent, self).__init__(**kwargs)
        self.add_achieve('export', self.export)
        global owl_agent
        owl_agent = self  # bind the global
        #self.make_query()

    def export(self):
        logger.debug('testing achieve export')
        # initiate a query to the session reasoner

    def make_query(self):
        if self.name is not None:
            perf = KQMLPerformative('ask-all')
            perf.set('sender', self.name)
            perf.set('receiver', 'session-reasoner')
            perf.set('language', 'python')
            content = KQMLList(['predFacts', 'consumedObject'])
            perf.set('content', content)
            self.send(perf)
        
# To test exporter, send:
# (agents::send *facilitator* 'OwlAgent '(achieve :content (task :action (export))))
        

_OWL_COMMENT_ = """
       Next KB Knowledge Base

       Portions of this ontology were derived from OpenCyc, VerbNet, FrameNet, WordNet.
       Portions of this KB were developed by the Qualitive Reasoning Group at Northwestern University.
       This work is licensed under the Creative Commons Attribution 4.0 International License. 
       To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
     
      """

def export_owl(mt):
    seen = set()
    n_ary = {}
    impl = xml.dom.getDOMImplementation()
    dtype = impl.createDocumentType('RDF', None, None)
    doc = impl.createDocument("nextkb", "nextkb_name", None)
    rdf = setup_rdf_root(doc, mt)
    owl = setup_owl_root(doc, rdf, mt)
    populate_owl(doc, rdf, mt, seen, n_ary)
    outpath = pick_file()
    f = open(outpath, "w", encoding="utf-8")
    # output header
    doc.writexml(f, indent = "", addindent = "  ", newl = "\n")
    # output footer
    
def pick_file ():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    return asksaveasfilename()

def setup_rdf_root(doc, mt):
    root = doc.firstChild
    rdf = doc.createElement('RDF')
    base = "http://qrg.cs.northwestern.edu/nextkb/" + mt + ".owl"
    rdf.setAttribute("xmlns:cycAnnot", "&cycAnnot;")
    rdf.setAttribute("xmlns:opencyc", "&opencyc;")
    rdf.setAttribute("xmlns:cyc", "&cyc;")
    rdf.setAttribute("xmlns:skos", "&skos;")
    rdf.setAttribute("xmlns:owl2xml", "&owl2xml;")
    rdf.setAttribute("xmlns:owl", "&owl;")
    rdf.setAttribute("xmlns:rdfs", "&rdfs;")
    rdf.setAttribute("xmlns:rdf", "&rdf;")
    rdf.setAttribute("xmlns:xsd", "&xsd;")
    rdf.setAttribute("xml:base", base)
    rdf.setAttribute("xmlns", base + "#")
    root.appendChild(rdf)
    return rdf
    
def setup_owl_root(doc, rdf, mt):
    ont = doc.createElement("owl:Ontology")
    ver = doc.createElement("owl:versionInfo")
    tn = doc.createTextNode("Version 1.0")
    ont.setAttribute("rdf:about", mt)
    ver.appendChild(tn)
    ont.appendChild(ver)
    append_text_child(doc, ont, "rdfs:comment", _OWL_COMMENT_, True)
    rdf.appendChild(ont)
    return ont
    
def populate_owl(doc, rdf, mt, seen, nary):
    append_dom_comment(doc, rdf, "Annotation Properties")
    append_annotation_properties(doc, rdf, mt, seen)
    append_dom_comment(doc, rdf, "Datatype Properties")
    append_datatype_properties(doc, rdf, mt, seen)
    append_dom_comment(doc, rdf, "Object Properties")
    append_object_properties(doc, rdf, mt, seen)
    append_dom_comment(doc, rdf, "N-ary predicates")
    append_n_ary_predicates(doc, rdf, mt, seen, nary)
    append_dom_comment(doc, rdf, "Classes")
    append_owl_classes(doc, rdf, mt, seen)
    append_dom_comment(doc, rdf, "Instances")
    append_owl_individuals(doc, rdf, mt, seen)
    append_dom_comment(doc, rdf, "Axioms")
    append_nary_relation_instances(doc, rdf, mt, nary)

def append_annotation_properties(doc, root, mt, seen):
    for annotation in ["&rdfs;label", "&rdfs;comment"]:
        append_annotation_property(doc, root, annotation)

def append_annotation_property(doc, root, annotation):
    element = doc.createElement("owl:AnnotationProperty")
    element.setAttribute("rdf:about", annotation)
    root.appendChild(element)
    #append_linefeed(doc, root)


### Append datatype properties
### Iterate over the facts in the mt, picking out collections 
### corresponding to primitive datatypes and append a datatype property
def append_datatype_properties(doc, root, mt, seen):
    pass

### Append object properties
### Here, we want to go through binary predicates
### and set the properties
def append_object_properties(doc, root, mt, seen):
    pass

### Append N-ary predicates
### *** Actually, this is just for higher-arity preds.  It totally bails on true n-ary preds.
### n-ary is a hash table of higher-arity predicates that have been translated into 
### classes with local binary predicate roles.
def append_n_ary_predicates(doc, root, mt, seen, nary):
    pass

### Append classes
###   gather collections in mt
###   filter NATs
###   for each, call append_DOM_class
def append_owl_classes(doc, root, mt, seen):
    pass
    
### From the entity, you can get the comments, disjoints and the genls.
### isas seems to be empty in the object, though.

### Append individuals
def append_owl_individuals(doc, root, mt, seen):
    pass

### What we want to do is normalize this so that the tag name is the OpenCyc type,
### rather than just "owl:Thing"
### The name of the individual element should be the value of the about attribute,
### not the tagname


### Append instances of nary-relations
def append_nary_relation_instances(doc, root, mt, nary):
    pass

def append_dom_comment(doc, parent, text):
    append_linefeed(doc, parent)
    node = doc.createComment(" " + text + " ")
    parent.appendChild(node)

def append_linefeed(doc, parent):
    txtnode = doc.createTextNode('\n')
    parent.appendChild(txtnode)

def append_text_child(doc, parent, name, text, lang):
    # text = insert_string("&amp;", "&", text)
    # wrap CDATA around text containing tags ...
    child = doc.createElement(name)
    txtnode = doc.createTextNode(text)
    if lang:
        child.setAttribute("xml:lang", "en")
    child.appendChild(txtnode)
    parent.appendChild(child)
    # compress node?
    return child
    

def append_integer_child(doc, parent, name, int):
    child = doc.createElement(name)
    txtnode = doc.createTextNode(int)
    child.setAttribute("rdf:datatype", "&xsd;integer")
    child.appendChild(txtnode)
    parent.appendChild(child)
    
def append_resource_child(doc, parent, name, resource):
    child = doc.createElement(name)
    iri = iri_token(resource)
    child.setAttribute("rdf:resource", iri)
    parent.appendChild(child)
    
def append_collection_child(doc, parent, name, resource_type, member_names):
    child = doc.createElement(name)
    child.setAttribute("rdf:parseType", "Collection")
    for member in member_names:
        append_resource_child(doc, child, resource_type, member)
    parent.appendChild(child)

def append_datatype_child(doc, parent, name, type, value):
    child = doc.createElement(name)
    txtnode = doc.createTextNode(value)
    child.setAttribute("rdf:datatype", type)
    child.appendChild(txtnode)
    parent.appendChild(child)


###
### Utilities
###

def previously_seen(item, seen):
    if item in seen:
        return True
    else:
        seen.add(item)
        return False

### Intercept references to primitive datatypes:
def maps_to_datatype (collection):
    if collection in {'CharacterString', 'ProperNameString', 'ControlCharacterFreeString',
                      'Abbreviation', 'IDString', 'Acronym', 'PhoneNumber', 'SubLString',
                      'HumanGivenNameString', 'EPIC-FinancialIDString', 'IPAddress',
                      'MACAddress', 'EMailAddress', 'GUIDString', 'GraphicalStructure',
                      'Pathname'}:
        return "&xsd;string"
    elif collection == 'Date':
        return "&xsd;date"
    elif collection == 'Integer':
        return "&xsd;integer"
    elif collection == 'PositiveInteger':
        return "&xsd;positiveInteger"
    elif collection == 'NegativeInteger':
        return "&xsd;negativeInteger"
    elif collection == 'NonNegativeInteger':
        return "&xsd;nonNegativeInteger"
    elif collection == 'NonPositiveInteger':
        return "&xsd;nonPositiveInteger"
    elif collection == 'BitWidth':
        return "&xsd;positiveInteger"  # really from 1-128
    elif collection == 'UniformResourceIdentifier':
        return "&xsd;anyURI"
    else:
        return None
    

### Make sure obj serializes to a named entity reference.
### ie, disallow logic variables, make sure it doesn't start with a digit,
### turn NATs into names by converting "(" into _op_ and ")" into _cp_
### and turn spaces into underscores.  Also drop any occurence of "http"
### in the string.
def iri_token(resource):
    if isinstance(resource, str):
        return resource
    else:
        return maps_to_datatype(resource) or "#" + token(resource)

def token(obj):
    pass

### lisp symbols can start with numbers, but XML names can't.
def maybe_fix_first_char(symbol):
    if symbol[0].isalpha() or symbol[0] == '_':
        return symbol
    else: return "_" + symbol
    

### Matt Anderson's multi-replace:
def multi_replace(pairs, text):
    stack = list(pairs)
    stack.reverse()
    def replace(stack, parts):
        if not stack:
            return parts
        # copy the stack so I don't disturb parallel recursions
        stack = list(stack) 
        from_, to = stack.pop()
        #print 'split (%r=>%r)' % (from_, to), parts
        split_parts = [replace(stack, part.split(from_)) for part in parts]
        parts = [to.join(split_subparts) for split_subparts in split_parts]
        #print 'join (%r=>%r)' % (from_, to), parts
        return parts
    return replace(stack, [text])[0]


#print multi_replace(
#    [('foo', 'bar'), ('baaz', 'foo'), ('quux', 'moop')], 
#    'foobarbaazfooquuxquux')

###-------------------------------------------
###
### KB accessors
###

# (kb::list-mt-facts mt)
# (kb::map-over-facts #'append-datatype-properties-int)
# (kb::retrieve-collection colname)
# (kb::retrieve-predicate predname)
# (kb::the-arity entity)
# (kb::nat? entity)
# (kb::arg-isas entity)
# (kb::lisp-form (kb::id->conceptual-entity arg2Isa))
# (kb::instance-of? name 'd::FunctionalPredicate 'd::EverythingPSC)
# (kb::instance-of? name 'd::TransitiveBinaryPredicate 'd::EverythingPSC))
# (kb::genlpreds entity)
# (kb::dynamic? entity)
# (kb::comments entity)

# ToDo: make one query for a predicate that returns its arity, argIsas
# whether it's a NAT, functional, transitive, dynamic, genlpreds, comments.
# And how about a query to retrieve all binary predicates?


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    try:
        OwlAgent(host='localhost', port=9000, localPort=8950, debug=True)
    except Exception as error:
        print(error)
    time.sleep(20)

