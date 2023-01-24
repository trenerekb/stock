import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP(timezone=True))
    name = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.Text)
    description = db.Column(db.Text)

    specifications = db.relationship('Specification', secondary='article_specification',
                                     back_populates='articles', lazy=True)
    categories = db.relationship('Category', secondary='category_article',
                                 back_populates='articles', lazy=True)

    @classmethod
    def get_articles_list(cls):
        try:
            all_articles = cls.query.all()
            db.session.commit()
            if not all_articles:
                raise Exception('list of articles is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_articles

    @classmethod
    def get_article(cls, article_id):
        try:
            article = cls.query.filter(cls.id == article_id).first()
            if article is None:
                raise Exception(f'there is no such id({article_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return article

    @classmethod
    def save_article(cls, new_data):
        try:
            new_article = cls(name=new_data['name'],
                              full_name=new_data['full_name'],
                              description=new_data['description'])
            db.session.add(new_article)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_article

    @classmethod
    def update_article(cls, new_data):
        try:
            article = cls.query.filter(cls.id == new_data['id']).first()
            if article is None:
                raise Exception(f'there is no article with this id({new_data["id"]}) in the database')
            article.name = new_data['name']
            article.full_name = new_data['full_name']
            article.updated_at = datetime.now()
            article.description = new_data['description']

            db.session.add(article)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return article

    @classmethod
    def delete_article(cls, article_id):
        try:
            article = cls.query.filter(cls.id == article_id).first()
            if article is None:
                raise Exception(f'there is no such id({article_id}) in the database')
            db.session.delete(article)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self):
        return f'<Article id:{self.id}, created_at:{self.created_at}, update_at:{self.updated_at}, ' \
               f'name:{self.name} full_name:{self.full_name}>'


class Specification(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('group_spec.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.VARCHAR(255), default='', nullable=False)
    default_value = db.Column(db.JSON)
    is_required = db.Column(db.Boolean, default=False, nullable=False)
    order_number = db.Column(db.Integer, nullable=False)

    articles = db.relationship('Article', secondary='article_specification',
                               back_populates='specifications', lazy=True)

    @classmethod
    def get_spec_list(cls):
        try:
            all_spec = cls.query.all()
            db.session.commit()
            if not all_spec:
                raise Exception('list of specifications is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_spec

    @classmethod
    def get_spec(cls, spec_id):
        try:
            spec = cls.query.filter(cls.id == spec_id).first()
            if spec is None:
                raise Exception(f'there is no such id({spec_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return spec

    @classmethod
    def save_spec(cls, new_data):
        try:
            new_spec = cls(name=new_data['name'],
                           group_id=new_data['group_id'],
                           type=new_data['type'],
                           default_value=new_data['default_value'],
                           is_required=new_data['is_required'],
                           order_number=new_data['order_number'])
            db.session.add(new_spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_spec

    @classmethod
    def update_spec(cls, new_data):
        try:
            spec = cls.query.filter_by(id=new_data['id']).first()
            if spec is None:
                raise Exception(f'there is no specification with this id({new_data["id"]}) in the database')
            spec.name = new_data['name']

            spec.type = new_data['type']
            spec.default_value = new_data['default_value']
            spec.is_required = new_data['is_required']
            spec.order_number = new_data['order_number']

            db.session.add(spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return spec

    @classmethod
    def delete_spec(cls, spec_id):
        try:
            spec = cls.query.filter(cls.id == spec_id).first()
            if spec is None:
                raise Exception(f'there is no such id({spec_id}) in the database')
            db.session.delete(spec)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


class GroupSpec(db.Model):
    __tablename__ = 'group_spec'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    specifications = db.relationship('Specification', backref='group_spec',
                                     lazy=True, cascade='all,delete, delete-orphan')

    @classmethod
    def get_group_spec_list(cls):
        try:
            all_group_spec = cls.query.all()
            db.session.commit()
            if not all_group_spec:
                raise Exception('list of group_spec is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_group_spec

    @classmethod
    def get_group_spec(cls, group_spec_id):
        try:
            group_spec = cls.query.filter(cls.id == group_spec_id).first()
            if group_spec is None:
                raise Exception(f'there is no such id({group_spec_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return group_spec

    @classmethod
    def save_group_spec(cls, new_data):
        try:
            new_group_spec = cls(name=new_data['name'],
                                 category_id=new_data['category_id'],
                                 description=new_data['description'])
            db.session.add(new_group_spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_group_spec

    @classmethod
    def update_group_spec(cls, new_data):
        try:
            group_spec = cls.query.filter(cls.id == new_data['id']).first()
            if group_spec is None:
                raise Exception(f'there is no group_spec with this id({new_data["id"]}) in the database')
            group_spec.name = new_data['name']
            group_spec.category_id = new_data['category_id']
            group_spec.description = new_data['description']

            db.session.add(group_spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return group_spec

    @classmethod
    def delete_group_spec(cls, group_spec_id):
        try:
            group_spec = cls.query.filter(cls.id == group_spec_id).first()
            if group_spec is None:
                raise Exception(f'there is no such id({group_spec_id}) in the database')
            db.session.delete(group_spec)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


class Category(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    articles = db.relationship('Article', secondary='category_article', back_populates='categories', lazy=True)
    groups = db.relationship('GroupSpec', backref='category', lazy=True)

    @classmethod
    def get_categories_list(cls):
        try:
            all_categories = cls.query.all()
            db.session.commit()
            if not all_categories:
                raise Exception('list of categories is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_categories

    @classmethod
    def get_category(cls, category_id):
        try:
            category = cls.query.filter(cls.id == category_id).first()
            if category is None:
                raise Exception(f'there is no such id({category_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return category

    @classmethod
    def save_category(cls, new_data):
        try:
            new_category = cls(name=new_data['name'],
                               description=new_data['description'])
            db.session.add(new_category)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_category

    @classmethod
    def update_category(cls, new_data):
        try:
            category = cls.query.filter(cls.id == new_data['id']).first()
            if category is None:
                raise Exception(f'there is no category with this id({new_data["id"]}) in the database')
            category.name = new_data['name']
            category.description = new_data['description']

            db.session.add(category)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return category

    @classmethod
    def delete_category(cls, category_id):
        try:
            category = cls.query.filter(cls.id == category_id).first()
            if category is None:
                raise Exception(f'there is no such id({category_id}) in the database')
            db.session.delete(category)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def __repr__(self):
        return f'<Category id:{self.id}, name:{self.name}, description:{self.description}>'


class ArticleSpecification(db.Model):
    __tablename__ = 'article_specification'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    article_id = db.Column(UUID(as_uuid=True), db.ForeignKey('article.id'), nullable=False)
    specification_id = db.Column(UUID(as_uuid=True), db.ForeignKey('specification.id'), nullable=False)

    value = db.Column(db.JSON)

    @classmethod
    def get_art_spec_list(cls):
        try:
            all_art_spec = cls.query.all()
            db.session.commit()
            if not all_art_spec:
                raise Exception('list of all_art_spec is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_art_spec

    @classmethod
    def get_art_spec(cls, art_spec_id):
        try:
            art_spec = cls.query.filter(cls.id == art_spec_id).first()
            if art_spec is None:
                raise Exception(f'there is no such id({art_spec_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return art_spec

    @classmethod
    def save_art_spec(cls, new_data):
        try:
            new_art_spec = cls(value=new_data['value'],
                               article_id=new_data['article_id'],
                               specification_id=new_data['specification_id'])
            db.session.add(new_art_spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_art_spec

    @classmethod
    def update_art_spec(cls, new_data):
        try:
            art_spec = cls.query.filter(cls.id == new_data['id']).first()
            if art_spec is None:
                raise Exception(f'there is no art_spec with this id({new_data["id"]}) in the database')
            if new_data['article_id']:
                art_spec.article_id = new_data['article_id']
            if new_data['specification_id']:
                art_spec.article_id = new_data['specification_id']
            if new_data['value']:
                art_spec.value = new_data['value']

            db.session.add(art_spec)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return art_spec

    @classmethod
    def delete_art_spec(cls, art_spec_id):
        try:
            art_spec = cls.query.filter(cls.id == art_spec_id).first()
            if art_spec is None:
                raise Exception(f'there is no such id({art_spec_id}) in the database')
            db.session.delete(art_spec)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


class CategoryArticle(db.Model):
    __tablename__ = 'category_article'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))
    article_id = db.Column(UUID(as_uuid=True), db.ForeignKey('article.id'))

    @classmethod
    def get_cat_art_list(cls):
        try:
            all_cat_art = cls.query.all()
            db.session.commit()
            if not all_cat_art:
                raise Exception('list of all_cat_art is empty')
        except Exception:
            db.session.rollback()
            raise
        return all_cat_art

    @classmethod
    def get_cat_art(cls, cat_art_id):
        try:
            cat_art = cls.query.filter(cls.id == cat_art_id).first()
            if cat_art is None:
                raise Exception(f'there is no such id({cat_art_id}) in the database')

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return cat_art

    @classmethod
    def save_cat_art(cls, new_data):
        try:
            new_cat_art = cls(article_id=new_data['article_id'],
                              category_id=new_data['category_id'])
            db.session.add(new_cat_art)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return new_cat_art

    @classmethod
    def update_cat_art(cls, new_data):
        try:
            cat_art = cls.query.filter(cls.id == new_data['id']).first()
            if cat_art is None:
                raise Exception(f'there is no cat_art with this id({new_data["id"]}) in the database')
            if new_data['article_id']:
                cat_art.article_id = new_data['article_id']
            if new_data['category_id']:
                cat_art.article_id = new_data['category_id']

            db.session.add(cat_art)
            db.session.commit()

        except Exception:
            db.session.rollback()
            raise
        return cat_art

    @classmethod
    def delete_cat_art(cls, cat_art_id):
        try:
            cat_art = cls.query.filter(cls.id == cat_art_id).first()
            if cat_art is None:
                raise Exception(f'there is no such id({cat_art_id}) in the database')
            db.session.delete(cat_art)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise


