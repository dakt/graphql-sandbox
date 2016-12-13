from flask import Flask
from flask_cors import CORS, cross_origin
from flask_graphql import GraphQLView
from blog.schema import schema
from blog.model import populate_database, db
from manager import Manager


manager = Manager()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.add_url_rule(
        '/blog',
        view_func=GraphQLView.as_view(
            'blog',
            schema=schema,
            graphiql=True
        )
    )
    CORS(app)
    db.connect()
    return app


@manager.command
def rungraphql():
    app = create_app()
    app.run(host='0.0.0.0', port=3000)


@manager.command
def seeddb():
    populate_database()


if __name__ == '__main__':
    manager.main()
