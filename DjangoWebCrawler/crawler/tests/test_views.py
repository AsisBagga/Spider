from .test_setup import TestSetUp

class TestViews(TestSetUp):
    def test_user_can_not_post_with_no_base_url(self):
        res = self.client.post(self.crawler_url)
        self.assertEqual(res.status_code, 400)

    def test_post_to_return_correct_status_code(self):
        res = self.client.post(
            self.crawler_url, self.user_data, format="json"
        )
        self.assertEqual(res.status_code, 200)

    def test_post_to_return_correct_data(self):
        res = self.client.post(
            self.crawler_url, self.user_data, format="json"
        )
        self.assertEqual(res.data, "abc.com/xyz\n")
