import configparser
from atlassian.client import AtlassianAPI


class Jira(AtlassianAPI):
    """
    JIRA API Reference
    https://docs.atlassian.com/software/jira/docs/api/REST/7.6.1/
    """

    def get_status(self, issue_key):
        url = "/rest/api/2/issue/{issue_key}?fields=status".format(issue_key=issue_key)
        return (((self.get(url) or {}).get("fields") or {}).get("status") or {}).get("name") or {}


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    jira_url = config['jira']['url']
    jira_usr = config['jira']['username']
    jira_psw = config['jira']['password']

    jira = Jira(url=jira_url, username=jira_usr, password=jira_psw)
    status = jira.get_status('MVQA-901')
    print(status)
