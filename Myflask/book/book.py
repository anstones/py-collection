from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# CREATE DATABASE flask_books CHARACTER SET utf8

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@192.168.253.128:3306/flask_books"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'Curtis&|'

db = SQLAlchemy(app)

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(16), unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        return 'Author:%s' % self.name

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(16), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        return 'Books:%s %s' % (self.name, self.author_id)

# 自定义表单类
class AuthorForm(FlaskForm):
    author = StringField('作者：', validators=[DataRequired()])
    book = StringField('书籍：', validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/', methods=['GET', 'POST'])
def index():
    author_form = AuthorForm()

    if author_form.validate_on_submit():
        author_name = author_form.author.data
        book_name = author_form.book.data
        author = Author.query.filter_by(author_name=author_name).first()
        if author:
            book = Book.query.filter_by(book_name=book_name).first()
            if book:
                flash("已存在同名书籍")
            else:
                try:
                    new_book = Book(book_name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("添加书籍失败")
                    db.session.rollback()
        else:
            new_author = Author(author_name=author_name)
            db.session.add(new_author)
            db.session.commit()
            new_book = Book(book_name=book_name, author_id=new_author.id)
            db.session.add(new_book)
            db.session.commit()
    else:
        if request.method == 'POST':
            flash("参数不全")

    authors = Author.query.all()

    return render_template('book.html', authors=authors, form=author_form)

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除书籍出错")
            db.session.rollback()
    else:
        flash("未找到要删除的数据")
    return redirect(url_for('index'))

@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            Book.query.filter_by(author_id=author_id).delete()
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("删除作者失败")
            db.session.rollback()
    else:
        flash("作者未找到")
    return redirect(url_for('index'))

if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    #
    # au1 = Author(author_name='尤瓦尔·赫拉利')
    # au2 = Author(author_name='瑞·达利欧')
    # au3 = Author(author_name='稻盛和夫')
    #
    # db.session.add_all([au1, au2, au3])
    # db.session.commit()
    #
    # bk1 = Book(book_name='未来简史', author_id=au1.id)
    # bk2 = Book(book_name='原则', author_id=au2.id)
    # bk3 = Book(book_name='活法', author_id=au3.id)
    # bk4 = Book(book_name='干法', author_id=au3.id)
    #
    # db.session.add_all([bk1, bk2, bk3, bk4])
    # db.session.commit()

    app.run(debug=True)
