import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import datetime
logo = os.path.join("image", 'vergelijken.png')
print(open(logo))


def make_image_vacation(dates, name, total_days = 25, logo = 'De_Watergroep.jpg',
                        tff_reg = "OpenSans-Regular.ttf"):
    tff_reg = os.path.join("image", tff_reg)
    logo = os.path.join("image", logo)

    # Colors of DWG corporate identity
    #  DWG_green = Color((164,196,49))  #hoe definieer ik een kleur?
    #  DWG_blue = RGB(52,84,163)
    fnt = ImageFont.truetype(tff_reg, 14)

    width = 225  # The width of the table
    text_height = 16
    logo_img = Image.open(logo).convert("RGB")
    # calculating the height of the logo if the width is the right size.
    logo_scaled_height = round(logo_img.size[1] * width / logo_img.size[0])
    logo_img = logo_img.resize((width, logo_scaled_height))
    image = Image.new('RGB', (width, logo_scaled_height +
                              text_height * (len(dates) + 3) + 15))

    d = ImageDraw.Draw(image)
    y_c = 0  # current height
    image.paste(logo_img, [0, 0])
    y_c += logo_scaled_height
    d.rectangle([0, y_c, width, y_c + 30], (164, 196, 49))  # Green back-ground
    d.text((30, y_c), 'Datum', font = fnt)
    d.text((115, y_c), name, font = fnt)
    y_c += text_height + 5
    d.rectangle([0, y_c, width, y_c + len(dates) * text_height + 20],
                (52, 84, 163))  # Blue back-ground

    # Text print
    for i, date in enumerate(dates):
        d.text((20, y_c), date.strftime("%d-%b-%y"), font = fnt)
        if date >= datetime.datetime.now():
            d.text((125, y_c), "Ingepland", font = fnt)
        else:
            d.text((125 - 5, y_c), "Opgenomen", font = fnt)
        y_c += text_height

    y_c += 5
    d.rectangle([0, y_c, width, y_c + 40], (164, 196, 49))  # Green back-ground
    d.text((15, y_c), 'Vakantiedagen', font = fnt)
    # print(PIL.ImageFont.ImageFont.getsize('Vakantiedagen'))
    d.text((40, y_c + text_height), 'over', font = fnt)
    d.text((140, y_c + text_height / 2), str(total_days -
                                             len(dates)) + "/" + str(total_days), font = fnt)

    filename = "vacation_dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("image", "generated", filename))
    return filename


def make_image_verhuizen(info_dict, name, logo ='verhuizen.png', tff_reg = "OpenSans-Regular.ttf"):
    logo = os.path.join("image", logo)
    tff_reg = os.path.join("image", tff_reg)
    # Colors of DWG corporate identity

    #Color = namedtuple("Color", "R G B")
    #DWG_green = Color(164,196,49)
    #  DWG_green = Color((164,196,49))  #hoe definieer ik een kleur?
    #  DWG_blue = RGB(52,84,163)
    fnt = ImageFont.truetype(tff_reg, 14)
    fnt_header = ImageFont.truetype(tff_reg, 18)

    width = 430  # The width of the table
    text_height = 16
    logo_img = Image.open(logo).convert("RGB")
    # calculating the height of the logo if the width is the right size.
    logo_scaled_height = round(logo_img.size[1] * width / logo_img.size[0])
    logo_img = logo_img.resize((width, logo_scaled_height))
    image = Image.new(
        'RGB', (width, logo_scaled_height + text_height * 6 + 15))

    d = ImageDraw.Draw(image)
    y_c = 0  # current height
    image.paste(logo_img, [0, 0])
    y_c += logo_scaled_height
    d.rectangle([0, y_c, width, y_c + 30],
                (164, 196, 49))  # Green back-ground
    d.text((30, y_c), "Verhuizing doorgeven", font = fnt_header)
    y_c += text_height + 4 + 5
    d.rectangle([0, y_c, width, y_c + 4 * text_height + 5],
                (52, 84, 163))  # Blue back-ground

    # Text print
    # info = ["nlp_street", "nlp_postcode", "nlp_loc",
    # "sql_street", "sql_postcode", "sql_city"]
    d.text(
        (20, y_c), "Hartelijk bedankt voor het doorgeven van uw nieuwe adres.", font = fnt)
    y_c += text_height
    d.text((20, y_c), "Uw nieuwe adres is " + info_dict["nlp_street"] +
           ", " + info_dict["nlp_postcode"] + " " + info_dict["nlp_loc"] + ".", font = fnt)
    y_c += text_height
    d.text((20, y_c), "Uw oude adres was " + info_dict["sql_street"] +
           ", " + info_dict["sql_postcode"] + " " + info_dict["sql_city"] + ".", font = fnt)
    y_c += text_height
    d.text((20, y_c), "Veel plezier in uw nieuwe woning.", font = fnt)
    y_c += text_height

    y_c += 5
    d.rectangle([0, y_c, width, y_c + text_height],
                (164, 196, 49))  # Green back-ground
    filename = "vacation_dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("image", "generated", filename))
    return filename


def make_image_factuur(name, persoonsgegevens, factuur = 'watergroep_factuur.png',
                       tff_reg = "OpenSans-Regular.ttf",
                       tff_bold = "OpenSans-Bold.ttf"):
    # persoonsgegevens = {"date":"13-03-2018","city":"Amsterdam","street":"Paasheuvelweg","number":"26","zipcode":"4323 GB","service_id":"0000000000"
                    # ,"firstName":"Klaas","lastName":"Jan","invoice_period":"22-09-2017 tot 10-01-2018","euro_amount":np.random.randint(1,99)}
    tff_reg = os.path.join("image", tff_reg)
    factuur = os.path.join("image", factuur)
    tff_bold = os.path.join("image", tff_bold)

    date = datetime.datetime.now()
    persoonsgegevens['date'] = date.strftime("%d-%b-%y")
    persoonsgegevens["euro_amount"] = np.random.randint(1, 99)
    persoonsgegevens["service_id"] = str(str(persoonsgegevens["sql_id"]).zfill(10))

    excl_btw = persoonsgegevens["euro_amount"] / 1.06
    btw = persoonsgegevens["euro_amount"] - excl_btw

    #Color = namedtuple("Color", "R G B")
    #DWG_green = Color(164,196,49)
    #  DWG_green = Color((164,196,49))  #hoe definieer ik een kleur?
    #  DWG_blue = RGB(52,84,163)
    fnt = ImageFont.truetype(tff_reg, 25)
    fnt_header = ImageFont.truetype(tff_reg, 25)
    fnt_small = ImageFont.truetype(tff_reg, 20)
    fnt_bold = ImageFont.truetype(tff_bold, 25)
    fnt_bold_small = ImageFont.truetype(tff_bold, 20)
    fnt_bold_large = ImageFont.truetype(tff_bold, 35)

    width = 1920  # The width of the table
    text_height = 28
    factuur_img = Image.open(factuur).convert("RGB")
    # calculating the height of the factuur_image if the width is the right size.
    factuur_scaled_height = round(factuur_img.size[1] * width / factuur_img.size[0])
    factuur_img = factuur_img.resize((width, factuur_scaled_height))
    image = Image.new('RGB', (width, factuur_scaled_height + text_height * 1 + 1))

    d = ImageDraw.Draw(image)
    y_c = 360  # current height
    image.paste(factuur_img, [0, 0])
    # y_c+=factuur_scaled_height
    # d.rectangle([0,y_c,width, y_c+30],(164,196,49)) # Green back-ground
    #d.text((width/2-70, y_c),"Zaal reserveren", font = fnt_header)
    # y_c+=text_height+4+5
    # d.rectangle([0,y_c,width,y_c + 4*text_height+5],(52,84,163)) # Blue back-ground

    # Text print
    d.text((175, y_c), "leveringsadres", font = fnt_bold, fill=(0, 0, 0, 0))
    y_c += (3 * text_height)
    d.text((175, y_c), "Service-ID: " +
           persoonsgegevens["service_id"], font = fnt, fill=(0, 0, 0, 0))
    y_c += text_height
    d.text((175, y_c), persoonsgegevens["nlp_f_name"] + " " +
           persoonsgegevens["nlp_l_name"], font = fnt, fill=(0, 0, 0, 0))
    y_c += text_height
    d.text((175, y_c), persoonsgegevens["sql_street"], font = fnt, fill=(0, 0, 0, 0))
    y_c += text_height
    d.text((175, y_c), persoonsgegevens["sql_postcode"] + " " +
           persoonsgegevens["sql_city"], font = fnt, fill=(0, 0, 0, 0))

    y_c = 360  # reset height
    d.text((930, y_c), "Afz. De Watergroep West-Vlaanderen - Roggelaan 2, 8500 Kortrijk",
           font = fnt_small, fill=(0, 0, 0, 0))

    y_c += (3 * text_height)
    d.text((930, y_c), persoonsgegevens["nlp_f_name"] + " " +
           persoonsgegevens["nlp_l_name"], font = fnt_bold, fill=(0, 0, 0, 0))
    y_c += text_height
    d.text((930, y_c), persoonsgegevens["sql_street"], font = fnt, fill=(0, 0, 0, 0))
    y_c += text_height
    d.text((930, y_c), persoonsgegevens["sql_postcode"] + " " +
           persoonsgegevens["sql_city"], font = fnt, fill=(0, 0, 0, 0))

    y_c = 830  # reset height
    d.text((185, y_c), "verbruiksperiode:" + " " +
           persoonsgegevens["invoice_period"], font = fnt, fill=(0, 0, 0, 0))

    d.text((1740, y_c), str("%.2f" %
                            (persoonsgegevens["euro_amount"])), font = fnt_bold, fill=(0, 0, 0, 0))

    d.text((1180, y_c), str("%.2f" % (excl_btw)), font = fnt, fill=(0, 0, 0, 0))

    d.text((1350, y_c), str("%.2f" % (btw)), font = fnt, fill=(0, 0, 0, 0))

    d.text((1485, y_c), "6%", font = fnt, fill=(0, 0, 0, 0))

    y_c += (3 * text_height)
    d.text((185, y_c), "Totaal excl. BTW", font = fnt, fill=(0, 0, 0, 0))
    d.text((1740, y_c), str("%.2f" % (excl_btw)), font = fnt, fill=(0, 0, 0, 0))

    d.text((1740, y_c), str("%.2f" % (excl_btw)), font = fnt, fill=(0, 0, 0, 0))
    y_c += (2 * text_height)
    d.text((185, y_c), "BTW 6%", font = fnt, fill=(0, 0, 0, 0))
    d.text((1740, y_c), str("%.2f" % (btw)), font = fnt, fill=(0, 0, 0, 0))
    y_c += (2 * text_height)
    d.text((185, y_c), "Factuur totaal", font = fnt_bold, fill=(0, 0, 0, 0))
    d.text((1740, y_c), str("%.2f" %
                            (persoonsgegevens["euro_amount"])), font = fnt_bold, fill=(0, 0, 0, 0))

    y_c += (4 * text_height)
    d.text((1600, y_c), str("%.2f" %
                            (persoonsgegevens["euro_amount"])) + " " + "EURO", font = fnt_bold_large, fill=(0, 0, 0, 0))

    # y_c+=5
    # d.rectangle([0,y_c,width, y_c+text_height],(164,196,49)) # Green back-ground
    # imshow(image)
    filename = "factuur_dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("image", "generated", filename))
    return filename


def make_image_meeting(name, info_dict, logo = 'reservering.png',
                       tff_reg = "OpenSans-Regular.ttf"):
    tff_reg = os.path.join("image", tff_reg)
    logo = os.path.join("image", logo)
    # tff_bold = os.path.join("image", tff_bold)
    # Colors of DWG corporate identity

    #Color = namedtuple("Color", "R G B")
    #DWG_green = Color(164,196,49)
    #  DWG_green = Color((164,196,49))  #hoe definieer ik een kleur?
    #  DWG_blue = RGB(52,84,163)
    info_dict["begintijd"] = info_dict['time'].strftime("%H:%M")
    info_dict["eindtijd"] = info_dict['time'].strftime("%H:%M")
    info_dict["datum"] = info_dict['time'].strftime("%d-%m")
    fnt = ImageFont.truetype(tff_reg, 14)
    fnt_header = ImageFont.truetype(tff_reg, 18)

    width = 280  # The width of the table
    text_height = 16
    logo_img = Image.open(logo).convert("RGB")
    # calculating the height of the logo if the width is the right size.
    logo_scaled_height = round(logo_img.size[1] * width / logo_img.size[0])
    logo_img = logo_img.resize((width, logo_scaled_height))
    image = Image.new('RGB', (width, logo_scaled_height + text_height * 5 + 12))

    d = ImageDraw.Draw(image)
    y_c = 0  # current height
    image.paste(logo_img, [0, 0])
    y_c += logo_scaled_height
    d.rectangle([0, y_c, width, y_c + 30], (164, 196, 49))  # Green back-ground
    d.text((width / 2 - 70, y_c), "Zaal reserveren", font = fnt_header)
    y_c += text_height + 4 + 5
    d.rectangle([0, y_c, width, y_c + 4 * text_height + 5], (52, 84, 163))  # Blue back-ground

    # Text print
    d.text((20, y_c), "Uw reservering is afgerond.", font = fnt)
    y_c += text_height
    d.text((20, y_c), "U heeft de " + info_dict["loc"] + " gereserveerd", font = fnt)
    y_c += text_height
    d.text((20, y_c), "voor " + info_dict["datum"] + " van " +
           info_dict["begintijd"] + " tot " + info_dict["eindtijd"] + ".", font = fnt)
    y_c += text_height

    y_c += 5
    d.rectangle([0, y_c, width, y_c + text_height], (164, 196, 49))  # Green back-ground

    filename = "meeting_dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("image", "generated", filename))
    return filename


def make_image_vergelijken(name, persoonsgegevens, logo = 'vergelijken.png',
                           tff_reg = "OpenSans-Regular.ttf"):
    tff_reg = os.path.join("image", tff_reg)
    logo = os.path.join("image", logo)
    # Colors of DWG corporate identity

    #Color = namedtuple("Color", "R G B")
    #DWG_green = Color(164,196,49)
    #  DWG_green = Color((164,196,49))  #hoe definieer ik een kleur?
    #  DWG_blue = RGB(52,84,163)
    fnt = ImageFont.truetype(tff_reg, 14)
    fnt_header = ImageFont.truetype(tff_reg, 18)

    width = 430  # The width of the table
    text_height = 16
    logo_img = Image.open(logo).convert("RGB")
    # calculating the height of the logo if the width is the right size.
    logo_scaled_height = round(logo_img.size[1] * width / logo_img.size[0])
    logo_img = logo_img.resize((width, logo_scaled_height))
    image = Image.new('RGB', (width, logo_scaled_height + text_height * 5 + 15))
    d = ImageDraw.Draw(image)
    y_c = 0  # current height
    image.paste(logo_img, [0, 0])
    y_c += logo_scaled_height
    d.rectangle([0, y_c, width, y_c + 30], (164, 196, 49))  # Green back-ground
    d.text((width / 2 - 100, y_c), "Waterstand vergelijken", font = fnt_header)
    y_c += text_height + 4 + 5
    d.rectangle([0, y_c, width, y_c + 4 * text_height + 5], (52, 84, 163))  # Blue back-ground

    # Text print
    d.text((20, y_c), "Uw waterstand is " +
           str(persoonsgegevens["waterstand"]) + ' m' + u'\u00B3.', font = fnt)
    y_c += text_height
    d.text((20, y_c), "Een gemiddeld huishouden heeft een stand van " +
           str(persoonsgegevens["waterstand_norm"]) + ' m' + u'\u00B3.', font = fnt)
    y_c += text_height
    d.text((20, y_c), "U gebruikt dus " + persoonsgegevens["vergelijking"], font = fnt)
    y_c += text_height

    y_c += 5
    d.rectangle([0, y_c, width, y_c + text_height], (164, 196, 49))  # Green back-ground

    filename = "vergelijken_dyn_" + name.replace(" ", "_").lower() + ".png"
    image.save(os.path.join("image", "generated", filename))
    return filename
