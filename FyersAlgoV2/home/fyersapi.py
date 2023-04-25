from fyers_api import fyersModel, accessToken


class FyerApiClass:
    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token

    def fyers_model_instance(self):
        fyers = fyersModel.FyersModel(
            client_id=self.client_id,
            token=self.access_token,
            log_path= "",
        )
        return fyers

    def user_profile(self):
        profile = self.fyers_model_instance().get_profile()

        if profile["code"] == 200:
            return profile["data"]["fy_id"]
        else:
            return profile["message"]

    def market_status(self):
        market_status = self.fyers_model_instance().market_status()

        if market_status["code"] == 200:
            return market_status
        else:
            return market_status["message"]

    def available_funds(self):
        funds = self.fyers_model_instance().funds()

        if funds["code"] == 200:
            return funds["fund_limit"][-2]["equityAmount"]
        else:
            return funds["message"]

    def get_quote(self, symbol):
        data = {"symbols": symbol}
        get_quote = self.fyers_model_instance().quotes(data)["d"][0]["v"]["lp"]
        return get_quote

    def orderbook(self):
        orderbook = self.fyers_model_instance().orderbook()
        return orderbook

    def order_stock_specific_details(self, id):
        orderID = id
        data = {"id": orderID}
        return self.fyers_model_instance().orderbook(data=data)

    def positions(self):
        position = self.fyers_model_instance().positions()
        return position

    def tradebook(self):
        tradebook = self.fyers_model_instance().tradebook()
        return tradebook

    # Limit Orders

    def intraday_buy_limit_order(self, symbol, qty, limitPrice):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 1,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": limitPrice,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    def intraday_sell_limit_order(self, symbol, qty, limitPrice):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 1,
            "side": -1,
            "productType": "INTRADAY",
            "limitPrice": limitPrice,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    # Place Market Orders

    def intraday_buy_market_order(self, symbol, qty):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 2,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    def intraday_sell_market_order(self, symbol, qty):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 2,
            "side": -1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    # Stop order Market

    def intraday_buy_stop_market_order(self, symbol, qty, stopPrice):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 3,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": stopPrice,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    def intraday_sell_stop_market_order(self, symbol, qty, stopPrice):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 3,
            "side": -1,
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": stopPrice,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    # Stop loss Limit Order

    def intraday_buy_stop_limit_order(self, symbol, qty, stopPrice, tick_size):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 4,
            "side": 1,
            "productType": "INTRADAY",
            "limitPrice": stopPrice,
            "stopPrice": stopPrice - tick_size,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    def intraday_sell_stop_limit_order(self, symbol, qty, stopPrice, tick_size):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 4,
            "side": -1,
            "productType": "INTRADAY",
            "limitPrice": stopPrice,
            "stopPrice": stopPrice + tick_size,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": 0,
            "takeProfit": 0,
        }
        return data

    # bracket order

    def bracket_order_buy_market_order(
        self, symbol, qty, stopPrice, stopLoss, takeProfit, tick_size
    ):
        data = {
            "symbol": symbol,
            "qty": int(qty),
            "type": 4,
            "side": 1,
            "productType": "BO",
            "limitPrice": round(stopPrice, 2),
            "stopPrice": round(stopPrice - tick_size, 2),
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": "False",
            "stopLoss": stopLoss,
            "takeProfit": takeProfit,
        }
        return data

        def bracket_order_sell_market_order(
            self, symbol, qty, stopPrice, stopLoss, takeProfit, tick_size
        ):
            data = {
                "symbol": symbol,
                "qty": int(qty),
                "type": 4,
                "side": -1,
                "productType": "BO",
                "limitPrice": round(stopPrice,2),
                "stopPrice": round(stopPrice + tick_size,2),
                "validity": "DAY",
                "disclosedQty": 0,
                "offlineOrder": "False",
                "stopLoss": stopLoss,
                "takeProfit": takeProfit,
            }

        return data

    def place_order(self, data):
        return self.fyers_model_instance().place_order(data)
