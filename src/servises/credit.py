
# creating credit class with the loan divided into small periodic payment where commission taken every payment
'''
My plan is to make a full loan experience
created funcrions :
standart credit periodic payment
baloon payment
crditt schedule
credit details ( current interest , current debt, initial loan amount, APR, current loan cost, current commission, current profit)
functions to add :
early loan repayment ( what if client whant to close credir early, what amount should he pay to close a loan?  )
loan closig function  ( when credit repayed credit status "closed" )
'''

# creating a credot class with simple compuunding 
class CreditS:
    def __init__(self, lender, borrower , N, P0, P, loan_id, loan_due_date = None, commission = 0.2): 
        self.lender = lender # who gives money
        self.borrower = borrower  # who get money
        self.status ='active' # loan  is open and cane be closed
        self.loan_id = loan_id #loan id 
        self.N = N          # N- number of periods 
        self.P0 = P0        #P0 - intitial amount money to lend,
        self.P = P          #P - expected return at the end of a loan,
        self.loan_due_date = loan_due_date # when return money date
        self.loan_amount = self.P0 + self.P
        
        self.commission = commission
    
        if self.P <= 0:  # if loan at 0% per year only our commission applied
            self.commission = 1
            self.P = P0 * 0.2 # our commission became expecter return at the end of  a loan

        
        self.R = (((self.P + self.P0)/self.P0) - 1) / self.N
        self.APR = round(self.R * 360, 2)
        self.payment_amount = self.P0 * (1 + self.R * self.N) # calculated amount to pay at the end of a loan
        self.balance = self.loan_balance() # loan balance to see how interest adjusted
        

        self.remaining_principal = self.P0
        self.remaining_interest = self.P
        self.current_debt = self.remaining_principal + self.remaining_interest
    
 
    # pay day loan balance
    def loan_balance(self):
        balance = []

        for period in range( 1, self.N +1):
            principal = self.P0
            interest = round(self.P0 *(self.R * period), 2)
            debt = principal + interest
            period_commission = round( interest * self.commission,2)
            period_profit = interest - period_commission
            balance.append({
                'Principal' : principal,
                'Interest' : interest,
                'Debt' : debt,
                'Commission': period_commission,
                'Profit' : period_profit
            })
        return balance 
        #0,0625
        # 200 + 12,6
        # 200 + 25
        # 200 + 37.5
        # 200 + 50
    
# repaying credit proccess
    def repay_credit(self , amount):
        
        if self.status == 'closed':
            return f" This loan is already repayed , details:\n{self.show_credit_details()}"
        if amount < 0:
            return 'Payment must be positive'
        payment = amount
        # paynig interest first
        if self.remaining_interest > 0:
            if self.remaining_interest <= payment:
                payment -= self.remaining_interest
                self.remaining_interest = 0
            else:
                self.remaining_interest -= payment
                payment = 0
        # paying principal 
        if payment > 0 and self.remaining_principal > 0:
            if payment > self.remaining_principal:
                payment -= self.remaining_principal
                self.remaining_principal = 0
            else:
                self.remaining_principal -= payment
                payment = 0
        # updating credit debt
        self.current_debt = self.remaining_interest + self.remaining_principal
        if self.current_debt == 0:
            self.status = 'closed'
            
        return f'This loan repayed successfully:\n {self.show_credit_details()}'


    def credit_details(self):

        return{
            'Borrower' : self.borrower.user_name,
            'LoanId' :self.loan_id,
            'Status' : self.status,
            'IntitialPrincipal' : self.P0,
            'RemainingPrincipal' : round(self.remaining_principal,2),
            'RemainingInterest' : round(self.remaining_interest,2),
            'TotalDebt' : round(self.current_debt, 2),
            'APR' : self.APR,
            'Days' : self.N,
            'Commission' : self.commission * self.remaining_interest,
            'Profit' : self.remaining_interest - (self.commission * self.remaining_interest),
            'Loan_due_date' : self.loan_due_date
           
        }
        
    


    
    def borrower_view(self): # to show how much loan you got and more total details
        details = self.credit_details()
        return {
            'Lender' : self.lender.user_name, # to whom you owe money
            'AmountGet' : details['TotalDebt'], #what amount you get
            'Interest' : details['RemainingInterest'],
            'Days' : details['Days'], # for how much days
            'Repay' : details['RemainingInterest'] + details['RemainingPrincipal'], #what amount to return
            'Status' : details['Status'], #current status of a loan
            'LoanId' : details['LoanId'],   #loan id to repay
        }
    
    def lender_view(self):
        details = self.credit_details()
         #to see how much money you lend, to whom and etc
        return {
            'Borrower' : self.borrower.user_name,
            'AmountLent' : details['TotalDebt'], #what amount you lend
            'Days' : details['Days'], # for how much days
            'ExpectedReturn' : details['RemainingInterest'] + details['RemainingPrincipal'], #what amount expected to get
            'Commission' : details['Commission'],
            'Profit' : details['Profit'],
            'Status' : details['Status'], #current status of a loan
            'LoanId' : details['LoanId'],   #loan id to repay 
        }
     
    
 