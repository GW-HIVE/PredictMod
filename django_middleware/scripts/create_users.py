from users.models import SiteUser
from django.contrib.auth.models import User

users = {
    0: {
        "username": "mazumderlab@gwu.edu",
        "email": "mazumderlab@gwu.edu",
        "password": "SampleUser",
        "first_name": "Sample",
        "last_name": "User",
    },
    1: {  # Patient
        "username": "p@p.p",
        "email": "p@p.p",
        "password": "p",
        "first_name": "p",
        "last_name": "p",
    },
    2: {  # Clinician
        "username": "c@c.c",
        "email": "c@c.c",
        "password": "c",
        "first_name": "c",
        "last_name": "c",
    },
    3: {  # Researcher
        "username": "r@r.r",
        "email": "r@r.r",
        "password": "r",
        "first_name": "r",
        "last_name": "r",
        "is_staff": True,
    },
    4: {  # Admin + superuser
        "username": "a",
        "email": "a",
        "password": "a",
        "first_name": "a",
        "last_name": "a",
        "is_staff": True,
        "is_superuser": True,
    },
}

categories = [3, 1, 2, 3, 3]

print(f"====\tCreating USERS\t====")

for k, v in users.items():
    user = User.objects.create_user(**users[k])
    SiteUser.objects.create(user=user, category=categories[k])

# user1 = User.objects.create_user(**users[0])
# siteuser1 = SiteUser.objects.create(user=user1, category=3)

# user2 = User.objects.create_user(**users[1])
# siteuser2 = SiteUser.objects.create(user=user2, category=1)

# user3 = User.objects.create_user(**users[2])
# siteuser3 = SiteUser.objects.create(user=user3, category=2)

# user4 = User.objects.create_user(**users[3])
# siteuser4 = SiteUser.objects.create(user=user4, category=3)
