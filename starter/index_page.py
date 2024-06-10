from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

from starter.query.query_service import QueryService
from starter.result.result import is_failure


def index_page(query_service: QueryService) -> Blueprint:
    page = Blueprint('index_page', __name__)

    @page.get('/')
    def index() -> ResponseReturnValue:
        return render_template('index.html')

    @page.post('/')
    def query() -> ResponseReturnValue:
        user_query = request.form.get('query')
        result = query_service.fetch_response(user_query)
        if is_failure(result):
            return render_template(
                'error.html',
                message=result.message,
            )

        chat_response = result.value
        return render_template(
            'response.html',
            query=user_query,
            source=chat_response.source,
            response=chat_response.response,
        )

    return page
