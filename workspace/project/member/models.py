from django.db import models

from project.period import Period


class Member(Period):
    member_name = models.CharField(null=True, blank=True, max_length=20)
    member_birth = models.DateField(null=True, blank=False)
    member_phone = models.CharField(null=True, blank=False, max_length=11)
    member_id = models.CharField(null=True, blank=False, max_length=20)
    member_email = models.CharField(null=False, blank=False, max_length=50)
    member_password = models.TextField(null=True, blank=False)
    member_type = models.TextField(blank=False, default="project")

    class Meta:
        db_table = 'tbl_member'


class MemberFile(Period):
    member = models.ForeignKey(Member, null=False, on_delete=models.PROTECT)
    path = models.ImageField(null=False, blank=False, upload_to='member/%Y/%m/%d')

    class Meta:
        db_table = 'tbl_member_file'