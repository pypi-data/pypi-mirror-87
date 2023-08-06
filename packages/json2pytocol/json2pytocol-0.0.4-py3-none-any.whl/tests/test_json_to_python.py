import json2pytocol.json_to_python_protocol as jp
import json


def test_generate_classes_text_basic():
    test_json = """
    {
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """
from typing import Protocol, Optional, List, Union


class Test(Protocol):
	glossary: "Glossary"


class Glossary(Protocol):
	GlossDiv: "Glossdiv"
	title: str


class Glossdiv(Protocol):
	GlossList: "Glosslist"
	title: str


class Glosslist(Protocol):
	GlossEntry: "Glossentry"


class Glossentry(Protocol):
	Abbrev: str
	Acronym: str
	GlossDef: "Glossdef"
	GlossSee: str
	GlossTerm: str
	ID: str
	SortAs: str


class Glossdef(Protocol):
	GlossSeeAlso: List[str]
	para: str

""".lstrip()


def test_generate_classes_text_subsets():
    test_json = """
{
    "person":{
        "address":{
            "line1":"some address"
        },
        "children":[
            {
                "address":{
                    "line1": "some address",
                    "additional_field": "more info"
                }
            }
        ]
    }
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """
from typing import Protocol, Optional, List, Union


class Test(Protocol):
	person: "Person"


class Person(Protocol):
	address: "Address"
	children: List["Children"]


class Address(Protocol):
	additional_field: str
	line1: str


class Children(Protocol):
	address: "Address"

""".lstrip()


def test_generate_classes_text_spaces_in_key():
    test_json = """
{
    "person":{
        "address":{
            "line1":"some address"
        },
        "children":[
            {
                "address":{
                    "line1": "some address",
                    "additional field": "more info"
                }
            }
        ]
    }
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """
from typing import Protocol, Optional, List, Union


class Test(Protocol):
	person: "Person"


class Person(Protocol):
	address: "Address"
	children: List["Children"]


class Address(Protocol):
	additional_field: str
	line1: str


class Children(Protocol):
	address: "Address"

""".lstrip()


def test_generate_classes_text_optional_fields():
    test_json = """
{
    "persons":[
        {
            "name": "Fred",
            "age": 10,
            "suffix": "jr"
        },
        {
            "name" : "Tom",
            "suffix": null
        }
    ]
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """
from typing import Protocol, Optional, List, Union


class Test(Protocol):
	persons: List["Persons"]


class Persons(Protocol):
	age: int
	name: str
	suffix: Optional[str]

""".lstrip()


def test_generate_classes_text_union():
    test_json = """
{
    "persons":[
        {
            "name": "Fred",
            "age": 10,
            "suffix": "jr"
        },
        {
            "name" : "Tom",
            "suffix": 10
        }

    ]
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """
from typing import Protocol, Optional, List, Union


class Test(Protocol):
	persons: List["Persons"]


class Persons(Protocol):
	age: int
	name: str
	suffix: Union[int,str]

""".lstrip()


def test_multiple_top_level():
    test_json = """
{
    "persons":"thing",
    "thing":"other"
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	persons: str
	thing: str

""".lstrip()


def test_all_null():
    test_json = """
{
    "persons":null,
    "thing":null
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	persons: None
	thing: None

""".lstrip()


def test_dots_in_keys():
    test_json = """
{
    "persons.other":"thing",
    "thing.bla":3
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	persons_other: str
	thing_bla: int

""".lstrip()


def test_multiple_classes_of_same_name():
    test_json = """
{
    "type1":{ "address":{"street":2}},
    "type2":{ "address":{"street1":3}},
    "type3":{ "address":{"street2":4}}
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	type1: "Type1"
	type2: "Type2"
	type3: "Type3"


class Type1(Protocol):
	address: "Address3"


class Address3(Protocol):
	street: int


class Type2(Protocol):
	address: "Address"


class Address(Protocol):
	street1: int


class Type3(Protocol):
	address: "Address2"


class Address2(Protocol):
	street2: int

""".lstrip()


def test_list_of_list_of_lists():
    test_json = """
{
    "type":[[1]],
    "type2":[[[{"something":2}]]]
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	type2: List[List[List["Type2"]]]
	type: List[List[int]]


class Type2(Protocol):
	something: int

""".lstrip()


def test_optional_list():
    test_json = """
{
    "type":[{"something":[1,2,3]},
    {"something":null}]
}
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	type: List["Type"]


class Type(Protocol):
	something: List[int]

""".lstrip()


def test_nullable_object():
    test_json = """
    {
    "type":[{ "address":{"address1":{"street": 2}}},
    { "address":null}]
    }
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == """from typing import Protocol, Optional, List, Union


class Test(Protocol):
	type: List["Type"]


class Type(Protocol):
	address: Optional["Address"]


class Address(Protocol):
	address1: "Address1"


class Address1(Protocol):
	street: int

"""


def test_bject_with_value_should_be_union():
    test_json = """
    {
    "type":[{ "address":{"address1":{"street": 2}}},
    { "address":"value"}]
    }
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == ""


def test_object_missing_should_be_optional():
    test_json = """
    {
    "type":[{ "address":{"address1":{"street": 2},"address2":{"street": 3}}},
    { "address":{"address1":{"street": 2}}}]
    }
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == ""


def test_should_create_wrapper_on_top_list():
    test_json = """
    [
    {"number":1},
    {"number":2}
    ]
    """
    result = jp._generate_classes_text(file_name="test", parsed_json=json.loads(test_json))
    assert result == ""
