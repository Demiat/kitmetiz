def urlparams(request):
    """Собирает параметры в одну строку."""
    params = {
        'urlparams': '&'.join(
            f'{k}={v}' for k, v in request.GET.items() if k not in (
                'page', 'category'
            )
        )
    }
    if request.GET.get('category'):
        params['last_category'] = f'category={request.GET["category"]}'
    return params
