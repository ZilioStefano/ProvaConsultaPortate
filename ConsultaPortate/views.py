from django.shortcuts import render
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import folium
from statistics import mean


def image_to_base64(image):

    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    img_str = img_str.decode("utf-8")  # convert to str and cut b'' chars

    return img_str


def createPlot(data, Name):

    if Name == "Merone3":
        yMax = 150
        Name = "Merone III salto"
    else:
        yMax = 150

    t = data["t"]
    # t = pd.to_datetime(t, format='%d/%m/%Y %H:%M:%S')
    # Q = np.array(data["Q"])
    Q = data["Q"]
    fig1 = px.line(x=t, y=Q, template="ggplot2")
    fig1.update_layout(yaxis_range=[0, yMax], xaxis_title="", yaxis_title="Portata [l/s]", paper_bgcolor='whitesmoke',
                       height=800)
    dataPlot = fig1.to_html(Name+".html")

    return dataPlot


def createHistogram(data, Name):

    if Name == "Merone3":
        xMax = 120
        xMin = 0
        Name = "Merone III salto"
    else:
        xMax = 150
        xMin = -10

    Q = data["Q"]
    NSamples = len(Q)

    fig1 = px.histogram(Q) #, template="ggplot2", title=Name)
    fig1.update_layout(xaxis_range=[xMin, xMax], xaxis_title="Portata [ l/s ]", yaxis_title="Conteggi [minuti]", paper_bgcolor='whitesmoke', bargap=0.1, height=500)
    dataPlot = fig1.to_html("Histo"+Name+".html")

    return dataPlot


def HomePage(request):

    #   CARICO LA LISTA DEI MISURATORI
    MeasureList = pd.read_excel("Misuratori installati.xlsx")
    Lat = MeasureList["Latitudine"]
    Long = MeasureList["Longitudine"]

    Name = MeasureList["Punto di misura"]
    MeanLat = mean(Lat)
    MeanLong = mean(Long)

    figure = folium.Figure()
    map = folium.Map(location = [MeanLat, MeanLong],  zoom_start=9, control_scale=True,
                     tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                     attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')

    for i in range(len(Lat)):
        folium.Marker(location=[Lat[i], Long[i]], tooltip=Name[i], max_width=2000,
                     icon=folium.Icon(icon='fa-weight-scale', prefix='fa')).add_to(map)

    map.add_to(figure)
    figure.render()
    figure2 = map._repr_html_()

    Template = "HP.html"
    Logo = Image.open('im innovation logo abbreviato BASSA RISOLUZIONE.png')
    Logo64 = image_to_base64(Logo)

    Graphs = {"Map": figure2, "Logo": Logo64}

    #   CREO LA MAPPA
    #   carico nel template

    return render(request, Template, context=Graphs)


def Trebisacce(request):

    data = pd.read_csv("PortateTrebisacce.csv")
    Graph = createPlot(data, "Trebisacce")
    Histo = createHistogram(data, "Trebisacce")
    Logo = Image.open('im innovation logo abbreviato BASSA RISOLUZIONE.png')
    Logo64 = image_to_base64(Logo)
    Graphs = {"Graph": Graph, "Histo": Histo, "Logo": Logo64, "Name": "Partitore Trebisacce"}

    Template = "Misure.html"

    return render(request, Template, context=Graphs)


def Merone3(request):

    data = pd.read_csv("PortateMerone3.csv")
    Graph = createPlot(data, "Merone3")
    Histo = createHistogram(data, "Merone3")
    Logo = Image.open('im innovation logo abbreviato BASSA RISOLUZIONE.png')
    Logo64 = image_to_base64(Logo)
    Graphs = {"Graph": Graph, "Histo": Histo, "Logo": Logo64, "Name": "Merone III salto"}

    Template = "Misure.html"

    return render(request, Template, context=Graphs)
