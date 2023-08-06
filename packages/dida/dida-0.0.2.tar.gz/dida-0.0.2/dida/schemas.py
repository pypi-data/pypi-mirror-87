from marshmallow import Schema, fields, validate, pre_dump, ValidationError, post_load, pre_load, post_dump

from dida import triggers
from dida.core import Function


class DateTriggerSchema(Schema):
    run_date = fields.DateTime()

    @post_load
    def make(self, data, **_):
        return triggers.DateTrigger(**data)


class IntervalTriggerSchema(Schema):
    weeks = fields.Integer()
    days = fields.Integer()
    hours = fields.Integer()
    minutes = fields.Integer()
    seconds = fields.Integer()
    interval = fields.TimeDelta(dump_only=True)
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    jitter = fields.Integer()

    @post_load
    def make(self, data, **_):
        return triggers.IntervalTrigger(**data)

    @post_dump
    def post_dump(self, output, **_):
        seconds = output['interval']

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        weeks, days = divmod(days, 7)

        for key, value in dict(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds).items():
            output[key] = value
        return output


class TriggerSchema(Schema):
    type = fields.String(validate=validate.OneOf(['date', 'interval']), required=True)
    params = fields.Mapping()
    expression = fields.String(dump_only=True)

    @pre_dump
    def pre_dump(self, obj, **_):
        expression = str(obj)
        if isinstance(obj, triggers.DateTrigger):
            type = 'date'
            params = DateTriggerSchema().dump(obj)
        elif isinstance(obj, triggers.IntervalTrigger):
            type = 'interval'
            params = IntervalTriggerSchema().dump(obj)
        else:
            raise ValidationError('%r is not a trigger object.' % obj)
        return dict(type=type, params=params, expression=expression)

    @post_load
    def post_load(self, data: dict, **_):
        mapping = {
            "date": DateTriggerSchema,
            "interval": IntervalTriggerSchema
        }
        return mapping[data['type']]().load(data.get('params', {}))


class FunctionParamSchema(Schema):
    name = fields.String()
    value = fields.Raw()
    default = fields.Raw()
    required = fields.Boolean()


class FunctionSchema(Schema):
    id = fields.String()
    name = fields.String(dump_only=True)
    params = fields.List(fields.Nested(FunctionParamSchema), dump_only=True)

    @post_load
    def post_load(self, data, **_):
        func_id = data['id']
        func = Function.manager.get(func_id)
        if not func:
            raise ValidationError('Not found function: %s' % func_id)
        return func


class JobSchema(Schema):
    id = fields.String()
    name = fields.String(validate=validate.Length(min=1))
    kwargs = fields.Mapping()
    func = fields.Nested(FunctionSchema, required=True)
    func_ref = fields.String()
    next_run_time = fields.DateTime()
    pending = fields.Boolean()
    coalesce = fields.Boolean()
    max_instances = fields.Integer()
    misfire_grace_time = fields.Integer()
    trigger = fields.Nested(TriggerSchema, required=True)

    @pre_load
    def pre_load(self, in_data, **_):
        func = in_data['func']
        if 'params' in func:
            in_data['kwargs'] = func['params']
            del func['params']
        return in_data

    @post_dump
    def post_dump(self, output, **_):
        func_kwargs = output['kwargs']
        for param in output['func']['params']:
            param_name = param['name']
            if param_name in func_kwargs:
                param.update(value=func_kwargs[param_name])
        del output['kwargs']
        return output


class SchedulerSchema(Schema):
    state = fields.Integer()
