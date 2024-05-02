# AI-Lab Recipes Infrastructure Documentation

## Standard Wofklows

Our standard workflows deal with building components and pushing their images to `quay.io/ai-lab`. These components include:
    - recipe applications:
        - Chatbot
        - Codegen
        - Summarizer
        - RAG
    - model_servers
    - models
    - instructlab workflows
    - training bootc workflows

For a full list of the images we build check out or [quay organization](https://quay.io/organization/ai-lab). These standard workflows should all be run against our standard repo `containers/ai-labs-recipes` rather than the mirror repo.

## Testing frameworks

Our testing frameworks are a bit different from our standard workflows. In terms of compute, some of these jobs run either AWS machines provisioned via terraform using secrets in the github repository, or customized github hosted action runners, as well as the standard ubuntu-22.04 github runners for jobs not requiring additional resources.

These workflows start by checking out the [terraform-test-environment-module](https://github.com/containers/terraform-test-environment-module) repo, as well as the code in `containers/ai-lab-recipes` at the `main` branch. Then it will provision the terraform instance, install the correct ansible playbook requirements, and runs a coressponding playbook. Aditional actions may also be taken depending on the testing framework in question.

Finally all of our testing framework workflows will call `terraform destroy` to remove the aws instance we have provisioned and publish the results of the workflow to slack.

IMPORTATNT: If you are doing development and testing, please make sure that instances in AWS are spun down before leaving if you have access to the AWS account.

### training-e2e

The test environment is initially based off of `Fedroa 40`. 
It bootstraps a `g5.8xlarge` AWS EC2 instance with Terraform.
Provisioning is executed with ansible. The ansible playbook is invoking bootc install and
reboots the instance.
