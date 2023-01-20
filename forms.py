from wtforms import Form, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired,Length,Email,EqualTo

# Article Form Class
class ArticleForm(Form):
    title = StringField(
        '标题',
        validators=[
            # DataRequired(message= '标题长度应该在2-30字符之间'),
            DataRequired(message='长度不少于5个字符'),
            Length(min=2,max=30)
        ]
    )
    content = TextAreaField(
        '内容',
        validators=[
            DataRequired(message='长度不少于5个字符'),
            Length(min=5)
        ]
    )
   
    zt = TextAreaField(
        '状态',
        validators=[
            DataRequired(message='长度不少于5个字符'),
            Length(min=1)
        ]
    )
