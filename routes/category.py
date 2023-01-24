from flask import request, jsonify, Blueprint
from pydantic import ValidationError

from models import Category

from schemas import CategorySchema, GroupSchema, SpecificationSchema, ValidIdSchema


category = Blueprint('category', __name__)


@category.route('/', methods=['GET'])
def get_list_categories():
    if request.method == 'GET':

        list_categories = []

        try:
            all_category = Category.get_categories_list()
            for cat in all_category:
                created_category = CategorySchema.from_orm(cat).dict()
                list_categories.append(created_category)
            return jsonify(list_categories)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@category.route('/<category_id>', methods=['GET'])
def get_one_category(category_id):
    if request.method == 'GET':
        try:
            ValidIdSchema(id=category_id)

            target_category = Category.get_category(category_id)

            cat_dict = CategorySchema.from_orm(target_category).dict()
            cat_dict['groupSpec'] = []
            if target_category.groups:
                for i, group in enumerate(target_category.groups):
                    cat_dict['groupSpec'].append(GroupSchema.from_orm(group).dict())
                    cat_dict['groupSpec'][i]['specifications'] = []
                    if group.specifications:
                        for spec in group.specifications:
                            cat_dict['groupSpec'][i]['specifications'].append(SpecificationSchema.from_orm(spec).dict())

            return jsonify(cat_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@category.route('/', methods=['POST'])
def creation_category():
    if request.method == 'POST':

        try:
            new_data = CategorySchema(**request.get_json()).dict()

            new_category = Category.save_category(new_data)

            created_category_dict = CategorySchema.from_orm(new_category).dict()
            created_category_dict["groupsSpecs"] = []
            if new_category.groups:
                for group in new_category.groups:
                    created_category_dict["groupsSpecs"].append(GroupSchema.from_orm(group).dict())

            return jsonify(created_category_dict)

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@category.route('/', methods=['PUT'])
def edit_category():
    if request.method == 'PUT':
        try:
            new_data = CategorySchema(**request.get_json()).dict()

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            updated_category = Category.update_category(new_data)
            update_category_dict = CategorySchema.from_orm(updated_category).dict()
            update_category_dict["groupsSpecs"] = []

            if updated_category.groups:
                for group in updated_category.groups:
                    update_category_dict["groupsSpecs"].append(GroupSchema.from_orm(group).dict())

            return jsonify(update_category_dict)
        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@category.route('/', methods=['DELETE'])
def delete_category():
    if request.method == 'DELETE':

        try:
            new_data = request.get_json()
            ValidIdSchema(id=new_data['id'])

            if new_data['id'] is None:
                return jsonify({'error': 'missing a required field "id" '}), 400

            Category.delete_category(new_data['id'])

            return jsonify({})

        except ValidationError as err:
            return err.json()
        except Exception as e:
            return jsonify({'error': str(e)}), 400