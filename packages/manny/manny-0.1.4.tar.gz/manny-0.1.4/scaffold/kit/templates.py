from abc import ABC, abstractmethod
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


class CommonTemplate(ABC):
    @abstractmethod
    def convert(self, context):
        pass


class FieldTemplate(CommonTemplate):
    def convert(self, context):
        type = context[1]
        try:
            pattern, options = Field[type].value[0], Field[type].value[1]
        except KeyError:
            pattern, options = Field.Genl.value[0], Field.Genl.value[1]
        template_context = dict(zip(options, context))
        return Template(pattern).render(context=Context(template_context))


class ModelTemplate(CommonTemplate):
    def convert(self, context):
        return Template(MODEL_TEMPLATE).render(context=Context(context))


class SerializerTemplate(CommonTemplate):
    def convert(self, context):
        return Template(SERIALIZER_TEMPLATE).render(context=Context(context))


class UrlTemplate(CommonTemplate):
    def convert(self, context):
        return Template(VIEW_SET_URL_TEMPLATE).render(context=Context(context))


class ViewTemplate(CommonTemplate):
    def convert(self, context):
        return Template(VIEW_SET_VIEW_TEMPLATE).render(context=Context(context))
