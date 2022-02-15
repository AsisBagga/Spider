from .test_setup import TestSetUp
from crawler.models import CrawlerModel

class TestViews(TestSetUp):
    def test_user_can_not_post_with_no_base_url(self):
        res = self.client.post(self.crawler_url)
        self.assertEqual(res.status_code, 400)

    def test_post_to_return_correct_status_code(self):
        res = self.client.post(
            self.crawler_url, self.user_data, format="json"
        )
        self.assertEqual(res.status_code, 201)

    def test_post_to_return_correct_data(self):
        res = self.client.post(
            self.crawler_url, self.user_data, format="json"
        )
        self.assertEqual(res.data, "abc.com/xyz")
    
    def test_to_check_if_object_exists(self):
        entry = CrawlerModel.objects.create(
            base_url="abc.com/xyz",
            site_links="abc.com"
        )
        entry.save()
        res = self.client.post(
            self.crawler_url, self.user_data, format="json"
        )
        self.assertEqual(res.data, "abc.com")
        self.assertEqual(res.status_code, 200)