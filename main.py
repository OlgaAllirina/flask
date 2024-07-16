from flask import Flask, jsonify, request, Response
from flask.views import MethodView

from sqlalchemy.exc import IntegrityError

from models import Ads, Session

app = Flask("app")


class ApiError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def add_ad(ad: Ads):
    try:
        request.session.add(ad)
        request.session.commit()
    except IntegrityError:
        raise ApiError(409, "user already exists")
    return ad


@app.errorhandler(ApiError)
def error_handler(err: ApiError):
    http_response = jsonify({"error": err.message})
    http_response.status_code = err.status_code
    return http_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: Response):
    request.session.close()
    return http_response


def get_ad(ad_id: int):
    ad = request.session.get(Ads, ad_id)
    if ad is None:
        raise ApiError(404, "user not found")
    return ad


class UserView(MethodView):
    def get(self, ad_id: int):
        ad = get_ad(ad_id)
        return jsonify(ad.json())

    def post(self):
        json_data = request.json

        new_ad = Ads(
                title=json_data["title"],
                description=json_data["description"],
                owner=json_data["owner"],
            )
        new_ad = add_ad(new_ad)

        return jsonify(new_ad.json())

    def patch(self, ad_id):
        json_data = request.json
        ad = get_ad(ad_id)
        for field, value in json_data.items():
            setattr(ad, field, value)
        ad = add_ad(ad)
        return jsonify(ad.json())

    def delete(self, ad_id):
        ad = get_ad(ad_id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({"status": "deleted"})


user_view = UserView.as_view("ad")


app.add_url_rule("/ad/<int:ad_id>/",
                 view_func=user_view,
                 methods=["GET", "PATCH", "DELETE"])

app.add_url_rule('/ad/',
                 view_func=user_view,
                 methods=["POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
