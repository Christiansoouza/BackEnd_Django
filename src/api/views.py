from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .repositories.UserRepository import UserRepository


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
            return Response({"message": "Usuário não encontrado!!"},status=status.HTTP_404_NOT_FOUND)  
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
            return Response({"message": "Usuário não encontrado"}, status=status.HTTP_204_NO_CONTENT)