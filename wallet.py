import datetime

class Wallet:
    def __init__(self, n_keys, k_threshold, delay_hours=24):
        self.n_keys = n_keys
        self.k_threshold = k_threshold
        self.delay_hours = delay_hours
        self.pending_withdrawals = []  # Store pending withdrawal requests

    def order_withdrawal(self, number_of_keys):
        if number_of_keys > self.n_keys:
            raise ValueError("Number of keys exceeds total wallet keys")

        # Create a new withdrawal request
        withdrawal_request = {
            "keys": number_of_keys,
            "timestamp": datetime.datetime.now(),
            "status": "pending"
        }

        # Update pending withdrawals:
        self.manage_pending_withdrawals(withdrawal_request)

    def manage_pending_withdrawals(self, new_request):
        for pending in self.pending_withdrawals:
            if new_request['keys'] > pending['keys']:
                # Cancel lower key request
                pending['status'] = "cancelled"

            elif new_request['keys'] == self.n_keys:
                # If full threshold, execute all pending and clear
                for withdrawal in self.pending_withdrawals:
                    self.execute_withdrawal(withdrawal)  # Replace with actual transaction logic
                self.pending_withdrawals = []
                return

        # Add the new request to the list
        self.pending_withdrawals.append(new_request)

        # Schedule expiration for delayed withdrawals
        self.schedule_expiration(new_request)

    def schedule_expiration(self, request):
        expiration = request['timestamp'] + datetime.timedelta(hours=self.delay_hours)

        # ... (Implement a task scheduler to execute withdrawal after expiration
        #      or mark as "expired")

    def execute_withdrawal(self, withdrawal):
        # ... (Implement the actual withdrawal logic: transfer funds,
        #      interact with blockchain, etc.)
        print("Withdrawal executed with keys:", withdrawal['keys'])

# # Example usage
# my_wallet = Wallet(n_keys=5, k_threshold=3)  # Wallet with 5 keys, requiring 3 for withdrawal
#
# my_wallet.order_withdrawal(2)  # Order a withdrawal with 2 keys (delayed)
# my_wallet.order_withdrawal(4)  # Order with 4 keys, cancels previous, but still delayed
# my_wallet.order_withdrawal(5)  # Order with 5 keys, executes all pending immediately

