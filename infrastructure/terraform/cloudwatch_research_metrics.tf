# ==============================================================================
# CloudWatch Research Metrics & Cross-Layer Threat Correlation Alarms
# ==============================================================================

resource "aws_cloudwatch_log_metric_filter" "events_ingested" {
  name           = "${local.name_prefix}-events-ingested"
  pattern        = "[timestamp, level, thread, logger, corr, msg = \"*CROSS_LAYER_CORRELATION*\", ...]"
  log_group_name = aws_cloudwatch_log_group.ecs_logs.name

  metric_transformation {
    name          = "SecurityEventsIngested"
    namespace     = "AppShieldX/ThreatCorrelation"
    value         = "1"
    default_value = 0
  }
}

resource "aws_cloudwatch_log_metric_filter" "validation_rejections" {
  name           = "${local.name_prefix}-validation-rejections"
  pattern        = "[timestamp, level, thread, logger, corr, msg = \"*VALIDATION_REJECT*\", ...]"
  log_group_name = aws_cloudwatch_log_group.ecs_logs.name

  metric_transformation {
    name          = "ValidationRejections"
    namespace     = "AppShieldX/ThreatCorrelation"
    value         = "1"
    default_value = 0
  }
}

resource "aws_cloudwatch_log_metric_filter" "corr_rule_01_matches" {
  name           = "${local.name_prefix}-rule-corr-01-matches"
  pattern        = "[timestamp, level, thread, logger, corr, msg = \"*Rule=RULE-CORR-01*\", ...]"
  log_group_name = aws_cloudwatch_log_group.ecs_logs.name

  metric_transformation {
    name          = "RuleCorr01Matches"
    namespace     = "AppShieldX/ThreatCorrelation"
    value         = "1"
    default_value = 0
  }
}

resource "aws_cloudwatch_log_metric_filter" "policy_restrictions" {
  name           = "${local.name_prefix}-policy-restrictions"
  pattern        = "[timestamp, level, thread, logger, corr, msg = \"*Action: RESTRICT_SENSITIVE_ACTIONS*\", ...]"
  log_group_name = aws_cloudwatch_log_group.ecs_logs.name

  metric_transformation {
    name          = "PolicyRestrictionsEnforced"
    namespace     = "AppShieldX/ThreatCorrelation"
    value         = "1"
    default_value = 0
  }
}

resource "aws_cloudwatch_log_metric_filter" "step_up_challenges" {
  name           = "${local.name_prefix}-step-up-challenges"
  pattern        = "[timestamp, level, thread, logger, corr, msg = \"*Action: STEP_UP_AUTHENTICATION*\", ...]"
  log_group_name = aws_cloudwatch_log_group.ecs_logs.name

  metric_transformation {
    name          = "StepUpChallengesEnforced"
    namespace     = "AppShieldX/ThreatCorrelation"
    value         = "1"
    default_value = 0
  }
}

resource "aws_cloudwatch_metric_alarm" "high_severity_threat_burst" {
  alarm_name          = "${local.name_prefix}-high-severity-burst"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "RuleCorr01Matches"
  namespace           = "AppShieldX/ThreatCorrelation"
  period              = 60
  statistic           = "Sum"
  threshold           = 5
  alarm_description   = "Triggered when 5 or more cross-layer critical attacks are correlated within 1 minute"
  treat_missing_data  = "notBreaching"
}

# CloudWatch Dashboard for Research Telemetry & Cross-Layer Posture
resource "aws_cloudwatch_dashboard" "research_posture" {
  dashboard_name = "${local.name_prefix}-research-evaluation"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AppShieldX/ThreatCorrelation", "SecurityEventsIngested", { stat = "Sum", label = "Events Ingested" }],
            [".", "RuleCorr01Matches", { stat = "Sum", label = "Cross-Layer Attacks Correlated" }],
            [".", "ValidationRejections", { stat = "Sum", label = "Invalid/Malformed Events" }]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Cross-Layer Ingestion & Correlation Stream"
          period  = 60
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AppShieldX/ThreatCorrelation", "PolicyRestrictionsEnforced", { stat = "Sum", label = "Transactions Restricted (Band 4)" }],
            [".", "StepUpChallengesEnforced", { stat = "Sum", label = "Step-Up MFA Enforced (Band 3)" }]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Server-Side Risk-Adaptive Policy Enforcement"
          period  = 60
        }
      }
    ]
  })
}
