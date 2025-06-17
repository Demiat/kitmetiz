def urlparams(request):
    """Собирает параметры в одну строку."""
    return {
        'urlparams': '&'.join(
            f'{k}={v}' for k, v in request.GET.items() if k != 'page'
        )
    }
