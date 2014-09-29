'''
Created on Mar 22, 2013

@author: Ash Booth
'''

class OrderList(object):
 '''
A doubly linked list of Orders. Used to iterate through Orders when
a price match is found. Each OrderList is associated with a single
price. Since a single price match can have more quantity than a single
Order, we may need multiple Orders to fullfill a transaction. The
OrderList makes this easy to do. OrderList is naturally arranged by time.
Orders at the front of the list have priority.
'''    
    
    def __init__(self):
        self.headOrder = None   # first order in the list
        self.tailOrder = None   # last order in the list
        self.length = 0         # number of Orders in the list
        self.volume = 0         # sum of Order quantity in the list AKA Total share volume
        self.last = None        # helper for iterating 
        
    def __len__(self):
        return self.length
    
    def __iter__(self):
        self.last = self.headOrder
        return self
    
    def next(self):
        '''Get the next order in the list.
        Set self.last as the next order. If there is no next order, stop
        iterating through list.
        '''        
        if self.last == None:
            raise StopIteration
        else:
            returnVal = self.last
            self.last = self.last.nextOrder
            return returnVal
        
    def getHeadOrder(self):
        return self.headOrder
    
    def appendOrder(self, order):
        if len(self) == 0:
            order.nextOrder = None
            order.prevOrder = None
            self.headOrder = order
            self.tailOrder = order
        else:
            order.prevOrder = self.tailOrder
            order.nextOrder = None
            self.tailOrder.nextOrder = order
            self.tailOrder = order
        self.length += 1
        self.volume += order.qty
        
    def removeOrder(self, order):
        self.volume -= order.qty
        self.length -= 1
        if len(self) == 0:  # if there are no more Orders, stop/return
            return
        # Remove from list of orders
        # Remove an Order from the OrderList. First grab next / prev order
        # from the Order we are removing. Then relink everything. Finally
        # remove the Order.        
        nextOrder = order.nextOrder
        prevOrder = order.prevOrder
        if nextOrder != None and prevOrder != None:
            nextOrder.prevOrder = prevOrder
            prevOrder.nextOrder = nextOrder
        elif nextOrder != None: # There is no previous order
            nextOrder.prevOrder = None
            self.headOrder = nextOrder  # The next order becomes the first order in the OrderList after this Order is removed
        elif prevOrder != None:     # There is no next order
            prevOrder.nextOrder = None
            self.tailOrder = prevOrder  # The previous order becomes the last order in the OrderList after this Order is removed
            
    def moveTail(self, order):
    '''After updating the quantity of an existing Order, move it to the tail of the OrderList
    Check to see that the quantity is larger than existing, update the quantities, then move to tail.
    '''        
        if order.prevOrder != None: # This Order is not the first Order in the OrderList
            order.prevOrder.nextOrder = order.nextOrder # Link the previous Order to the next Order, then move the Order to tail
        else:  # This Order is the first Order in the OrderList
            # Update the head order
            self.headOrder = order.nextOrder # Make next order the first
        order.nextOrder.prevOrder = order.prevOrder
        # Set the previous tail order's next order to this order
        # Move Order to the last position. Link up the previous last position Order
        self.tailOrder.nextOrder = order
        self.tailOrder = order
        order.prevOrder = self.tailOrder
        order.nextOrder = None
        
    def __str__(self):
        from cStringIO import StringIO
        file_str = StringIO()
        for order in self:
            file_str.write("%s\n" % str(order))
        return file_str.getvalue()
