from enum import Enum

from django.template import Context, Template

from scaffold.kit.patterns import (
    CHAR_FIELD_TEMPLATE,
    DECIMAL_FIELD_TEMPLATE,
    FIELD_TEMPLATE,
    FOREIGN_KEY_TEMPLATE,
    MANY_TO_MANY_FIELD_TEMPLATE,
    MODEL_TEMPLATE,
    ONE_TO_ONE_FIELD_TEMPLATE,
    SERIALIZER_TEMPLATE,
    VIEW_SET_URL_TEMPLATE,
    VIEW_SET_VIEW_TEMPLATE,
)


class Field(Enum):
    Genl = (FIELD_TEMPLATE, ["name", "type"])
    Char = (CHAR_FIELD_TEMPLATE, ["name", "type", "max"])
    Foreign = (FOREIGN_KEY_TEMPLATE, ["name", "type", "model", "delete"])
    ManyToMany = (MANY_TO_MANY_FIELD_TEMPLATE, ["name", "type", "model", "delete"])
    OneToOne = (ONE_TO_ONE_FIELD_TEMPLATE, ["name", "type", "model", "delete"])
    Decimal = (DECIMAL_FIELD_TEMPLATE, ["name", "type", "max", "places"])


class FieldTemplate:
    @staticmethod
    def convert(args):
        type = args[1]
        try:
            pattern, options = Field[type].value[0], Field[type].value[1]
            context = dict(zip(options, args))
        except KeyError:
            pattern, options = Field.Genl.value[0], Field.Genl.value[1]
            context = dict(zip(options, args))
        return Template(pattern).render(context=Context(context))


class ModelTemplate:
    @staticmethod
    def convert(context):
        return Template(MODEL_TEMPLATE).render(context=Context(context))


class SerializerTemplate:
    @staticmethod
    def convert(context):
        return Template(SERIALIZER_TEMPLATE).render(context=Context(context))


class UrlTemplate:
    @staticmethod
    def convert(context):
        return Template(VIEW_SET_URL_TEMPLATE).render(context=Context(context))


class ViewTemplate:
    @staticmethod
    def convert(context):
        return Template(VIEW_SET_VIEW_TEMPLATE).render(context=Context(context))
