
from . import credit
from servises.user_servises import get_or_create_user , update_balance
from servises.loan_services import insert_loan 

class User:
    def __init__(self, user_id, user_name, user_phone,balance = 1000):
        self.user_id = user_id
        self.user_name = user_name
        self.balance = balance
        self.user_phone = user_phone

        
        # given loans for creditor to see profit, commission etc
        # taken loan for debtor to see interest rate, periodic payment, schedule etc
        self.taken_loans = []
        self.given_loans = []
      
        
    # sending data to db after creating a user class
    @classmethod
    async def from_phone(cls , name, phone):
        record = await get_or_create_user(name, phone)
        return cls(user_phone = record['phone_number'], user_name = record['name'] ,user_id = record['id'])


    
    def info(self): # this will return all info about user : name, id , balance, debit, credit etc
        info = {}
        total_lent = 0
        total_debt = 0
        total_repay = 0
        n_contracts = 0
        
        total_profit = 0
        total_interest = 0
        for contract in self.given_loans:
            
            total_lent += contract.P0
            total_repay += contract.P
            total_profit += contract.credit_details()['Profit']

         # credit amount
        
    
        for loan in self.taken_loans:
            
            total_debt += loan.current_debt
            total_interest += loan.remaining_interest
        
        info  = {
            'UserId' : self.user_id,
             'UserName': self.user_name,
             'Balance': self.balance,
             'Total_lent' : total_lent,
             'ExpectedReturn' : total_profit,
             'Margin': total_repay,
             'ContractNumber' : n_contracts,
             'TotalContracts' : len(self.given_loans),
            'TotalDebt' : round(total_debt,2),
            'TotalInterest' : round(total_interest,2),
            'LoanNumber' : len(self.taken_loans)
             
             }
        print()

        return info
    #showing user's info :balance, id, etc
    
    
    # sending money function
    def transaction(self, amount, reciever):
        if amount > self.balance:
            return f"Error: {self.user_name} have balance less than {amount} to transfer money to {reciever.user_name}, {self.user_name}'s balance: {self.balance}"
        else:
            self.balance -= amount
            reciever.balance += amount
            return(
            f" { amount} som tranfser from {self.user_name} to {reciever.user_name} successfuly. "
            f"{self.user_name} balance {self.balance} "
            f" {reciever.user_name} balance {reciever.balance}"
            )
        
    # function to repay debt
         




    # function lend money, expected attributes: create a loan, add loan to the user balance
    async def lend_money_short(self, amount, term, repay, debtor, loan_due_date, loan_session_id): # what amount, for what period, and to whom you lend money
        if amount > self.balance:
            return "You don't have enough money"
        # moving money from person to person
        self.balance -= amount
        debtor.balance += amount


        #creating a loan
        loan = credit.CreditS(
            lender = self, 
            borrower = debtor,
            P0 = amount,
            N = term,
            P = repay,
            loan_id = f"{self.user_id}-{debtor.user_id}-{amount}-{term}-{repay}",
            loan_due_date = loan_due_date
        )

        #registering a loan
        self.given_loans.append(loan)
        debtor.taken_loans.append(loan)
        print(loan.credit_details())
        # presist in db (updating balance , inserting loans)
        await update_balance(self.user_id, self.balance)
        await update_balance(debtor.user_id, debtor.balance)
        await insert_loan(
            lender_id = self.user_id,
            borrower_id = debtor.user_id,
            loan_amount = amount,
            days = term,
            return_amount = repay,
            due_date = loan_due_date,
            session_id = loan_session_id
            
        )

        return ("Contract created succesfully!")
        
    # function to show every credit that user has and and all credit details, so it should looks like that: credits>>>credit>>>credit_details
    #def show_taken_loans(self):
        

    def repay_debt(self, amount, loan_id):
        if amount > self.balance:
             return f" not enough balance"
         
         
        for loan in self.taken_loans:
            
            print(f'Searching loan id { loan.loan_id}')
            if loan.loan_id ==loan_id: # we are looking for exact loan by loan id
                print(loan.loan_id)

                if loan.status == 'closed': # and checking if that loan is already closed
                    return f" This loan {loan.loan_id}is already repayed " # if closed than return that is closed
                else:
                    if amount < loan.payment_amount:
                        return f" not enoungh money to repay debt, your debt is: {loan.payment_amount}"
                    else:
                        self.balance -=amount # substracting repayment amount from user's balance
                        loan.repay_credit(amount) # substracting repayment amount from user's liabilities
                        return f" This loan to {loan.lender.user_name} repayed successfully!"
            
            
                        
        return f' no such credit with that loan_id'
    



'''
Docstring for project_2.test_my
The goal is to make a simulation of:
1) money transfering ---- done
2) money lending --- done
3) loan repayment

the second step:
1) auto loan repayment
2) early repayment

'''
'''
Every user can transfer, lend each other money, but only if there is enough balance and, so
1) check balance 
2) do action

after one user lend to another user,
every transfer from that another user wold firstly check for liabilities (credit) if so, that amount will repay that liability and remainder of that transaction will top up balance

'''