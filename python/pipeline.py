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
        if not self.config.send_email_summary():
            self.log.info("Email disabled")
            return

        self.log.info("Sending email")
        self.emailer.send(summary)

    def create_email_summary(self, deploy_successful, tests_passed):
        if not tests_passed:
            return "Tests failed"

        if not deploy_successful:
            return "Deployment failed"

        return "Deployment completed successfully"

    def deploy_successful(self, project, tests_passed):
        if not tests_passed:
            return False

        if "success" != project.deploy():
            self.log.error("Deployment failed")
            return False

        self.log.info("Deployment successful")
        return True

    def run_tests(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return True

        if "success" != project.run_tests():
            self.log.error("Tests failed")
            return False

        self.log.info("Tests passed")
        return True
