import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route('/items/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        if items.get(item_id) is not None:
            return items[item_id]
        abort(404, message="Item not found!")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemSchema)
    def put(self, item_data, item_id):
        if items.get(item_id) is not None:
            item = items[item_id]
            item |= item_data
            return item
        abort(404, message="Item not found!")

    def delete(self, item_id):
        if items.get(item_id) is not None:
            del items[item_id]
            return {"message": "Item Deleted!"}
        abort(404, message="Item not found!")


@blp.route('/items')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # if item_data["store_id"] not in stores:
        #     abort(404, message="Store not found!")
        #     # return {"message": "Store not found!"}, 404

        for item in items.values():
            if (
                    item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists!")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
