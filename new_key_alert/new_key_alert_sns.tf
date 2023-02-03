# Cloud Trail and Cloud Watch
resource "aws_cloudtrail" "new_key_created" {
  name                          = "new_key_created"
  s3_bucket_name                = var.s3_bucket_name
  is_multi_region_trail         = true
  include_global_service_events = true
  depends_on                    = [aws_s3_bucket_policy.new_key_alert_bucket_policy]
}

resource "aws_cloudwatch_event_rule" "new_key_created" {
  name          = "new_key_created"
  event_pattern = <<PATTERN
{
  "source": [
    "aws.iam"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "iam.amazonaws.com"
    ],
    "eventName": [
      "CreateAccessKey"
    ]
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "new_key_created" {
  rule       = aws_cloudwatch_event_rule.new_key_created.name
  target_id  = "new_key_created"
  arn        = "arn:aws:lambda:us-east-1:${var.accont_number}:function:new_key_created_alert"
  depends_on = [aws_cloudwatch_event_rule.new_key_created]
}

# SNS
resource "aws_sns_topic" "new_key_created" {
  name = "new_key_created"
}

resource "aws_sns_topic_subscription" "new_key_created_email_subscription" {
  topic_arn  = aws_sns_topic.new_key_created.arn
  protocol   = "email"
  endpoint   = var.endpoint
  depends_on = [aws_sns_topic.new_key_created]
}

# S3
module "s3_bucket" {
  source = "terraform-aws-modules/s3-bucket/aws"

  bucket        = var.s3_bucket_name
  acl           = "private"
  force_destroy = true

  versioning = {
    enabled = true
  }

}

resource "aws_s3_bucket_policy" "new_key_alert_bucket_policy" {
  depends_on = [module.s3_bucket]
  bucket     = var.s3_bucket_name
  policy     = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AWSCloudTrailAclCheck",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:GetBucketAcl",
            "Resource": "arn:aws:s3:::${var.s3_bucket_name}"
        },
        {
            "Sid": "AWSCloudTrailWrite",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudtrail.amazonaws.com"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::${var.s3_bucket_name}/*",
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                }
            }
        }
    ]
}
EOF
}

# LAMBDA
resource "aws_lambda_function" "new_key_created_alert" {
  function_name = "new_key_created_alert"
  runtime       = "python3.9"
  handler       = "new_key_created_alert.lambda_handler"
  filename      = "new_key_created_alert.zip"
  role          = aws_iam_role.lambda_new_key_created_alert_role.arn
}

resource "aws_iam_role" "lambda_new_key_created_alert_role" {
  name = "lambda_new_key_created_alert_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "new_key_created_alert" {
  name = "new_key_created_alert"
  role = aws_iam_role.lambda_new_key_created_alert_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:us-east-1:${var.accont_number}:new_key_created" 
        }
    ]
}
EOF
}

resource "aws_lambda_permission" "new_key_created" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "arn:aws:lambda:us-east-1:${var.accont_number}:function:new_key_created_alert"
  principal     = "events.amazonaws.com"
  depends_on    = [aws_lambda_function.new_key_created_alert]
}
