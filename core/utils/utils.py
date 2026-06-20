def _simpan(instance, data: dict):
    for key, value in data.items():
        setattr(instance, key, value)
    
    instance.save()
    
    return instance
    
def _filter_model_data(model, data: dict):
    """
    filter 

    Args:
        model (_type_): _description_
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    fields = {
        field.name
        for field in model._meta.fields
    }

    return {
        key: value
        for key, value in data.items()
        if key in fields
    }