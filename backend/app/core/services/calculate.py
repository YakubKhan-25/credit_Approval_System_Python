from core.models.customer import Customer
from core.models.loan import Loan
import math
from datetime import datetime


def calculate_credit_score(customer_id):
    try:
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            return 0
        loans = Loan.objects.filter(customer=customer)
        if not loans.exists():
            return 100

        current_year = datetime.now().year
        score = 100

        on_time_emis = sum(loan.emis_paid_on_time for loan in loans)
        total_emis = sum(loan.tenure for loan in loans)
        loan_count = loans.count()
        loan_volume = sum(loan.loan_amount for loan in loans)
        current_year_loans = loans.filter(start_date__year=current_year).count()

        total_debt = sum(
            loan.monthly_installment * (loan.tenure - loan.emis_paid_on_time)
            for loan in loans
        )
        if total_debt > customer.approved_limit:
            return 0

        if loan_count > 5:
            score -= 10
        if total_emis > 0 and (on_time_emis / total_emis) < 0.75:
            score -= 20
        if current_year_loans > 2:
            score -= 10
        if loan_volume > customer.approved_limit * 1.5:
            score -= 15

        return max(0, round(score))
    except Exception as e:
        # Optionally log error
        return 0


def calculate_emi(principal, annual_interest_rate, tenure_months):
    try:
        R = annual_interest_rate / 12 / 100
        N = tenure_months
        if R == 0:
            return round(principal / N, 2)
        EMI = (principal * R * math.pow(1 + R, N)) / (math.pow(1 + R, N) - 1)
        return round(EMI, 2)
    except Exception as e:
        # Optionally log error
        return 0


def checkEligibilityService(data):
    try:
        customer_id = data.get("customer_id")
        loan_amount = float(data.get("loan_amount"))
        interest_rate = float(data.get("interest_rate"))
        tenure = int(data.get("tenure"))

        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            raise Exception("Customer not found")
        credit_score = calculate_credit_score(customer_id)

        approval = False
        corrected_interest_rate = interest_rate

        loans = Loan.objects.filter(customer=customer)
        existing_emis = sum(loan.monthly_installment for loan in loans)
        max_allowed_emis = customer.monthly_income * 0.5

        if credit_score > 50:
            approval = True
        elif credit_score > 30 and interest_rate > 12:
            approval = True
        elif credit_score > 10 and interest_rate > 16:
            approval = True

        if credit_score <= 10 or existing_emis > max_allowed_emis:
            approval = False

        if credit_score > 50 and interest_rate < 10:
            corrected_interest_rate = 10
        elif credit_score > 30 and interest_rate < 12:
            corrected_interest_rate = 12
        elif credit_score > 10 and interest_rate < 16:
            corrected_interest_rate = 16

        monthly_payment = calculate_emi(loan_amount, corrected_interest_rate, tenure)

        return {
            "customer_id": customer_id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_interest_rate,
            "tenure": tenure,
            "monthly_payment": monthly_payment,
        }
    except Exception as e:
        return {"error": str(e)}
