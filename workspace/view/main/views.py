from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        # try:
        #     member = request.session['member']
        # except KeyError:
        #     member = None
        # return render(request, 'main.html', {'member': member})
        return render(request, 'main.html')
