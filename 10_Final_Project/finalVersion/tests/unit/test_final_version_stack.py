import aws_cdk as core
import aws_cdk.assertions as assertions

from final_version.final_version_stack import FinalVersionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in final_version/final_version_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = FinalVersionStack(app, "final-version")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
