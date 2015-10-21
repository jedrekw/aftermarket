import os
from sauceclient import SauceClient

USERNAME = os.environ.get('SAUCE_USERNAME', "testuj")
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', "0029898f-54be-48b2-9166-9306282bef0c")
sauce = SauceClient(USERNAME, ACCESS_KEY)

USER = "alfa"
PASSWORD = "testujalfa"

USER_BETA = "beta"
PASSWORD_BETA = "testujbeta"

USER_GAMMA = "gamma"
PASSWORD_GAMMA = "testujgamma"

USER_DELTA = "delta"
PASSWORD_DELTA = "testujdelta"


# browsers = [{"platform": "Windows 8.1",
#              "browserName": "firefox",
#              "version": "33"}]

# browsers = [{"platform": "Windows 8.1",
#              "browserName": "internet explorer",
#              "version": "11"}]

browsers = [{"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "8"},
            {"platform": "Windows 8.1",
             "browserName": "firefox",
             "version": "35"}]

# browsers = [{"platform": "Windows 8.1",
#              "browserName": "chrome",
#              "version": "31"},
#             {"platform": "Windows 8.1",
#              "browserName": "internet explorer",
#              "version": "11"},
#             {"platform": "Windows 8.1",
#              "browserName": "firefox",
#              "version": "33"}]