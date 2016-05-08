import hashlib

from django.db import models

minimum_char_hash = 8


class Url(models.Model):
    original_url = models.CharField(max_length=500)
    hash_url = models.CharField(max_length=40)
    short_url = models.CharField(max_length=40)
    count = models.IntegerField(default=1)

    def set_hash(self, original_url):
        url_to_hash = original_url + str(self.count)
        self.hash_url = hashlib.sha1(url_to_hash).hexdigest()

    def set_short_url(self):
        hashed_url = self.hash_url
        current_hash_digits = minimum_char_hash
        min_short_url = hashed_url[:current_hash_digits]
        while Url.objects.filter(hash_url__startswith=min_short_url).exists():
            current_hash_digits += 2
            min_short_url = hashed_url[:current_hash_digits]

        self.short_url = min_short_url

    def add_analytics(self):
        self.analytics = Analytics.create_analytics()

    @classmethod
    def create_url(cls, original_url):
        # TODO: possible race condition on count
        current_count = Url.objects.filter(original_url=original_url).count() + 1
        url = cls(original_url=original_url, count=current_count)
        url.set_hash(original_url)
        url.set_short_url()
        url.add_analytics()
        url.save()

        return url

    def __str__(self):
        return self.original_url


class Analytics(models.Model):
    url = models.OneToOneField(Url, on_delete=models.CASCADE)
    visit_count = models.IntegerField(default=0)

    @classmethod
    def create_analytics(cls):
        return Analytics(visit_count=0)

    def add_visit(self, referrer):
        self.visit_count += 1
        self.visit_set.create(referrer=referrer)
        self.save()


class Visit(models.Model):
    analytics = models.ForeignKey(Analytics, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500)
