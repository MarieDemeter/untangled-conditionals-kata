class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        tests_passed = self.run_tests(project)
        deploy_successful = self.deploy_successful(project, tests_passed)
        summary = self.create_email_summary(deploy_successful, tests_passed)
        self.send_email(summary)

    def send_email(self, summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(summary)
        else:
            self.log.info("Email disabled")

    def create_email_summary(self, deploy_successful, tests_passed):
        if tests_passed:
            if deploy_successful:
                summary = "Deployment completed successfully"
            else:
                summary = "Deployment failed"
        else:
            summary = "Tests failed"
        return summary

    def deploy_successful(self, project, tests_passed):
        if tests_passed:
            deploy_success = self.is_success(project.deploy(), "Deployment successful", "Deployment failed")
        else:
            deploy_success = False

        return deploy_success

    def run_tests(self, project):
        if project.has_tests():
            tests_passed = self.is_success(project.run_tests(), "Tests passed", "Tests failed")
        else:
            self.log.info("No tests")
            tests_passed = True

        return tests_passed

    def is_success(self, method, log_info, log_error):
        if "success" == method:
            self.log.info(log_info)
            result = True
        else:
            self.log.error(log_error)
            result = False

        return result
