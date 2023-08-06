# Event Targets for Amazon EventBridge

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library contains integration classes to send Amazon EventBridge to any
number of supported AWS Services. Instances of these classes should be passed
to the `rule.addTarget()` method.

Currently supported are:

* Start a CodeBuild build
* Start a CodePipeline pipeline
* Run an ECS task
* Invoke a Lambda function
* Publish a message to an SNS topic
* Send a message to an SQS queue
* Start a StepFunctions state machine
* Queue a Batch job
* Make an AWS API call
* Put a record to a Kinesis stream
* Log an event into a LogGroup
* Put a record to a Kinesis Data Firehose stream

See the README of the `@aws-cdk/aws-events` library for more information on
EventBridge.

## LogGroup

Use the `LogGroup` target to log your events in a CloudWatch LogGroup.

For example, the following code snippet creates an event rule with a CloudWatch LogGroup as a target.
Every events sent from the `aws.ec2` source will be sent to the CloudWatch LogGroup.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_logs as logs
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets

log_group = logs.LogGroup(self, "MyLogGroup",
    log_group_name="MyLogGroup"
)

rule = events.Rule(self, "rule",
    event_pattern=EventPattern(
        source=["aws.ec2"]
    )
)

rule.add_target(targets.CloudWatchLogGroup(log_group))
```
