# -------------------------
# PCOD Care App - main.py
# -------------------------

from functools import partial  # for screen button fix
from kivy.lang import Builder
Builder.load_string('')  # prevent Kivy from looking for a .kv file

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.storage.jsonstore import JsonStore

store = JsonStore("user_data.json")

# ---------------- HOME ----------------
class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text="PCOD CARE APP", font_size=32, bold=True))

        # Buttons and corresponding screens
        screens = [
            ("Period Tracker", "period"),
            ("BMI Calculator", "bmi"),
            ("PCOD Risk Score", "risk"),
            ("PCOD Recipes & Tips", "tips")
        ]

        for text, screen_name in screens:
            btn = Button(text=text, size_hint_y=None, height=60)
            btn.bind(on_press=partial(lambda s, instance: setattr(self.manager, 'current', s), screen_name))
            layout.add_widget(btn)

        self.add_widget(layout)

# ---------------- PERIOD TRACKER ----------------
class Period(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.input = TextInput(hint_text="Last Period Date (DD-MM-YYYY)")
        layout.add_widget(self.input)

        self.result = Label(text="")
        layout.add_widget(self.result)

        save = Button(text="Save")
        save.bind(on_press=self.save)
        layout.add_widget(save)

        back = Button(text="Back")
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)

        self.add_widget(layout)

    def save(self, instance):
        store.put("period", last_date=self.input.text)
        self.result.text = "Saved successfully"

# ---------------- BMI ----------------
class BMI(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.w = TextInput(hint_text="Weight (kg)", input_filter='float')
        self.h = TextInput(hint_text="Height (cm)", input_filter='float')
        layout.add_widget(self.w)
        layout.add_widget(self.h)

        self.result = Label(text="")
        layout.add_widget(self.result)

        calc = Button(text="Calculate BMI")
        calc.bind(on_press=self.calc)
        layout.add_widget(calc)

        back = Button(text="Back")
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)

        self.add_widget(layout)

    def calc(self, instance):
        try:
            bmi = float(self.w.text) / ((float(self.h.text)/100) ** 2)
            self.result.text = f"BMI: {bmi:.2f}"
        except:
            self.result.text = "Invalid input"

# ---------------- PCOD RISK ----------------
class Risk(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.q1 = TextInput(hint_text="Irregular periods? (yes/no)")
        self.q2 = TextInput(hint_text="Weight gain? (yes/no)")
        self.q3 = TextInput(hint_text="Acne / Hair growth? (yes/no)")

        layout.add_widget(self.q1)
        layout.add_widget(self.q2)
        layout.add_widget(self.q3)

        self.result = Label(text="")
        layout.add_widget(self.result)

        btn = Button(text="Check Risk")
        btn.bind(on_press=self.check)
        layout.add_widget(btn)

        back = Button(text="Back")
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)

        self.add_widget(layout)

    def check(self, instance):
        score = 0
        for q in [self.q1, self.q2, self.q3]:
            if q.text.lower().startswith("y"):
                score += 1
        self.result.text = "High PCOD Risk" if score >= 2 else "Low PCOD Risk"

# ---------------- PCOD RECIPES & TIPS ----------------
class Tips(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        scroll = ScrollView()
        tips_text = (
            "🌿 PCOD Recipes & Tips 🌿\n\n"
            "1. Include high-fiber foods: whole grains, vegetables, fruits.\n"
            "2. Prefer lean protein: chicken, fish, tofu.\n"
            "3. Use healthy fats: olive oil, nuts, seeds.\n"
            "4. Avoid refined sugar & processed food.\n"
            "5. Regular exercise: 30 min/day.\n"
            "6. Stay hydrated.\n"
            "7. Track period and symptoms for better insights."
        )
        lbl = Label(text=tips_text, font_size=18, markup=True, size_hint_y=None)
        lbl.bind(texture_size=lbl.setter('size'))
        scroll.add_widget(lbl)
        layout.add_widget(scroll)

        back = Button(text="Back")
        back.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        layout.add_widget(back)

        self.add_widget(layout)

# ---------------- APP ----------------
class PCODApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home(name="home"))
        sm.add_widget(Period(name="period"))
        sm.add_widget(BMI(name="bmi"))
        sm.add_widget(Risk(name="risk"))
        sm.add_widget(Tips(name="tips"))
        return sm

if __name__ == "__main__":
    PCODApp().run()

