def urlparams(request):
    """Собирает параметры в одну строку."""
    params = {
        'urlparams': '&'.join(
            f'{k}={v}' for k, v in request.GET.items() if k not in (
                'page', 'category'
            )
        )
    }

    return params
