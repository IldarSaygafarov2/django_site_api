from django.shortcuts import render


def show_telegram_redirect_page(request):
    user_id = request.GET.get('user_id')
    context = {
        'user_id': user_id
    }
    return render(request, 'tg_bot/index.html', context)
