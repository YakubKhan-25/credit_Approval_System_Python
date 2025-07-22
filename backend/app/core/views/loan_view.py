from core.models.customer import Customer
from core.models.loan import Loan
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models.loan import Loan
from core.services.calculate import checkEligibilityService
import math
from datetime import datetime, timedelta


@api_view(["POST"])
def check_eligibility_view(request):
    try:
        data = request.data
        result = checkEligibilityService(data)
        return Response(result, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def createLoan(request):
    try:
        data = request.data
        customer_id = data.get("customer_id")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        tenure = int(data.get("tenure"))

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        eligibility = checkEligibilityService(data)

        if not eligibility.get("approval"):
            return Response(
                {
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": False,
                    "message": "Loan not approved based on eligibility criteria",
                    "monthly_installment": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=tenure * 30)  # Approximate for months

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=eligibility.get("corrected_interest_rate"),
            tenure=tenure,
            monthly_installment=eligibility.get("monthly_payment"),
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date,
        )

        return Response(
            {
                "loan_id": loan.id,
                "customer_id": customer.id,
                "loan_approved": True,
                "message": "Loan approved and created",
                "monthly_installment": eligibility.get("monthly_payment"),
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def view_loan_by_id(request, loan_id):
    try:
        loan = Loan.objects.filter(id=loan_id).first()
        if not loan:
            return Response(
                {"error": "Loan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        customer = loan.customer

        return Response(
            {
                "loan_id": loan.id,
                "customer": {
                    "id": customer.id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.phone_number,
                    "age": customer.age,
                },
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "tenure": loan.tenure,
            }
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )

        loans = Loan.objects.filter(customer=customer)
        results = []
        for loan in loans:
            results.append(
                {
                    "loan_id": loan.id,
                    "loan_amount": loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": loan.monthly_installment,
                    "repayments_left": loan.tenure - loan.emis_paid_on_time,
                }
            )

        return Response(results)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
