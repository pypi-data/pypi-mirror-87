from itsimodels.core.fields import (
    DictField,
    ListField,
    TypeField
)


class FieldDecoder(object):
    """Decodes raw data for a model"""

    def decode(self, field_name, field, data):
        """
        Decodes the data located at the given field

        :param field_name: the field name
        :param field: the model field
        :param data: the encoded object data
        :return: the model data for the given field
        """
        from itsimodels.core.base_models import BaseModel

        name = self.decode_field_name(field, field_name)

        field_value = data.get(name)
        if field_value is None:
            return field.decode(field_value)

        if isinstance(field, ListField) and field.subtype and issubclass(field.subtype, BaseModel):
            return self.handle_list_of_models(field, field_value)

        if isinstance(field, DictField) and field.subtype and issubclass(field.subtype, BaseModel):
            return self.handle_dict_of_models(field, field_value)

        if isinstance(field, TypeField) and field.type and issubclass(field.type, BaseModel):
            model = field.type

            return model(data=field_value, field_decoder=self)

        return field.decode(field_value)

    def decode_field_name(self, field, field_name):
        return field_name

    def handle_list_of_models(self, field, lst):
        model_class = field.subtype
        models = []

        for model_data in lst:
            model = model_class(data=model_data, field_decoder=self)
            models.append(model)

        return models

    def handle_dict_of_models(self, field, dct):
        model_class = field.subtype
        models = {}

        for key, model_data in dct.items():
            model = model_class(data=model_data, field_decoder=self)
            models[key] = model

        return models
