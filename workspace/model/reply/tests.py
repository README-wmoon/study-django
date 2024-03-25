from django.db.models import F, Count
from django.test import TestCase

from member.models import Member
from post.models import Post
from reply.models import Reply


class ReplyTest(TestCase):

    # 댓글 추가
    # member_data = {
    #     'member_email': 'test5@gmail.com',
    #     'member_password': '1234'
    # }
    #
    # member = Member.enabled_objects.get(**member_data)
    # post = Post.objects.get(id=7)
    #
    # reply_data = {
    #     'reply_content': '댓글 테스트2',
    #     'member': member,
    #     'post': post,
    #
    # }
    #
    # reply = Reply.objects.create(**reply_data)
    # reply.group_id = reply.id
    # reply.save()

    member_data = {
        'member_email': 'wooram@gmail.com',
        'member_password': '1234',
    }
    member = Member.objects.get(**member_data)
    post = Post.objects.get(id=108)
    reply = Reply.objects.filter(post_id=post.id, reply_depth=1)[0]
    reply_data = {
        'reply_content': '댓글 테스트중1',
        'group_id': 5,
        'member': member,
        'post': post,
        'reply_depth': 1,
        'reply_private_status': True,

    }

    replies = Reply.objects.create(**reply_data)

    # 대댓글 3개 등록하기
    # ※ 실행 3번으로 3개 등록하기
    # member_data = {
    #     'member_email': 'test6@gmail.com',
    #     'member_password': '1234'
    # }
    # member = Member.objects.get(**member_data)
    # post = Post.objects.get(id=7)
    # reply = Reply.objects.filter(post_id=post.id, reply_depth=1)[0]
    #
    # re_reply_data = {
    #     'reply_content': '테스트 대댓글3',
    #     'post': post,
    #     'member': member,
    #     'group_id': reply.id,
    #     'reply_depth': 2,
    #     'reply_private_status': True
    # }
    #
    # re_reply = Reply.objects.create(**re_reply_data)
    # print(re_reply)
    #
    # replies = Reply.objects.filter(group_id=2)
    # for reply in replies:
    #     print(reply.get_reply_private_status_display())

    # 게시글 상세보기
    # 게시글 정보, 회원 정보, 댓글 목록, 댓글의 대댓글 목록
    # 7번 게시글의 내용과 작성자 정보를 가져온다.
    # post = Post.objects.filter(id=7)\
    #     .annotate(member_name=F('member__member_name'))\
    #     .values(
    #     'id',
    #     'post_title',
    #     'post_content',
    #     'member_name').first()

    # 게시글에 맞는 댓글 목록
    # replies = Reply.objects.filter(post_id=post['id'], reply_depth=1)
    #
    # for reply in replies:
    #     print(reply)

    # 댓글 번호를 전달받은 뒤
    # data = {
    #     'id': 2
    # }

    # 전달받은 댓글의 대댓글을 모두 가져온다.
    # re_replies = Reply.objects.filter(group_id=data['id'], reply_depth=2)
    #
    # for re_reply in re_replies:
    #     print(re_reply)

    # 게시글을 작성한 적이 있는 회원 목록 출력
    # members = Member.objects.filter(post__isnull=False).values()
    # for member in members:
    #     print(member)

    # 대댓글을 작성한 적이 없는 회원 목록 출력
    # replies = Reply.objects.filter(reply_depth=2).values('member_id')
    # member_ids = set()
    # for reply in replies:
    #     member_ids.add(reply['member_id'])
    #
    # members = Member.objects.exclude(id__in=member_ids).values()
    # for member in members:
    #     print(member)

    # members = Member.objects.exclude(reply__reply_depth=2).values('id', 'reply')
    # for member in members:
    #     print(member)

    # 나는 웹개발을 배울떄 데이터 짜는것까지 했다.
    pass









