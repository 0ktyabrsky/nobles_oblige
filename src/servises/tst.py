from user import User as us
maro = us(user_id = '88', user_name = "Maro")
lola = us(user_id = '44', user_name = 'Lola')
maro.lend_money_short(
    400, 5,100, lola
)
maro.lend_money_short(
    200,
    5,
    50,
    lola
)

    
lola.lend_money_short(400,3,20,maro)

data = maro.given_loans[0].credit_details()
loan_amount = data[0]['Loan amount']
loan_id = data[0]['LoanId']
debt = data[0]['Debt']
total_interest = data[0]['Interest']
total_profit = data[0]['Profit']
# print(loan_id, loan_amount, debt,total_interest)
total_lend = 0


def load_contracts(user):
    for loan in user.given_loans:

        return loan.credit_details()
list_loans = load_contracts(maro)



l_s = maro.given_loans



print(maro.info())

