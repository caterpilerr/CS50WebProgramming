import decimal

def user_directory_path(instance, filename):
    return "uploads/user_{0}/{1}".format(instance.owner.id, filename)

def get_bid_increment(listing):
    if listing.bids.count() == 0:
        return decimal.Decimal(0)
    digits = len(str(int(listing.price)))
    if digits > 2:
        return decimal.Decimal(10 ** digits / 100)
    return decimal.Decimal(1)
