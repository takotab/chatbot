import os
import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from pandas.plotting import table
import numpy as np
import sqlite3
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import datetime
# from matplotlib.pyplot import imshow
import image.make_image as make_image
datetime_ = datetime.datetime
names_dict = {}


def make_plot_of_days(list_w_vacation_days, name):

    dates = list_w_vacation_days
    dates.sort()

    filename = make_image.make_image_vacation(dates, name)
    return len(dates), filename

    # "2913" is Cristina


def get_plot_from_sql(sql_filename, sql_id, true_name=None):
    conn = sqlite3.connect(sql_filename)
    # c = conn.cursor()
    # if not names == '*':
    #     names.append('date')
    #     names.append('INDEX')
    sql_query = "SELECT {} FROM {}".format(",".join("*"), '\'head\'')

    df = pd.read_sql(sql_query, conn)

    dict_w_id = df.loc[df['sql_id'] == int(sql_id)].to_dict()
    row_in_db = int(sql_id) - 1
    list_vacation_days = []
    for c_date in dict_w_id:
        if len(c_date.split("-")) == 3:  # expect dd-mm-yy this is the check
            value = dict_w_id[c_date]
            if value[int(row_in_db)] == 1:
                list_vacation_days.append(
                    datetime_.strptime(c_date, "%d-%m-%y"))
    print(len(list_vacation_days), list_vacation_days)

    vacationdays, filename = make_plot_of_days(
        list_vacation_days, name=true_name)

    return vacationdays, filename

# name = ['takotabak','waltersnel']
# sqlite_file = "randomminidb"
# get_df_from_sql(sqlite_file,name)


def make_image_devoteam(dates, name, total_days=25, logo='devoteam.png',
                        tff_reg="OpenSans-Regular.ttf"):
    #   print(logo)
    logo_img = Image.open(logo).convert("RGB")
    image = Image.new('RGB', (225, 222 + 16 * len(dates)))
    image.paste(logo_img, [0, 0])
    d = ImageDraw.Draw(image)
    d.rectangle([0, 165, 225, 220 + 16 * len(dates)],
                (86, 85, 90))  # black stone
    d.rectangle([0, 185, 225, 190 + len(dates) * 16],
                (248, 72, 94))  # red poppy

    fnt = ImageFont.truetype(tff_reg, 14)
    d.text((30, 168), 'Datum', font=fnt)
    d.text((115, 168), name, font=fnt)
    for i, date in enumerate(dates):
        d.text((20, 190 + i * 16), date.strftime("%d-%b-%y"), font=fnt)
        if date >= datetime.datetime.now():
            d.text((125, 190 + i * 16), "Ingepland", font=fnt)
        else:
            d.text((125 - 5, 190 + i * 16), "Opgenomen", font=fnt)

    d.text((15, 190 + (i + 1) * 16), 'Vakantie dagen', font=fnt)
    d.text((40, 190 + (i + 2) * 16), 'over', font=fnt)
    d.text((140, 190 + (i + 1.5) * 16), str(total_days -
                                            len(dates)) + "/" + str(total_days), font=fnt)

    filename = "dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("vacation", filename))
    return filename



# img = make_image(date, "Melis Schaap", total_days = 25)
if __name__ == "__main__":
    sql_filename = 'sqlite/random_table_dwg.db'
    get_plot_from_sql(sql_filename, "2913", true_name='Melis Schaap')
