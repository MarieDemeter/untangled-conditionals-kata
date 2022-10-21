class TestFailedException(Exception):
    pass


class DeploymentFailedException(Exception):
    pass


class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):
        try:
            self.run_tests(project)
            self.deploy_successful(project)
            self.send_email("Deployment completed successfully")
        except TestFailedException:
            self.send_email("Tests failed")
        except DeploymentFailedException:
            self.send_email("Deployment failed")

    def send_email(self, summary):
        if not self.config.send_email_summary():
            self.log.info("Email disabled")
            return

        self.log.info("Sending email")
        self.emailer.send(summary)

    def deploy_successful(self, project):
        if "success" != project.deploy():
            self.log.error("Deployment failed")
            raise DeploymentFailedException

        self.log.info("Deployment successful")

    def run_tests(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return

        if "success" != project.run_tests():
            self.log.error("Tests failed")
            raise TestFailedException

        self.log.info("Tests passed")
