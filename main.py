import manager
import datetime


def get_notification_settings(group_id):
    groups = [{
        "id": 33,
        "name": "MTS IoT HUB",
        "options": {
            "telegram": "-1001496682475",
            "email": "idobryak@gmail.com",
        },
        "users": [
            {
                "id": 1,
                "name": "Alexander Lakhno",
                "telegram": "2194759",
                "email": "aalakhn4@mts.ru",
            }
        ],
    },
        {
            "id": 34,
            "name": "Staff",
            "options": {
                "telegram": "-1003496682475",
            },
        }
    ]

    notification = {
        "channels": ['telegram', 'email'],
        "groups": groups,
        'message': "Hello, World"
    }
    return notification


if __name__ == "__main__":
    group = get_notification_settings(1)
    manager.send_notification(f"{datetime.datetime.now()}: Hello world!", group)
