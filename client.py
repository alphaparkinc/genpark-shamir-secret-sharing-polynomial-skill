"""Shamir's (k, n) Threshold Secret Sharing.
100% Python Standard Library.
"""

import secrets

class ShamirSecretSharing:
    """Threshold secret sharing splitting secret into n shares, reconstructable with any k shares."""
    PRIME = 2**256 - 189

    @classmethod
    def split(cls, secret: int, k: int, n: int) -> list:
        coeffs = [secret] + [secrets.randbelow(cls.PRIME - 1) + 1 for _ in range(k - 1)]
        shares = []
        for x in range(1, n + 1):
            y = 0
            x_pow = 1
            for a in coeffs:
                y = (y + a * x_pow) % cls.PRIME
                x_pow = (x_pow * x) % cls.PRIME
            shares.append((x, y))
        return shares

    @classmethod
    def recover(cls, shares: list) -> int:
        secret = 0
        k = len(shares)
        for i in range(k):
            xi, yi = shares[i]
            num = 1
            den = 1
            for j in range(k):
                if i != j:
                    xj, _ = shares[j]
                    num = (num * (-xj)) % cls.PRIME
                    den = (den * (xi - xj)) % cls.PRIME
            inv_den = pow(den, cls.PRIME - 2, cls.PRIME)
            li = (num * inv_den) % cls.PRIME
            secret = (secret + yi * li) % cls.PRIME
        return secret
