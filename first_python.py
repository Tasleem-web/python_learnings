import sys
import time

class ATM_Operation:
    def __init__(self, initial_atm_cash=50000):
        self.atm_cash_reserve = initial_atm_cash
        self.user_balance = 1000
        
    def main(self):
        # Using a loop keeps the menu running safely until the user quits
        while True:
            print("\nPlease enter a number to perform the operations...")
            print("""
            1. Cash deposit
            2. Cash withdrawal
            3. Balance Inquiry
            4. Mini statements
            5. Quit
            """)
            
            try:
                user_input = int(input("Selection: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            match user_input:
                case 1:
                    self.cash_deposit()
                case 2:
                    self.cash_withdrawal()
                case 3:
                    self.balance_inquiry()
                case 4: 
                    self.mini_statements()
                case 5:
                    self.exit_program()
                case _:
                    print("Unknown user input. Try again.") 

    def cash_deposit(self):
        print("\n--- Cash Deposit ---")
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Please enter a valid amount.")
                return
            self.user_balance += amount
            print(f"Successfully deposited ${amount:.2f}")
        except ValueError:
            print("Invalid amount entered.")

    def cash_withdrawal(self):
        print("\n--- Cash Withdrawal ---")
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount > self.user_balance:
                print("❌ Error: Insufficient personal funds.")
            elif amount > self.atm_cash_reserve:
                print("❌ Error: ATM out of cash.")
            elif amount <= 0:
                print("Please enter a valid amount.")
            else:
                self.user_balance -= amount
                self.atm_cash_reserve -= amount
                print(f"✅ Success: Please collect ${amount:.2f}")
        except ValueError:
            print("Invalid amount entered.")

    def balance_inquiry(self):
        print("\n--- Balance Inquiry ---")
        print(f"Your current balance is: ${self.user_balance:.2f}")
        
    def mini_statements(self):
        print('\n--- Mini Statement ---')
        print("Feature coming soon! (Track transactions here)")

    def exit_program(self):
        print("\nProgram will self-destruct in 2 seconds...")
        time.sleep(2.0)
        print("Exiting now. Goodbye!")
        sys.exit(0)
        
if __name__ == "__main__":
    # Create the ATM object instance
    atm = ATM_Operation()
    # Call the main loop function
    atm.main()
