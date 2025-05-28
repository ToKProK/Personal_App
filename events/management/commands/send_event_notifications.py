from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import send_mail
from events.models import Event, Subscribe
from datetime import timedelta

class Command(BaseCommand):
    help = 'Отправляет напоминания участникам мероприятий, которые начнутся завтра.'

    def handle(self, *args, **options):
        tomorrow = now().date() + timedelta(days=1)

        events = Event.objects.filter(start_datetime__date=tomorrow, is_published=True)

        for event in events:
            subscriptions = Subscribe.objects.filter(event=event)

            for sub in subscriptions:
                user = sub.user
                if user.email:
                    send_mail(
                        subject=f'Напоминание: завтра начинается мероприятие "{event.title}"',
                        message=(
                            f'Здравствуйте, {user.get_full_name() or user.username}!\n\n'
                            f'Вы зарегистрированы на мероприятие "{event.title}", которое начнётся завтра '
                            f'{event.start_datetime.strftime("%d.%m.%Y в %H:%M")}.\n\n'
                            f'Место проведения: {"онлайн" if event.online_event else event.location}\n'
                            f'{f"Ссылка: {event.online_link}" if event.online_event and event.online_link else ""}\n\n'
                            f'Описание мероприятия:\n{event.description}\n\n'
                            'С уважением,\nКоманда организаторов.'
                        ),
                        from_email=None,  # Использует DEFAULT_FROM_EMAIL
                        recipient_list=[user.email],
                        fail_silently=False,
                    )

        self.stdout.write(self.style.SUCCESS('Уведомления отправлены.'))