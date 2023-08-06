import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, Union, Dict, Tuple, Any
from dotmap import DotMap


class _NodeType(Enum):
    CLASS = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    NULL = auto()


@dataclass
class _Node:
    name: str
    types: List[_NodeType]
    optional: bool = True
    is_list: bool = False
    nested_lists: int = 1
    parent: Optional["_Node"] = None
    children: List["_Node"] = field(default_factory=list)
    class_name: Optional[str] = None
    final_class_name: Optional[str] = None
    extends: Optional["_Node"] = None

    def path(self):
        result = []
        current_node = self
        while parent := current_node.parent:
            result.append(current_node.name)
            current_node = parent
        return ".".join(result)


def _determine_if_optional(values: Set) -> bool:
    for value in values:
        if value is type(None):
            return True
    return False


def _generate_class_for_node(current_node: _Node, class_map):
    if _NodeType.CLASS in current_node.types:
        class_name = current_node.class_name
        if current_node.final_class_name is not None:
            class_name = current_node.final_class_name
        fields = []
        for child in current_node.children:
            fields.append(child.name + ": " + _get_node_class_type(child))
        fields_string = "\n\t".join(sorted(fields))
        extends = ""
        if current_node.extends is not None:
            extends = ", " + current_node.extends.class_name
        result = f"""
class {class_name}(Protocol{extends}):
\t{fields_string}

"""
        class_map[class_name] = result


def _get_node_class_type(child: _Node):
    def base_value(types):
        if child.optional and ((len(types) == 1 and types[0] != "None") or (len(types) == 2 and "None" in types)):
            return f"Optional[{types[0]}]"
        if len(types) > 1:
            return "Union[" + (",".join(types)) + "]"
        return types[0]

    result = []
    if _NodeType.CLASS in child.types:
        name = child.class_name
        if child.final_class_name is not None:
            name = child.final_class_name
        result.append(f'"{name}"')
    if _NodeType.NUMBER in child.types:
        result.append("int")
    if _NodeType.STRING in child.types:
        result.append("str")
    if _NodeType.BOOLEAN in child.types:
        result.append("bool")
    if _NodeType.NULL in child.types:
        result.append("None")

    if child.is_list:
        list_string = ""
        for each in range(child.nested_lists):
            list_string += "List["
        list_string += base_value(result)
        for each in range(child.nested_lists):
            list_string += "]"
        return list_string
    else:
        return base_value(result)


def _get_name_to_node_map(node_map):
    result = {}
    for _, node in node_map.items():
        if result.get(node.class_name) is None:
            result[node.class_name] = []
        result[node.class_name].append(node)
    return result


def _generate_classes(node_map: Dict[str, _Node], root_name: str):
    # find root
    # set node class names

    root: Optional[_Node] = None
    for _, node in node_map.items():
        if _NodeType.CLASS in node.types:
            node.class_name = node.name.title()
        elif _NodeType.CLASS in node.types and node.is_list:
            # remove plural end from end of string
            node.class_name = re.sub(pattern='s$', repl='', string=node.name.title())
        if node.parent is None:
            root = node
    assert root is not None
    root.class_name = root_name[0].upper() + root_name[1:]
    root.name = root_name[0].lower() + root_name[1:]
    # rename duplicates with different properties
    # extends duplicates when its properties are subsets of another of same name
    name_to_node_map = _get_name_to_node_map(node_map)
    class_usage_count: Dict[str, int] = {}
    for _, node in node_map.items():
        for other_node in name_to_node_map[node.class_name]:  # type:_Node
            if node != other_node and _NodeType.CLASS in node.types and _NodeType.CLASS in other_node.types:
                children_names = set([x.name for x in node.children])
                other_children_names = set([x.name for x in other_node.children])
                if len(children_names) != len(other_children_names):
                    if set.issubset(children_names, other_children_names):
                        node.extends = other_node
                    elif set.issubset(other_children_names, children_names):
                        other_node.extends = node
                if node.extends is None and other_node.extends is None and len(
                        children_names.intersection(other_children_names)) == 0 and other_node.final_class_name is None:
                    assert other_node.class_name is not None
                    if class_usage_count.get(other_node.class_name) is None:
                        class_usage_count[other_node.class_name] = 0
                    class_usage_count[other_node.class_name] = class_usage_count[other_node.class_name] + 1
                    if class_usage_count[other_node.class_name] == 1:
                        other_node.final_class_name = other_node.class_name
                    else:
                        other_node.final_class_name = other_node.class_name + str(
                            class_usage_count[other_node.class_name])

    # Depth first traversal while creating classes
    class_map: Dict[str, str] = {}

    def loop(current_node: _Node):
        _generate_class_for_node(current_node, class_map)
        for child in current_node.children:
            loop(child)

    loop(root)
    # if root is a list make a root container
    #     if root.is_list:
    #         class_map[f"{root.class_name}Container"] = f"""
    # class {root.class_name}Container(Protocol):
    #     {root.name}:List["{root.class_name}"]
    # """
    return class_map


def generate_python_protocol_classes_from_json(parsed_json: Union[List, Dict], file_name: str = "json"):
    """

    :param file_name: name to be used to save file and for root class when top level json is a list. Ending '_interface' will
    be appended to ending of file name
    :param parsed_json:
    :return:
    """
    all_text = _generate_classes_text(file_name, parsed_json)
    print(all_text)
    if file_name.endswith(".py"):
        file_name = file_name.strip(".py")
        file_name += "_protocol.py"
    else:
        file_name += "_protocol.py"
    if os.path.exists(file_name):
        raise Exception(f"File '{file_name}' already exists")
    else:
        with open(file_name, "w") as file:
            file.write(all_text)
            print(f"Saved file '{file_name}'")


def _generate_classes_text(file_name, parsed_json):
    # convert to dotmap
    class_name = file_name
    if "_" in class_name:
        class_name = class_name.replace("_", " ").title().replace(" ", "")
    json_map = _dict_to_dot_map({class_name: parsed_json}, class_name)
    #   iterate over key and objects keeping track of parentage
    parent_dict = _create_parent_dictionary(json_map)
    # build node tree
    node_map = _create_node_map(parent_dict)
    classes = _generate_classes(node_map, class_name)
    all_text = "from typing import Protocol, Optional, List, Union\n\n"
    for _, code in classes.items():
        all_text += code
    return all_text


def _normalize(map_or_list_of_maps: Union[List, Dict[str, Any]]):
    if isinstance(map_or_list_of_maps, list):
        for item in map_or_list_of_maps:
            _normalize(item)
    elif isinstance(map_or_list_of_maps, dict):
        # get immutalbe list
        keys = tuple(map_or_list_of_maps.keys())
        for key in keys:
            if re.search(pattern=r"[ \.]", string=key):
                value = map_or_list_of_maps[key]
                map_or_list_of_maps.pop(key, None)
                map_or_list_of_maps[re.sub(pattern=r"[ \.]", string=key, repl="_")] = value
        for key, value in map_or_list_of_maps.items():
            _normalize(value)


def _dict_to_dot_map(map_or_list_of_maps: Union[List, Dict], root_name_when_list="root"):
    """
    Turns dictionary created from json into a dotMap where items can be accessed as members. We also
    cleanup the json when there are spaces in keys. We create a sibling key with spaces replaced by underscores
    pointing to the same value, we then remove the previous key
    :param map_or_list_of_maps:
    :param root_name_when_list: name to be used for root class when top level json is a list
    :return:
    """
    _normalize(map_or_list_of_maps)
    json_map = None
    if isinstance(map_or_list_of_maps, dict):
        json_map = DotMap(map_or_list_of_maps)
    elif isinstance(map_or_list_of_maps, list):
        json_map = DotMap({root_name_when_list: map_or_list_of_maps})
    return json_map


def dict_to_dot_map(map_or_list_of_maps: Union[List, Dict]) -> Union[List, DotMap]:
    result = _dict_to_dot_map(map_or_list_of_maps)
    if dir(result)[0] == "root":
        return result.root
    else:
        return result


def _create_parent_dictionary(map):
    parent_dict = {}

    # depth first search to aggregate all possible values and paths
    def loop(obj, parent_string: str):
        if isinstance(obj, DotMap) or isinstance(obj, dict):
            properties = dir(obj)
            if isinstance(obj, dict):
                properties = obj.keys()
            for prop in properties:
                child = obj[prop]
                if parent_string.strip() == "":
                    new_parent = prop
                else:
                    new_parent = parent_string + "." + prop
                if isinstance(child, DotMap) or isinstance(child, list) or isinstance(child, dict):
                    loop(child, new_parent)
                else:
                    if parent_dict.get(new_parent) is None:
                        parent_dict[new_parent] = set()
                    parent_dict[new_parent].add(type(child))

        elif isinstance(obj, list):
            for index, child in enumerate(obj):
                list_parent_string = parent_string + "[x]"
                if isinstance(child, DotMap) or isinstance(child, list) or isinstance(child, dict):
                    loop(child, list_parent_string)
                else:
                    if parent_dict.get(list_parent_string) is None:
                        parent_dict[list_parent_string] = set()
                    parent_dict[list_parent_string].add(type(child))

    loop(map, "")
    # cleanup situations where a list could also be null
    to_test = [key for key, x in parent_dict.items() if type(None) in x]
    # remove these keys if there is a list version of them
    parent_keys = [k for k, y in parent_dict.items()]
    to_remove = [key for key in to_test if len([y for y in parent_keys if f"{key}[x]" in y]) > 0]
    [parent_dict.pop(x) for x in to_remove]
    # mark the optional lists are nullable
    # TODO
    return parent_dict


def _create_node_map(parent_dict):
    node_map = {}
    for key, value in parent_dict.items():  # type:str,Set
        split = key.split(".")
        for index in range(len(split)):
            node_key = ".".join(split[0:index + 1])
            # if not exists add new
            parent_node = None
            node_types, is_list, nested_lists = _determine_type(index, split, value)
            name = split[index].replace("[x]", "")
            optional = _determine_if_optional(value)
            if index > 0:
                parent_node = node_map[".".join(split[0:index])]
            if node_map.get(node_key) is None:
                node_map[node_key] = _Node(name=name, types=node_types, optional=optional, is_list=is_list,
                                           nested_lists=nested_lists)
            elif optional and index==len(split)-1:
                node_map[node_key].optional = optional
            if parent_node and node_map[node_key].parent is None:
                node_map[node_key].parent = parent_node
                parent_node.children.append(node_map[node_key])
    return node_map


def _determine_type(index, split, value: Set) -> Tuple[List[_NodeType], bool, int]:
    node_types = []
    is_list = False
    if "[x]" in split[index]:
        is_list = True
        if len(value) > 0 and index == (len(split) - 1):
            if _has_type(value, str):
                node_types.append(_NodeType.STRING)
            if _has_type(value, int):
                node_types.append(_NodeType.NUMBER)
            if _has_type(value, bool):
                node_types.append(_NodeType.BOOLEAN)
            if _has_type(value, None):
                node_types.append(_NodeType.NULL)
        else:
            node_types.append(_NodeType.CLASS)
    else:
        if index < len(split) - 1:
            node_types.append(_NodeType.CLASS)
        else:
            if _has_type(value, str):
                node_types.append(_NodeType.STRING)
            if _has_type(value, int):
                node_types.append(_NodeType.NUMBER)
            if _has_type(value, bool):
                node_types.append(_NodeType.BOOLEAN)
            if _has_type(value, None):
                node_types.append(_NodeType.NULL)
    nested_lists = len(re.findall(pattern=r"\[x\]", string=split[index]))
    return node_types, is_list, nested_lists


def _has_type(array: Union[List, Set], clazz):
    for value in array:
        if value is not type(None) and value is clazz:
            return True
        if value is type(None) and value is type(clazz):
            return True
    return False


def main():
    arg_length = len(sys.argv)
    if arg_length < 3:
        json_path = input("Enter json file path: ")
        name_to_save = input("Enter name of file to save, '_protocol' will be appended to the end of it: ")
        with open(json_path, "r") as file:
            json_obj = json.load(file)
        generate_python_protocol_classes_from_json(json_obj, name_to_save)
    elif arg_length == 3:
        with open(sys.argv[1], "r") as file:
            json_obj = json.load(file)
        generate_python_protocol_classes_from_json(json_obj, sys.argv[2])


if __name__ == '__main__':
    main()
