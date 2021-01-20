import itertools

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase

from kivy.utils import get_color_from_hex as rgb
from kivy_garden.graph import Graph, MeshLinePlot
from math import sin


KV = '''

Screen:     
    NavigationLayout:

        ScreenManager:

            Screen:

                BoxLayout:
                    orientation: 'vertical'

                    MDToolbar:
                        size_hint: 1, .1
                        title: "MyDiabetes Control"
                        elevation: 10
                        left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

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
        
            
<DiabetesCard>:
    orientation: "vertical"
    padding: "8dp"
    size_hint_y: None
    height: self.height
    pos_hint: {"center_x": .5, "center_y": .5}
    MDLabel:
        #size_hint_y: None
        #height: self.height
        text: root.title
        theme_text_color: "Secondary"
                    
    # MDSeparator:
    #     height: "2dp"

    BoxLayout:
        size_hint_y: None
        height: "30dp"
        MDLabel:
            text: root.line
        MDIconButton:
            icon: "trash-can"
            text: "Deletar"
        MDIconButton:
            icon: "pencil"
            text: "Editar"
                    
                    
<Tab>:
    BoxLayout:
        orientation: 'vertical'
        padding_right: 5
        id: label

'''


class ContentNavigationDrawer(BoxLayout):
    pass


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class DiabetesCard(MDCard):
    """Classe que implementa os cards de medição"""
    title = StringProperty()
    line = StringProperty()


class Example(MDApp):
    data = {
        'language-python': 'Python',
        'scale-bathroom': 'Peso',
        'diabetes': 'Glicemia',
    }
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.root.ids.tabs.add_widget(Tab(text=f"Diário"))
        self.root.ids.tabs.add_widget(Tab(text=f"Semanal"))
        self.root.ids.tabs.add_widget(Tab(text=f"Mensal"))

        #pegar do banco
        self.root.ids.md_list.add_widget(DiabetesCard(title="Em Jejum",
                                                     line="08:05h  250"))
        self.root.ids.md_list.add_widget(DiabetesCard(title="Após o Almoço",
                                                     line="14:35h  230"))
        self.root.ids.md_list.add_widget(DiabetesCard(title="Após o Jantar",
                                                     line="21:15h  200"))

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        box = instance_tab.ids.label
        graph = self.create_graph()
        if len(box.children) > 0:
            for graph in box.children:
                box.remove_widget(graph)
        box.add_widget(graph)

    def create_graph(self):
        colors = itertools.cycle([
            rgb('7dac9f'), rgb('dc7062'), rgb('66a8d4'), rgb('e5b060')
        ])
        graph_theme = {
            'label_options': {
                'color': (0, 0, 0, 1),
                'bold': False},
            'background_color': (.9, .9, .9, 1),
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

        #plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot = MeshLinePlot(color=next(colors))
        plot.points = [(x, sin(x/10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        return graph


Example().run()
