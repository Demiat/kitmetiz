from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class OnlyAuthorMixin(UserPassesTestMixin):
    """Проверяет на авторство объекта."""

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    # def handle_no_permission(self):
    #     return redirect(
    #             'pages:nom_card_detail',
    #             pk=self.kwargs.get('pk')
    #         )
