from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import Member
from member.serializers import MemberSerializer


class MemberCheckIdView(APIView):
    def get(self, request):
        member_id = request.GET['member-id']
        is_duplicated = Member.objects.filter(member_id=member_id).exists()
        return Response({'isDup': is_duplicated})


class MemberJoinView(View):
    def get(self, request):
        context = {
            'memberEmail': request.GET.get('member_email'),
            'id': request.GET.get('id')
        }
        return render(request, 'member/join.html', context)

    def post(self, request):
        data = request.POST
        data = {
            'member_name': data['member-name'],
            'member_birth': data['member-birth'],
            'member_phone': data['member-phone'],
            'member_id': data['member-id'],
            'member_password': data['member-password'],
            'member_email': data['member-email'],
        }

        # OAuth 최초 로그인 시 TBL_MEMBER에 INSERT된 회원 ID가 member_id이다.
        member = Member.objects.filter(id=request.POST.get('id'))
        # OAuth 최초 로그인 후 회원가입 시
        if member.exists():
            del data['member_email']
            data['updated_date'] = timezone.now()
            member.update(**data)

        else:
            member = Member.objects.create(**data)

        member = Member.objects.create(**data)

        return redirect('member:login')


class MemberLoginView(View):
    def get(self, request):
        return render(request, 'member/login.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_id': data['member-id'],
            'member_password': data['member-password']
        }

        members = Member.objects.filter(member_id=data['member_id'], member_password=data['member_password'])
        members = Member.objects.filter(member_id=data['member_id'], member_password=data['member_password'])
        if members.exists():
            request.session['member'] = MemberSerializer(members.first()).data
            previous_uri = request.session.get('previous_uri')
            path = '/post/list?page=1'

            if previous_uri is not None:
                path = previous_uri
                del request.session['previous_uri']

            return redirect(path)

        return render(request, 'member/login.html', {'check': False})


class MemberLogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect("/member/login")

class MemberMyPageAppView(View):
    def get(self, request):
        member = request.session['member']
        return render(request, 'member/mypage.html', context={'member': member})

    def post(self, request):
        pass

class MemberCollegeJoinView(View):
    def get(self, request):
        print(request.GET.get('member_name'))
        context = {
            'memberEmail': request.GET.get('member_email'),
            'memberType': request.GET.get('member_type'),
            'memberName': request.GET.get('member_name')
        }
        # member_info = request.session['join-member-data']
        # context = {
        #     'member_email': member_info['member_email'],
        #     'member_name': member_info['member_name']
        # }
        return render(request, 'member/college-student-normal-join.html', context)

    def post(self, request):
        data = request.POST
        data = {
            'member_name': data['member-name'],
            'member_birth': data['member-birth'],
            'member_phone': data['member-phone'],
            'member_id': data['member-id'],
            'member_password': data['member-password'],
            'member_email': data['member-email'],
        }

        # OAuth 검사
        # OAuth 최초 로그인 시 TBL_MEMBER에 INSERT된 회원 ID가 member_id 이다.
        member = Member.objects.filter(id=request.POST.get('member_id'))
        #   1. 아이디는 중복이 없다
        #   2. 이메일과 타입에 중복이 있다.
        #   3. OAuth로 최초 로그인된 회원을 찾아라

        # OAuth 최초 로그인 후 회원 가입
        if member.exists():
            del data['member_email']
            data['updated_date'] = timezone.now()
            member.update(**data)

        else:
            member = Member.objects.create(**data)

        return redirect('member:login')










