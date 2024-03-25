from django.db import models

from member.models import Member
from post.managers import PostManager
# 학생의 번호, 국어, 영어, 수학 점수를 전달받은 뒤
# 총점과 평균을 화면에 출력한다.

class Student(models.Model):
    student_number = models.CharField(max_length=50, null=False, blank=False)
    student_korean = models.CharField(max_length=3000, null=False, blank=False)
    student_english = models.BigIntegerField(null=False, default=0)
    student_math = models.BooleanField(default=True)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)

    class Meta:
        db_table = 'tbl_student'
        ordering = ['-id']

    # def get_absolute_url(self):
    #     return f'/post/detail/{self.id}'
