import unittest
from wallet import Wallet

class MajorityWalletTests(unittest.TestCase):

    def setUp(self):
        self.wallet = Wallet(n_keys=5, k_threshold=3)

    def test_delayed_withdrawal(self):
        print("Ordering a delayed withdrawal with 2 keys...")
        self.wallet.order_withdrawal(2)
        self.assertEqual(self.wallet.pending_withdrawals[0]["status"], "pending")
        print("Withdrawal status is pending as expected.")

    def test_cancellation(self):
        print("Ordering a withdrawal with 2 keys...")
        self.wallet.order_withdrawal(2)
        print("Ordering a withdrawal with 4 keys, expecting the first to be cancelled...")
        self.wallet.order_withdrawal(4)
        self.assertEqual(self.wallet.pending_withdrawals[0]["status"], "cancelled")
        self.assertEqual(self.wallet.pending_withdrawals[1]["status"], "pending")
        print("Cancellation successful.")

    def test_immediate_execution(self):
        print("Ordering a withdrawal with 2 keys...")
        self.wallet.order_withdrawal(2)
        print("Ordering a withdrawal with 5 keys, expecting immediate execution...")
        self.wallet.order_withdrawal(5)
        # ... Assertions to verify that execute_withdrawal was called for all pending

    def test_invalid_key_count(self):
        print("Attempting a withdrawal with an invalid number of keys...")
        with self.assertRaises(ValueError):
            self.wallet.order_withdrawal(6)

if __name__ == "__main__":
    unittest.main()
