from django.contrib.auth.models import User

user1 = User.objects.create_user(
    username="mazumderlab@gwu.edu",
    email="mazumderlab@gwu.edu",
    password="SampleUser",
    first_name="Sample",
    last_name="User",
)

user2 = User.objects.create_user(
    username="p@p.p", email="p@p.p", password="p", first_name="p", last_name="p"
)
