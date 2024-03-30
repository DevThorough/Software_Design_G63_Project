def fuelPrice(gallons, hasHistory, state):
    if gallons < 0:
        raise ValueError("Gallons can not be negative.")
    rate = 3.99
    if hasHistory == True:
        ## Apply discount
        rate = 3.50
    price = rate * gallons
    if state == "TX":
        price += 5.00
    else:
        price += 15.00 ## Out of state shipping
    return price