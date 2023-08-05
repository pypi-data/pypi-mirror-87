"""Translator module where it change ADFH into SDL."""
from ihsan.schema import IhsanType
from ihsan.sdl.utils import (
    find_action,
    find_field,
    find_model,
    get_all_field_with_certain_type,
)


def to_sdl(schema: IhsanType, indention: int = 4) -> str:
    """Function that transfer ADFH into SDL aka GraphQL schema.

    Args:
        schema: IhsanType model.
        indention: The indention of the generated SDL.

    Returns:
        SDL aka Graphql schema.
    """
    text = ""
    choices = get_all_field_with_certain_type(
        fields=schema.adfh.fields_list, keyword="choice"
    )
    if choices:
        for choice in choices:
            text += f"enum {choice.name.capitalize()}Type {'{'}\n"
            if choice.options:
                for option in choice.options:
                    placeholder = f"{option.upper()}\n"
                    text += placeholder.rjust(len(placeholder) + indention)
                text += "}\n"

    for model in schema.adfh.models:
        text += f"type {model.name} {'{'}\n"
        for pro in model.properties:
            new_pro = find_field(fields=schema.adfh.fields_list, field_id=pro.assign)
            placeholder = f"{new_pro.name}: {new_pro.type}{new_pro.mandatory}\n"
            text += placeholder.rjust(len(placeholder) + indention)
        text += "}\n"

    if schema.adfh.actions:
        show_me_list = find_action(actions=schema.adfh.actions, keyword="show me list")
        show_me_certain_item = find_action(
            actions=schema.adfh.actions, keyword="show me a certain item"
        )
        let_me_remove = find_action(
            actions=schema.adfh.actions, keyword="let me remove"
        )
        let_me_add = find_action(actions=schema.adfh.actions, keyword="let me add")

        text += "type Query {\n"
        for item in show_me_list:
            model = find_model(
                models=schema.adfh.models, model_id=item.get("model", "")
            )
            placeholder = f"{item.get('name')}: [{model.name}]\n"
            text += placeholder.rjust(len(placeholder) + indention)

        for item in show_me_certain_item:
            placeholder = f"{item.get('name')}("
            text += placeholder.rjust(len(placeholder) + indention)
            field = find_field(
                fields=schema.adfh.fields_list, field_id=item.get("subject", "")
            )
            text += f"{field.name}: {field.type}{field.mandatory}, "
            model = find_model(
                models=schema.adfh.models, model_id=item.get("model", "")
            )
            text += f"): {model.name}\n"
        text += "}\n"

        text += "type Mutation {\n"

        for item in let_me_add:
            placeholder = f"{item.get('name')}("
            text += placeholder.rjust(len(placeholder) + indention)

            for input_action in item["input"]:
                input_action = find_field(
                    fields=schema.adfh.fields_list, field_id=input_action.get("assign")
                )

                text += f"{input_action.name}: {input_action.type}{input_action.mandatory}, "  # noqa B950

            model = find_model(
                models=schema.adfh.models, model_id=item.get("model", "")
            )
            text += f"): {model.name}\n"

        for item in let_me_remove:
            placeholder = f"{item.get('name')}("
            text += placeholder.rjust(len(placeholder) + indention)
            field = find_field(
                fields=schema.adfh.fields_list, field_id=item.get("subject", "")
            )
            text += f"{field.name}: {field.type}{field.mandatory}, "
            model = find_model(
                models=schema.adfh.models, model_id=item.get("model", "")
            )
            text += f"): {model.name}\n"

        text += "}\n"

    text += """schema {
    query: Query,
    mutation: Mutation
}
    """
    return text
