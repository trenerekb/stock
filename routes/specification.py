from flask import request, jsonify, Blueprint, abort
from pydantic import ValidationError

from models import Specification
from schemas import SpecificationSchema, ValidIdSchema, ArtSchema

spec = Blueprint('specifications', __name__)


@spec.route('/', methods=['GET'])
def get_list_specifications():
    if request.method == 'GET':

        try:
            all_specifications = Specification.get_spec_list()
            list_specifications = []
            for specification in all_specifications:
                list_specifications.append(SpecificationSchema.from_orm(specification).dict())

            return jsonify(list_specifications)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@spec.route('/<specification_id>', methods=['GET'])
def get_one_specification(specification_id):
    if request.method == 'GET':
        try:
            ValidIdSchema(id=specification_id)
            target_specification = Specification.get_spec(specification_id)

            specification_dict = SpecificationSchema.from_orm(target_specification).dict()
            specification_dict['articles'] = []

            if target_specification.articles:
                for art in target_specification.articles:
                    specification_dict['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(specification_dict)
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@spec.route('/', methods=['POST'])
def creation_specification():
    if request.method == 'POST':
        try:
            new_data = SpecificationSchema(**request.get_json()).dict()
            if new_data['group_id'] is None:
                return jsonify({'error': "missing a required field 'group_id'"}), 400

            new_spec = Specification.save_spec(new_data)
            created_spec_dict = SpecificationSchema.from_orm(new_spec).dict()

            created_spec_dict['articles'] = []
            if new_spec.articles:
                for art in new_spec.articles:
                    created_spec_dict['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(created_spec_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@spec.route('/', methods=['PUT'])
def edit_specification():
    if request.method == 'PUT':
        try:
            new_data = SpecificationSchema(**request.get_json()).dict()

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_spec = Specification.update_spec(new_data)
            updated_spec_dict = SpecificationSchema.from_orm(updated_spec).dict()
            updated_spec_dict['articles'] = []

            if updated_spec.articles:
                for art in updated_spec.articles:
                    updated_spec_dict['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(updated_spec_dict)
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@spec.route('/', methods=['DELETE'])
def delete_specification():
    if request.method == 'DELETE':
        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            Specification.delete_spec(new_data['id'])

            return jsonify({})
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400