import argparse
import math

parser = argparse.ArgumentParser(description='The program calculates different types of loans \
and their parameters after entering the appropriate data.')
parser.add_argument('--type', choices=['annuity', 'diff'], help='annuity - annuity payment; \
                        diff - differentiated payments')
parser.add_argument('--periods')
parser.add_argument('--principal')
parser.add_argument('--interest', help="Must be in annuity payment.")
parser.add_argument('--payment', help="It can't be in differentiated payments.")

# loading the file
# Namespace(
#  interest=<_io.TextIOWrapper name='interest.txt' mode='w' encoding='UTF-8'>,
#  principal=<_io.TextIOWrapper name='principal.txt' mode='r' encoding='UTF-8'>,
#  periods=<_io.TextIOWrapper name='periods.txt' mode='w' encoding='UTF-8'>
# )
commands = []
checking =[]

args = parser.parse_args()  # parse result 'Namespace'
commands = [args.type, args.principal, args.periods, args.interest, args.payment]
for arg in commands:
    if arg is not None:
        checking.append(arg)

class LoanCalculator:

    def __init__(self):
        self.last_installment = 0
        self.loan_principal = int(commands[1]) if commands[1] is not None else 0
        self.interest = float(commands[3]) if commands[3] is not None else 0
        self.n_of_periods = int(commands[2]) if commands[2] is not None else 0
        self.annuity_payment = int(commands[4]) if commands[4] is not None else 0
        self.year = 0
        self.overpayment = 0
        self.diff_overpayment = 0
        LoanCalculator.menu(self)

    def menu(self):
        if commands[0] == "annuity":
            if len(checking) <= 3:
                print('Incorrect parameters.''One parameter is missing.')
            elif args.interest is None:
                print('Incorrect parameters.'"Interest parameter must be here.")
            elif (self.n_of_periods < 0) or (self.loan_principal < 0) or (self.interest < 0) or (self.annuity_payment < 0):
                print('Incorrect parameters.''The parameter value cannot be negative.')
            elif (self.n_of_periods != 0) and (self.loan_principal != 0) and (self.interest != 0):
                LoanCalculator.interest_rate(self)
                LoanCalculator.annuity_payment(self)
                LoanCalculator.overpayment(self)
                print(f'Your annuity payment = {self.annuity_payment}!')
                print(f'Overpayment = {self.overpayment}')
            elif (self.n_of_periods != 0) and (self.annuity_payment != 0) and (self.interest != 0):
                LoanCalculator.interest_rate(self)
                LoanCalculator.loan_principal_value(self)
                LoanCalculator.overpayment(self)
                print(f'Your loan principal = {self.loan_principal}!')
                print(f'Overpayment = {self.overpayment}')
            elif (self.loan_principal != 0) and (self.annuity_payment != 0) and (self.interest != 0):
                LoanCalculator.interest_rate(self)
                LoanCalculator.n_of_months(self)
                LoanCalculator.months_to_years(self)
                if self.year >= 1:
                    if self.number_of_months == 1:
                        print(
                            f'It will take {self.year} years and {int(self.number_of_months)} months to repay this loan!')
                    elif self.number_of_months == 0:
                        print(
                            f'It will take {self.year} years to repay this loan!')
                    else:
                        print(
                            f'It will take {self.year} years and {int(self.number_of_months)} months to repay this loan!')
                else:
                    if self.number_of_months == 1:
                        print(f'It will take {int(self.number_of_months)} month to repay the loan!')
                    else:
                        print(f'It will take {int(self.number_of_months)} months to repay the loan!')
                LoanCalculator.overpayment_2(self)
                print(f'Overpayment = {self.overpayment}')

        elif commands[0] == "diff":
            if len(checking) <= 3:
                print('Incorrect parameters.''One parameter is missing.')
            elif args.payment is not None:
                print('Incorrect parameters.'"Payment parameter can't be here.")
            elif (self.n_of_periods < 0) or (self.loan_principal < 0) or (self.interest < 0):
                print('Incorrect parameters.''The parameter value cannot be negative.')
            elif (self.n_of_periods != 0) and (self.loan_principal != 0) and (self.interest != 0):
                LoanCalculator.interest_rate(self)
                LoanCalculator.diff_payment(self)
                LoanCalculator.overpayment(self)
                print(f'\nOverpayment = {self.overpayment}')

        else:
            print('Incorrect parameters.'"No loan type selection.")

    def interest_rate(self):  # calculation of interest - i
        self.interest_value = float((self.interest / 100) / (12 * 1))  # X% and 100%
        return self.interest_value

    def annuity_payment(self):  # calculating the annuity payment - A
        numeral = float(self.interest_value * ((1 + self.interest_value) ** self.n_of_periods))
        denominator = float(((1 + self.interest_value) ** self.n_of_periods) - 1)
        self.annuity_payment = math.ceil(self.loan_principal * (numeral / denominator))
        return self.annuity_payment

    def loan_principal_value(self):  # calculating the loan principal - P
        numeral = float(self.interest_value * (1 + self.interest_value) ** self.n_of_periods)
        denominator = float(((1 + self.interest_value) ** self.n_of_periods) - 1)
        self.loan_principal = math.floor(float(self.annuity_payment / (numeral / denominator)))
        return self.loan_principal

    def n_of_months(self):  # calculating the number of payments logarithm - n
        numeral = float(self.annuity_payment)
        denominator = float(self.annuity_payment - (self.interest_value * self.loan_principal))
        log_base = float(1 + self.interest_value)
        self.number_of_months = math.floor(math.log((numeral / denominator), log_base))
        return self.number_of_months

    def months_to_years(self):  # change of months into years
        if self.number_of_months >= 12:
            self.year = math.floor(self.number_of_months / 12)
            self.number_of_months = math.ceil(self.number_of_months % 12)
        else:
            self.number_of_months = math.ceil(self.number_of_months % 12)
        return self.year, self.number_of_months

    def diff_payment(self):
        self.diff_overpayment = 0
        for m in range(1, int(self.n_of_periods) + 1):
            numeral = self.loan_principal * ( m - 1)
            diff_payment = math.ceil((self.loan_principal / self.n_of_periods) + self.interest_value * (self.loan_principal - (numeral / self.n_of_periods)))
            print(f'Month {m}: payment is {diff_payment}')
            self.diff_overpayment += diff_payment
        print(self.diff_overpayment)
        return self.diff_overpayment

    def overpayment(self):
        if commands[0] == "annuity":
            self.overpayment = math.ceil((self.annuity_payment * self.n_of_periods) - self.loan_principal)
        elif commands[0] == "diff":
            self.overpayment = math.ceil(self.diff_overpayment - self.loan_principal)
        return self.overpayment

    def overpayment_2(self):
        if self.year > 0:
            additiona_months = self.year * 12
            self.number_of_months = self.number_of_months + additiona_months
        self.overpayment = int(math.fabs(self.loan_principal - (self.number_of_months * self.annuity_payment)))
        return self.overpayment


customer = LoanCalculator()