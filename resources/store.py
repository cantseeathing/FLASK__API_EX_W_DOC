import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        if stores.get(store_id) is not None:
            return stores[store_id]
        abort(404, message="Store not found!")
        # return {"message": "Store not found!"}, 404

    def delete(self, store_id):
        if stores.get(store_id) is not None:
            del stores[store_id]
            return {"message": "Store Deleted!"}
        abort(404, message="Store not found!")


@blp.route('/stores')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists!")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201

