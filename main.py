import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
SECRET_KEY = os.urandom(64)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
  cafe = StringField('Cafe name', validators=[DataRequired()])
  location = StringField('Location', validators=[DataRequired()])
  open = StringField('Open Time e.g. 0800', validators=[DataRequired()])
  close = StringField('Close Time e.g. 1900', validators=[DataRequired()])
  coffee = SelectField(label='Coffe Rating',
                       choices=[("1", "☕"), ("2", "☕☕"), ("3", "☕☕☕"),
                                ("4", "☕☕☕☕"), ("5", "☕☕☕☕☕"), ("0", "✘")],
                       validators=[DataRequired()])
  wifi = SelectField(label='WI-FI Rating',
                     choices=[("1", "🛜"), ("2", "🛜🛜"), ("3", "🛜🛜🛜"),
                              ("4", "🛜🛜🛜🛜"), ("5", "🛜🛜🛜🛜🛜"), ("0", "✘")],
                     validators=[DataRequired()])
  power = SelectField(label='Power Rating',
                      choices=[("1", "💪"), ("2", "💪💪"), ("3", "💪💪💪"),
                               ("4", "💪💪💪💪"), ("5", "💪💪💪💪💪"), ("0", "✘")],
                      validators=[DataRequired()])
  
  submit = SubmitField('Submit')


@app.route("/")
def home():
  return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
  form = CafeForm()
  if form.validate_on_submit():
    with open('./static/data/cafe-data.csv', 'a') as csv_file:
      csv_file.writelines(f"\n{form.cafe.data},{form.location.data},{form.open.data},"
                          f"{form.close.data}, {form.coffee.data}, {form.wifi.data}, {form.power.data}")
      return redirect(url_for('cafes'))
  return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
  with open('static/data/cafe-data.csv', newline='', encoding='utf-8') as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    list_of_rows = []
    for row in csv_data:
      list_of_rows.append(row)
  return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
  app.run(debug=True)
