from flask import request, jsonify, Blueprint
from pydantic import ValidationError

from models import GroupSpec
from schemas import GroupSchema, SpecificationSchema, ValidIdSchema, ArtSchema

group_spec = Blueprint('group_spec', __name__)


@group_spec.route('/', methods=['GET'])
def get_list_groups():
    if request.method == 'GET':
        list_groups = []

        try:
            all_groups = GroupSpec.get_group_spec_list()
            for group in all_groups:
                created_groups = GroupSchema.from_orm(group).dict()
                list_groups.append(created_groups)

            return jsonify(list_groups)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@group_spec.route('/<group_id>', methods=['GET'])
def get_one_group(group_id):
    if request.method == 'GET':
        try:
            ValidIdSchema(id=group_id)
            target_group = GroupSpec.get_group_spec(group_id)

            groups_dict = GroupSchema.from_orm(target_group).dict()
            groups_dict['specifications'] = []

            if target_group.specifications:
                for i, spec in enumerate(target_group.specifications):
                    groups_dict['specifications'].append(SpecificationSchema.from_orm(spec).dict())
                    groups_dict['specifications'][i]['articles'] = []
                    if spec.articles:
                        for art in spec.articles:
                            groups_dict['specifications'][i]['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(groups_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@group_spec.route('/', methods=['POST'])
def creation_group():
    if request.method == 'POST':
        try:
            new_data = GroupSchema(**request.get_json()).dict()
            if new_data['category_id'] is None:
                return jsonify({'error': "missing a required field 'category_id'"}), 400

            new_group = GroupSpec.save_group_spec(new_data)

            created_group_dict = GroupSchema.from_orm(new_group).dict()
            created_group_dict["specifications"] = []
            if new_group.specifications:
                for i, spec in enumerate(new_group.specifications):
                    created_group_dict['specifications'].append(SpecificationSchema.from_orm(spec).dict())
                    created_group_dict['specifications'][i]['articles'] = []
                    if spec.articles:
                        for art in spec.articles:
                            created_group_dict['specifications'][i]['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(created_group_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@group_spec.route('/', methods=['PUT'])
def edit_group():
    if request.method == 'PUT':

        try:
            new_data = GroupSchema(**request.get_json()).dict()

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_group = GroupSpec.update_group_spec(new_data)
            update_group_dict = GroupSchema.from_orm(updated_group).dict()

            update_group_dict["specifications"] = []
            if updated_group.specifications:
                for i, spec in enumerate(updated_group.specifications):
                    update_group_dict['specifications'].append(SpecificationSchema.from_orm(spec).dict())
                    update_group_dict['specifications'][i]['articles'] = []
                    if spec.articles:
                        for art in spec.articles:
                            update_group_dict['specifications'][i]['articles'].append(ArtSchema.from_orm(art).dict())

            return jsonify(update_group_dict)
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@group_spec.route('/', methods=['DELETE'])
def delete_group():
    if request.method == 'DELETE':
        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            GroupSpec.delete_group_spec(new_data['id'])

            return jsonify({})

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400
