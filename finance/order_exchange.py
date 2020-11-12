from collections import defaultdict, namedtuple, deque


LimitOrder = namedtuple("LimitOrder", ["client", "size", "price"])
MarketOrder = namedtuple("MarketOrder", ["client", "size", "price"])
Info = namedtuple("Info", ["time", "direction"])


class Order:  # to parse the input
    def __init__(self, s):  # init from a string
        ss = s.split(" ")
        self.time = ss[0]  # no need to create a class for time
        self.client = ss[1]
        self.direction = ss[2]
        self.size = int(ss[3])
        self.type = ss[4]
        self.price = float(ss[5]) if self.type != 'm' else None

    def __repr__(self):
        return " ".join([
            "Time {}".format(self.time),
            "Client {}".format(self.client),
            "Direction {}".format(self.direction),
            "Size {}".format(self.size),
            "Type {}".format(self.type),
            "Price {}".format(self.price),
        ])


def build_message(client, limit_order, size, info):
    if size > 0:
        buyer, seller = (client, limit_order.client) if info.direction == 'b' else (limit_order.client, client)
        s_price = "{:.2f}".format(limit_order.price)
        # time, buyer, seller, price, quantity
        print(" ".join(map(str, (info.time, buyer, seller, s_price, size))))


def execute(client, limit_order, info):
    # killing the limit_order, no output
    build_message(client, limit_order, limit_order.size, info)


def execute_partial(client, limit_order, partial_size, info):
    build_message(client, limit_order, partial_size, info)
    return limit_order._replace(size=limit_order.size - partial_size)


class Book:
    def __init__(self):
        self.bid = defaultdict(deque)
        self.ask = defaultdict(deque)
        # dictionary mapping price vs order
        self.level_size = defaultdict(int)
        # maps the price with the number of limit orders

    def get_min_ask(self):
        return min(self.ask.keys())

    def get_max_bid(self):
        return max(self.bid.keys())

    def process_market_buy(self, order, time):
        return self.process_market(order=order,
                                   info=Info(time, "b"),
                                   bid_or_ask=self.ask,
                                   price_level_getter=self.get_min_ask
                                   )

    def process_market_sell(self, order, time):
        return self.process_market(order=order,
                                   info=Info(time, "s"),
                                   bid_or_ask=self.bid,
                                   price_level_getter=self.get_max_bid
                                   )

    def add_limit_buy(self, order):
        self.bid[order.price].append(order)
        self.level_size[order.price] += order.size

    def add_limit_sell(self, order):
        self.ask[order.price].append(order)
        self.level_size[order.price] += order.size

    def process_limit_buy(self, order, time):
        return self.process_limit(order=order,
                                  info=Info(time, "b"),
                                  bid_or_ask=self.ask,
                                  price_level_getter=self.get_min_ask,
                                  limit_adder=self.add_limit_buy,
                                  compare_to_price=(lambda x, y: x <= y)
                                  )

    def process_limit_sell(self, order, time):
        return self.process_limit(order=order,
                                  info=Info(time, "s"),
                                  bid_or_ask=self.bid,
                                  price_level_getter=self.get_max_bid,
                                  limit_adder=self.add_limit_sell,
                                  compare_to_price=(lambda x, y: x >= y)
                                  )

    def add(self, order):
        # print("Added {}".format(order))
        if (order.direction, order.type) == ('b', "m"):
            self.process_market_buy(MarketOrder(order.client, order.size, order.price), order.time)
        if (order.direction, order.type) == ('s', "m"):
            self.process_market_sell(MarketOrder(order.client, order.size, order.price), order.time)
        if (order.direction, order.type) == ('b', "l"):
            self.process_limit_buy(LimitOrder(order.client, order.size, order.price), order.time)
        if (order.direction, order.type) == ('s', "l"):
            self.process_limit_sell(LimitOrder(order.client, order.size, order.price), order.time)

    def process_market(self, order, info, bid_or_ask, price_level_getter):
        if not bid_or_ask:
            return
            # I have some to execute
        price_limit = price_level_getter()
        level = self.level_size[price_limit]
        l = bid_or_ask[price_limit]
        remaining_size = order.size
        while level <= remaining_size:
            for u in l:
                execute(order.client, u, info)
            bid_or_ask.pop(price_limit)
            self.level_size.pop(price_limit)
            remaining_size -= level
            if not bid_or_ask:
                return
            price_limit = price_level_getter()
            level = self.level_size[price_limit]
            l = bid_or_ask[price_limit]

        # at this point, I have reached the last level of price I'm using
        while True:
            u = l.popleft()
            if u.size <= remaining_size:
                execute(order.client, u, info)
                remaining_size -= u.size
                self.level_size[price_limit] -= u.size
            else:
                new_u = execute_partial(client=order.client,
                                        limit_order=u,
                                        partial_size=remaining_size,
                                        info=info)
                self.level_size[price_limit] -= remaining_size
                l.appendleft(new_u)
                break

    def process_limit(self, order, info, bid_or_ask, price_level_getter, limit_adder, compare_to_price):
        if not bid_or_ask:
            return limit_adder(order)
        price_limit = price_level_getter()
        level = self.level_size[price_limit]
        l = bid_or_ask[price_limit]
        remaining_size = order.size
        while level <= remaining_size and compare_to_price(price_limit, order.price):
            for u in l:
                execute(order.client, u, info)
            bid_or_ask.pop(price_limit)
            self.level_size.pop(price_limit)
            remaining_size -= level
            if not bid_or_ask:
                break
            price_limit = price_level_getter()

            level = self.level_size[price_limit]
            l = bid_or_ask[price_limit]

        if (not bid_or_ask) or (not compare_to_price(price_limit, order.price)):
            return limit_adder(order._replace(size=remaining_size))

        # at this point, I have reached the last level of price I'm using
        while True:
            u = l.popleft()
            if u.size <= remaining_size:
                execute(order.client, u, info)
                remaining_size -= u.size
                self.level_size[price_limit] -= u.size
            else:
                new_u = execute_partial(client=order.client, limit_order=u, partial_size=remaining_size, info=info)
                self.level_size[price_limit] -= remaining_size
                l.appendleft(new_u)
                break


def solve(s):
    ss = s.split("\n")
    iss = iter(ss)
    n = next(iss)
    b = Book()
    for u in iss:
        order = Order(u)
        b.add(order=order)


if __name__ == "__main__":
    s = """5
09:30:00 1 b 100 l 9.99
09:31:00 2 b 1000 l 9.95
09:32:00 3 s 100 l 10.01
09:33:00 4 s 1000 l 10.05
09:41:00 5 b 200 m 10.02"""
    solve(s)
    print("I'm Here")
