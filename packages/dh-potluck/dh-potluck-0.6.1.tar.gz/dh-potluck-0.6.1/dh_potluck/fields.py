import enum

from marshmallow.fields import Field


class EnumField(Field):
    """
    This replacement for EnumField is used to resolve an issue where the default marshmallow enum
    did not work to properly serialize allowed values and the property, missing, for the API spec.
    """

    default_error_messages = {
        'invalid': 'Invalid enum value {input}',
    }

    def __init__(self, enum_type, *args, **kwargs):
        self.enum = enum_type

        super().__init__(*args, **kwargs)

        # Detect type of enum and make it available to apispec
        values = [e.value for e in self.enum if e.value is not None]
        if all(isinstance(v, int) for v in values):
            self.metadata['type'] = 'integer'
        elif all(isinstance(v, (float, int)) for v in values):
            self.metadata['type'] = 'number'
        elif all(isinstance(v, bool) for v in values):
            self.metadata['type'] = 'boolean'
        elif all(isinstance(v, str) for v in values):
            self.metadata['type'] = 'string'

        # Ensure all enum values are made available to apispec
        self.metadata['enum'] = sorted([e.value for e in self.enum])

        # Ensure we're using a serializable value for missing
        if isinstance(self.missing, enum.Enum):
            self.missing = self.missing.value

    # These template methods are not invoked when constructing the apispec
    # but they are used by the routes
    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self.enum(value)
        except ValueError:
            self.fail('invalid', input=value, value=value)

    def fail(self, key, **kwargs):
        kwargs['values'] = ', '.join([str(mem.value) for mem in self.enum])
        super().fail(key, **kwargs)
