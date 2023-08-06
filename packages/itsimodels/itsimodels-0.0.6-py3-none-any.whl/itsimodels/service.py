from itsimodels.core.base_models import BaseModel, ChildModel
from itsimodels.core.fields import (
    BoolField,
    DictField,
    ForeignKey,
    ForeignKeyList,
    ListField,
    NumberField,
    StringField,
    TypeField
)
from itsimodels.team import GLOBAL_TEAM_KEY


class ThresholdLevel(ChildModel):
    severity_color = StringField(alias='severityColor')

    severity_color_light = StringField(alias='severityColorLight')

    severity_label = StringField(alias='severityLabel')

    threshold_value = NumberField(alias='thresholdValue')


class KpiThresholds(ChildModel):
    base_severity_color = StringField(alias='baseSeverityColor')

    base_severity_color_light = StringField(alias='baseSeverityColorLight')

    base_severity_label = StringField(default='info', alias='baseSeverityLabel')

    base_severity_value = NumberField(alias='baseSeverityValue')

    gauge_max = NumberField(default=100, alias='gaugeMax')

    gauge_min = NumberField(default=0, alias='gaugeMin')

    is_max_static = BoolField(default=False, alias='isMaxStatic')

    is_min_static = BoolField(default=False, alias='isMinStatic')

    metric_field = StringField(alias='metricField')

    render_boundary_max = NumberField(alias='renderBoundaryMax')

    render_boundary_min = NumberField(alias='renderBoundaryMin')

    threshold_levels = ListField(ThresholdLevel, alias='thresholdLevels')


class KpiTimePolicy(ChildModel):
    title = StringField(required=True)

    aggregate_thresholds = TypeField(KpiThresholds)

    entity_thresholds = TypeField(KpiThresholds)

    policy_type = StringField(default='static')

    time_blocks = ListField(object)


class KpiTimePolicies(ChildModel):
    policies = DictField(KpiTimePolicy)


class MetricSearchSpec(ChildModel):
     metric_index = StringField(default='')

     metric_name = StringField(default='')


class Kpi(ChildModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    aggregate_statop = StringField(default='avg')

    adaptive_thresholds_is_enabled = BoolField(default=False)

    aggregate_thresholds = TypeField(KpiThresholds)

    aggregate_thresholds_custom_alert_rules = ListField()

    alert_lag = StringField(default='30')

    alert_on = StringField()

    alert_period = StringField()

    anomaly_detection_alerting_enabled = BoolField(default=False)

    anomaly_detection_is_enabled = BoolField(default=False)

    anomaly_detection_sensitivity = NumberField()

    anomaly_detection_training_window = StringField()

    aggregate_threshold_alert_enabled = BoolField(default=False)

    backfill_earliest_time = StringField(default='-7d')

    backfill_enabled = BoolField(default=False)

    base_search = StringField()

    base_search_id = ForeignKey('itsimodels.kpi_base_search.KpiBaseSearch')

    base_search_metric = ForeignKey('itsimodels.kpi_base_search.SearchMetric')

    cohesive_ad = DictField()

    cohesive_anomaly_detection_is_enabled = BoolField(default=False)

    description = StringField(default='')

    enabled = BoolField(default=False)

    entity_filter_field = StringField(default='', alias='entity_id_fields')

    entity_split_field = StringField(default='', alias='entity_breakdown_id_fields')

    entity_statop = StringField(default='avg')

    entity_thresholds = TypeField(KpiThresholds)

    fill_gaps = StringField(default='null_value')

    gap_custom_alert_value = NumberField()

    gap_severity = StringField(default='unknown')

    gap_severity_color = StringField(default='')

    gap_severity_color_light = StringField(default='')

    gap_severity_value = StringField(default='-1')

    kpi_template_kpi_id = ForeignKey('itsimodels.kpi_threshold_template.KpiThresholdTemplate')

    kpi_threshold_template_id = StringField()

    is_filter_entities_to_service = BoolField(default=False, alias='is_service_entity_filter')

    is_split_by_entity = BoolField(default=False, alias='is_entity_breakdown')

    metric_search_spec = TypeField(MetricSearchSpec, alias='metric')

    metric_qualifier = StringField()

    search = StringField()

    search_alert = StringField()

    search_alert_earliest = StringField()

    search_alert_entities = StringField()

    search_buckets = StringField()

    search_occurrences = NumberField()

    search_type = StringField(default='adhoc')

    threshold_field = StringField(default='')

    time_policies = TypeField(KpiTimePolicies, alias='time_variate_thresholds_specification')

    trending_ad = DictField()

    type = StringField(default='kpis_primary')

    tz_offset = StringField()

    unit = StringField(default='')

    use_time_policies = BoolField(default=False, alias='time_variate_thresholds')

    urgency = NumberField()


class EntityRuleItem(ChildModel):
    field = StringField()

    field_type = StringField()

    rule_type = StringField()

    value = StringField()


class EntityRule(ChildModel):
    rule_condition = StringField()

    rule_items = ListField(EntityRuleItem)


class ServiceDependency(ChildModel):
    kpis_depending_on = ForeignKeyList('itsimodels.service.Kpi')

    service_id = ForeignKey('itsimodels.service.Service', alias='serviceid')


class ServiceTags(ChildModel):
    tags = ListField(str)

    template_tags = ListField(str)


class Service(BaseModel):
    key = StringField(required=True, alias='_key')

    title = StringField(required=True)

    description = StringField(default='')

    enabled = BoolField(default=False)

    entity_rules = ListField(EntityRule)

    kpis = ListField(Kpi)

    services_depends_on = ListField(ServiceDependency)

    services_depending_on_me = ListField(ServiceDependency)

    service_template_id = ForeignKey('itsimodels.service_template.ServiceTemplate', alias='base_service_template_id')

    service_tags = TypeField(ServiceTags)

    team_id = ForeignKey('itsimodels.team.Team', default=GLOBAL_TEAM_KEY, alias='sec_grp')
