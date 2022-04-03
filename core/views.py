from django.shortcuts import render


def homeview(request):
    # 아마 여기서 로그인 체크를 해야겠지?

    return render(request, "home/home.html")
