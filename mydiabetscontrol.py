from collections import OrderedDict
from math import sin

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex as rgb
from kivy_garden.graph import Graph, MeshLinePlot
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularElevationBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase

KV = '''
Screen:     
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        id: toolbar
                        padding: 5
                        size_hint: 1, .1
                        title: "MyDiabetes Control"
                        elevation: 10
                        left_action_items: [['menu',
                                    lambda x: nav_drawer.set_state("open")]]
                        
                        MDIconButton:
                            id: button_2
                            icon: "dots-vertical"
                            pos_hint: {"center_y": .5}
                            on_release: app.menu_2.open()
                        
                    BoxLayout:
                        size_hint: 1, .75
                        MDTabs:
                            id: tabs
                            on_tab_switch: app.on_tab_switch(*args)
                    MDLabel:
                        text: "Recentes:"
                        bold: True
                        size_hint: 1, .1
                    ScrollView:
                        MDList:
                            id: md_list
                            padding: 0
                    MDFloatingActionButtonSpeedDial:
                        size_hint_y: None
                        height: self.height
                        data: app.data
                        root_button_anim: True
                        hint_animation: True
                        bg_hint_color: app.theme_cls.primary_light
                        md_bg_color: app.theme_cls.primary_color

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                id: content_drawer
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"
            
                MDLabel:
                    text: "MyDiabets Control"
                    font_style: "Button"
                    size_hint_y: None
                    height: self.texture_size[1]
            
                MDSeparator:

                ScrollView:
                    DrawerList:
                        id: nd_list

# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)
    divider: None
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color
'''

Builder.load_file('tab.kv')
Builder.load_file('diabetescard.kv')


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Tab(FloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class DiabetesCard(MDCard):
    """Classe que implementa os cards de medição"""
    title = StringProperty()
    line = StringProperty()


class DiabetesToolbar(
    ThemableBehavior, RectangularElevationBehavior, MDBoxLayout,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = self.theme_cls.primary_color


class Example(MDApp):
    data = {
        'language-python': 'Python',
        'scale-bathroom': 'Peso',
        'diabetes': 'Glicemia',
    }

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.primary_light_hue = "200"
        self.theme_cls.accent_palette = "Yellow"
        return Builder.load_string(KV)

    def on_start(self):
        icons_item = OrderedDict({
            "calendar-today": "Diário",
            "calendar-week": "Semanal",
            "calendar-month": "Mensal",
            "account": "Perfil",
            "file-chart-outline": "Relatórios",
            "cog": "Configurações",
            "information-outline": "Sobre o App",
            "message-alert": "Ajuda e Feedback",
        })
        for icon_name in icons_item.keys():
            if icon_name == 'cog':
                self.root.ids.nd_list.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name])
                )
                self.root.ids.nd_list.add_widget(MDSeparator())
            elif icon_name == 'file-chart-outline':
                self.root.ids.nd_list.add_widget(MDSeparator())
                self.root.ids.nd_list.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name])
                )
            else:
                self.root.ids.nd_list.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name])
                )

        self.root.ids.tabs.add_widget(Tab(text=f"Diário"))
        self.root.ids.tabs.add_widget(Tab(text=f"Semanal"))
        self.root.ids.tabs.add_widget(Tab(text=f"Mensal"))

        # pegar do banco
        self.root.ids.md_list.add_widget(DiabetesCard(title="Em Jejum",
                                                      line="08:05h  250"))
        self.root.ids.md_list.add_widget(DiabetesCard(title="Após o Almoço",
                                                      line="14:35h  230"))
        self.root.ids.md_list.add_widget(DiabetesCard(title="Após o Jantar",
                                                      line="21:15h  200"))
        self.menu_2 = self.create_menu(
            [{'icon': 'printer', 'text': "Imprimir"},
             {'icon': 'cog', 'text': "configurações"}],
            self.root.ids.button_2, )

    def create_menu(self, text, instance):
        menu_items = [{"icon": i['icon'], "text": i['text']} for i in text]
        menu = MDDropdownMenu(caller=instance, items=menu_items, width_mult=4)
        menu.bind(on_release=self.menu_callback)
        return menu

    def menu_callback(self, instance_menu, instance_menu_item):
        if instance_menu_item.icon == 'printer':
            print("imprimindo")
        else:
            print('configurando')
        instance_menu.dismiss()

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        """Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """

        box = instance_tab.ids.label
        graph = self.create_graph()
        if len(box.children) > 0:
            for graph in box.children:
                box.remove_widget(graph)
        box.add_widget(graph)

    def create_graph(self):
        # colors = itertools.cycle([
        #     rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')
        # ])
        graph_theme = {
            'label_options': {
                'color': (0, 0, 0, 1),
                'bold': False},
            'background_color': (.98, .98, .98, 1),
            'tick_color': rgb('808080'),
            'border_color': rgb('808080')
        }
        graph = Graph(xlabel='',
                      ylabel='Glicemia',
                      font_size=14,
                      x_ticks_minor=0,
                      x_ticks_major=25,
                      y_ticks_major=1,
                      y_grid_label=True,
                      x_grid_label=True,
                      padding=5,
                      x_grid=True,
                      y_grid=True,
                      xmin=-0,
                      xmax=100,
                      ymin=-1,
                      ymax=1,
                      **graph_theme)

        plot = MeshLinePlot(color=rgb('66a8d4'))
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        return graph


Example().run()
