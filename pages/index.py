from flet import*
from database.quere import Login

class Index :
    def __init__(self,page:Page):
        self.page = page
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
        self.chose = Dropdown(
               width=370,
             
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
    def login(self, e):
        admin = self.chose.value
        us_name = self.user_name.value
        pass1 = self.password.value
        db = Login(self.page)

        if admin == "admin":
            success, msg, user = db.login(us_name, pass1)
            if success:
                # تخزين الجلسة مع نوع المستخدم "admin"
                self.page.session.set("user_id", user["id"])
                self.page.session.set("user_name", user["user_name"])
                self.page.session.set("full_access", user["full_access"])
                self.page.session.set("user_role", "admin")  # <-- هنا نحدد النوع

                if user["full_access"]:
                    text = f"✅ Welcome {user['user_name']} (Full Access)"
                    self.page.go("/home")
                    self.page.update()
                else:
                    text = f"🔒 Welcome {user['user_name']} (Limited Access)"
                    self.page.go("/home")
                    self.page.update()
            else:
                text = msg  # رسالة الخطأ

        elif admin == "user":
            success, msg, user = db.login_users(us_name, pass1)
            if success:
                # تخزين الجلسة مع نوع المستخدم "user"
                self.page.session.set("user_id", user["id"])
                self.page.session.set("user_name", user["user_name"])
                self.page.session.set("user_role", "user")  # <-- هنا نحدد النوع

                text = "✅ Welcome back"
                self.page.go("/feeder")
                self.page.update()
            else:
                text = msg

        # عرض رسالة التنبيه/snackbar
        snac = SnackBar(Text(text))
        snac.open = True
        self.page.overlay.append(snac)
        self.page.update()





            


    
    def get_view(self):

        return View(
            '/',
            bgcolor = "#101F3C",
            controls=[
                 ResponsiveRow(
                    columns=12,
                    controls=[
                        Container(
                            col={"xs": 12, "sm": 12, "md": 6},
                            expand=True,
                            content=Column(
                                alignment=MainAxisAlignment.START,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=80,
                                controls=[
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            Container(
                                                margin=margin.only(top=50),
                                                content=Text("LOG-IN", 
                                                    size=40,
                                                    color="white",
                                                    weight=FontWeight.BOLD,
                                                    style=TextStyle(
                                                        shadow=BoxShadow(
                                                            blur_radius=20,
                                                            color=Colors.WHITE24,
                                                            offset=Offset(0,0)
                                                        ),
                                                        font_family="Orbitron"
                                                    )
                                                ),
                                            ),
                                            Container(
                                                bgcolor="white",
                                                height=3
                                            ),
                                        ]
                                    ),
                                    Container(
                                        bgcolor="white",
                                        height=3,
                                        width=300
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            self.user_name
                                        ]
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            self.password
                                        ]
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                             
                                            self.chose
                                        ]
                                    ),
                                    Row(wrap=True,
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            ElevatedButton(
                                                "login",
                                                icon=Icons.LOGIN,
                                                width=200,
                                                style=ButtonStyle(
                                                    bgcolor="#1A2B4C",
                                                    color=Colors.GREEN_300,
                                                    padding=6,
                                                    shape=RoundedRectangleBorder(radius=5),
                                                    icon_color=Colors.GREEN_300,
                                                    text_style=TextStyle(
                                                        weight=FontWeight.BOLD,
                                                        size=20
                                                    )
                                                ),on_click=self.login
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