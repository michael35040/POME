Python Orderbook & Matching Engine (POME)
=========
POME, is a fully functioning fast Matching engine and limit order book financial exchange, developed for modelling. The aim is to allow exploration of automated trading strategies that deal with "Level 2" market data.

It is written in Python, single-threaded and opperates a standard price-time-priority. It supports both market and limit orders, as well as add, cancel and update functionality. The model is based on few simplifying assumptions, chief of which is zero latency: if a trader issues a new quote, that gets processed by the exchange, all other traders can react to it before any other quote is issued.


How it Works (Double Auctions)
=========
Gode and Sunder (1993) implement a simplified order book mechanism in a double auction market. As described in their paper: "We made three choices to simplify our implementation of the double auction. Each bid, ask, and transaction was valid for a single unit. A transaction canceled any unaccepted bids and offers. Finally, when a bid and ask crossed, the transaction price was equal to the earlier of the two." (p. 122). Thus there are four possible current states of the order book: 
* a) no best ask (lowest ask price) nor a best bid (highest bid price); 
* b) a best ask and no best bid; 
* c) no best ask but a best bid; or 
* d) both a best ask and best bid. Note that the best ask will be greater than the best bid in case (d) and that there is at most one best ask and one best bid on the order book at any time.


Copyright:
===============
All credit goes to:
* Ash Booth (ab24v07) for all of the actual code
* Julienne Walker for the algorithms
* Michael Nguyen (dyn4mik3) for adding some comments to the code

The code is open-sourced via the MIT Licence: see the LICENSE file for full text. (copied from http://opensource.org/licenses/mit-license.php)

Features:
=============
* Standard price-time priority
* Market orders
* Limit Orders
* Add orders
* Cancel orders
* Update/Modify orders


Requirements:
=============
* bintrees
To ensure easy distribution and use I've tried to ensure that there are no requirements other than a standard python install. The code for the RBTrees was taken directly from the bintrees library and is implemented in pure python. This is to improve portability and ensure easy of use for all. Credit to Julienne Walker ( http://eternallyconfuzzled.com/jsw_home.aspx ) for the great algorithms.


Key Functions
=============

Create an Order Book:

```python
if __name__ == '__main__':
    
    from PyLOB import OrderBook
    
    # Create a LOB object
    lob = OrderBook()
```

Limit Orders
```python
    ########### Limit Orders #############
    
    # Create some limit orders
    someOrders = [{'type' : 'limit', 
                   'side' : 'ask', 
                    'qty' : 5, 
                    'price' : 101,
                    'tid' : 100},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'qty' : 5, 
                    'price' : 103,
                    'tid' : 101},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'qty' : 5, 
                    'price' : 101,
                    'tid' : 102},
                   {'type' : 'limit', 
                    'side' : 'ask', 
                    'qty' : 5, 
                    'price' : 101,
                    'tid' : 103},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'qty' : 5, 
                    'price' : 99,
                    'tid' : 100},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'qty' : 5, 
                    'price' : 98,
                    'tid' : 101},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'qty' : 5, 
                    'price' : 99,
                    'tid' : 102},
                   {'type' : 'limit', 
                    'side' : 'bid', 
                    'qty' : 5, 
                    'price' : 97,
                    'tid' : 103},
                   ]
    
    # Add orders to LOB
    for order in someOrders:
        trades, idNum = lob.processOrder(order, False, False)
    
    # The current book may be viewed using a print
    print lob
    
    # Submitting a limit order that crosses the opposing best price will 
    # result in a trade.
    crossingLimitOrder = {'type' : 'limit', 
                          'side' : 'bid', 
                          'qty' : 2, 
                          'price' : 102,
                          'tid' : 109}
    trades, orderInBook = lob.processOrder(crossingLimitOrder, False, False)
    print "Trade occurs as incoming bid limit crosses best ask.."
    print trades
    print lob
    
    # If a limit order crosses but is only partially matched, the remaining 
    # volume will be placed in the book as an outstanding order
    bigCrossingLimitOrder = {'type' : 'limit', 
                             'side' : 'bid', 
                             'qty' : 50, 
                             'price' : 102,
                             'tid' : 110}
    trades, orderInBook = lob.processOrder(bigCrossingLimitOrder, False, False)
    print "Large incoming bid limit crosses best ask.\
           Remaining volume is placed in the book.."
    print lob
```

Market Orders
```python
    ############# Market Orders ##############
    
    # Market orders only require that the user specifies a side (bid
    # or ask), a quantity and their unique tid.
    marketOrder = {'type' : 'market', 
                   'side' : 'ask', 
                   'qty' : 40, 
                   'tid' : 111}
    trades, idNum = lob.processOrder(marketOrder, False, False)
    print "A limit order takes the specified volume from the\
            inside of the book, regardless of price" 
    print "A market ask for 40 results in.."
    print lob
```

cancelOrder
```python
    ############ Cancelling Orders #############
    
    # Order can be cancelled simply by submitting an order idNum and a side
    print "cancelling bid for 5 @ 97.."
    lob.cancelOrder('bid', 8)
    print lob
```

modifyOrder
```python
    ########### Modifying Orders #############
    
    # Orders can be modified by submitting a new order with an old idNum
    lob.modifyOrder(5, {'side' : 'bid', 
                    'qty' : 14, 
                    'price' : 99,
                    'tid' : 100})
    print "book after modify..."
    print lob
```


getVolumeAtPrice

getBestBid
getWorstBid

getBestAsk
getWorstAsk

tapeDump


Data Structure
==============

Orders are sent to the order book using the process_order function. The Order is created using a quote.

```python
# For a limit order
quote = {'type' : 'limit', 
         'side' : 'bid', 
         'qty' : 6, 
         'price' : 108.2, 
         'tid' : 001}  #trade_id
         
# and for a market order:
quote = {'type' : 'market',
         'side' : 'ask', 
         'qty' : 6, 
         'tid' : 002}
```







Check the Wiki!
===============
For details on limit order books as well as usage guides and examples, please see the wiki.

Usage
=====

Install package:

```
pip install pome 
```

Import package:

```python
from orderbook import pome
```

