from wooper.test_class import ApiTestCase


class TestGithubApi(ApiTestCase):

    """
    or, alternatively, if you need to add some mixins you can go like that:

     from unittest import TestCase
     from wooper.test_class import ApiMixin

     class TestGithubApi(TestCase, ApiMixin):

    """

    server_url = "https://api.github.com/"
    print_url = True

    def test_what_it_returns_correct_headers(self):
        self.GET("/users/actionless")
        self.expect_status(200)
        self.expect_headers({
            'Content-Type': 'application/json; charset=utf-8',
            'Server': 'GitHub.com',
        })

    def test_what_user_item_has_login_and_id(self):
        self.GET("/users/actionless")
        self.expect_json_contains({
            "login": "actionless",
            "id": 1655669,
        })
        self.expect_json_match(
            "https://github.com/actionless",
            path="html_url"
        )
        self.expect_json_match(
            {"html_url": "https://github.com/actionless"}
        )
