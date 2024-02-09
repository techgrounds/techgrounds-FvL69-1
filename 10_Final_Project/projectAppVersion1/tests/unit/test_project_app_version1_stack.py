import aws_cdk as core
import aws_cdk.assertions as assertions

from project_app_version1.project_app_version1_stack import ProjectAppVersion1Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in project_app_version1/project_app_version1_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProjectAppVersion1Stack(app, "project-app-version1")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
