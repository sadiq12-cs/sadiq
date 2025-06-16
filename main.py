import flet 
from flet import*
from database.mydata import get_connection,create_database
from pages.index import Index
from pages.home import Home
from pages.feeders import Feeder
import mysql.connector

 
def main(page: Page):
    
    create_database()
    page.window.width= 500
    page.window.height = 900
    page.scroll = "auto"
    page.bgcolor = "#101F3C"
    page.rtl =True


    def route_change(e):
        page.views.clear()

        if page.route == "/":
            view = Index(page).get_view()
        elif page.route == "/feeder":
            view = Feeder(page).get_view()    
        elif page.route == "/home":
            view = Home(page).get_view()
        


            
             
                      
               
        page.views.append(view)
        

        page.update()
    
    page.on_route_change = route_change
    page.go(page.route)

flet.app(target=main)
