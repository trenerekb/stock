from routes.article import article
from routes.article_specification import art_spec
from routes.category_article import cat_art
from routes.group_spec import group_spec
from routes.specification import spec
from app import app
from routes.category import category


app.register_blueprint(article, url_prefix='/articles')
app.register_blueprint(spec, url_prefix='/specifications')
app.register_blueprint(group_spec, url_prefix='/groupSpec')
app.register_blueprint(category, url_prefix='/categories')
app.register_blueprint(art_spec, url_prefix='/articleSpec')
app.register_blueprint(cat_art, url_prefix='/categoryArticle')


client = app.test_client()


if __name__ == '__main__':
    app.run(host='0.0.0.0')



