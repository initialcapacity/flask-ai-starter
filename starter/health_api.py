from flask import Blueprint, jsonify
from flask.typing import ResponseReturnValue

from starter.database_support.database_template import DatabaseTemplate
from starter.database_support.result_mapping import map_one_result


def __check_db(db_template: DatabaseTemplate) -> bool:
    try:
        result = db_template.query("SELECT true as success")
        return map_one_result(result, lambda row: row['success'])
    except Exception as e:
        return False


def health_api(db_template: DatabaseTemplate) -> Blueprint:
    api = Blueprint('health_api', __name__)

    @api.get('/health')
    def health() -> ResponseReturnValue:
        success = __check_db(db_template)
        if success:
            return jsonify({
                'status': 'UP',
                'database': 'UP',
            }), 200
        else:
            return jsonify({
                'status': 'DOWN',
                'database': 'DOWN',
            }), 504

    return api
