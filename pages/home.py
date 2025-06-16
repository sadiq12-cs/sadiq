from flet import*
from database.quere import Login
from mysql.connector import Error
from database.mydata import get_connection 
import os
import pandas as pd
from datetime import datetime
import platform
import subprocess
class Home :
    def __init__(self,page:Page):
        self.page = page


        self.user_id = self.page.session.get("user_id")
       

        self.us_name = self.page.session.get("us_name")


        self.namefeeder = TextField(
                                                label="name feeder",
                                                icon=Icons.POWER,
                                                border_radius=20,
                                                border_color="transparent",
                                                focused_border_color="#00B0FF",
                                                cursor_color="#00B0FF",
                                                text_style=TextStyle(color="white",size=20),
                                                label_style=TextStyle(color="white"),
                                                filled=True,
                                                fill_color="#1A2B4C",
                                                width=400,
                                                height=60,
                                                value=self.page.session.get("us_name")
                                            )
        
        self.chose2 = Dropdown(
               width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
               border_color="transparent",
               focused_border_color="#00B0FF",
             #  cursor_color="#00B0FF",
               filled=True,
               fill_color="#1A2B4C",
               label="11 or 33",
        options=[
            dropdown.Option("11"),
            dropdown.Option("33"),
            
        ],
            
        )
        self.chose3 = Dropdown(
               width=360,
               
               label="11 or 33",
        options=[
            dropdown.Option("11"),
            dropdown.Option("33"),
            
        ],
            
        )
        self.feeder_id = TextField(
             label="id",

        )
        self.namefeeder1 = TextField(
             label="new name",

        )
       
        self.user_name = TextField(
                                                label="Username",
                                                icon=Icons.PERSON,
                                                border_radius=20,
                                                border_color="transparent",
                                                focused_border_color="#00B0FF",
                                                cursor_color="#00B0FF",
                                                text_style=TextStyle(color="white",size=20),
                                                label_style=TextStyle(color="white"),
                                                filled=True,
                                                fill_color="#1A2B4C",
                                                width=400,
                                                height=60,
                                                value=self.page.session.get("us_name")
                                            )
        self.password = TextField(
                                                label="password",
                                                icon=Icons.PASSWORD,
                                                can_reveal_password=True,
                                                password=True,
                                                width=400,
                                                text_style=TextStyle(color="white",size=20),
                                                label_style=TextStyle(color=Colors.WHITE),
                                                border_radius=20,
                                                border_color="transparent",
                                                focused_border_color="#00B0FF",
                                                cursor_color="#00B0FF",
                                                filled=True,
                                                fill_color="#1A2B4C",
                                            )
        self.chose1 = Dropdown(
               width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
               border_color="transparent",
               focused_border_color="#00B0FF",
             #  cursor_color="#00B0FF",
               filled=True,
               fill_color="#1A2B4C",
               label="user or admin",
        options=[
            dropdown.Option("admin","Admin"),
            dropdown.Option("user","User"),
            
        ],
            
        )
        self.fild_delete = TextField(
             label="user_name ...."
        )

        ####insert users and admin######

    def insert(self,e):
        admin = self.chose1.value
        us_name = self.user_name.value
        pass1 = self.password.value
        id = self.user_id

        db =Login(self.page)

        if admin == "admin":
            sucess ,msg = db.Create_admin(us_name,pass1)
            if sucess :

                snac = SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update()
            else:  
                snac = SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update()  
        elif admin == "user":
            sucess ,msg = db.Create_user(us_name,pass1,id)
            if sucess :

                snac = SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update()
            else:  
                snac = SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update()  


    def delete_user(self,e):
        
        self.dialog =   AlertDialog(
            modal=True,
            title=Text(f"برجاء تحديد أسم المستخدم فقط!!", style=TextStyle(weight=FontWeight.BOLD)),
            content=Container(
            width=400,
            height=400,
            alignment=alignment.center,
            
            padding=10,
            border_radius=10,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                           
                     self.fild_delete       
                            
                    
                ]
            ),
                ),
                actions=[
                    ElevatedButton(
                        "Close  !",
                        icon=Icons.CLOSE,
                        expand=True,
                        bgcolor=Colors.RED_200,
                        on_click=lambda e: [setattr(self.dialog, "open", False), self.page.update()],
                        style =ButtonStyle(
                            color=Colors.WHITE
                        )
                    ),
                    ElevatedButton(
                        "delete",
                        icon=Icons.UPDATE,
                        expand=True,
                        bgcolor=Colors.GREEN_200,
                       on_click=lambda e:self.del_user(e),
                        style =ButtonStyle(
                            color=Colors.BLACK
                        )
                    ),
                ],
                actions_alignment=MainAxisAlignment.END
            )

         
            
        self.page.dialog = self.dialog
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
      


    def del_user(self,e):
         user_name = self.fild_delete.value
         db = Login(self.page)
         success ,msg = db.delete_user_by_id(user_name)

         if success :
               snac = SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
               snac.open =True
               self.page.overlay.append(snac)
               self.page.update()

         else:
               snac = SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
               snac.open =True
               self.page.overlay.append(snac)
               self.page.update()
  
        ####insert users and admin######
    

    def show_users_table(self):
        db = Login(self.page)
        success, users = db.get_all_users_with_creator()
        if success:
            return Column([
                Text("قائمة المستخدمين:", size=20, color="white"),
                DataTable(
                    columns=[
                        DataColumn(label=Text("اسم المستخدم")),
                        DataColumn(label=Text("الرمز")),
                        DataColumn(label=Text("أُنشئ بواسطة")),
                        

                    ],
                    rows=[
                        DataRow(cells=[
                            DataCell(Text(u["username"])),
                             DataCell(Text(u["password"])),
                            DataCell(Text(u["added_by"])),
                           
                        ]) for u in users
                    ]
                )
            ])
        else:
            return Text(users, color="red")
        

    def insert_feeders(self,e):
        
        name = self.namefeeder.value
        id = self.user_id
        db =Login(self.page)
        type1 = self.chose2.value

        success ,msg = db.Create_feeder(name,id,type1)

        if success :
                snac = SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update()
        else:  
                snac = SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
                snac.open=True
                self.page.overlay.append(snac)
                self.page.update() 

    def show_feederss_table(self):
        db = Login(self.page)
        success, users = db.get_all_feeders_with_creator()
        if success:
            return Column(scroll="auto",
                          controls=[
                Text("قائمة المفذيات:", size=20, color="white"),
                DataTable(
                    columns=[
                        DataColumn(label=Text("id")),
                        DataColumn(label=Text("اسم المغذي")),
                        DataColumn(label=Text("نوع المغذي")),
                        DataColumn(label=Text("أُنشئ بواسطة")),
                        

                    ],
                    rows=[
                        DataRow(cells=[
                            DataCell(Text(u["id"])),

                            DataCell(Text(u["feeder_name"])),
                            DataCell(Text(u["feeder_type"])),
                           
                            DataCell(Text(u["added_by"])),
                           
                        ]) for u in users
                    ]
                )
            ])
        else:
            

            return Text(users, color="red")  
        
    def delete_feders(self,e):
            self.dialog =   AlertDialog(
            modal=True,
            title=Text(f"-لحذف المفذي حدد فقط ال (id)", style=TextStyle(weight=FontWeight.BOLD)),
            content=Container(
            width=400,
            height=400,
            alignment=alignment.center,
            
            padding=10,
            border_radius=10,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                      self.feeder_id    
                            
                    
                ]
            ),
                ),
                actions=[
                    ElevatedButton(
                        "Close  !",
                        icon=Icons.CLOSE,
                        expand=True,
                        bgcolor=Colors.RED_200,
                        on_click=lambda e: [setattr(self.dialog, "open", False), self.page.update()],
                        style =ButtonStyle(
                            color=Colors.WHITE
                        )
                    ),
                    ElevatedButton(
                        "delete",
                        icon=Icons.UPDATE,
                        expand=True,
                        bgcolor=Colors.GREEN_200,
                        on_click=lambda e:self.delete_feeder(e),
                        style =ButtonStyle(
                            color=Colors.BLACK
                        )
                    ),
                ],
                actions_alignment=MainAxisAlignment.END
            )

         
            
            self.page.dialog = self.dialog
            self.page.overlay.append(self.dialog)
            self.dialog.open = True
            self.page.update()    

    def delete_feeder(self,e):
        id = self.feeder_id.value
        db = Login(self.page)
        success ,msg = db.delete_feeder_by_id(id)
        if success :
            snac  =SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
            snac.open =True
            self.page.overlay.append(snac)
            self.page.update()
        else:   
            snac  =SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
            snac.open =True
            self.page.overlay.append(snac)
            self.page.update() 


    def update_feders(self,e):
            self.dialog =   AlertDialog(
            modal=True,
            title=Text(f"برجاء ادخال المعلومات التالية للحذف", style=TextStyle(weight=FontWeight.BOLD)),
            content=Container(
            width=400,
            height=400,
            alignment=alignment.center,
            
            padding=10,
            border_radius=10,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                      self.feeder_id,
                      self.namefeeder1,
                      self.chose3,   
                            
                    
                ]
            ),
                ),
                actions=[
                    ElevatedButton(
                        "Close  !",
                        icon=Icons.CLOSE,
                        expand=True,
                        bgcolor=Colors.RED_200,
                        on_click=lambda e: [setattr(self.dialog, "open", False), self.page.update()],
                        style =ButtonStyle(
                            color=Colors.WHITE
                        )
                    ),
                    ElevatedButton(
                        "update",
                        icon=Icons.UPDATE,
                        expand=True,
                        bgcolor=Colors.GREEN_200,
                        on_click=lambda e:self.update_feeder(e),
                        style =ButtonStyle(
                            color=Colors.BLACK
                        )
                    ),
                ],
                actions_alignment=MainAxisAlignment.END
            )

         
            
            self.page.dialog = self.dialog
            self.page.overlay.append(self.dialog)
            self.dialog.open = True
            self.page.update() 

    def update_feeder(self,e):
        id = self.feeder_id.value
        name = self.namefeeder1.value
        type1 = self.chose3.value
        db = Login(self.page)
        success ,msg = db.update_feeder(id,name,type1)
        if success :
            snac  =SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
            snac.open =True
            self.page.overlay.append(snac)
            self.page.update()
        else:   
            snac  =SnackBar(Text(msg,color=Colors.RED),bgcolor=Colors.WHITE)
            snac.open =True
            self.page.overlay.append(snac)
            self.page.update()                              
    def export_events_to_excel(self, e):
        import pandas as pd
        from datetime import datetime
        import os

        from pathlib import Path

        db = Login(self.page)

        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM events")
            data = cur.fetchall()

            if not data:
                self.page.snack_bar = SnackBar(Text("⚠️ لا توجد بيانات لتصديرها"), bgcolor=Colors.ORANGE)
                self.page.snack_bar.open = True
                self.page.update()
                return

            df = pd.DataFrame(data)

            # 🗂️ احفظ في مجلد التنزيلات (Downloads)
            downloads_folder = str(Path.home() / "Downloads")
            filename = f"events_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(downloads_folder, filename)

            df.to_excel(filepath, index=False)

            self.page.snack_bar = SnackBar(
                Text(f"✅ تم الحفظ في: {filepath}"),
                bgcolor=Colors.GREEN
            )

        except Exception as err:
            self.page.snack_bar = SnackBar(Text(f"❌ خطأ أثناء التصدير: {err}"), bgcolor=Colors.RED)

        finally:
            if cur: cur.close()
            if conn: conn.close()
            self.page.snack_bar.open = True
            self.page.update()


    def refresh_page(self, e):
    # إنشاء نسخة جديدة من الواجهة
        new_view = self.get_view()
        
        # مسح جميع المناظر الحالية
        self.page.views.clear()
        
        # إضافة المنظر الجديد
        self.page.views.append(new_view)
        
        # تحديث الصفحة
        self.page.update()


    def get_view(self):

        return View(
            '/home',
            bgcolor = "#101F3C",
            scroll="auto",
           
            controls=[
                 ResponsiveRow(
                    columns=12,
                    controls=[
                        Container(
                            col={"xs": 12, "sm": 12, "md": 6},
                            expand=True,
                            content=Column(

                               [ 
                                    Row(
                    controls = [
                             IconButton(
                        icon=Icons.ARROW_BACK,
                        on_click=lambda x: self.page.go("/feeder")
                    )
                , 
                
                IconButton(
                   
                    icon=Icons.REFRESH,
                    on_click=self.refresh_page,
                  
                    
                ),
                    ]
                )
                  ,
                                   Tabs(
                                       selected_index=0,
                                        animation_duration=300,
                                        unselected_label_color="#94B4C1",
                                        label_color="#FFF2DB",
                                        divider_color="#493D9E",
                                        indicator_color=Colors.WHITE10,
                                        tabs=[


                                            Tab(
                                                icon=Icons.HOME,
                                                 text="الرئيسية",
    content=Container(
        padding=20,
        content=Column(
            horizontal_alignment="center",
            spacing=20,
            controls=[
                Text("👋 مرحبًا بك، مدير النظام", size=24, color="white", weight="bold"),
                Text(
                    "هذا النظام صُمم لإدارة المغذيات الكهربائية، ومتابعة حالات التشغيل والإطفاء بدقة وفعالية.",
                    size=16,
                    color="#E0E0E0",
                    text_align="center",
                ),
                Text(
                    "نهدف لتوفير أدوات تواصل سهلة وفعّالة مع الإدارة.\nنحن معك من أجل التطوير المستمر 🌟",
                    size=16,
                    color="#E0E0E0",
                    text_align="center",
                ),
                Divider(color="white"),

                Text(
                    "⚡ واجهة بسيطة – وظائف قوية\n📈 تقارير دقيقة – تواصل مباشر\n🛠️ دعم مستمر – تحديثات مستقبلية",
                    size=14,
                    color="#B0C4DE",
                    text_align="center",
                )
            ]
        )
    )
                                                
                                                
                                                
                                                ),




                                             Tab(
                                    icon=Icons.ADD,
                                    text="مستخدمين",
                                     content=Container(
        padding=20,
        content=Column(
            horizontal_alignment="center",
            spacing=20,
            controls=[
                Text("👋 مرحبًا بك، مدير النظام", size=24, color="white", weight="bold"),
                Text("أضافة مستخدم جديد,!!", size=24, color="white", weight="bold"),
                self.user_name,
                self.password,
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[Container(content=Text("       ")),self.chose1,]
                ),
                
                
                Divider(color="white"),

                Row(alignment=MainAxisAlignment.CENTER,vertical_alignment=CrossAxisAlignment.CENTER,
                    controls=[ 
                         ElevatedButton("أضافه",icon=Icons.ADD,bgcolor="#9FC87E",color=Colors.WHITE,
                               style=ButtonStyle(
                                   shape=RoundedRectangleBorder(radius=5),
                                   text_style=TextStyle(
                                       weight=FontWeight.BOLD,
                                       size=20
                                   )
                               ),width=150,on_click=self.insert),
                               ElevatedButton("حذف",icon=Icons.ADD,bgcolor="#D74806",color=Colors.WHITE,
                               style=ButtonStyle(
                                   shape=RoundedRectangleBorder(radius=5),
                                   text_style=TextStyle(
                                       weight=FontWeight.BOLD,
                                       size=20
                                   )
                               ),width=150,on_click=self.delete_user),
                               ]
                               )
            ]
        )
    )
                                                    )
                                                    ,
                                              Tab(icon=Icons.VIEW_AGENDA,
                                                  text="عرض المستخدمين",
                                                  
                                                  content=
                                                  
                                                      self.show_users_table()
                                                  ),


                                    Tab(
                                    icon=Icons.POWER,
                                    text="المغذيات",
                                     content=Container(
        padding=20,
        content=Column(
            horizontal_alignment="center",
            spacing=20,
            controls=[
                Text("👋 مرحبًا بك، مدير النظام", size=24, color="white", weight="bold"),
                Text("أضافة مغذي جديد,!!", size=24, color="white", weight="bold"),
                self.namefeeder,
                Row(alignment=MainAxisAlignment.CENTER,
                    vertical_alignment=CrossAxisAlignment.CENTER
                    ,controls=[
                        Text("    "),
                        self.chose2,
                    ]),
                
                
                       Row(alignment=MainAxisAlignment.CENTER,
                           vertical_alignment=CrossAxisAlignment.CENTER,
                           controls=[
                                 ElevatedButton("أضافه",icon=Icons.ADD,bgcolor="#9FC87E",color=Colors.WHITE,
                               style=ButtonStyle(
                                   shape=RoundedRectangleBorder(radius=5),
                                   text_style=TextStyle(
                                       weight=FontWeight.BOLD,
                                       size=20
                                   )
                               ),width=100,on_click=self.insert_feeders),
                              
                                ElevatedButton("حذف",icon=Icons.DELETE,bgcolor="#C64146",color=Colors.WHITE,
                               style=ButtonStyle(
                                   shape=RoundedRectangleBorder(radius=5),
                                   text_style=TextStyle(
                                       weight=FontWeight.BOLD,
                                       size=20
                                   )
                               ),width=100,on_click=self.delete_feders),


                         ElevatedButton("تعديل",icon=Icons.EDIT,bgcolor="#242EA0",color=Colors.WHITE,
                               style=ButtonStyle(
                                   shape=RoundedRectangleBorder(radius=5),
                                   text_style=TextStyle(
                                       weight=FontWeight.BOLD,
                                       size=20
                                   )
                               ),width=100,on_click=self.update_feders),


                           ]),
                
                
              
                                 Divider(color="white"),
                                 self.show_feederss_table()

            ]
        )
    )
                                                    )
                                                    ,

                                    Tab(
                                                icon=Icons.HOME,
                                                 text="الرئيسية",
    content=Container(
        padding=20,
        content=Column(
            horizontal_alignment="center",
            spacing=20,
            controls=[
                
                Text(
                  "بعض من الأدوات المفيدة لعمل النظام بشكل جيد...",
                   
                    color="#E0E0E0",
                 
                    size=20
                ),
               
                Divider(color="white"),
                 Row(
                    alignment=MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ElevatedButton(
                            "📤 تصدير الأحداث إلى Excel",
                            icon=Icons.FILE_DOWNLOAD,
                            bgcolor=Colors.BLUE,
                            color=Colors.WHITE,
                            on_click=self.export_events_to_excel
                        ),
                        ElevatedButton(
                            "🗑️ تفريغ جدول الأحداث",
                            icon=Icons.DELETE_FOREVER,
                            bgcolor=Colors.RED,
                            color=Colors.WHITE,
                           # on_click=self.clear_events_table
                        )
                    ]
                )

              
            ]
        )
    )
                                                
                                                
                                                
                                                ),

                                   

                                        ]

                                   )
                               ]

                            )
                        )
                    ]
                )
            ]
        )