import attr

from tdxapi.models.custom_attribute_list import CustomAttributeList


def new_model(class_, manager, **kwargs):
    model = class_(**kwargs)

    # New objects should not be flagged as partial to allow saving
    model._partial = False

    # If manager has an app_id, set it on new object
    try:
        model.app_id = manager.app_id
    except AttributeError:
        pass

    # If object has attributes and manager has a template, set it on the object
    try:
        model.attributes.match_template(manager.attribute_template)
    except AttributeError:
        pass

    return model


def save_check(model):
    if model._partial:
        raise ValueError(
            "object data may not be complete, saving could "
            "result in data loss (use force=True to override)"
        )


def save_model(model, manager, force, *args, **kwargs):
    if not force:
        save_check(model)

    if model.id:
        updated_model = manager._update(model, *args, **kwargs)
    else:
        updated_model = manager._create(model, *args, **kwargs)

    update_model(model, updated_model)

    try:
        model.attributes.match_template(manager.attribute_template)
    except AttributeError:
        pass


def format_search_params(class_, manager, dictionary):
    # dictionary comes from locals(), so remove self from the list and do not
    # set any search parameters that were not specified or custom attributes
    # because custom attributes need to be formatted first
    kwargs = {
        k: v
        for k, v in dictionary.items()
        if k not in ("self", "custom_attributes") and v is not None
    }

    # Create search object from search data
    search_params = class_(**kwargs)

    search_attrs = dictionary.get("custom_attributes", None)

    # If there are no custom attributes specified for searching, return object
    if search_attrs is None:
        return search_params

    formatted_search_attrs = CustomAttributeList()

    # If custom attributes were specified, get the attribute objects from template
    for search_attr in search_attrs:
        formatted_search_attrs.append(
            manager.attribute_template.update_copy(search_attr[0], search_attr[1])
        )

    search_params.custom_attributes = formatted_search_attrs

    return search_params


def update_model(old, new):
    """Update old_model with data from new_model."""
    for field in [f for f in attr.fields(old.__class__) if f.repr]:
        setattr(old, field.name, getattr(new, field.name))


def build_notify_list(notify):
    if notify is None:
        return []

    elif isinstance(notify, str):
        return [notify]

    else:
        return notify
