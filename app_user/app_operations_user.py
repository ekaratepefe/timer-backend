from app_user.models import Payment


class UserOperations:
    @staticmethod
    def process_payment(payment_data, user):
        """
        Process the payment to upgrade the user's status to premium.

        Args:
            payment_data (dict): A dictionary containing payment details.
            user (User): The user object that is being upgraded.

        Returns:
            bool: True if the payment processing is successful and the user is upgraded to premium.
        """
        # Payment processing logic would go here (to be implemented later).

        # Assuming payment processing is successful, upgrade the user to premium.
        user.is_premium = True
        user.save()
        return True

    @staticmethod
    def revoke_premium(user):
        """
        Revoke the premium status of the user.

        Args:
            user (User): The user object whose premium status is being revoked.

        Returns:
            bool: True if the user's premium status is successfully revoked.
        """
        # Revoke the user's premium status.
        user.is_premium = False
        user.save()
        return True


