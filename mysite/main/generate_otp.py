import pyotp


class HandleOTP():
    def __init__(self):
        self.totp = pyotp.TOTP('base32secret3232', interval=120)

    def generate_otp(self):
        otp = self.totp.now()
        return otp

    def verify_otp(self, otp):
        return self.totp.verify(otp)
