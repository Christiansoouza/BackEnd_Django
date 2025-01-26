from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from rest_framework import status
from .serializers import UserSerializer,TransactionSerializer
from .repositories.UserRepository import UserRepository
from .repositories.TransactionRepository import TransactionRepository


class UserView(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')  
        if user_id:
            try: 
                user = UserRepository.get_user_by_id(user_id)  
                if user:
                    serializer = UserSerializer(user)  
                    return Response(serializer.data)
                else:
                    return Response({"error": "O usuario não foi encontrado"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as _:
                return Response({"error": "Servidor indisponivel"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Usuario inválido"}, status=status.HTTP_404_NOT_FOUND)

    # Método POST para criar um novo usuário
    def post(self, request):
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            # Cria o usuário no banco
            user = UserRepository.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            # Serializar o novo usuário
            response_data = UserSerializer(user).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método PUT para atualizar um usuário específico
    def put(self, request):
        user_id = request.data.get('id')
        try:
            user = UserRepository.get_user_by_id(user_id)
        except Exception as _:
            return Response({"error": "Usuário não encontrado!!"},status=status.HTTP_404_NOT_FOUND)  
        serializer = UserSerializer(user, data=request.data, partial=True)  
        if serializer.is_valid():
            updated_user = UserRepository.update_user(
                user_id=user_id,
                username=serializer.validated_data.get('username', user.username),
                email=serializer.validated_data.get('email', user.email)
            )
            return Response(UserSerializer(updated_user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Método DELETE para excluir um usuário específico
    def delete(self, request):
        user_id = request.data.get('id')
        try:
            UserRepository.delete_user(user_id)  
            return Response({"message": "Usuario deletado com sucesso"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as _:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_204_NO_CONTENT)

class TransactionView(APIView):
    def get(self,request):
        ...
    def post(self,request):
        def validate_balance(
            sender: int,
            amount:float
        ):
            if isinstance(sender, User):
                sender = sender.id  # Extrai o ID de uma instância de Us
            balance = UserRepository.get_amount(user_id=sender)
             
            return balance >= amount 
            
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                sender_id = serializer.validated_data['sender']
                receiver_id = serializer.validated_data['receiver']
                amount = serializer.validated_data['amount']
                if validate_balance(sender=sender_id,amount=amount):
                    # Cria a transação no banco
                    transaction = TransactionRepository.create_transaction(
                        sender=sender_id,
                        receiver=receiver_id,
                        amount=amount
                    )

                    if not transaction:
                        return Response(
                            {"error": "Não foi possível realizar a transação"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                        
                    # Atualiza o saldo do receiver
                    UserRepository.update_balance(
                        amount=transaction.amount,
                        user_id=transaction.receiver.id if isinstance(transaction.receiver, User) else transaction.receiver,
                        type_transaction='increase'
                    )
                    UserRepository.update_balance(
                        amount=transaction.amount,
                        user_id=transaction.sender.id if isinstance(transaction.sender, User) else transaction.sender,
                        type_transaction='decrease'                    
                        )

                    # Retorna sucesso
                    return Response(
                        {"success": "Transferência realizada com sucesso!"},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response({"error": "Você está duro!!"},status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                # Trata erros inesperados
                return Response(
                    {"error": f"Erro ao processar a transação: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        # Retorna erros de validação do serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
