#ordertree
from rbtree import RBTree
from orderlist import OrderList
from order import Order

'''A red-black tree used to store OrderLists in price order
The exchange will be using the OrderTree to hold bid and ask data (one OrderTree for each side).
Keeping the information in a red black tree makes it easier/faster to detect a match.
'''    
class OrderTree(object):
    def __init__(self):
        self.priceTree = RBTree() 
        self.priceMap = {}  # Map from price -> orderList object; # Dictionary containing price : OrderList object
        self.orderMap = {}  # Order ID to Order object; # Dictionary containing order_id : Order object
        self.volume = 0     # How much volume on this side?; # Contains total quantity from all Orders in tree
        self.nOrders = 0   # How many orders?; # Contains count of Orders in tree
        self.lobDepth = 0  # How many different prices on lob?; # Number of different prices in tree (http://en.wikipedia.org/wiki/Order_book_(trading)#Book_depth)
        
    def __len__(self):
        return len(self.orderMap)
    
    def getPrice(self, price):
        return self.priceMap[price]
    
    def getOrder(self, idNum): #idNum is Order_ID
        return self.orderMap[idNum]
    
    def createPrice(self, price):
        self.lobDepth += 1 # Add a price depth level to the tree
        newList = OrderList()
        self.priceTree.insert(price, newList) # Insert a new price into the tree
        self.priceMap[price] = newList # Can i just get this by using self.price_tree.get_value(price)? Maybe this is faster though.
        
    def removePrice(self, price):
        self.lobDepth -= 1 # Remove a price depth level
        self.priceTree.remove(price)
        del self.priceMap[price]
        
    def priceExists(self, price):
        return price in self.priceMap
    
    def orderExists(self, idNum): #idNum = Order; is different from the other idNum for dyn4mik3 OrderBook
        return idNum in self.orderMap #might be able to change this and previous line from idNum to 'order'
    
    def insertOrder(self, quote):
        if self.orderExists(quote['idNum']): #where this one is equal to his 'order_id' vice the previous line 49 'Order'
            self.removeOrderById(quote['idNum'])
        self.nOrders += 1
        if quote['price'] not in self.priceMap:
            self.createPrice(quote['price']) # If price not in Price Map, create a node in RBtree
        order = Order(quote, self.priceMap[quote['price']]) # Create an order
        self.priceMap[order.price].appendOrder(order)  # Add the order to the OrderList in Price Map
        self.orderMap[order.idNum] = order
        self.volume += order.qty
        
    def updateOrder(self, orderUpdate):
        order = self.orderMap[orderUpdate['idNum']]
        originalVolume = order.qty
        if orderUpdate['price'] != order.price:
            # Price changed. Remove order and update tree.
            orderList = self.priceMap[order.price]
            orderList.removeOrder(order)
            if len(orderList) == 0: # If there is nothing else in the OrderList, remove the price from RBtree
                self.removePrice(order.price) 
            self.insertOrder(orderUpdate)
        else:
            # Quantity changed. Price is the same.
            order.updateQty(orderUpdate['qty'], orderUpdate['timestamp'])
        self.volume += order.qty - originalVolume
        
    def removeOrderById(self, idNum):
        self.nOrders -= 1
        order = self.orderMap[idNum]
        self.volume -= order.qty
        order.orderList.removeOrder(order)
        if len(order.orderList) == 0:
            self.removePrice(order.price)
        del self.orderMap[idNum]
        
    def maxPrice(self):
        if self.lobDepth > 0:
            return self.priceTree.max_key()
        else: return None
    
    def minPrice(self):
        if self.lobDepth > 0:
            return self.priceTree.min_key()
        else: return None
    
    def maxPriceList(self):
        if self.lobDepth > 0:
            return self.getPrice(self.maxPrice())
        else: return None
    
    def minPriceList(self):
        if self.lobDepth > 0:
            return self.getPrice(self.minPrice())
        else: return None
