# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from datetime import datetime

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    when = models.DateField(blank=True, null=True)
    what = models.CharField(max_length=255, blank=True, null=True)
    from_hour = models.TimeField(blank=True, null=True)
    to_hour = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return self.what

    def delete(self):
        super(Task, self).delete()

    @property
    def delta(self):
        fmt = '%H:%M:%S'
        if self.from_hour and self.to_hour:
            return str(datetime.strptime(str(self.to_hour), fmt)
                    - datetime.strptime(str(self.from_hour), fmt)
                    )
        return ''

    @property
    def barWidth(self):
        fmt = '%H:%M:%S'
        if self.from_hour and self.to_hour:
            return str((datetime.strptime(str(self.to_hour), fmt)
                    - datetime.strptime(str(self.from_hour), fmt)).total_seconds() / 10
                    )
        return 0

    @staticmethod
    def get_nextautoincrement():
        cursor = connection.cursor()
        cursor.execute( "SELECT Auto_increment FROM information_schema.tables WHERE table_name='%s';" % \
                        Task._meta.db_table)
        row = cursor.fetchone()
        cursor.close()
        return row[0]
