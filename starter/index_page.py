from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

from starter.query.query_service import QueryService


def index_page(query_service: QueryService) -> Blueprint:
    page = Blueprint('index_page', __name__)

    @page.get('/')
    def index() -> ResponseReturnValue:
        return render_template('index.html')

    @page.post('/')
    def query() -> ResponseReturnValue:
        user_query = request.form.get('query')
        result = query_service.fetch_response(user_query)

        return render_template(
            'response.html',
            query=user_query,
            source=result.source,
            response=result.response,
        )

    return page
