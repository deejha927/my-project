from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .data import *
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class SignupView(APIView):
    def post(self, request):
        data = request.data
        userExist = User.objects.filter(Q(email=data.get("email", None)) | Q(username=data.get("username", None)))
        if userExist:
            return Response({"message": "Account already exist"}, status=400)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh_token": str(token),
                    "access_token": str(token.access_token),
                },
                status=200,
            )
        return Response(serializer.errors, status=401)


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        invoice = Invoices.objects.filter(user=request.user.id)
        serializer = InvoiceSerializer(invoice, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Invoice created"}, status=201)
        return Response(serializer.errors, status=401)


class InvoiceDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            invoice = Invoices.objects.get(invoice_id=id, user=request.user.id)
            serializer = InvoiceSerializer(invoice).data
            return Response(serializer)
        except:
            return Response({"message": "Invoice not found"}, status=404)


class AddInvoiceItem(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = request.data
        data["invoices"] = id
        serializer = ItemsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Item added to invoice"}, status=201)
        return Response(serializer.errors, status=401)
