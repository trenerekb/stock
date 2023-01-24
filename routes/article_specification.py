from flask import request, jsonify, Blueprint
from pydantic import ValidationError

from models import ArticleSpecification
from schemas import ArtSpecSchema, ValidIdSchema

art_spec = Blueprint('article_specification', __name__)


@art_spec.route('/', methods=['GET'])
def get_list_art_spec():
    if request.method == 'GET':
        try:
            all_art_spec = ArticleSpecification.get_art_spec_list()
            list_art_spec = []
            for a_s in all_art_spec:
                list_art_spec.append(ArtSpecSchema.from_orm(a_s).dict())

            return jsonify(list_art_spec)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@art_spec.route('/<art_spec_id>', methods=['GET'])
def get_one_art_spec(art_spec_id):
    if request.method == 'GET':
        try:
            ValidIdSchema(id=art_spec_id)
            target_art_spec = ArticleSpecification.get_art_spec(art_spec_id)
            art_spec_dict = ArtSpecSchema.from_orm(target_art_spec).dict()

            return jsonify(art_spec_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@art_spec.route('/', methods=['POST'])
def creation_art_spec():
    if request.method == 'POST':
        try:
            new_data = ArtSpecSchema(**request.get_json()).dict()

            if new_data['article_id'] is None or new_data['specification_id'] is None:
                return jsonify({'error': "missing a required field 'article_id' or 'specification_id'"}), 400

            new_art_spec = ArticleSpecification.save_art_spec(new_data)

            created_art_spec_dict = ArtSpecSchema.from_orm(new_art_spec).dict()
            return jsonify(created_art_spec_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@art_spec.route('/', methods=['PUT'])
def edit_art_spec():
    if request.method == 'PUT':
        try:
            new_data = ArtSpecSchema(**request.get_json()).dict()
            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_art_spec = ArticleSpecification.update_art_spec(new_data)
            updated_art_spec_dict = ArtSpecSchema.from_orm(updated_art_spec).dict()

            return jsonify(updated_art_spec_dict)
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@art_spec.route('/', methods=['DELETE'])
def delete_art_spec():
    if request.method == 'DELETE':
        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            ArticleSpecification.delete_art_spec(new_data['id'])

            return jsonify({})

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400
