import unittest
import urlparse

from selenium import webdriver

import config
from posts import AppPost, Post
from tentapp import TentApp


class FunctionalTentAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global app
        app_post = AppPost('Xiaoping Test App',
                           write=['https://tent.io/types/status/v0'])
        app = TentApp(config.TEST_ENTITY, app_post)
        link = app.start_setup()
        if config.USE_SAUCE_FOR_TESTS:
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            desired_capabilities['version'] = '23'
            desired_capabilities['platform'] = 'Linux'
            desired_capabilities['name'] = 'Test Xiaoping using Selenium.'

            global driver
            driver = webdriver.Remote(
                desired_capabilities=desired_capabilities,
                command_executor=("http://" + config.SAUCE_USERNAME + ":" +
                                  config.SAUCE_KEY +
                                  "@ondemand.saucelabs.com:80/wd/hub")
            )
            driver.implicitly_wait(30)

            driver.get('https://micro.cupcake.io/signin')
            username_field = driver.find_element_by_name('username')
            username_field.send_keys(config.TENT_SERVER_USERNAME)
            password_field = driver.find_element_by_name('passphrase')
            password_field.send_keys(config.TENT_SERVER_PASSWORD)
            driver.find_element_by_class_name('btn-primary').click()

            driver.get(link)
            driver.find_element_by_class_name('btn-success').click()
            url_parameter = urlparse.urlparse(driver.current_url).query
            code = urlparse.parse_qs(url_parameter)['code'][0]
        else:
            print 'Go to the link, click accept, and enter the "code" part'
            print 'of the url argument here.'
            print link
            code = raw_input('> ')
        app.finish_setup(code)

    def test_setup(self):
        self.assertTrue(app.token_attachment)

    def test_post_status(self):
        status_post = Post('https://tent.io/types/status/v0#',
                           {'text': 'Test post.'})
        response = app.create_post(status_post)
        self.assertTrue(response)

    @classmethod
    def tearDownClass(self):
        driver.quit()


if __name__ == '__main__':
    unittest.main()
