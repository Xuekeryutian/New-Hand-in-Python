#!/usr/bin/env python

"""
XML-RPC support using libxml2dom.

See: http://www.xmlrpc.com/spec

Copyright (C) 2007, 2008 Paul Boddie <paul@boddie.org.uk>

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.

--------

The sending and receiving of XML-RPC messages can be done using traditional HTTP
libraries.

See tests/test_xmlrpc_parse.py for more details.

Useful properties:

  * container - returns the actual value element containing transmitted data
  * contents  - returns the converted data from within a container or a
                container object
"""

import libxml2dom
from libxml2dom.macrolib import *
from libxml2dom.macrolib import \
    createDocument as Node_createDocument
import datetime
import xml.dom
from libxml2dom.values import ContentValue, SequenceValue

# Node classes.

class XMLRPCNode(libxml2dom.Node):

    "Convenience modifications to nodes specific to libxml2dom.xmlrpc."

    def add_or_replace_element(self, new_element):

        """
        Add or replace the given 'new_element', using its localName to find any
        element to be replaced.
        """

        elements = self.xpath(new_element.localName)
        if elements:
            self.replaceChild(new_element, elements[0])
        else:
            self.appendChild(new_element)

    def serialise_value(self, parent, value):

        "Serialise, under the 'parent', the given 'value' object."

        if isinstance(value, (str, int, float, bool)):
            valueElement = parent.makeValue(typenames[value.__class__.__name__])
            valueElement.container.value = str(value)

        elif isinstance(value, datetime.datetime):
            valueElement = parent.makeValue("dateTime.iso8601")
            valueElement.container.value = value.strftime("%Y%m%dT%H:%M:%S")

        elif isinstance(value, (tuple, list)):
            array = parent.makeValue("array").container
            dataElement = array.makeData()
            for v in value:
                self.serialise_value(dataElement, v)

        elif isinstance(value, dict):
            struct = parent.makeValue("struct").container
            for k, v in value.items():
                member = struct.makeMember()
                member.memberName = str(k)
                self.serialise_value(member, v)

        else:
            raise ValueError, "Value %r cannot be serialised." % value

class XMLRPCElement(XMLRPCNode):

    "An XML-RPC element."

    pass

class XMLRPCDocument(libxml2dom._Document, XMLRPCNode):

    "An XML-RPC document fragment."

    def _method(self):
        return (self.xpath("methodCall|methodResponse") or [None])[0]

    def _fault(self):
        if self.method is not None:
            return self.method.fault
        else:
            return None

    method = property(_method)
    fault = property(_fault)

    # Node construction methods.

    def createMethodCall(self):
        return self.ownerDocument.createElement("methodCall")

    def makeMethodCall(self):
        e = self.createMethodCall()
        self.add_or_replace_element(e)
        return e

    def createMethodResponse(self):
        return self.ownerDocument.createElement("methodResponse")

    def makeMethodResponse(self):
        e = self.createMethodResponse()
        self.add_or_replace_element(e)
        return e

class XMLRPCMethodElement(XMLRPCNode):

    "An XML-RPC method element."

    def _fault(self):
        return (self.xpath("./fault") or [None])[0]

    def _params(self):
        return (self.xpath("./params") or [None])[0]

    def _methodNameElement(self):
        return (self.xpath("./methodName") or [None])[0]

    def _methodName(self):
        name = self.methodNameElement
        if name is not None:
            return name.value
        else:
            return None

    def _setMethodName(self, name):
        if self.methodNameElement is None:
            methodName = self.createMethodName()
            self.appendChild(methodName)
        self.methodNameElement.value = name

    def _parameterValues(self):
        if self.params:
            return self.params.values()
        else:
            return None

    def _setParameterValues(self, values):
        params = self.makeParameters()
        for value in values:
            param = params.makeParameter()
            self.serialise_value(param, value)

    def _parameters(self):

        "Return a list of the individual param elements."

        return self.xpath("./params/param")

    # Node construction methods.

    def createMethodName(self):
        return self.ownerDocument.createElement("methodName")

    def makeMethodName(self):
        e = self.createMethodName()
        self.add_or_replace_element(e)
        return e

    def createParameters(self):
        return self.ownerDocument.createElement("params")

    def makeParameters(self):
        e = self.createParameters()
        self.add_or_replace_element(e)
        return e

    def createFault(self):
        return self.ownerDocument.createElement("fault")

    def makeFault(self):
        e = self.createFault()
        self.add_or_replace_element(e)
        return e

    fault = property(_fault)
    params = property(_params)
    methodNameElement = property(_methodNameElement)
    methodName = property(_methodName, _setMethodName)
    parameterValues = property(_parameterValues, _setParameterValues)
    parameters = property(_parameters)

class XMLRPCParametersElement(SequenceValue, XMLRPCNode):

    """
    An XML-RPC parameters/params element.

    This element behaves like a list in that values can be appended to it and
    these will be added as new parameters.
    """

    def _parameters(self):

        "Return a list of the individual param elements."

        return self.xpath("./param")

    # Sequence emulation.

    def append(self, value):
        param = self.makeParameter()
        self.serialise_value(param, value)

    def values(self):
        return [value.contents for value in self.xpath("./param/value")]

    def __repr__(self):
        return "<XMLRPCParametersElement: %r>" % self.parameters

    # Node construction methods.

    def createParameter(self):
        return self.ownerDocument.createElement("param")

    def makeParameter(self):
        e = self.createParameter()
        self.appendChild(e)
        return e

    parameters = property(_parameters)

class XMLRPCParameterElement(ContentValue, XMLRPCNode):

    """
    An XML-RPC parameter/param element.

    This element behaves like a list in that values can be appended to it and
    these will be added either as new elements in an existing array or struct,
    or as new elements in a new array.
    """

    def _valueElement(self):
        return (self.xpath("./value") or [None])[0]

    def _contents(self):
        if self.valueElement is not None:
            return self.valueElement.contents
        else:
            return self

    # Sequence emulation.

    def __len__(self):
        return len(self.values())

    def __getitem__(self, i):
        return self.values()[i]

    def append(self, value):
        if self.valueElement is None:
            self.makeValue("array")
        self.contents.append(value)

    def values(self):
        if self.contents is not self:
            return self.contents.values()
        else:
            return []

    def __repr__(self):
        if self.contents is self:
            return "<XMLRPCParameterElement>"
        else:
            return "<XMLRPCParameterElement: %r>" % self.contents

    # Node construction methods.

    def createValue(self, typename=None):
        value = self.ownerDocument.createElement("value")
        if typename is not None:
            contents = self.ownerDocument.createElement(typename)
            value.appendChild(contents)
        return value

    def makeValue(self, typename=None):
        value = self.createValue(typename)
        self.add_or_replace_element(value)
        return value

    valueElement = property(_valueElement)
    contents = property(_contents)

class XMLRPCArrayElement(SequenceValue, XMLRPCNode):

    """
    An XML-RPC array element.

    This element behaves like a list in that values can be appended to it and
    these will be added as new elements in the array.
    """

    def _dataElement(self):
        return (self.xpath("./data") or [None])[0]

    def _contents(self):
        return self

    # Sequence emulation.

    def append(self, value):
        if self.dataElement is None:
            self.makeData()
        self.serialise_value(self.dataElement, value)

    def values(self):
        return [v.contents for v in self.xpath("./data/value")]

    def __repr__(self):
        return "<XMLRPCArrayElement: %r>" % self.values()

    # Node construction methods.

    def createData(self):
        return self.ownerDocument.createElement("data")

    def makeData(self):
        e = self.createData()
        self.add_or_replace_element(e)
        return e

    dataElement = property(_dataElement)
    contents = property(_contents)

class XMLRPCStructElement(SequenceValue, XMLRPCNode):

    """
    An XML-RPC structure element.

    This element behaves like a list in that values can be appended to it and
    these will be added as new (name, value) members in the structure.
    """

    def _members(self):
        return self.xpath("./member")

    def _contents(self):
        return self

    # Sequence emulation.

    def __len__(self):
        return len(self.members)

    def __getitem__(self, i):
        return self.members[i]

    def append(self, item):
        name, value = item
        member = self.makeMember()
        member.memberName = name
        self.serialise_value(member, value)

    def __repr__(self):
        return "<XMLRPCStructElement: %r>" % self.items()

    # Dictionary emulation.

    def keys(self):
        return [member.memberName for member in self.members]

    def values(self):
        return [member.memberValue for member in self.members]

    def items(self):
        return [(member.memberName, member.memberValue) for member in self.members]

    # Node construction methods.

    def createMember(self):
        return self.ownerDocument.createElement("member")

    def makeMember(self):
        e = self.createMember()
        self.appendChild(e)
        return e

    members = property(_members)
    contents = property(_contents)

class XMLRPCDataElement(SequenceValue, XMLRPCNode):

    """
    An XML-RPC array data element.

    This element behaves like a list in that values can be appended to it and
    these will be added as new elements in the array.
    """

    def _contents(self):
        return self

    # Sequence emulation.

    def append(self, value):
        self.serialise_value(self, value)

    def values(self):
        return [v.contents for v in self.xpath("./value")]

    # Node construction methods.

    def createValue(self, typename=None):
        value = self.ownerDocument.createElement("value")
        if typename is not None:
            contents = self.ownerDocument.createElement(typename)
            value.appendChild(contents)
        return value

    def makeValue(self, typename=None):
        value = self.createValue(typename)
        self.appendChild(value)
        return value

    contents = property(_contents)

class XMLRPCMemberElement(XMLRPCNode):

    """
    An XML-RPC structure member element.

    This element behaves like a tuple of the form (name, value).
    """

    def _valueElement(self):
        return (self.xpath("./value") or [None])[0]

    def _nameElement(self):
        return (self.xpath("./name") or [None])[0]

    def _memberName(self):
        if self.nameElement is not None:
            return self.nameElement.value
        else:
            return None

    def _setMemberName(self, name):
        if self.nameElement is None:
            nameElement = self.createName()
            self.appendChild(nameElement)
        self.nameElement.value = name

    def _memberValue(self):
        if self.valueElement is None:
            return None
        else:
            return self.valueElement.contents

    def _contents(self):
        return self

    # Item (name, value) emulation.

    def __len__(self):
        return 2

    def __getitem__(self, i):
        return (self.memberName, self.valueElement.contents)[i]

    # Equality testing.

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    def __ne__(self, other):
        return not self.__eq__(other)

    # Node construction methods.

    def createName(self):
        return self.ownerDocument.createElement("name")

    def makeName(self):
        e = self.createName()
        self.add_or_replace_element(e)
        return e

    def createValue(self, typename=None):
        value = self.ownerDocument.createElement("value")
        if typename is not None:
            contents = self.ownerDocument.createElement(typename)
            value.appendChild(contents)
        return value

    def makeValue(self, typename=None):
        value = self.createValue(typename)
        self.add_or_replace_element(value)
        return value

    nameElement = property(_nameElement)
    memberName = property(_memberName, _setMemberName)
    memberValue = property(_memberValue)
    valueElement = property(_valueElement)
    contents = property(_contents)

class XMLRPCStringElement(ContentValue, XMLRPCNode):

    "An XML-RPC string element."

    typename = "string"

    def _value(self):
        return self.textContent.strip()

    def _setValue(self, value):
        for node in self.childNodes:
            self.removeChild(node)
        text = self.ownerDocument.createTextNode(value)
        self.appendChild(text)

    def _contents(self):
        return convert(self.typename, self.value)

    def __repr__(self):
        return "<%s: %r>" % (self.__class__.__name__, self.contents)

    value = property(_value, _setValue)
    contents = property(_contents)

class XMLRPCNameElement(XMLRPCStringElement):

    "An XML-RPC name element."

    pass

class XMLRPCMethodNameElement(XMLRPCNameElement):

    "An XML-RPC method element."

    pass

class XMLRPCValueElement(XMLRPCStringElement):

    "An XML-RPC value element."

    def _value(self):
        if self.container is self:
            return XMLRPCStringElement._value(self)
        else:
            return self.container.value

    def _setValue(self, value):
        if self.container is self:
            XMLRPCStringElement._setValue(self, value)
        else:
            self.container.value = value

    def _contents(self):
        if self.container is self:
            return XMLRPCStringElement._contents(self)
        else:
            return self.container.contents

    def _type(self):
        if self.container is self:
            return "string"
        else:
            return self.container.localName

    def _setType(self, typename):
        new_contents = self.ownerDocument.createElement(typename)
        self.add_or_replace_element(new_contents)

    def _container(self):
        return (self.xpath("*") or [self])[0]

    value = property(_value, _setValue)
    type = property(_type, _setType)
    container = property(_container)
    contents = property(_contents)

class XMLRPCIntegerElement(XMLRPCStringElement):

    "An XML-RPC integer element."

    typename = "int"

class XMLRPCBooleanElement(XMLRPCStringElement):

    "An XML-RPC boolean element."

    typename = "boolean"

class XMLRPCDoubleElement(XMLRPCStringElement):

    "An XML-RPC double floating point number element."

    typename = "double"

class XMLRPCDateTimeElement(XMLRPCStringElement):

    "An XML-RPC date/time element."

    typename = "datetime"

class XMLRPCBase64Element(XMLRPCStringElement):

    "An XML-RPC integer element."

    typename = "base64"

class XMLRPCFaultElement(XMLRPCNode):

    "An XML-RPC fault element."

    def _code(self):
        code = self.xpath("./value/struct/member[./name/text() = 'faultCode']/value/int")
        if code:
            return code[0].value
        else:
            return None

    def _reason(self):
        reason = self.xpath("./value/struct/member[./name/text() = 'faultString']/value/string")
        if reason:
            return reason[0].value
        else:
            return None

    code = property(_code)
    reason = property(_reason)

# Conversion functions.

def convert(typename, value):
    return default_converters[typename](value)

def boolean(s):
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        raise ValueError, "String value %r not convertable to boolean." % s

def iso8601(s):
    year, month, day, hour, minute, second = map(int, (s[:4], s[4:6], s[6:8], s[9:11], s[12:14], s[15:17]))
    return datetime.datetime(year, month, day, hour, minute, second)

default_converters = {
    "string" : unicode,
    "int" : int,
    "i4" : int,
    "double" : float,
    "boolean" : boolean,
    "dateTime.iso8601" : iso8601,
    "base64" : str
    }

typenames = {
    "str" : "string",
    "int" : "int",
    "bool" : "boolean",
    "float" : "double"
    }

# Implementation-related functionality.

class XMLRPCImplementation(libxml2dom.Implementation):

    "Contains an XML-RPC-specific implementation."

    # Mapping of element names to wrappers.

    _class_for_name = {
        "methodCall" : XMLRPCMethodElement,
        "methodResponse" : XMLRPCMethodElement,
        "methodName" : XMLRPCMethodNameElement,
        "params" : XMLRPCParametersElement,
        "param" : XMLRPCParameterElement,
        "fault" : XMLRPCFaultElement,
        "string" : XMLRPCStringElement,
        "int" : XMLRPCIntegerElement,
        "i4" : XMLRPCIntegerElement,
        "boolean" : XMLRPCBooleanElement,
        "double" : XMLRPCDoubleElement,
        "dateTime.iso8601" : XMLRPCDateTimeElement,
        "base64" : XMLRPCBase64Element,
        "struct" : XMLRPCStructElement,
        "member" : XMLRPCMemberElement,
        "value" : XMLRPCValueElement,
        "name" : XMLRPCNameElement,
        "array" : XMLRPCArrayElement,
        "data" : XMLRPCDataElement
        }

    # Wrapping of documents.

    def adoptDocument(self, node):
        return XMLRPCDocument(node, self)

    # Factory functions.

    def get_node(self, _node, context_node):

        """
        Get a libxml2dom node for the given low-level '_node' and libxml2dom
        'context_node'.
        """

        if Node_nodeType(_node) == context_node.ELEMENT_NODE:

            # Make special objects for certain elements.
            # Otherwise, make generic XML-RPC elements.

            cls = self._class_for_name.get(Node_localName(_node)) or XMLRPCElement
            return cls(_node, self, context_node.ownerDocument)

        else:
            return libxml2dom.Implementation.get_node(self, _node, context_node)

    # Convenience functions.

    def createXMLRPCMessage(self, namespaceURI, localName):

        "Create a new XML-RPC message document (fragment)."

        return XMLRPCDocument(Node_createDocument(namespaceURI, localName, None), self).documentElement

    def createMethodCall(self, name=None):

        """
        Create and return a message fragment for a method call having the given
        'name'.
        """

        message = self.createXMLRPCMessage(None, "methodCall")
        if name is not None:
            message.methodName = name
        return message

    def createMethodResponse(self):

        "Create and return a message fragment for a method response."

        return self.createXMLRPCMessage(None, "methodResponse")

# Utility functions.

createDocument = libxml2dom.createDocument
createDocumentType = libxml2dom.createDocumentType

def createXMLRPCMessage(namespaceURI, localName):
    return default_impl.createXMLRPCMessage(None, localName)

def createMethodCall(name=None):
    return default_impl.createMethodCall(name)

def createMethodResponse():
    return default_impl.createMethodResponse()

def parse(stream_or_string, html=0, htmlencoding=None, unfinished=0, impl=None):
    return libxml2dom.parse(stream_or_string, html=html, htmlencoding=htmlencoding, unfinished=unfinished, impl=(impl or default_impl))

def parseFile(filename, html=0, htmlencoding=None, unfinished=0, impl=None):
    return libxml2dom.parseFile(filename, html=html, htmlencoding=htmlencoding, unfinished=unfinished, impl=(impl or default_impl))

def parseString(s, html=0, htmlencoding=None, unfinished=0, impl=None):
    return libxml2dom.parseString(s, html=html, htmlencoding=htmlencoding, unfinished=unfinished, impl=(impl or default_impl))

def parseURI(uri, html=0, htmlencoding=None, unfinished=0, impl=None):
    return libxml2dom.parseURI(uri, html=html, htmlencoding=htmlencoding, unfinished=unfinished, impl=(impl or default_impl))

# Single instance of the implementation.

default_impl = XMLRPCImplementation()

# vim: tabstop=4 expandtab shiftwidth=4
