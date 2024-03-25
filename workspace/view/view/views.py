# 학생의 번호, 국어, 영어, 수학 점수를 전달받은 뒤
# 총점과 평균을 화면에 출력한다.
from django.db.models import F
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post


# form태그는 get방식을 사용한다.
# 출력 화면에서 다시 입력화면으로 돌아갈 수 있게 한다.

# 입력: task/student/register.html
# 출력: task/student/result.html

class StudentRegisterFormView(View):
    def get(self, request):
        return render(request, 'task/student/register.html')


class StudentRegisterView(View):
    def get(self, request):
        data = request.GET
        data = {
            'id': data['id'],
            'kor': int(data['kor']),
            'eng': int(data['eng']),
            'math': int(data['math'])
        }

        total = data['kor'] + data['eng'] + data['math']
        average = round(total / 3, 2)

        return redirect(f'/student/result?total={total}&average={average}')


class StudentResultView(View):
    def get(self, request):
        data = request.GET
        context = {
            'total': request.GET['total'],
            'average': request.GET['average']
        }
        return render(request, 'task/student/result.html', context)

# 회원의 이름과 나이를 전달받는다.
# 전달받은 이름과 나이를 아래와 같은 형식으로 변경시킨다.
# "홍길동님은 20살!"
# 결과 화면으로 이동한다.

# 이름과 나이 작성: task/member/register.html
# 결과 출력: task/member/result.html


class MemberRegisterFormView(View):
    def get(self, request):
        return render(request, 'task/member/register.html')


class MemberRegisterView(View):
    def get(self, request):
        data = request.GET
        data = {
            'name': data['name'],
            'age': data['age']
        }
        result = f'{data["name"]}님은 {data["age"]}살!'
        return redirect(f'/member/result?result={result}')

    def post(self, request):
        data = request.POST
        data = {
            'name': data['name'],
            'age': data['age']
        }
        result = f'{data["name"]}님은 {data["age"]}살!'
        return redirect(f'/member/result?result={result}')

class MemberResultView(View):
    def get(self, request):
        result = request.GET['result']

        return render(request, 'task/member/result.html', {'result': result})


# 덧셈 뺼셈 곱셈 나눗셈
class UserCalculatorViewForm(View):
    def get(self, request):
        return render(request, 'task/users/register.html')

class UserCalculatorView(View):
    def get(self, request):
        data = request.GET
        data = {
            'number1': int(data['number1']),
            'number2': int(data['number2']),
            'number3': int(data['number3'])
        }

        add = data['number1'] + data['number2'] + data['number3']
        sub = data['number1'] - data['number2'] - data['number3']
        divide = round((data['number1'] / data['number2']) / data['number3'],2)
        multiple = data['number1'] * data['number2'] * data['number3']

        return redirect(f'/users/result?add={add}&sub={sub}&divide={divide}&multiple={multiple}')

class UserResultView(View):
    def get(self, request):
        data = request.GET
        context = {
            'add': request.GET['add'],
            'sub': request.GET['sub'],
            'divide': request.GET['divide'],
            'multiple': request.GET['multiple'],
        }
        return render(request, 'task/users/result.html', context)

class PlaceTravelViewForm(View):
    def get(self, request):
        return render(request, 'task/place/register.html')

class PlaceTravelView(View):
    def post(self, request):
        data = request.POST
        data = {
            'travel-day-count': int(data['travel-day-count']),
            'payment': int(data['payment']),
            'day': data['day'],
        }
        result = (f'여행{data["travel-day-count"]} 일차이며'
                  f' 가고싶은 여행지는 {data["day"]}이고'
                  f' 예산을 {data["payment"]}로 쓸것이다!!')
        return redirect(f'/place/result?result={result}')


class PlaceTravelResultView(View):
    def get(self, request):
        data = request.GET
        context = {
           'result': request.GET['result']
        }
        return render(request, 'task/place/result.html', context)


# 상품 정보
# 번호, 상품명, 가격, 재고
# 상품 1개 정보를 REST 방식으로 설계한 뒤
# 화면에 출력하기
# task/product/1
# task/product/product-list.html

class ProductInfoView(View):
    def get(self, request):
        return render(request, 'task/product/product-list.html')

class ProductInfoAPI(APIView):
    def get(self, request, product_id):
        data = {
            'id': product_id,
            'product_name': '마우스',
            'product_price': 50000,
            'product_stock': 50
        }
        return Response(data)


    #     data = {
    #         'id': product_id,
    #         'product_name': '마우스',
    #         'product_stock': 50,
    #     }
    #
    #     row_count = 5
    #
    #     offset = (product_id - 1) * row_count
    #     limit = product_id * row_count
    #
    #
    #     # API 쓸때는 항상 딕셔너리 상태 values()를 써서 나타내자
    #     # http://127.0.0.1:8000/post/list/1/
    #
    #     columns = [
    #         'id',
    #         'post_title',
    #         'post_content',
    #         'post_view_count',
    #         'member_name'
    #     ]
    #     posts = Post.enabled_objects \
    #                 .annotate(member_name=F('member__member_name')) \
    #                 .values(*columns)[offset:limit]
    #
    #     has_next = Post.enabled_objects.filter()[limit:limit + 1].exists()
    #
    #     post_info = {
    #         'posts': posts,
    #         'hasNext': has_next
    #     }
    #
    #     return Response(data)








