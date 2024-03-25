from django.db.models import Q, Count, F, ProtectedError, Max, Min
from django.test import TestCase

from member.models import Member


class MemberTest(TestCase):
    # pass
    # 클래스 내부에 코드를 작성하면 연결한 테이블에 저장되고,
    # 메소드 내에서 코드를 작성하면 임시 테이블에 저장된 뒤 사라진다.


    # create
    # member = Member.objects.create(
    #     member_email='test1@gmail.com',
    #     member_password='1234',
    #     member_age=20,
    #     member_name='테스트1',
    # )
    #
    # print(member.__dict__)

    # member = Member.objects.create(
    #     member_email='wooram@gmail.com',
    #     member_password='1234',
    #     member_age=30,
    #     member_name = '원랩',
    # )
    #
    # print(member.__dict__)

    # 테이블에 추가하지 않고 하려면 여기다가 test를 써주어야 된다.
    # def test_member_creation(self):
    #     member = Member.objects.create(
    #         member_email='test1@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트1',
    #     )
    #
    #     print(member.__dict__)

    # 회원 1명 추가
    # member = Member.objects.create(
    #     member_email='admin@gmail.com',
    #     member_password='1234',
    #     member_age=30,
    #     member_name='우람',
    #     member_status=False
    # )

    # print(member.__dict__)
    # 회원 3명 추가
    # for i in range(3):
    #     member = Member.objects.create(
    #         member_email=f'woorams{i}@gmail.com',
    #         member_password='1234',
    #         member_age=30,
    #         member_name=f'우람스{i}',
    #     )
    #
    #     print(member.__dict__)

    # save
    # datas = {
    #     'member_email': 'test1@gmail.com',
    #     'member_password': '1234',
    #     'member_age':20,
    #     'member_name':'테스트2',
    # }
    #
    # member = Member(**datas)
    # member.save()

    # 회원 1명 추가
    # datas = {
    #     'member_email': 'test9@gmail.com',
    #     'member_password': '1234',
    #     'member_age':20,
    #     'member_name':'테스트9',
    # }
    #
    # member = Member(**datas)
    # member.save()
    # 회원 2명 추가
    # datas = [     -> 회원 추가할떄 이걸로 받고 쓰인다.
    #     {},
    #     {},
    # ]

    # for i in range(2):
    #     datas = {
    #         'member_email': f'test{i + 9}@gmail.com',
    #         'member_password': '1234',
    #         'member_age': 20,
    #         'member_name': f'테스트{i + 9}',
    #     }
    #
    #     member = Member(**datas)
    #     member.save()

    # bulk_create
    # id는 가져오지 않는다.
    # members = Member.objects.bulk_create([
    #     Member(
    #         member_email='test3@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트3'),
    #
    #     Member(
    #         member_email='test4@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트4'),
    #
    #     Member(
    #         member_email='test5@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트5'),
    # ])
    #
    # for member in members:
    #     print(member.__dict__)

    # 회원 2명 추가
    # members = Member.objects.bulk_create([
    #     Member(
    #         member_email='test3@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트3'),
    #
    #     Member(
    #         member_email='test4@gmail.com',
    #         member_password='1234',
    #         member_age=20,
    #         member_name='테스트4'),
    # for member in members:
    #     print(member.__dict__)


    # get_or_create -> 회원가입
    # datas = {
    #     'member_password': '1234',
    #     'member_age':50,
    #     'member_name':'테스트6',
    # }
    # member, created = Member.objects.get_or_create(member_email='test5@gamil.com', defaults=datas)
    # print(member.__dict__, created)

    # member_email이 'admin1@gmail.com'인 회원을 조회한다.
    # 만약 없으면 새로운 정보를 전달하여 회원을 추가한다.

    # member, created = Member.objects.get_or_create(member_email= 'admin2@gmail.com', member_status=False, defaults=datas)
    # print(member.__dict__, created)

    # get
    # member = Member.objects.get(id=3)
    # print(member.__dict__)

    # all
    # paging 처리 요거 한줄
    # members = Member.objects.all()[1:3]
    # members = Member.enabled_objects.all()
    # for member in members:
    #     print(member.__dict__)

    # filter
    # member_queryset = Member.enabled_objects.filter(member_name='테스트6')
    # print(member_queryset.exists())
    # print(member_queryset[0].__dict__)

    # 로그인된 회원의 상세페이지에서 내가 등록한 맵주소 찾기
    # data = {
    #     'member_email': 'test4@gmail.com',
    #     'member_password': '1234'
    # }
    #
    # member = Member.enabled_objects.get(**data)
    # print(member.member_name)

    # 게시글과 댓글을 모두 작성한 회원을 찾으세요
    # 화면 예시
    # 회원 정보, 게시글 개수, 댓글 개수
    # query = """
    #     select * from
    #     (
    #         select m_p.id, m.member_email, m.member_name, count(p.id) m_p.post_count, count(r.id) reply_count
    #         from tbl_member m left outer join tbl_post p
    #         on m.id = p.member_id
    #         group by m.id, m.member_email, m.member_name
    #     ) m_p left outer join tbl_reply r
    #     on m_p.id = r.member_id
    #     group by m_p.id, m_p.member_email, m_p.member_name, m_p.post_count
    # """
    #
    # cursor = connection.cursor()
    # cursor.execute()
    # members = cursor.fecheall()
    # for descriptions in cursor.description:
    #     descriptions, *res
    #
    # for member in members:
    #     print(member)


    # members_post = Member.objects.values(
    #     'id',
    #     'member_email',
    #     'member_name',
    # ).annotate(post_count=Count('post'))
    #
    # members_reply = Member.objects.values(
    #     'id',
    #     'member_email',
    #     'member_name',
    # ).annotate(reply_count=Count('reply'))
    #
    # for i in range(len(members_post)):
    #     members_post[i]['reply_count'] = members_reply[i]['reply_count']
    #
    # for member_post in members_post:
    #     print(member_post)
    # range
    # 회원의 나이가 20이상 30이하인 회원이 작성한 게시글 중 post_title에 "테"가 들어가고 내용에 "7"로 끝나는 게시글 정보 조회
    # members = Member.objects.filter(
    #     member_age__range=[20, 30],
    #     post__post_title__contains='테',
    #     post__post_content__endswith='7'
    # ).values('member_age', 'post__post_title', 'post__post_content')
    #
    # for member in members:
    #     print(member)

    # posts = Post.objects.filter(
    #     member__member_age__range=[20, 30],
    #     post_title__contains='테',
    #     post_content__endswith='7'
    # ).values('member__member_age', 'post_title', 'post_content')
    #
    # for post in posts:
    #     print(post)


    # member들을 가져올때 -> 상세보기
    # members = []
    # for group in Group.enabled_objects.filter(id=3):
    #     members.append(group.member_set)
    #
    #     return members

    # contains
    # member_queryset = Member.enabled_objects.filter(member_name__contains='테')
    # print(member_queryset.exists())
    #
    # for member in member_queryset:
    #     print(member.__dict__)

    # startswith, endswith
    # member_queryset = Member.enabled_objects.filter(member_name__contains='3')
    # print(member_queryset.exists())
    #
    # for member in member_queryset:
    #     print(member.__dict__)

    # in -> 왼쪽에는 한개인데 오른쪽에 여러개일때 쓰임
    # values 쓰는 순간 딕셔너리로 객체로 return 한다.
    # in을 쓸때 list로 전달한다.
    # member_queryset = Member.enabled_objects.filter(member_email__in=['test3@gmail.com', 'test6@gmail.com']).values('member_email')
    # print(member_queryset.query)
    # for member_email in member_queryset:
    #     print(member_email.get('member_email'))

    # exclude()
    # member_queryset = Member.enabled_objects.exclude(member_email='test3@gmail.com').values('member_email')
    # for member in member_queryset:
    #     print(member['member_email'])

    # AND, OR
    # member_queryset = Member.objects.filter(status=True) & Member.objects.filter(member_age__gt=29)
    # condition1 = Q(status=True)
    # condition2 = Q(member_age__gt=29)
    #
    # member_queryset = Member.objects.filter(condition1 & condition2)
    # member_queryset = Member.objects.filter(condition1 | condition2)
    # for member in member_queryset:
    #     print(member.member_email, member.member_age, sep=", ")

    # order_by
    # member_queryset = Member.objects.all().order_by('-id')
    # for member in member_queryset:
    #     print(member.__dict__)

    # aggregate
    # 전체 대상
    # annotate()는 QuerySet객체로 리턴하기 때문에 뒤에 이어서 추가 작업이 가능하지만
    # aggregate()는 전체 대상이므로 뒤에 이어서 추가 작업이 불가능하다.
    # member = Member.objects.aggregate(max_age=Max('member_age'), min_age=Min('member_age'))
    # print(member['max_age'], member['min_age'])
    #
    # # save
    # # 회원 이름 수정
    # data = {
    #     'member_email': 'test3@gmail.com',
    #     'member_password': '1234'
    # }

    # member = Member.objects.get(**data)
    # member.member_name = '수정된 이름'
    # save()는 모든 필드에 넣어주기 떄문에
    # update_fields를 써서 해주어야 된다.
    # ex) member.member_password = 3333을 하면 save()를 하면 다 수정이 되지만
    # member.save(update_fields=['member_name'])요걸를 쓰임으로써 member_name만 수정된다.
    # member.save(update_fields=['member_name'])

    # member = Member.objects.get(**data)
    # count = member.update(member_name='다시 수정된 이름')
    # print(count)

    # 전체 다 바뀜
    # count = Member.objects.update(member_name='수정된 이름')
    # print(count)

    # 나이가 20살 이하인 회원의 나이를 +1한다.
    # 내꺼 갖고 올때 F를 쓰인다.
    # 할인율 적용이나 쿠폰 적용할 때
    # count = Member.object.filter(member_age__lte=20).update(mamber_age=F('mamber_age') + 1)

    # delete
    # try:
    #     count = Member.objects.get(id=26).delete()
    #     print(count)
    # except ProtectedError:
    #     print('ProtectedError')

   pass