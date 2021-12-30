from shopify.config import OrderProcessorConfig
from typing import Tuple


class OrderProcessor:
    def __init__(self, cfg: OrderProcessorConfig):
        self.static_breakdown_template = cfg.static_breakdown_template
        self.dynamic_breakdown_template = cfg.dynamic_breakdown_template

    def process_orders(self, orders: list, dates: list) -> Tuple[dict, dict]:
        all_consolidated_items = {}
        all_breakdown_items = {}
        for date in dates:
            consolidated_items = {}
            breakdown_items = {}
            filtered_orders = self._filter_order_by_date(orders, date)
            filtered_orders = self._filter_order_by_financial_status(
                filtered_orders, ["paid", "partially_refunded"]
            )
            for order in filtered_orders:
                order_number = order["order_number"]
                # populate consolidated_items dict
                for line_item in order["line_items"]:
                    name = line_item["name"]
                    quantity = line_item["quantity"]
                    if name in consolidated_items:
                        consolidated_items[name]["quantity"] += quantity
                        consolidated_items[name]["order_numbers"].add(order_number)
                    else:
                        consolidated_items[name] = {
                            "quantity": quantity,
                            "order_numbers": {order_number},
                        }
                # populate breakdown_items dict
                order_breakdown = self._breakdown_order(order)
                for item, quantity in order_breakdown.items():
                    if item in breakdown_items:
                        breakdown_items[item]["quantity"] += quantity
                        breakdown_items[item]["order_numbers"].add(order_number)
                    else:
                        breakdown_items[item] = {
                            "quantity": quantity,
                            "order_numbers": {order_number},
                        }
            # only add when there's at least one item
            if len(consolidated_items) > 0:
                all_consolidated_items[date] = consolidated_items
            if len(breakdown_items) > 0:
                all_breakdown_items[date] = breakdown_items
        return all_consolidated_items, all_breakdown_items

    def _filter_order_by_date(self, orders: list, date: str) -> list:
        # assumption: date in the format of "%d/%m/%Y" is available in "tags" of the order
        return [order for order in orders if order["tags"] == date]

    def _filter_order_by_financial_status(self, orders: list, statuses: list) -> list:
        return [order for order in orders if order["financial_status"] in statuses]

    def _breakdown_order(self, order) -> dict:
        breakdown = {}
        for line_item in order["line_items"]:
            # title is title of the product
            title = line_item["title"]
            # name is {title} - {variant} of the product
            name = line_item["name"]
            quantity = line_item["quantity"]
            items = []
            if title in self.static_breakdown_template:
                if type(self.static_breakdown_template[title]) == dict:
                    variant = " - ".join(name.split(" - ")[1:])
                    items = self.static_breakdown_template[title][variant]
                else:
                    items = self.static_breakdown_template[title]
            elif title in self.dynamic_breakdown_template:
                if type(self.dynamic_breakdown_template[title]) == dict:
                    variant = " - ".join(name.split(" - ")[1:])
                    items = self.dynamic_breakdown_template[title][variant]
                else:
                    items = self.dynamic_breakdown_template[title]
                line_properties = {}
                for line_property in line_item["properties"]:
                    line_properties[line_property["name"]] = line_property["value"]
                formatted_items = []
                for item in items:
                    template_args = []
                    if "properties" in item:
                        for property in item["properties"]:
                            value = line_properties.get(
                                property["name"], "missing-property"
                            )
                            if "value_map" in property:
                                value = property["value_map"].get(
                                    value, "missing-property"
                                )
                            template_args.append(value)
                    formatted_item = item["template"].format(*template_args)
                    formatted_items.append(formatted_item)
                items = formatted_items
            else:
                # no breakdowns for products not in static/dynamic breakdown templates
                items.append(name)
            for item in items:
                if item in breakdown:
                    breakdown[item] += quantity
                else:
                    breakdown[item] = quantity
        return breakdown
