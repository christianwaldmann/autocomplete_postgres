from flask import jsonify
from flask.blueprints import Blueprint
import psycopg
import os
from dotenv import load_dotenv
from timer import tic, toc


load_dotenv()


app_bp = Blueprint("application", __name__)


def flat_list(list_):
    return [item for x in list_ for item in x]


@app_bp.route("/api/search/<path:search_string>")
def index(search_string):
    with psycopg.connect(
        dbname=os.getenv("DATABASE_DBNAME"),
        user=os.getenv("DATABASE_USERNAME"),
        password=os.getenv("DATABASE_PASSWORD"),
        host="localhost",
        port=5432
    ) as conn:
        with conn.cursor() as cur:
            tic()
            res = cur.execute(f"""
                SELECT
                    name
                FROM domainindexed
                WHERE
                    name LIKE '%{search_string}%'
                ORDER BY (CASE WHEN name LIKE '{search_string}%' THEN 1 ELSE 2 END), name
                LIMIT 10
            """)  # TODO: rewrite so no sql injection
            data = res.fetchmany(10)
            conn.commit()
            time_in_s = toc(hide_output=True)
            print(time_in_s * 1000)
            return jsonify(flat_list(data))


@app_bp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
