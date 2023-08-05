"""Collection of utils for SDL."""
from typing import Any, Dict, List

from ihsan.schema import ADFHActionsType, ADFHFieldsType, ADFHModelsType


def sdl_data_type_converter(*, data: str) -> str:
    """Converting ADFH data type into sdl data type.

    Args:
        data: ADFH data type.

    Examples:
        >>> from ihsan.sdl.utils import sdl_data_type_converter
        >>> unique_id = sdl_data_type_converter(data="unique id")
        >>> unique_id == "String"
        True
        >>> text = sdl_data_type_converter(data="text")
        >>> text == "String"
        True
        >>> checkbox = sdl_data_type_converter(data="checkbox")
        >>> checkbox == "Boolean"
        True
        >>> number = sdl_data_type_converter(data="number")
        >>> number == "Int"
        True

    Returns:
        SDL data type.
    """
    types = {
        "unique id": "String",
        "text": "String",
        "checkbox": "Boolean",
        "number": "Int",
    }
    return types.get(data, "String")


def find_action(
    *, actions: List[ADFHActionsType], keyword: str
) -> List[Dict[str, Any]]:
    """Search for a certain action.

    Args:
        actions: List of ADFHActionsType model.
        keyword: word or the action that has been required.

    Returns:
        List of selected actions.
    """
    return [action.dict() for action in actions if action.type == keyword]


def find_field(*, fields: List[ADFHFieldsType], field_id: str) -> ADFHFieldsType:
    """Search for a certain field.

    Args:
        fields: List of ADFHFieldsType model.
        field_id: The id of the field.

    Returns:
        ADFHFieldsType model.
    """
    field_dict = {}
    for field in fields:
        if field.id == field_id:
            if field.type == "choice":
                data_type = f"{field.name.capitalize()}Type"
            else:
                data_type = sdl_data_type_converter(data=field.type)
            field_dict.update(
                {
                    "id": field.id,
                    "name": field.name,
                    "type": data_type,
                    "mandatory": "!" if field.mandatory == "yes" else "",
                }
            )
    return ADFHFieldsType(**field_dict)


def get_all_field_with_certain_type(
    *, fields: List[ADFHFieldsType], keyword: str
) -> List[ADFHFieldsType]:
    """Get all field with a certain type.

    Args:
        fields: List of ADFHFieldsType model.
        keyword: word or the type that has been required.

    Returns:
        List of selected fields.
    """
    return [ADFHFieldsType(**field.dict()) for field in fields if field.type == keyword]


def find_model(*, models: List[ADFHModelsType], model_id: str) -> ADFHModelsType:
    """Search for a certain model.

    Args:
        models: List of ADFHModelsType model.
        model_id: The id of the model.

    Returns:
        ADFHModelsType model.
    """
    model_dict = {}
    properties_list = []
    for field in models:
        if field.id == model_id:
            model_dict.update({"id": field.id, "name": field.name})
            for pro in field.properties:
                properties_list.append(pro.dict())
    model_dict.update({"properties": properties_list})  # type: ignore
    return ADFHModelsType(**model_dict)
