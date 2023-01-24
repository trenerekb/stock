from flask import request, jsonify, Blueprint
from pydantic import ValidationError

from models import CategoryArticle
from schemas import ValidIdSchema, CatArtSchema

cat_art = Blueprint('category_article', __name__)


@cat_art.route('/', methods=['GET'])
def get_list_cat_art():
    if request.method == 'GET':
        try:
            all_art_spec = CategoryArticle.get_cat_art_list()
            list_cat_art = []
            for c_a in all_art_spec:
                list_cat_art.append(CatArtSchema.from_orm(c_a).dict())

            return jsonify(list_cat_art)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@cat_art.route('/<cat_art_id>', methods=['GET'])
def get_one_cat_art(cat_art_id):
    if request.method == 'GET':
        try:
            ValidIdSchema(id=cat_art_id)
            target_cat_art = CategoryArticle.get_cat_art(cat_art_id)
            cat_art_dict = CatArtSchema.from_orm(target_cat_art).dict()

            return jsonify(cat_art_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@cat_art.route('/', methods=['POST'])
def creation_cat_art():
    if request.method == 'POST':
        try:
            new_data = CatArtSchema(**request.get_json()).dict()

            if new_data['article_id'] is None or new_data['category_id'] is None:
                return jsonify({'error': "missing a required field 'article_id' or 'category_id'"}), 400

            new_cat_art = CategoryArticle.save_cat_art(new_data)

            created_cat_art_dict = CatArtSchema.from_orm(new_cat_art).dict()
            return jsonify(created_cat_art_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@cat_art.route('/', methods=['PUT'])
def edit_cat_art():
    if request.method == 'PUT':
        try:
            new_data = CatArtSchema(**request.get_json()).dict()
            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_cat_art = CategoryArticle.update_cat_art(new_data)
            updated_cat_art_dict = CatArtSchema.from_orm(updated_cat_art).dict()

            return jsonify(updated_cat_art_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@cat_art.route('/', methods=['DELETE'])
def delete_cat_art():
    if request.method == 'DELETE':
        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])
            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            CategoryArticle.delete_cat_art(new_data['id'])

            return jsonify({})

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400
