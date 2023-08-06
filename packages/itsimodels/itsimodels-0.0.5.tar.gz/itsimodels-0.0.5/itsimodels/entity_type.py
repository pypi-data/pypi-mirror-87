from itsimodels.core.base_models import (
    BaseModel,
    ChildModel
)
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ListField,
    StringField,
    TypeField
)


class DataDrilldown(ChildModel):
    title = StringField(required=True)

    type = StringField(required=True)

    entity_field_filter = DictField(object)

    static_filter = DictField(object)


class DashboardDrilldownParams(ChildModel):
    alias_param_map = ListField(object)

    static_params = DictField(object)


class DashboardDrilldown(ChildModel):
    title = StringField(required=True)

    id = StringField(required=True)

    base_url = StringField(default='')

    is_splunk_dashboard = BoolField(default=False)

    params = TypeField(DashboardDrilldownParams)


class VitalMetric(ChildModel):
    metric_name = StringField(required=True)

    search = StringField(required=True)

    is_key = BoolField(default=False)

    matching_entity_fields = ListField(str)

    split_by_fields = ListField(str)

    unit = StringField(default='')


class EntityType(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    description = StringField(default='')

    vital_metrics = ListField(VitalMetric)

    data_drilldowns = ListField(DataDrilldown)

    dashboard_drilldowns = ListField(DashboardDrilldown)
