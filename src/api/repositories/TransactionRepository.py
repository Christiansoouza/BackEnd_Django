from ..models import Transaction


class TransactionRepository:
    def create_transaction(
        sender:str,
        receiver:str,
        amount:float
    ):
        return Transaction.objects.create(
            sender = sender,
            receiver = receiver,
            amount = amount
        )
    def get_transactions():
        return Transaction.objects.all()
    def get_transaction(receiver:str):
        return Transaction.objects.get(receiver=receiver)
