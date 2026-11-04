from ninja import NinjaAPI
from ninja.security import django_auth
from apps.tracker.router import router as tracker_router

# auth=django_auth: пропускает только залогиненных пользователей (проверка sessionid)
api = NinjaAPI(
    title="Jira Clone API",
    description="API для Vue-компонентов трекера задач",
    urls_namespace="api",
    auth=django_auth
)


@api.get("/ping", auth=None)
def ping(request):
    return {"status": "ok", "message": "Django-Ninja is ready!"}


api.add_router("/tracker", tracker_router)
