from typing import Union, Optional, Dict, List, Tuple, Any
import json, builtins

JSONData = Union[
    str, int, float, bool,
    Dict[str, Any],
    List[Any],
    Tuple[Any]
]

def load(
    path: str,
    default_value: Optional[JSONData] = None,
    save_if_not_exists: bool = False
) -> Optional[JSONData]:
    try:
        with open(path, 'r') as file:
            obj = json.load(file)
    except:
        obj = None

    if obj is None:
        if default_value is not None:
            obj = default_value
        
            if save_if_not_exists:
                save(path, obj)
    
    return obj

def save(
    path: str,
    obj: Optional[JSONData]
) -> None:
    with open(path, 'w') as file:
        json.dump(obj, file, indent=4)

def print(obj: JSONData) -> None:
    builtins.print(json.dumps(obj, indent=4))