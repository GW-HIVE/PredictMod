from django.contrib.auth.models import User

user1 = User.objects.create_user(
    username="Sample User", email="mazumderlab@gwu.edu", password="SampleUser"
)

user2 = User.objects.create_user(username="p", email="p@p.com", password="p")
