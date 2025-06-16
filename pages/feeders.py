from database.quere import*
from flet import *
from datetime import datetime



class Feeder:
    def __init__(self, page: Page):
        self.page = page
        self.feeder_list_column = Column()


        self.user_id = self.page.session.get("user_id")
        self.user_role = self.page.session.get("user_role")
        self.admin_id = None
        if self.user_role == "admin":
            self.admin_id = self.user_id
            self.user_id = None
        else:
            self.admin_id = None

        self.us_name = self.page.session.get("us_name")


        self.note_title = TextField(label="عنوان الملاحظة",
                                     color="white", 
                                     border_color="white")
        self.note_content = TextField(
            label="محتوى الملاحظة",
            multiline=True,
            min_lines=15,
            max_lines=20,
            color="white",
            border_color="white"
        )
        self.hour_dropdown = Dropdown(width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
        options=[dropdown.Option(str(h)) for h in range(24)],  # 0 إلى 23
        label="ساعة الإطفاء"
    )

    # قائمة لاختيار الدقيقة
        self.minute_dropdown = Dropdown(width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
            options=[dropdown.Option(str(m).zfill(2)) for m in range(0, 60, 5)],  # 00, 05, 10, ..., 55
            label="الدقيقة"
    )
            
        self.chose1 =  TextField(
            label="سبب الاطفاء",
            multiline=True,
            min_lines=5,
            max_lines=5,
            color="white",
            border_color="white"
        )

        self.hour_dropdown1 = Dropdown(width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
        options=[dropdown.Option(str(h)) for h in range(24)],  # 0 إلى 23
        label="ساعة التشفيل"
    )

    # قائمة لاختيار الدقيقة
        self.minute_dropdown1 = Dropdown(width=360,
               text_style=TextStyle(color="white",size=20),
               label_style=TextStyle(color=Colors.WHITE),
               border_radius=20,
            options=[dropdown.Option(str(m).zfill(2)) for m in range(0, 60, 5)],  # 00, 05, 10, ..., 55
            label="الدقيقة"
    ) 
        
        self.search_field = TextField(
            label="البحث عن مفذي..",
            prefix_icon=Icons.SEARCH,
            width=200,
            height=60,border_radius=15,
            text_style=TextStyle(
                weight=FontWeight.BOLD,
                size=20,
            ),
          on_change=self.search_feeders
        ) 
      

   

    def show_note(self):
        self.page.update()
        db = Login(self.page)
        success, msg = db.get_all_feeders_with_creator()

        if success:
            self.page.update()
            rows = []

            # ترويسة الأعمدة
            header = Container(
                content=Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text("اسم المغذي", weight=FontWeight.BOLD, color=Colors.YELLOW, expand=True),
                        Text("الجهد          ", weight=FontWeight.BOLD, color=Colors.YELLOW, expand=True),
                        Text("تحكم", weight=FontWeight.BOLD, color=Colors.YELLOW)
                    ]
                ),
                bgcolor="#1A2B4C",
                padding=10,
                border_radius=6,
                margin=margin.only(bottom=10)
            )
            rows.append(header)

            # بقية الصفوف
            for count in msg:
                row1 = self.get_show_note(
                    count['id'],
                    count['feeder_name'],
                    count['feeder_type']
                )
                rows.append(row1)

            self.feeder_list_column.controls.clear()
            self.feeder_list_column.controls.extend(rows)
            self.page.update()

            self.page.update()
            return rows
        else:
            print(f"-----------{msg}")
            self.page.update()
 

    
    def get_show_note(self, id, feeder_name, added_by):
        return Container(
            content=Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text(feeder_name, size=16, color=Colors.WHITE, expand=True),
                    Text(added_by, size=16, color=Colors.WHITE, expand=True),
                    Row(
                        spacing=10,
                        controls=[
                            ElevatedButton(
                                "أطفاء",
                                bgcolor="red",
                                color=Colors.WHITE,
                                on_click=lambda e, id_feeder=id, name=feeder_name: self.shut_down(e, id_feeder, name),
                                style=ButtonStyle(
                                    text_style=TextStyle(weight=FontWeight.BOLD, size=14)
                                )
                            ),
                            ElevatedButton(
                                "تشغيل",
                                bgcolor="green",
                                color=Colors.WHITE,
                                on_click=lambda e, id_feeder=id, name=feeder_name: self.turn_on(e, id_feeder, name),
                                style=ButtonStyle(
                                    text_style=TextStyle(weight=FontWeight.BOLD, size=14)
                                )
                            )
                        ]
                    )
                ]
            ),
            bgcolor="#0B1D51",
            padding=10,
            border_radius=8,
            border=border.all(0.3, Colors.AMBER),
            margin=margin.only(bottom=5)
        )
    
    def shut_down(self,e,id_feeder,name):
        self.dialog =   AlertDialog(
            modal=True,
            title=Text(f"-{name}-{id_feeder}", style=TextStyle(weight=FontWeight.BOLD)),
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
                           Text("حدد وقت وسبب الاطفاء لطفاً",size=20),
                            self.hour_dropdown,
                            self.minute_dropdown,
                            self.chose1
                    
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
                        on_click=lambda e,id = id_feeder :self.insert_shut_down(e,id),
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


    def insert_shut_down(self,e,id):
        hour = int(self.hour_dropdown.value)
        minet = int(self.minute_dropdown.value)
        id_user = self.user_id
        id_admin = self.admin_id
        resone = self.chose1.value
        db = Login(self.page)
        now = datetime.now()

    # إنشاء وقت الإطفاء بناءً على اليوم الحالي والوقت المُدخل
        off_time = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=hour,
            minute=minet
        )
        print("feeder_id:", id, type(id))
        print("off_time_str:", off_time, type(off_time))
        print("reason:", resone, type(resone))
        print("added_by_admin_id:", id_admin, type(id_admin))
        print("added_by_user_id:", id_user, type(id_user))

        success ,msg = db.insert_event(id,off_time,resone,id_admin,id_user)
        print("✅ النتيجة:", success, msg)

        if success :
            snac  =SnackBar(Text(msg,color=Colors.GREEN),bgcolor=Colors.WHITE)
            snac.open =True
            self.page.overlay.append(snac)
            self.page.update()

            
        









    def turn_on(self,e,id_feeder,name):
        self.dialog =   AlertDialog(
            modal=True,
            title=Text(f"-{name}-{id_feeder}", style=TextStyle(weight=FontWeight.BOLD)),
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
                           Text("حدد وقت التشغيل لطفاً",size=20),
                            self.hour_dropdown1,
                            self.minute_dropdown1,
                            
                    
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
                        on_click=lambda e,id = id_feeder :self.insert_turn_on(e,id),
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




    def insert_turn_on(self,e,id):
        hour = int(self.hour_dropdown1.value)
        minet = int(self.minute_dropdown1.value)
      
      
        db = Login(self.page)
        now = datetime.now()

    # إنشاء وقت الإطفاء بناءً على اليوم الحالي والوقت المُدخل
        on_time = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=hour,
            minute=minet
        )
        print("feeder_id:", id, type(id))
        print("on_time:", on_time, type(on_time))

    

        success ,msg = db.update_event_on_time(id,on_time)
        
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


    def show_events(self):
        db = Login(self.page)
        events_data = db.fetch_events()

        rows = []
        for row in events_data:
            feeder_name = row['feeder_name']
            feeder_type = row['feeder_type']
            off_time = row['off_time']
            on_time = row['on_time']

            # استخراج الساعة والدقيقة فقط من وقت الإطفاء
            if hasattr(off_time, "strftime"):
                off_time_str = off_time.strftime("%H:%M")
            else:
                off_time_str = str(off_time)[11:16]

            # تحديد الحالة واللون بناءً على وقت التشغيل
            if on_time is None:
                color = Colors.RED_200
                status = "لم يعمل بعد"
            else:
                color = Colors.GREEN_700
                on_time_str = (
                    on_time.strftime("%H:%M") if hasattr(on_time, "strftime") else str(on_time)[11:16]
                )
                status = f"تم التشغيل: {on_time_str}"

            rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(feeder_name, weight=FontWeight.BOLD)),
                        DataCell(Text(str(feeder_type), weight=FontWeight.BOLD)),
                        DataCell(Text(off_time_str, weight=FontWeight.BOLD)),
                        DataCell(Text(status, weight=FontWeight.BOLD)),
                    ],
                    color=color
                )
            )

        return [
            Text(
                "بيانات الأحداث",
                size=24,
                weight=FontWeight.BOLD,
                color=Colors.WHITE
            ),
            DataTable(
                columns=[
                    DataColumn(Text("اسم المغذي")),
                    DataColumn(Text("الجهد ")),
                    DataColumn(Text("وقت الإطفاء")),
                    DataColumn(Text("وقت التشغيل / الحالة")),
                ],
                rows=rows
            )
        ]

    def search_feeders(self, e):
        keyword = self.search_field.value.strip().lower()
        db = Login(self.page)
        success, feeders = db.get_all_feeders_with_creator()

        if not success:
            return

        results = []
        for feeder in feeders:
            if keyword in feeder['feeder_name'].lower():
                row = self.get_show_note(
                    feeder['id'],
                    feeder['feeder_name'],
                    feeder['feeder_type']
                )
                results.append(row)

        self.note_column.controls = results
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
        
        self.note_column = Column(controls=self.show_note())

        return View(
            
            "/feeder",
            bgcolor="#101F3C",
             scroll="auto",
            controls=[
                Row(
                    controls = [
                             IconButton(
                        icon=Icons.ARROW_BACK,
                        on_click=lambda x: self.page.go("/")
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
                            icon=Icons.NOTE,
                            content=
                            Column(
                                scroll="auto",
                  alignment=MainAxisAlignment.START,
                  horizontal_alignment=CrossAxisAlignment.CENTER,
                  
                  
                  controls=[
                      
                      Container(alignment=alignment.center,margin=margin.only(top=10),
                                content=   Column(
    scroll="auto",
    alignment=MainAxisAlignment.START,
    horizontal_alignment=CrossAxisAlignment.CENTER,
    controls=[
        Container(
            alignment=alignment.center,
            margin=margin.only(top=10),
            content=self.search_field
        ),
        self.note_column
    ]
)
),
                   
                    ]
            )
                            
                        ),
                        Tab(
                            icon=Icons.CREATE,
                            content=Container(
                            padding=20,
                            content=Column(
                                spacing=20,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=self.show_events()  # هنا تستدعي الدالة مباشرة
                                    )
                                )
                        )
                    ]
                )
            ]
        )
