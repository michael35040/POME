'''
Created on Mar 20, 2013

@author: Ash Booth

Not sure if to use decimal or to just mulitply integer to prevent rounding errors
http://stackoverflow.com/questions/20354423/clarification-on-the-decimal-type-in-python
just multiply the integer and add decimal on view (i.e. 1 integer is $0.01 and 100 is $1.00)
'''

class Order(object):
'''
Orders represent the core piece of the exchange. Every bid/ask is an Order.
Orders are doubly linked and have helper functions (next_order, prev_order)
to help the exchange fullfill orders with quantities larger than a single
existing Order.
'''
    def __init__(self, quote, orderList):
        self.timestamp = int(quote['timestamp']) # integer representing the timestamp of order creation
        self.qty = int(quote['qty'])  # integer representing amount of thing - can be partial amounts
        self.price = quote['price'] # representing price (currency)
        self.idNum = quote['idNum'] # order ID
        self.tid = quote['tid'] # trade ID
         # doubly linked list to make it easier to re-order Orders for a particular price point
        self.nextOrder = None
        self.prevOrder = None
        self.orderList = orderList

     # helper functions to get Orders in linked list        
    def nextOrder(self):
        return self.nextOrder
    def prevOrder(self):
        return self.prevOrder
    
    def updateQty(self, newQty, newTimestamp):
        if newQty > self.qty and self.orderList.tailOrder != self:
            # Move order to end of the tier (loses time priority)  
            # check to see that the order is not the last order in list and the quantity is more
            self.orderList.moveTail(self) # move to the end
        self.orderList.volume -= (self.qty - newQty)  # update volume
        self.timestamp = newTimestamp
        self.qty = newQty

    def __str__(self):
        return "%s\t@\t%.4f\tt=%d" % (self.qty, self.price, self.timestamp)
        #could also do:
        #return "Order: Price - %s, Quantity - %s, Timestamp - %s" % (self.price, self.qty, self.timestamp)
