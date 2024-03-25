from django.shortcuts import redirect


def pre_handle_request(get_response):
    def middleware(request):
        uri = request.get_full_path()

        # 미들웨어에 작성한 코드가 반영되면 안되는 URI가 있고,
        # 이 URI가 아니라면,
        if 'admin' not in uri and 'accounts' not in uri and 'oauth' not in uri:
            # 요청한 서비스가 로그인을 필요로 한다면,
            if 'join' not in uri and 'login' not in uri:
                if request.session.get('member') is None:
                    # 요청한 경로를 session에 담은 뒤
                    request.session['previous_uri'] = uri
                    # 로그인 페이지로 이동시킨다.
                    return redirect('/member/login')

            if request.user_agent.is_mobile:
                uri = f'/mobile{uri}'
                request.path_info = uri

            # 모바일이 아니라면,
            else:
                uri.replace('/mobile', '')
                request.path_info = uri
        # 응답 전처리
        response = get_response(request)

        # 응답 후처리
        return response

    return middleware
