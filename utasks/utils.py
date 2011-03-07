# -*- coding: utf-8 -*-

from insanities.forms import *
from insanities.utils import cached_property

ValidationError = convs.ValidationError


class PasswordConv(convs.Char):

    def from_python(self, value):
        return dict([(field.name, None) for field in self.field.fields])

    def get_default(self):
        return ''

    def to_python(self, value):
        initial = self.field.form.initial.get(self.field.name)
        etalon = value[list(value)[0]]
        for field in self.field.fields:
            if not value[field.name] == etalon:
                raise ValidationError('password and confirm mismatch')
        if not initial and not etalon:
            raise ValidationError('password required')
        return etalon


def PasswordSet(name='password', label=None, pass_label=None,
                conf_label=None, **kwargs):
    # class implementation has problem with Fieldset copying:
    # it requires to save all kwargs in object's __dict__
    validators = kwargs.get('validators', (convs.limit(4,255),))
    required = kwargs.get('required', True)
    char = convs.Char(required=required, *validators)
    items = (('pass', pass_label), ('conf', conf_label))
    kwargs['fields'] = [Field(subfieldname,
                              conv=char,
                              label=l,
                              widget=widgets.PasswordInput())
                        for subfieldname, l in items]
    kwargs.setdefault('conv', PasswordConv(required=required))
    return FieldSet(name, label=label,
            get_default=lambda: '', **kwargs)


class ModelChoice(convs.EnumChoice):

    condition = None
    conv = convs.Int(required=False)
    pk_field = 'id'

    @property
    def query(self):
        query = self.env.db.query(self.model)
        if isinstance(self.condition, dict):
            query = query.filter_by(**self.condition)
        elif self.condition is not None:
            query = query.filter(self.condition)
        return query

    def from_python(self, value):
        conv = self.conv(field=self.field)
        if self.multiple:
            return [conv.from_python(getattr(obj, self.pk_field)) for obj in value or []]
        if value is not None:
            return conv.from_python(getattr(value, self.pk_field))
        else:
            return ''

    def _safe_to_python(self, value):
        conv = self.conv(field=self.field)
        try:
            value = conv.to_python(value)
        except ValidationError:
            return None
        else:
            return self.query.filter_by(id=value).first()

    @cached_property
    def choices(self):
        return iter(self)

    def __iter__(self):
        conv = self.conv(field=self.field)
        for obj in self.query.all():
            yield conv.from_python(getattr(obj, self.pk_field)), self.get_object_label(obj)
