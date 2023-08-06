from django.db import models


LOG_CHOICES = (
    ('release', 'RELEASE'),
    ('remove', 'REMOVE'),
    ('anticipate', 'ANTICIPATE'),
    ('improved', 'IMPROVED'),
)
LOG_DICT = dict(LOG_CHOICES)


class LogEntry(models.Model):
    class Meta:
        verbose_name = 'Log Entry'
        verbose_name_plural = 'Log Entries'
        ordering = ('-version',)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=20, choices=LOG_CHOICES, default='r')
    version = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return f'[{LOG_DICT.get(self.action, self.action.upper())}] {self.title}'
    
    def save(self, *args, **kwargs):
        try:
            cl = self.changelog.first()
            if cl: self.version = cl.version
        except:
            pass
        super().save(*args, **kwargs)

class Changelog(models.Model):
    class Meta:
        verbose_name = 'Changelog'
        verbose_name_plural = 'Changelogs'
        ordering = ('-created_at',)
    version = models.CharField(max_length=20)
    title = models.CharField(default='', max_length=200)
    description = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(LogEntry, related_name='changelog')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    @classmethod
    def latest(cls):
        return cls.objects.order_by('-created_at').prefetch_related('items').first()
    
    def __str__(self):
        return f'{self.version}: {self.title}'






