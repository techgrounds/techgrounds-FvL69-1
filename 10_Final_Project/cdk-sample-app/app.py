#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_sample_app.cdk_sample_app_stack import CdkSampleAppStack


app = cdk.App()
CdkSampleAppStack(app, "CdkSampleAppStack")

app.synth()
