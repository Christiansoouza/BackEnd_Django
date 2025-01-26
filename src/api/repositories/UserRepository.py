from ..models import User
from typing import Literal
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
    def update_balance(amount:float, user_id:int,type_transaction:Literal['increase','decrease']):
        user = User.objects.get(id=user_id)
        if type_transaction not in ['increase', 'decrease']:
            raise ValueError("Tipo de transação inválido")

        if type_transaction == 'increase':
            user.balance += amount
        elif type_transaction == 'decrease':
            user.balance -= amount

        user.save()
    @staticmethod
    def get_amount(user_id):
        user = User.objects.get(id=user_id)  # Busca usando o ID
        return user.balance
    @staticmethod
    def delete_user(user_id):
        user = User.objects.get(id=user_id)
        user.delete()
        return user