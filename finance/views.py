from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import (
    DailyRecord,
    Earning,
    Expenditure,
    ExpenseCategory
)
import json


# =========================
# EDIT SALARY
# =========================
@login_required
def edit_salary(request):

    if request.method == "POST":
        request.user.monthly_salary = request.POST['salary']
        request.user.save()
        return redirect('dashboard')

    return render(request, 'finance/edit_salary.html')


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):

    user = request.user

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    records = DailyRecord.objects.filter(user=user)

    if from_date and to_date:
        records = records.filter(date__range=[from_date, to_date])

    earnings = Earning.objects.filter(
        record__in=records
    ).order_by("-record__date")

    expenses = Expenditure.objects.filter(
        record__in=records
    ).order_by("-record__date")

    # -------------------------
    # BASIC CALCULATIONS
    # -------------------------
    additional_income = earnings.aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = expenses.aggregate(total=Sum("amount"))["total"] or 0

    salary = 0
    total_earnings = additional_income
    balance = additional_income - total_expenses

    if not user.is_daily_waged:
        salary = float(user.monthly_salary)
        total_earnings = salary + additional_income
        balance = total_earnings - total_expenses

    # -------------------------
    # CATEGORY BREAKDOWN
    # -------------------------
    category_summary = {}

    for expense in expenses:
        if expense.category:
            name = expense.category.name
            category_summary[name] = category_summary.get(name, 0) + float(expense.amount)

    # -------------------------
    # ANALYTICS
    # -------------------------
    expense_labels = list(category_summary.keys())
    expense_values = list(category_summary.values())

    max_expense = expenses.order_by("-amount").first()
    min_expense = expenses.order_by("amount").first()

    max_earning = earnings.order_by("-amount").first()
    min_earning = earnings.order_by("amount").first()

    
    daily_income = {}
    daily_expense = {}

    for e in earnings:
        d = str(e.record.date)
        daily_income[d] = daily_income.get(d, 0) + float(e.amount)

    for e in expenses:
        d = str(e.record.date)
        daily_expense[d] = daily_expense.get(d, 0) + float(e.amount)

    all_dates = sorted(set(list(daily_income.keys()) + list(daily_expense.keys())))

    income_chart = [daily_income.get(d, 0) for d in all_dates]
    expense_chart = [daily_expense.get(d, 0) for d in all_dates]

    expense_labels = []
    expense_values = []

    for category, amount in category_summary.items():
        expense_labels.append(category)
        expense_values.append(float(amount))


# ✅ ADD THIS BLOCK HERE (IMPORTANT)
    earning_labels = []
    earning_values = []

    for e in earnings:
        earning_labels.append(e.title)
        earning_values.append(float(e.amount))

    # -------------------------
    # CONTEXT (FIXED)
    # -------------------------
    context = {
        "earnings": earnings,
        "expenses": expenses,

        "salary": salary,
        "additional_income": additional_income,

        "total_earnings": total_earnings,
        "total_expenses": total_expenses,
        "balance": balance,

        "category_summary": category_summary,

        "from_date": from_date,
        "to_date": to_date,

        # charts
        "expense_labels": json.dumps(expense_labels),
        "expense_values": json.dumps(expense_values),

        "chart_dates": json.dumps(all_dates),
        "income_chart": json.dumps(income_chart),
        "expense_chart": json.dumps(expense_chart),

        "earning_labels": json.dumps(earning_labels),
        "earning_values": json.dumps(earning_values),

        # analytics cards
        "max_expense": max_expense,
        "min_expense": min_expense,
        "max_earning": max_earning,
        "min_earning": min_earning,
    }

    return render(request, "finance/dashboard.html", context)


# =========================
# ADD EARNING
# =========================
def add_earning(request):

    if request.method == "POST":

        selected_date = request.POST["date"]

        record, _ = DailyRecord.objects.get_or_create(
            user=request.user,
            date=selected_date
        )

        Earning.objects.create(
            record=record,
            title=request.POST["title"],
            client_name=request.POST["client_name"],
            location=request.POST["location"],
            amount=request.POST["amount"],
            description=request.POST.get("description", "")
        )

        return redirect("dashboard")

    return render(request, "finance/add_earning.html")


# =========================
# ADD EXPENSE
# =========================
def add_expense(request):

    if request.method == "POST":

        selected_date = request.POST["date"]

        record, _ = DailyRecord.objects.get_or_create(
            user=request.user,
            date=selected_date
        )

        category_name = request.POST["category"]

        if category_name == "Custom":
            category_name = request.POST.get("custom_category")

        category, _ = ExpenseCategory.objects.get_or_create(
            user=request.user,
            name=category_name
        )

        Expenditure.objects.create(
            record=record,
            title=request.POST["title"],
            category=category,
            location=request.POST["location"],
            amount=request.POST["amount"],
            description=request.POST.get("description", "")
        )

        return redirect("dashboard")

    return render(request, "finance/add_expense.html")


# =========================
# VIEW EARNING
# =========================
def view_earning(request, id):

    earning = get_object_or_404(Earning, id=id)

    if earning.record.user != request.user:
        return redirect("dashboard")

    return render(request, "finance/view_earning.html", {
        "earning": earning
    })


# =========================
# VIEW EXPENSE
# =========================
def view_expense(request, id):

    expense = get_object_or_404(Expenditure, id=id)

    if expense.record.user != request.user:
        return redirect("dashboard")

    return render(request, "finance/view_expense.html", {
        "expense": expense
    })


# =========================
# EDIT EARNING
# =========================
def edit_earning(request, id):

    earning = get_object_or_404(Earning, id=id)

    if earning.record.user != request.user:
        return redirect("dashboard")

    if request.method == "POST":

        earning.title = request.POST["title"]
        earning.client_name = request.POST["client_name"]
        earning.location = request.POST["location"]
        earning.amount = request.POST["amount"]
        earning.description = request.POST.get("description", "")
        earning.save()

        return redirect("dashboard")

    return render(request, "finance/edit_earning.html", {
        "earning": earning
    })


# =========================
# EDIT EXPENSE
# =========================
def edit_expense(request, id):

    expense = get_object_or_404(Expenditure, id=id)

    if expense.record.user != request.user:
        return redirect("dashboard")

    if request.method == "POST":

        category_name = request.POST.get("category")

        if category_name == "Custom":
            category_name = request.POST.get("custom_category")

        category, _ = ExpenseCategory.objects.get_or_create(
            user=request.user,
            name=category_name
        )

        expense.title = request.POST["title"]
        expense.category = category
        expense.location = request.POST["location"]
        expense.amount = request.POST["amount"]
        expense.description = request.POST.get("description", "")
        expense.save()

        return redirect("dashboard")

    categories = ExpenseCategory.objects.filter(user=request.user)

    return render(request, "finance/edit_expense.html", {
        "expense": expense,
        "categories": categories
    })


# =========================
# DELETE EARNING
# =========================
def delete_earning(request, id):

    earning = get_object_or_404(Earning, id=id)

    if earning.record.user == request.user:
        earning.delete()

    return redirect("dashboard")


# =========================
# DELETE EXPENSE
# =========================
def delete_expense(request, id):

    expense = get_object_or_404(Expenditure, id=id)

    if expense.record.user == request.user:
        expense.delete()

    return redirect("dashboard")