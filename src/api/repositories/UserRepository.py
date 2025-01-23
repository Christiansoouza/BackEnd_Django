from models import User

class UserRepository:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_user(username, email):
        return User.objects.create(username=username, email=email)

    @staticmethod
    def update_user(user_id, username, email):
        user = User.objects.get(id=user_id)
        user.username = username
        user.email = email
        user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return user