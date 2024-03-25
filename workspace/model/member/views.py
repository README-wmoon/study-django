import math

from django.db import transaction
from django.db.models import Q, Count, F
from django.db.models.functions import Concat
from django.forms import CharField
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from activity.models import Activity, ActivityReply
from club.models import Club, ClubPost, ClubPostReply
from festival.models import Festival
from letter.models import Letter
from member.models import AdminAccount, Member
from member.serializers import AdminAccountSerializer
from notice.models import Notice

from django.utils import timezone

from wishlist.models import Wishlist, WishlistReply


# 관리자 로그인 페이지 이동
class AdminLoginView(View):
    def get(self, request):
        return render(request, 'admin/web/admin-login-web.html')

    def post(self, request):
        data = request.POST

        data = {
            'admin_id': data['admin_id'],
            'admin_password': data['admin_password']
        }

        admin = AdminAccount.objects.filter(**data)

        context = {'admin_data': None}

        if admin.exists():
            admin_data = AdminAccountSerializer(admin.first()).data
            context['admin_data'] = admin_data

        return render(request, 'admin/web/user-web.html', context)


# 관리자 유저 - 페이지 이동
class AdminUserView(View):
    def get(self, request):
        return render(request, 'admin/web/user-web.html')


# 관리자 유저 - 데이터 가져오기
class AdminUserAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        category = request.GET.get('category', '')
        keyword = request.GET.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1) | Q(status=-1)
        if category:
            condition &= Q(status=category)

        if keyword:
            condition &= Q(member_nickname__contains=keyword)

        total = Member.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'member_nickname',
            'created_date',
            'status'
        ]

        members = Member.objects.filter(condition).values(*columns).order_by(ordering)

        club_count = members.values('id').annotate(club_count=Count('club'))
        club_action_count = members.values('id').annotate(club_action_count=Count('clubmember', filter=Q(clubmember__status=1)))
        activity_count = members.values('id').annotate(activity_count=Count('activitymember', filter=Q(activitymember__status=1)))
        activity_club_count = members.values('id').annotate(activity_club_count=Count('club__activity', filter=Q(club__activity__status=1)))

        for i in range(len(list(members))):
            members[i]['club_count'] = club_count[i]['club_count']
            members[i]['club_action_count'] = club_action_count[i]['club_action_count']
            members[i]['activity_count'] = activity_count[i]['activity_count'] + activity_club_count[i]['activity_club_count']

        context['members'] = list(members[offset:limit])

        return Response(context)


# 관리자 유저 - 상태 변경
class AdminUserUpdateAPI(APIView):
    def patch(self, request, member_id):
        updated_date = timezone.now()

        member = Member.objects.get(id=member_id)

        if member.status == 1:
            member.status = -1
        elif member.status == -1:
            member.status = 1

        member.updated_date = updated_date
        member.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 쪽지 - 페이지 이동
class AdminMessageView(View):
    def get(self, request):
        return render(request, 'admin/web/message-web.html')


# 관리자 쪽지 - API
class AdminMessageAPI(APIView):
    # 데이터 가져오기
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        category = request.GET.get('category', '')
        type = request.GET.get('type', '')
        keyword = request.GET.get('keyword', '')
        targetId = request.GET.get('targetId', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        # 삭제되지 않은 쪽지만 가져오기
        condition = Q(status=1)

        # 멤버의 상태에 따른 카테고리 조회
        if category:
            condition &= Q(member__status=category)

        # 검색 타입에 따른 검색 결과 필터
        if type:
            if keyword:
                # 보낸 사람
                if type == 's':
                    condition &= Q(letter__sender_id__contains=keyword)

                # 받은 사람
                elif type == 'r':
                    condition &= Q(letter__receiver_id__contains=keyword)

        # 만약, targetID에 값이 있다면,
        if targetId:
            # conditions에 필터 추가
            condition &= Q(id=targetId)

        # total= 쪽지 개수 세기
        total = Letter.objects.filter(condition).all().count()
        print(total)

        # 보여질 데이터의 개수
        page_count = 5

        # 페이징 처리
        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        # context에 필드 담기
        context = {
            'category': category,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        # 정렬(내림차순, 최신순)
        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        # colums 설정
        # 보낸 사람
        # 	letter__sent_letter__sender
        #
        # 받은 사람
        # 	letter__received_letter__letter
        #
        # 보낸 날짜
        # 	letter__created_date
        columns = [
            'id',
            'sender_id',
            'receiver_id',
            'created_date',
            'status',
            'letter_content'
        ]

        # 쪽지 가져오기
        letter = Letter.objects.filter(condition).values(*columns).order_by(ordering)
        is_read = letter.annotate(is_read=F('receivedletter__is_read'))
        read_date = letter.annotate(read_date=F('receivedletter__updated_date'))
        print(read_date)
        member_status = letter.annotate(member_status=F('sender_id__member__status'))

        for i in range(len(list(letter))):
            letter[i]['is_read'] = is_read[i]['is_read']
            letter[i]['read_date'] = read_date[i]['read_date']
            letter[i]['member_status'] = member_status[i]['member_status']

        context['letter'] = list(letter[offset:limit])

        return Response(context)


    # 회원 상태 변경
    @transaction.atomic
    def fetch(self, request, promote_id):
        status = 0
        updated_date = timezone.now()

        club_post = ClubPost.objects.get(id=promote_id)
        club_post.status = status
        club_post.updated_date = updated_date
        club_post.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 쪽지 - 상태 변경
class AdminMessageUpdateAPI(APIView):
    def patch(self, request):
        pass


# 관리자 틴플레이 - 페이지 이동
class AdminTeenplayView(View):
    def get(self, request):
        return render(request, 'admin/web/teenplay-web.html')


# 관리자 틴플레이 - 데이터 가져오기
class AdminTeenplayAPI(APIView):
    def get(self, request, page):
        pass


# 관리자 틴플레이 - 삭제하기
class AdminTeenplayDeleteAPI(APIView):
    def delete(self, request):
        pass


# 관리자 게시글 홍보글 - 페이지 이동
class AdminPromoteView(View):
    def get(self, request):
        return render(request, 'admin/web/promote-web.html')


# 관리자 게시글 홍보글 - 데이터 가져오기
class AdminPromoteAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        type = request.GET.get('type', '')
        keyword = request.GET.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if type:
            if keyword:
                # 모임 이름
                if type == 'w':
                    condition &= Q(club__club_name__contains=keyword)

                # 제목
                elif type == 'p':
                    condition &= Q(post_title__contains=keyword)

        total = ClubPost.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'post_title',
            'post_content',
            'image_path',
            'created_date',
            'view_count'
        ]

        club_post = ClubPost.objects.filter(condition).values(*columns).order_by(ordering)
        club_name = club_post.annotate(club_name=F('club__club_name'))
        club_reply_count = club_post.annotate(club_reply_count=Count('clubpostreply__id'))
        club_post_category = club_post.annotate(club_post_category=F('category__category_name'))

        for i in range(len(list(club_post))):
            club_post[i]['club_name'] = club_name[i]['club_name']
            club_post[i]['club_reply_count'] = club_reply_count[i]['club_reply_count']
            club_post[i]['club_post_category'] = club_post_category[i]['club_post_category']

        context['club_post'] = list(club_post[offset:limit])

        return Response(context)


# 관리자 게시글 홍보글 - 데이터 삭제
class AdminPromoteDeleteAPI(APIView):
    # 게시글 삭제
    @transaction.atomic
    def delete(self, request, promote_id):
        status = 0
        updated_date = timezone.now()

        club_post = ClubPost.objects.get(id=promote_id)
        club_post.status = status
        club_post.updated_date = updated_date
        club_post.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 게시글 활동 모집 - 페이지 이동
class AdminActivityView(View):
    def get(self, request):
        return render(request, 'admin/web/activity-web.html')


# 관리자 게시글 활동 모집 - 데이터 가져오기
class AdminActivityAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        type = request.GET.get('type', '')
        keyword = request.GET.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)

        if type:
            if keyword:
                # 작성자
                if type == 'w':
                    condition &= Q(club__member__member_nickname__contains=keyword)

                # 제목
                elif type == 'p':
                    condition &= Q(activity_title__contains=keyword)

        total = Activity.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'activity_title',
            'activity_content',
            'created_date',
            'recruit_start',
            'recruit_end',
        ]

        activity = Activity.objects.filter(condition).values(*columns).order_by(ordering)
        activity_writer = activity.annotate(activity_writer=F('club__member__member_nickname'))
        member_count = activity.annotate(member_count=Count('activitymember__member__id'))

        for i in range(len(list(activity))):
            activity[i]['activity_writer'] = activity_writer[i]['activity_writer']
            activity[i]['member_count'] = member_count[i]['member_count']

        context['activity'] = list(activity[offset:limit])

        return Response(context)


# 관리자 게시글 활동 모집 - 게시글 삭제
class AdminActivityDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request, activity_id):
        status = 0
        updated_date = timezone.now()

        activity = Activity.objects.get(id=activity_id)
        activity.status = status
        activity.updated_date = updated_date
        activity.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 게시글 위시리스트 - 페이지 이동
class AdminWishlistView(View):
    def get(self, request):
        return render(request, 'admin/web/wishlist-web.html')


# 관리자 게시글 위시리스트 - 데이터 가져오기
class AdminWishlistAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        category = request.GET.get('category', '')
        type = request.GET.get('type', '')
        keyword = request.GET.get('keyword', '')
        targetId = request.GET.get('targetId', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(member__status=1, status=1)

        if category:
            if category == '1':
                condition &= Q(is_private=1)

            elif category == '0':
                condition &= Q(is_private=0)

        if type:
            if keyword:
                if type == 'p':
                    condition &= Q(member__member_nickname__contains=keyword)

                elif type == 'w':
                    condition &= Q(wishlist_content__contains=keyword)

        if targetId:
            condition &= Q(id=targetId)

        total = Wishlist.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'wishlist_content',
            'is_private',
            'member__id',
            'member__member_nickname',
            'member__status',
            'category__category_name'
        ]

        wishlist = Wishlist.objects.filter(condition).values(*columns).order_by(ordering)

        wishlist_like = wishlist.values('member__id').annotate(wishlist_like_count=Count('wishlistlike'))
        wishlist_reply = wishlist.values('member__id').annotate(wishlist_reply_count=Count('wishlistreply'))

        for i in range(len(list(wishlist))):
            wishlist[i]['wishlist_like_count'] = wishlist_like[i]['wishlist_like_count']
            wishlist[i]['wishlist_reply_count'] = wishlist_reply[i]['wishlist_reply_count']

        context['wishlist'] = list(wishlist[offset:limit])

        return Response(context)


# 관리자 게시글 위시리스트 - 게시글 삭제
class AdminWishlistDeleteAPI(APIView):
    def delete(self, request, wishlist_id):
        status = 0
        updated_date = timezone.now()

        wishlist = Wishlist.objects.get(id=wishlist_id)
        wishlist.status = status
        wishlist.updated_date = updated_date
        wishlist.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 전체 모임 - 페이지 이동
class AdminMeetingView(View):
    def get(self, request):
        return render(request, 'admin/web/meeting-web.html')


# 관리자 전체 모임 - 데이터 가져오기
class AdminMeetingAPI(APIView):
    def get(self, request, page):
        pass


# 관리자 전체 모임 - 데이터 삭제
class AdminMeetingDeleteAPI(APIView):
    def delete(self, request):
        pass


# 관리자 축제 - 페이지 이동
class AdminFestivalView(View):
    def get(self, request):
        # 패스티벌 불러오기
        data = request.GET
        festivals = Festival.objects.all()

        festival_info ={
            'festivals':[]
        }

        for festival in festivals:
            festival_info['festivals'].append({
                'festival_id': festival.id,
                'festival_title': festival.festival_title,
                'festival_content': festival.festival_content,
                'festival_end': festival.festival_end,
                'festival_location': festival.festival_location,
            })
        # print(festival_info)
        # festival_id = data.get['id']
        # print(festival_id)
        print(festival_info)

        return render(request, 'admin/web/festival-list-web.html', {'festivals': festivals})

# 관리자 축제 관리 - 삭제부분 - update로 처리하겠습니다.
class AdmiFestivalDeleteAPI(APIView):
    def get(self, request):
        status = 0
        updated_date = timezone.now()

        festival = Notice.objects.get(id=festival_id)
        festival.status = status
        festival.updated_date = updated_date
        festival.save(update_fields=['status', 'updated_date'])

        return Response('success')


# 관리자 축제 작성 - 페이지 이동
class AdminFestivalWrite(View):
    def get(self, request):
        return render(request, 'admin/web/festival-create-web.html')


# 관리자 공지사항 - 페이지 이동
class AdminNoticeView(View):
    def get(self, request):
        return render(request, 'admin/web/notice-list-web.html')


# 관리자 공지사항 - 데이터 가져오기
class AdminNoticePaginationAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        category = request.GET.get('category', '')
        keyword = request.GET.get('keyword', '')
        targetId = request.GET.get('targetId', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(status=1)
        if category:
            condition &= Q(notice_type=category)

        if keyword:
            condition &= Q(notice_title__contains=keyword)

        if targetId:
            condition &= Q(id=targetId)

        total = Notice.objects.filter(condition).all().count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'category': category,
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        columns = [
            'id',
            'notice_title',
            'created_date',
            'notice_content',
            'notice_type'
        ]

        notices = Notice.objects.filter(condition).values(*columns).order_by(ordering)

        context['notices'] = list(notices[offset:limit])

        return Response(context)


# 관리자 공지사항 - 데이터 삭제
class AdminNoticeUpdateAPI(APIView):
    # 게시글 삭제
    def patch(self, request, notice_id):
        status = 0
        updated_date = timezone.now()

        notice = Notice.objects.get(id=notice_id)
        notice.status = status
        notice.updated_date = updated_date
        notice.save(update_fields=['status', 'updated_date'])

        return Response('success')


## 관리자 공지사항 작성
class AdminNoticeWriteView(View):
    # 페이지 이동
    def get(self, request):
        return render(request, 'admin/web/notice-create-web.html')

    # 작성
    @transaction.atomic
    def post(self, request):
        data = request.POST
        data = {
            'notice_title': data['notice_title'],
            'notice_content': data['notice_content'],
            'notice_type': data['notice_type']
        }

        Notice.objects.create(**data)
        return redirect('/admin/notice/')


# 관리자 댓글 - 페이지 이동
class AdminCommentView(View):
    def get(self, request):
        return render(request, 'admin/web/comment-web.html')


# 관리자 댓글 - 데이터 가져오기
class AdminCommentAPI(APIView):
    def get(self, request, page):
        order = request.GET.get('order', 'recent')
        category = request.GET.get('category', '')
        type = request.GET.get('type', '')
        keyword = request.GET.get('keyword', '')

        row_count = 10

        offset = (page - 1) * row_count
        limit = page * row_count

        condition = Q(member_status=1) | Q(member_status=-1)

        if category:
            condition &= Q(member_status=category)

        if type:
            if keyword:
                # 작성자
                if type == 'w':
                    condition &= Q(member_name__contains=keyword)

                # 포스트
                elif type == 'p':
                    condition &= Q(title__contains=keyword)

        columns = [
            'member_name',
            'title',
            'created',
            'reply',
            'member_status',
            'reply_id',
            'reply_member_id',
            'reply_status',
            'reply_updated_date'
        ]

        activities = Activity.enabled_objects \
            .annotate(
                member_name=F('activityreply__member__member_nickname'),
                title=F('activityreply__activity__activity_title'),
                created=F('activityreply__created_date'),
                reply=F('activityreply__reply_content'),
                member_status=F('activityreply__member__status'),
                reply_id=F('activityreply__id'),
                reply_member_id=F('activityreply__member__id'),
                reply_status=F('activityreply__status'),
                reply_updated_date=F('activityreply__updated_date'),
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        wishes = Wishlist.enabled_objects \
            .annotate(
                member_name=F('wishlistreply__member__member_nickname'),
                title=F('wishlist_content'),
                created=F('wishlistreply__created_date'),
                reply=F('wishlistreply__reply_content'),
                member_status=F('wishlistreply__member__status'),
                reply_id=F('wishlistreply__id'),
                reply_member_id=F('wishlistreply__member__id'),
                reply_status=F('wishlistreply__status'),
                reply_updated_date=F('wishlistreply__updated_date')
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        club_posts = ClubPost.enabled_objects \
            .annotate(
                member_name=F('clubpostreply__member__member_nickname'),
                title=F('clubpostreply__club_post__post_title'),
                created=F('clubpostreply__created_date'),
                reply=F('clubpostreply__reply_content'),
                member_status=F('clubpostreply__member__status'),
                reply_id=F('clubpostreply__id'),
                reply_member_id=F('clubpostreply__member__id'),
                reply_status=F('clubpostreply__status'),
                reply_updated_date=F('clubpostreply__updated_date')
            ) \
            .values(*columns).filter(member_name__isnull=False, reply_status=1)

        activity = activities.filter(condition)
        wishlist = wishes.filter(condition)
        club_post = club_posts.filter(condition)

        total = activity.union(wishlist).union(club_post).count()

        page_count = 5

        end_page = math.ceil(page / page_count) * page_count
        start_page = end_page - page_count + 1
        real_end = math.ceil(total / row_count)
        end_page = real_end if end_page > real_end else end_page

        if end_page == 0:
            end_page = 1

        context = {
            'total': total,
            'order': order,
            'start_page': start_page,
            'end_page': end_page,
            'real_end': real_end,
            'page_count': page_count,
        }

        ordering = '-id'
        if order == 'popular':
            ordering = '-post_read_count'

        comment = activity.union(wishlist).union(club_post).order_by('-created')

        context['comment'] = list(comment[offset:limit])

        return Response(context)


# 관리자 댓글 - 데이터 삭제
class AdminCommentDeleteAPI(APIView):
    @transaction.atomic
    def delete(self, request):
        reply_id = request.GET.get('reply_id', '')
        reply_member_id = request.GET.get('reply_member_id', '')
        created_date = request.GET.get('created_date', '')

        columns = [
            'member_name',
            'title',
            'created',
            'reply',
            'member_status',
            'reply_id',
            'reply_member_id',
            'reply_status',
            'reply_updated_date'
        ]

        activities = Activity.enabled_objects \
            .annotate(
            member_name=F('activityreply__member__member_nickname'),
            title=F('activityreply__activity__activity_title'),
            created=F('activityreply__created_date'),
            reply=F('activityreply__reply_content'),
            member_status=F('activityreply__member__status'),
            reply_id=F('activityreply__id'),
            reply_member_id=F('activityreply__member__id'),
            reply_status=F('activityreply__status'),
            reply_updated_date = F('activityreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        wishes = Wishlist.enabled_objects \
            .annotate(
            member_name=F('wishlistreply__member__member_nickname'),
            title=F('wishlist_content'),
            created=F('wishlistreply__created_date'),
            reply=F('wishlistreply__reply_content'),
            member_status=F('wishlistreply__member__status'),
            reply_id=F('wishlistreply__id'),
            reply_member_id=F('wishlistreply__member__id'),
            reply_status=F('wishlistreply__status'),
            reply_updated_date=F('wishlistreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        club_posts = ClubPost.enabled_objects \
            .annotate(
            member_name=F('clubpostreply__member__member_nickname'),
            title=F('clubpostreply__club_post__post_title'),
            created=F('clubpostreply__created_date'),
            reply=F('clubpostreply__reply_content'),
            member_status=F('clubpostreply__member__status'),
            reply_id=F('clubpostreply__id'),
            reply_member_id=F('clubpostreply__member__id'),
            reply_status=F('clubpostreply__status'),
            reply_updated_date=F('clubpostreply__updated_date')
        ) \
            .values(*columns).filter(member_name__isnull=False)

        activity = activities.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)
        wishlist = wishes.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)
        club_post = club_posts.filter(reply_id=reply_id, reply_member_id=reply_member_id, created=created_date)

        comment = activity.union(wishlist).union(club_post)
        comment = list(comment)[0]

        wishlist_replies = list(WishlistReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        activity_replies = list(ActivityReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        club_post_replies = list(ClubPostReply.objects\
            .filter(id=comment['reply_id'],
                    member_id=comment['reply_member_id'],
                    created_date=comment['created']))

        if wishlist_replies:
            for wishlist_reply in wishlist_replies:
                wishlist_reply.status = 0
                wishlist_reply.updated_date = timezone.now()
                wishlist_reply.save(update_fields=['status', 'updated_date'])

        elif activity_replies:
            for activity_reply in activity_replies:
                activity_reply.status = 0
                activity_reply.updated_date = timezone.now()
                activity_reply.save(update_fields=['status', 'updated_date'])

        elif club_post_replies:
            for club_post_reply in club_post_replies:
                club_post_reply.status = 0
                club_post_reply.updated_date = timezone.now()
                club_post_reply.save(update_fields=['status', 'updated_date'])

        return Response('success')





# ----------------------------------------------------------------------------------------------------------------------
# 회사 소개 페이지 이동
class CompanyIntroductionView(View):
    def get(self, request):
        return render(request, 'company-info/web/company-info-web.html')


# 회사 소개에서 공지사항 띄우기
class CompanyNoticeListAPI(APIView):
    def get(self, request, page):
        row_count = 7
        offset = (page - 1) * row_count
        limit = page * row_count

        notices = Notice.objects.filter(status=True).values()[offset:limit]

        has_next = Notice.objects.filter(status=True)[limit:limit+1].exists()

        total = Notice.objects.filter(status=True).count()

        notice_info = {
            'notices': notices,
            'hasNext': has_next,
            'total': total
        }

        return Response(notice_info)

