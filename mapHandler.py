import folium
from Configuration_database import repository
import os
import base64

sql = repository.SQL()


def mark(coord, id, map):
    folium.Marker(location=coord, popup=f"App #{id}").add_to(map)


def mark_from_db():
    if os.path.exists("F:\EcoSort_Telegram_BotMagistr\html\map.html"):
        os.remove("F:\EcoSort_Telegram_BotMagistr\html\map.html")
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    coordinates = sql.get_active_app_coordinates()
    encoded_photo_garbage = base64.b64encode(open('eco.jpg', 'rb').read()).decode()
    css = """
        <style>
            .leaflet-control-attribution {
                display: none !important;
            }
        </style>
        """
    map.get_root().html.add_child(folium.Element(css))

    for coord in coordinates:
        icon_html = f"""
        <div style="
            width: 30px;
            height: 30px;
            background-image: url('data:image/jpeg;base64,{encoded_photo_garbage}');
            background-size: cover;        /* Чтобы изображение заполнило круг */
            background-position: center;   /* Центрируем изображение */
            color: black;
            text-align: center;
            border-radius: 50%;
            line-height: 30px;
            font-weight: bold;">
            {coord[2]}
        </div>
        """
        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
                <div"> 
                <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
                <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
                🔰Заявка №{coord[2]}<br>
                Статус заявки:<br>{coord[4]}<br>
                🌐 Место положение:<br>{coord[5]}<br>
                ⏰ Дата и время:<br>{coord[6]} 
                </div>
                </div>
                """
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
    map.save("html/map.html")


def mark_from_db_user(user_id):
    if os.path.exists("F:\EcoSort_Telegram_BotMagistr\html\garbage.html"):
        os.remove("F:\EcoSort_Telegram_BotMagistr\html\garbage.html")
    map = folium.Map(location=[59.935699, 30.312334], zoom_start=10)
    coordinates = sql.get_active_app_coordinates_user(user_id)
    encoded_photo_pothole = base64.b64encode(open('eco.jpg', 'rb').read()).decode()
    css = """
            <style>
                .leaflet-control-attribution {
                    display: none !important;
                }
            </style>
            """
    map.get_root().html.add_child(folium.Element(css))

    for coord in coordinates:
        icon_html = f"""
            <div style="
                width: 30px;
                height: 30px;
                background-image: url('data:image/jpeg;base64,{encoded_photo_pothole}');
                background-size: cover;        /* Чтобы изображение заполнило круг */
                background-position: center;   /* Центрируем изображение */
                color: black;
                text-align: center;
                border-radius: 50%;
                line-height: 30px;
                font-weight: bold;">
                {coord[2]}
            </div>
            """
        encoded = base64.b64encode(coord[3]).decode()

        # создаем HTML с изображением и текстом под ним
        html_content = f"""
                    <div"> 
                    <img src="data:image/png;base64,{encoded}" style = "max-width:100%;height:auto;display: block;">
                    <div style="text-align: left;margin-top: 10px;font-weight: bold;"> 
                    🔰Заявка №{coord[2]}<br>
                    Статус заявки:<br>{coord[4]}<br>
                    🌐 Место положение:<br>{coord[5]}<br>
                    ⏰ Дата и время:<br>{coord[6]} 
                    </div>
                    </div>
                    """
        iframe = folium.IFrame(html_content, width=200, height=300)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(location=(coord[0], coord[1]), popup=popup, icon=folium.DivIcon(html=icon_html)).add_to(map)
    map.save(f"html/map{user_id}.html")



