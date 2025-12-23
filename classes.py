# Assumptions:
    # Integer value price, quantity
    # Time will also be an integer from 0-23, representing hours
    # Insertions follow chronological order


# Order book class
    # stores bids and offers
    # method to add Order object and execute any possible trades
    # method to show current bids and offers

class OrderBook:

    def __init__(self):
        self.bids = []
        self.offers = []
        self.history = []
    
    def add_order(self, new_order: Order):

        if new_order.order_type == 'bid':
            # first execute any possible trades
            new_order = self.execute_bid(new_order)
            if new_order:
                # proper insertion logic, by price then time
                # loop by price -> order should be high to low
                for i in range(len(self.bids)):
                    if new_order.price > self.bids[i].price:
                        self.bids.insert(i, new_order)
                        self.history.append(f"New bid inserted! | Time: {new_order.time} | Price: {new_order.price} | Quantity: {new_order.quantity}")
                        return None
                
                # if loop finishes without return, the new bid is at the end
                self.bids.append(new_order)
                self.history.append(f"New bid inserted! | Time: {new_order.time} | Price: {new_order.price} | Quantity: {new_order.quantity}")
                return None
                
        else:
            # first execute any possible trades
            new_order = self.execute_offer(new_order)
            if new_order:
                # proper insertion logic, by price then time
                # loop by price -> order should be low to high
                for i in range(len(self.offers)):
                    if new_order.price < self.offers[i].price:
                        self.offers.insert(i, new_order)
                        self.history.append(f"New offer inserted! | Time: {new_order.time} | Price: {new_order.price} | Quantity: {new_order.quantity}")
                        return None
            
            # if loop finishes without return, the new offer is at the end
            self.offers.append(new_order)
            self.history.append(f"New offer inserted! | Time: {new_order.time} | Price: {new_order.price} | Quantity: {new_order.quantity}")
            return None
                
    
    def execute_bid(self, new_order: Order) -> Order:
        """
        Return partial bid, if any
        """
        i = 0
        while i < len(self.offers): # assumes that offers are properly sorted by price-time priority
            offer = self.offers[i]
            if offer.price <= new_order.price:
                # here, the valid offer is the resting order; thus trade executes at the offer's price
                
                execution_price = offer.price
                execution_quantity = min(offer.quantity, new_order.quantity)
                self.history.append(f"Trade completed! | Time: {new_order.time} | Price: {execution_price} | Quantity: {execution_quantity}")
                
                # Resolve quantities

                if new_order.quantity == offer.quantity:
                    # delete bid and offer here
                    self.offers.pop(i)
                    return None # the bid is now nothing
                
                elif new_order.quantity > offer.quantity:
                    # now, check the new bid with reduced quantity against other resting offers
                    self.offers.pop(i)
                    new_order.quantity -= execution_quantity
                
                else: 
                    # this means delete bid, reduce offer quantity
                    self.offers[i].quantity -= execution_quantity
                    return None
            else:
                break
        
        # if the bid is not compatible with any resting offers, return the bid with (changed) quantity
        return new_order


    def execute_offer(self, new_order: Order) -> Order:
        """
        Return partial offer, if any
        """
        i = 0
        while i < len(self.bids): # assumes that offers are properly sorted by price-time priority
            bid = self.bids[i]
            if bid.price >= new_order.price:
                # here, the valid bid is the resting order; thus trade executes at the bid's price
                
                execution_price = bid.price
                execution_quantity = min(bid.quantity, new_order.quantity)
                self.history.append(f"Trade completed! | Time: {new_order.time} | Price: {execution_price} | Quantity: {execution_quantity}")
                
                # Resolve quantities

                if new_order.quantity == bid.quantity:
                    # delete bid and offer here
                    self.bids.pop(i)
                    return None # the offer is now resolved
                
                elif new_order.quantity > bid.quantity:
                    # now, check the new bid with reduced quantity against other resting offers
                    self.bids.pop(i)
                    new_order.quantity -= execution_quantity
                
                else: 
                    # this means delete bid, reduce offer quantity
                    self.bids[i].quantity -= execution_quantity
                    return None
            else:
                break
        
        # if the offer is not compatible with any resting bids, return the offer with (changed) quantity
        return new_order
    
    def show_history(self):
        for event in self.history:
            print(event)

# Order class
    # type = "bid" or "offer"
    # price
    # quantity
    # time

class Order:

    def __init__(self, order_type: str, price: int, quantity: int, time: int):
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.time = time
