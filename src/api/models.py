from django.db import models
#ORM para a tabela de usuarios
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username
#Tabela para salvar as transacoes realizadas
class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name="sent_transactions", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer from {self.sender.username} to {self.receiver.username} of {self.amount}"