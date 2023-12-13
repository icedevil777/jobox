from django.http.request import HttpRequest
from django.http.response import HttpResponseNotFound
from django.shortcuts import redirect
from core_base import models as cb_models


class OnlyIndustrialWorkerMixin:
    """Проверка, что пользователь является подборщиком"""

    view_uniq_name = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            req_user = request.user
            user_ty = cb_models.User.objects.get(email=req_user.email).user_type
            if req_user.is_authenticated:
                # Если почта не подтвепждена
                if not request.user.is_email_confirmed:
                    if self.view_uniq_name != "confirm_email_view" and self.view_uniq_name != 're_send_confirm_email_view':
                        if user_ty == 'INT':
                            return redirect('industrial:confirm_email')
                        if user_ty == 'APPLICANT':
                            return redirect('industrial:confirm_emailapp')
                    return super().dispatch(request, *args, **kwargs)

                if hasattr(request.user, 'industrial_worker'):
                    # Если не ознакомлен пользователь с аффертой
                    if not request.user.industrial_worker.is_agree_with_agreement:
                        if self.view_uniq_name == "industrial_user_agreement":
                            return super().dispatch(request, *args, **kwargs)
                        if user_ty == 'INT':
                            return redirect('industrial:user_agreement')

                if hasattr(request.user, 'app_user'):
                    if not request.user.app_user.is_agree_with_agreement:
                        if self.view_uniq_name == "industrial_user_agreement":
                            return super().dispatch(request, *args, **kwargs)
                        if user_ty == 'APPLICANT':
                            return redirect('industrial:user_agreementapp')
                return super().dispatch(request, *args, **kwargs)

            if user_ty == 'INT':
                return redirect('industrial:sign_in')
            elif user_ty == 'APPLICANT':
                return redirect('industrial:sign_in_app')
        except:
            return redirect('bulletin_board:index')


class IsAdminMixin:
    """Проверка, что пользователь является администратором"""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
        return HttpResponseNotFound("NOT FOUND 404")



