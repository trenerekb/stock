from flask import request, jsonify, Blueprint, abort
from pydantic import ValidationError

from models import Article
from schemas import ArtSchema, ValidIdSchema, CategorySchema, SpecificationSchema

article = Blueprint('articles', __name__)


@article.route('/', methods=['GET'])
def get_list_articles():
    if request.method == 'GET':

        list_dict_articles = []
        try:
            all_articles = Article.get_articles_list()
            for art in all_articles:
                created_article = ArtSchema.from_orm(art).dict()
                list_dict_articles.append(created_article)
            return jsonify(list_dict_articles)

        except ValidationError as err:
            return err.json()

        except Exception as e:
            return jsonify({'error': str(e)}), 400


@article.route('/<article_id>', methods=['GET'])
def get_one_article(article_id):
    if request.method == 'GET':

        try:
            ValidIdSchema(id=article_id)

            target_article = Article.get_article(article_id)

            art_dict = ArtSchema.from_orm(target_article).dict()
            art_dict['categoryArticle'] = []
            art_dict['articleSpecification'] = []

            if target_article.categories:
                for cat in target_article.categories:
                    art_dict['categoryArticle'].append(CategorySchema.from_orm(cat).dict())

            if len(target_article.specifications) > 0:
                for spec in target_article.specifications:
                    art_dict['articleSpecification'].append(SpecificationSchema.from_orm(spec).dict())

            return jsonify(art_dict)

        except ValidationError as err:
            return err.json()

        except Exception as e:
            return jsonify({'error': str(e)}), 400


@article.route('/', methods=['POST'])
def creation_article():
    if request.method == 'POST':

        try:
            new_data = ArtSchema(**request.get_json()).dict()

            new_article = Article.save_article(new_data)

            created_article_dict = ArtSchema.from_orm(new_article).dict()
            created_article_dict['categoryArticle'] = []
            created_article_dict['articleSpecification'] = []

            if new_article.categories:
                for cat_art in new_article.categories:
                    created_article_dict['categoryArticle'].append(CategorySchema.from_orm(cat_art).dict())
            if new_article.specifications:
                for spec_art in new_article.specifications:
                    created_article_dict['articleSpecification'].append(SpecificationSchema.from_orm(spec_art).dict())

            return jsonify(created_article_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@article.route('/', methods=['PUT'])
def edit_article():
    if request.method == 'PUT':
        try:
            new_data = ArtSchema(**request.get_json()).dict()

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_article = Article.update_article(new_data)
            update_article_dict = ArtSchema.from_orm(updated_article).dict()
            update_article_dict['categoryArticle'] = []
            update_article_dict['articleSpecification'] = []

            if updated_article.categories:
                for cat_art in updated_article.categories:
                    update_article_dict['categoryArticle'].append(CategorySchema.from_orm(cat_art).dict())
            if updated_article.specifications:
                for spec_art in updated_article.specifications:
                    update_article_dict['articleSpecification'].append(SpecificationSchema.from_orm(spec_art).dict())

            return jsonify(update_article_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@article.route('/', methods=['DELETE'])
def delete_article():
    if request.method == 'DELETE':
        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            Article.delete_article(new_data['id'])

            return jsonify({})

        except ValidationError as err:
            return err.json()

        except Exception as e:
            return jsonify({'error': str(e)}), 400

