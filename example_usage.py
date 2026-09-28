from client import ShamirSecretSharing

def main():
    secret = 0xCAFEBABEF00D
    shares = ShamirSecretSharing.split(secret, k=3, n=5)
    print("Generated 5 shares. Subset (shares 0, 2, 4):")
    subset = [shares[0], shares[2], shares[4]]
    recovered = ShamirSecretSharing.recover(subset)
    print("Recovered:", hex(recovered))
    assert recovered == secret

if __name__ == "__main__":
    main()
