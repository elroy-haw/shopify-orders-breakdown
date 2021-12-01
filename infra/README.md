# Infrastructure
This folder creates a CloudWatch Event Rule that invokes a Lambda on a daily basis, which sends an email using SES.

## Guide
1. Get the latest version of terraform.
2. Update the `ses.tf` file with the emails of your sender and receiver.
3. Update the `cloudwatch.tf` file with the cron expression you desire.
4. Run `terraform init` to get latest version of `aws` and `null` providers.
5. Run `terraform apply -auto-approve`.
