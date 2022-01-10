from service_factory import get_notification_service


def send_notification(msg, notif_settings) -> bool:
    # Проверяем, указаны ли сервисы доставки
    if len(notif_settings['channels']) == 0:
        return False

    # Перебираем каждый из каналов и рассылаем сообщения
    for ch in notif_settings['channels']:
        notif_service = get_notification_service(ch)
        print(f"-==== {ch} ====-")

        for g in notif_settings.get('groups', []):

            # Делаем отправку сообщения в группу
            target = g['options'].get(ch, '')
            if target != '':
                print(f"{g['id']}:{g['name']} - {target} --> {msg}")
                notif_service.send(target, msg)

            # Делаем отправку сообщения пользователю

            for u in g.get('users', []):
                target = u.get(ch, None)
                if target != '':
                    print(f"{u['id']}:{u['name']} - {target} --> {msg}")
                    notif_service.send(target, msg)
    return True


def send_simple_notification(service, target, message):
    notif_service = get_notification_service(service)
    notif_service.send(target, message)
