import decimal

def user_directory_path(instance, filename):
    return "uploads/user_{0}/{1}".format(instance.owner.id, filename)

def get_min_bid(listing):
    if listing.bids.count() == 0:
        return listing.start_price
    digits = len(str(int(listing.price)))
    if digits > 2:
        return listing.price + decimal.Decimal(10 ** digits / 100)
    return listing.price + decimal.Decimal(1)