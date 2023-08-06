# PyJSG -- JSON Schema Grammar Bindings for Python
Translate [JSON Schema Grammar](http://github.com/ericprud/jsg) into Python objects.

This tool generates Python 3 objects that represent the JSON objects defined in a JSG schema.  It uses the [Python Typing library](https://docs.python.org/3/library/typing.html) to add type hints to Python IDE's and includes a library to validate the python objects against the library definitions.


[![Pyversions](https://img.shields.io/pypi/pyversions/PyJSG.svg)](https://pypi.python.org/pypi/PyJSG)
[![PyPi](https://img.shields.io/pypi/v/PyJSG.svg)](https://pypi.python.org/pypi/PyJSG)
![Build](https://github.com/hsolbrig/pyjsg/workflows/Build/badge.svg)
![Publish](https://github.com/hsolbrig/pyjsg/workflows/Publish%20Python%20Package/badge.svg)


## Examples

<table><thead>
<tr><th>JSON Grammar</th><th>Python Objects</th><th></th></tr>
</thead><tbody>
<tr><td><pre>doc { status:"ready" }</pre></td><td>
<pre>class _Anon1(jsg.JSGString):
    pattern = jsg.JSGPattern(r'ready')<br/>
class doc(jsg.JSGObject):
    def __init__(self,
                 status: _Anon1 = None,
                 **_kwargs: Dict[str, object]):
        self.status = status
        super().__init__(self._context, **_kwargs)</td></tr>
<tr><td><pre>doc { street:@string no:@int }
</pre></td><td><pre>
class doc(jsg.JSGObject):
    def __init__(self,
                 street: str = None,
                 no: int = None,
                 **_kwargs: Dict[str, object]):
        self.street = jsg.String(street)
        self.no = jsg.Integer(no)
        super().__init__(self._context, **_kwargs)
</pre></td></tr>
<tr><td><pre>doc { street:(NAME|"*"|TEMPLATE) }<br/>
@terminals
NAME : [A-Za-z].*;
TEMPLATE : '{' .* '}';</pre></td><td><pre>class _Anon1(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\*')<br/>
class NAME(jsg.JSGString):
    pattern = jsg.JSGPattern(r'[A-Za-z].*')<br/>
class TEMPLATE(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\{.*\}')<br/>
class doc(jsg.JSGObject):    
    def __init__(self,
                 street: Union[_Anon1, NAME, TEMPLATE] = None,
                 **_kwargs: Dict[str, object]):
        self.street = street
        super().__init__(self._context, **_kwargs)</pre></td></tr>
<tr><td><pre>doc { street:nameOrTemplate }
nameOrTemplate = (NAME | TEMPLATE) ;<br/>
@terminals
NAME : .*;
TEMPLATE : '{' .* '}';</pre></td><td><pre>class NAME(jsg.JSGString):
    pattern = jsg.JSGPattern(r'.*')<br/>
class TEMPLATE(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\{.*\}')<br/>
nameOrTemplate = Union[NAME, TEMPLATE]<br/>
class doc(jsg.JSGObject):    
    def __init__(self,
                 street: nameOrTemplate = None,
                 **_kwargs: Dict[str, object]):
        self.street = street
        super().__init__(self._context, **_kwargs)</pre></td></tr>
<tr><td><pre>doc { street:[(NAME | "*" | TEMPLATE){2,}] }
@terminals
NAME : .*;
TEMPLATE : '{' .* '}';</pre></td><td><pre>class _Anon1(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\*')<br/>
class NAME(jsg.JSGString):
    pattern = jsg.JSGPattern(r'.*')<br/>
class TEMPLATE(jsg.JSGString):
    pattern = jsg.JSGPattern(r'\{.*\}')<br/>
class doc(jsg.JSGObject):
        def __init__(self,
                 street: List[Union[_Anon1, NAME, TEMPLATE]] = None,
                 **_kwargs: Dict[str, object]):
        self.street = street
        super().__init__(self._context, **_kwargs)</pre></td></tr>
</tbody></table>

## Usage
* Requires Python 3.x -- has been tested through Python 3.6.1.  (This module depends on some of the internal features of the [Python typing library](https://docs.python.org/3/library/typing.html), which is still under active development -- be careful upgrading to newer versions without first running the unit tests.)
```bash
> pip install pyjsg
> generate_parser -h
usage: generate_parser [-h] [-o OUTFILE] [-e] infile

positional arguments:
  infile                Input JSG specification

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Output python file (Default: {infile}.jsg)
  -e, --evaluate        Evaluate resulting python file as a test
  ```
### Setup
```bash
> curl https://raw.githubusercontent.com/hsolbrig/shexTest/master/doc/ShExJ.jsg -o ShExJ.jsg
> generate_parser ShExJ.jsg
Output written to ShExJ.py
```
### Python
```python
from tests.py import ShExJ
    from pyjsg.jsglib.jsg import loads
    from io import StringIO

    # Load an exsting schema
    shexj = """{
      "@context": "http://www.w3.org/ns/shex.jsonld",
      "type": "Schema",
      "shapes": [
        {
          "id": "http://a.example/S1",
          "type": "Shape",
          "expression": {
            "type": "TripleConstraint",
            "predicate": "http://a.example/p1",
            "valueExpr": {
              "type": "NodeConstraint",
              "datatype": "http://a.example/dt1"
            }
          }
        }
      ]
    }
    """
    s: ShExJ.Schema = loads(shexj, ShExJ)
    print(f"type(Schema) = {s.type}")
    print(f"PREDICATE: {s.shapes[0].expression.predicate}")

    # Add a new element
    s.shapes[0].closed = Boolean("true")

    # Emit modified JSON
    print(s._as_json_dumps())

    # Validate the JSON
    print(f"Valid: {s._is_valid()")

    # Add an invalid element that isn't caught
    s.shapes[0].expression.valueExpr = "Just text"
    log = StringIO()
    if not s._is_valid(log):
        print(log.getvalue())

    # Attempt to add in invalid string
    try:
        s.shapes[0].closed = Boolean("0", True)
    except ValueError:
        print("String mismatch")

    # Attempt to add in invalid property
    try:
        s.shapes[0].closd = Boolean("true")
    except ValueError:
        print("No attribute named 'closd'")

```

 ### Output 
 ```text
type(Shema): Schema
PREDICATE: http://a.example/p1
{
   "type": "Schema",
   "@context": "http://www.w3.org/ns/shex.jsonld",
   "shapes": [
      {
         "type": "Shape",
         "id": "http://a.example/S1",
         "closed": "true",
         "expression": {
            "type": "TripleConstraint",
            "predicate": "http://a.example/p1",
            "valueExpr": {
               "type": "NodeConstraint",
               "datatype": "http://a.example/dt1"
            }
         }
      }
   ]
}
Valid: True
String mismatch
No attribute named 'closd'
```
