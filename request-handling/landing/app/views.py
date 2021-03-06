from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    prev_page_mode = request.GET.get('from-landing')
    if prev_page_mode is not None:
        counter_click[prev_page_mode] += 1
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    mode = request.GET.get('ab-test-arg', 'original')
    counter_show[mode] += 1
    if mode == 'test':
        return render_to_response('landing_alternate.html')

    return render_to_response('landing.html')


def get_conversion(clicks, shows):
    conversion = 0 if shows == 0 else clicks / shows
    return conversion


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    counter_click[request.GET.get('marker')] += 1

    test_conversion = get_conversion(counter_click['test'], counter_show['test'])
    original_conversion = get_conversion(counter_click['original'], counter_show['original'])

    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
