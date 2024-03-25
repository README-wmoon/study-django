from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, redirect
from django.views import View

from member.models import Member
from member.serializers import MemberSerializer


class OAuthLoginView(View):
    def get(self, request):
        user = SocialAccount.objects.get(user_id=request.user.id)
        member_email = ""
        if user.provider == "kakao":
            member_email = user.extra_data.get("kakao_account").get("email")
        else:
            member_email = user.extra_data.get("email")

        member, created = Member.objects \
            .get_or_create(member_email=member_email, member_type=user.provider)

        # 최초 로그인 검사(회원가입 필요)
        if member.member_id is None or created:
            return redirect(f'/member/join?member_email={member_email}&id={member.id}')

        # OAuth 최초 로그인이 아닐 경우 조회된 member객체를 세션에 담아준다.
        request.session['member'] = MemberSerializer(member).data

        previous_uri = request.session.get('previous_uri')
        path = '/post/list?page=1'

        if previous_uri is not None:
            path = previous_uri
            del request.session['previous_uri']

        return redirect(path)