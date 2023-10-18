from datetime import datetime, timedelta
from pytz import utc
from django.core.mail import send_mail
from config import settings
from service import models


def send_mailing(recipients) -> None:
    """Отправка рассылки клиентам из списка recipients."""
    print('Отправка...')
    emails = recipients.client.values('email')  # список почтовых адресов для рассылки
    title = recipients.message.title  # тема письма
    text = recipients.message.message  # текст письма

    for email in emails:
        try:
            send_mail(
                title,  # Тема письма
                text,
                settings.EMAIL_HOST_USER,  # От кого письмо
                recipient_list=[email['email']]  # попытка отправить письмо
            )
            status = 'success'
            answer = 'Письмо отправлено успешно!'

        # Если при отправке письма возникает ошибка
        except Exception as err:
            status = 'error'
            answer = str(err)

        models.MailingLog.objects.create(status=status, answer=answer, mailing=recipients)  # создание записи в логе


def send_email_tasks():
    """Функция для управления рассылками."""
    print('Запущена функция для управления рассылками')
    now = datetime.now(utc)  # текущая дата и время
    mailings = models.Mailing.objects.filter(status__in=[2, 3])  # рассылки со статусом создана или запущена

    for mailing in mailings:
        mailing_datetime = mailing.date_time  # Получить дату и время рассылки

        # Проверить, что дата и время рассылки наступили
        if now >= mailing_datetime:
            last_log = models.MailingLog.objects.filter(mailing=mailing.id).last()  # последняя попытка отправки

            # если рассылка еще не отправлялась
            if not last_log:
                print(f'Рассылка {mailing.id}: Отправка, так как она еще не была отправлена')
                send_mailing(mailing)

            # Если рассылка уже отправлялась
            else:
                # вычисление разницы между текущей датой и последней попыткой отправки
                from_last = now - last_log.date_time
                print(f'Рассылка {mailing.id}: Дата последней попытки - {last_log.date_time}, Время с последней попытки - {from_last}')

                # Проверить периодичность отправки
                if mailing.periodicity == 1 and from_last >= timedelta(days=1):
                    print(f'Рассылка {mailing.id}: Отправка из-за ежедневной периодичности')
                    send_mailing(mailing)
                elif mailing.periodicity == 2 and from_last >= timedelta(days=7):
                    print(f'Рассылка {mailing.id}: Отправка из-за еженедельной периодичности')
                    send_mailing(mailing)
                elif mailing.periodicity == 3 and from_last >= timedelta(days=30):
                    print(f'Рассылка {mailing.id}: Отправка из-за ежемесячной периодичности')
                    send_mailing(mailing)
