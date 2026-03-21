'''
Plan for online negotiations page "session"
lender create save session where he and and borrower can negotiate loan terms
user find another people in server if true it create session with him 
session status - pendig, until borrower agreed and opend it too,

inside session
lender fill the form andd send loan setiings to borrower,and borrower  could agreed or negotiate
by changing loan settings
loan settings:
loan amount (input field)
loan days ( canbe used integer or calculated by date picker) ( input field)
retrun amount ( input fieldp)

buttons
lender (
date picker for loan due date,
resend ( default not active , active if user filed all forms, send loan details to borrower),
OK (default not active, active after borrower send changed loan terms),
cancel ( if lender decide to leave , kills all session, and status = canceld),
create contract ( default not active, only if borrower agreed)
)

borrower (
date picker for loan due date,
resend ( default not active , active if user filed all forms, send loan details to borrower),
OK (default not active, active after borrower send changed loan terms),
cancel ( if lender decide to leave , kills all session, and status = canceld),

)

'''