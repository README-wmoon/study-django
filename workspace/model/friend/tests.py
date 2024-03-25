from django.db.models import Q
from django.test import TestCase

from friend.models import Friend
from member.models import Member


class FriendTest(TestCase):
    # data = {
    #     'member_email': 'hoon@gmail.com',
    #     'member_password': 'hhhh',
    #     'member_name': '훈이',
    #     'member_age': 5
    # }
    #
    # Member.objects.create(**data)

    # 친구 요청
    # data = {
    #     'member_email': 'hoon@gmail.com',
    #     'member_password': 'hhhh'
    # }
    #
    # sender = Member.objects.get(**data)
    #
    # data = {
    #     'member_email': 'yuri@hanmail.net'
    # }
    #
    # receiver = Member.objects.get(member_email=data['member_email'])
    #
    # Friend.objects.create(sender=sender, receiver=receiver)

    # 친구 요청 조건(False일 때에만 요청 가능)
    # data = {
    #     'member_email': 'yuri@hanmail.net'
    # }
    #
    # receiver = Member.objects.get(member_email=data['member_email'])
    #
    # condition_exist = Q(receiver=receiver, sender=sender)
    # condition_status = Q(status=1) | Q(status=0)
    # condition = condition_exist & condition_status
    #
    # condition = Friend.objects.filter(condition).exists()
    # print(condition)

    # 친구 목록
    # data = {
    #     'member_email': 'yuri@hanmail.net',
    #     'member_password': 'yyyy'
    # }
    #
    # # 로그인한 회원
    # member = Member.objects.get(**data)

    # 친구 요청을 보냈거나 받은 목록에서
    # condition_sender = Q(sender=member)
    # condition_receiver = Q(receiver=member)
    # condition = condition_sender | condition_receiver

    #############################################################################
    # 친구 수락이 된 정보 모두 조회
    # friends = Friend.friends_objects.filter_member(member, status=True)
    # for friend in friends:
    #     Friend.objects.filter(id=friend).update(status=1)
    #     print(friend.friend)
    #############################################################################

    # members = Friend.enabled_objects.filter(condition, status=True)
    # friends = []
    # for friend in members:
    #     # 로그인한 회원이 아닌 상대 회원 정보 추출
    #     friends.append(friend.sender if friend.sender.id != member.id else friend.receiver)
    #
    # # 내 친구 목록
    # print(friends)
    #
    # for friend in friends:
    #     print(friend.__dict__)

    # 친구 삭제: 상태가 1인 친구들
    # 친구 거절: 상태가 0인 친구들
    # data = {
    #     'member_email': 'yuri@hanmail.net',
    #     'member_password': 'yyyy'
    # }
    #
    # member = Member.objects.get(**data)
    #
    # data = {
    #     'member_email': 'zzanggu@naver.com',
    # }
    #
    # friend = Member.objects.get(**data)
    #
    # Friend.friends_objects.filter_member(member, friend=friend.id, status=1).update(status=-1)

    # 친구 수락
    # data = {
    #     'member_email': 'yuri@hanmail.net',
    #     'member_password': 'yyyy'
    # }
    #
    # receiver = Member.objects.get(**data)
    #
    # data = {
    #     'member_email': 'hoon@gmail.com'
    # }
    #
    # sender = Member.objects.get(**data)
    #
    # Friend.objects.filter(sender=sender, receiver=receiver, status=0).update(status=True)
    pass