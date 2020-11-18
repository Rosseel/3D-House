import PySimpleGUI as sg
import DataReader as dr

class SGUI():

    def __init__(self,controller):
        self.controller=controller
        self.show_simple_gui()

    def show_simple_gui(self):
        sg.theme('DarkAmber')   # Add a touch of color
        # All the stuff inside your window.
        latDegreeBox = sg.InputText(default_text="211552.031768453")
        latMinutesBox = sg.InputText(default_text="211552.031768453")
        latSecondsBox = sg.InputText(default_text="211552.031768453")
        lonDegreeBox = sg.InputText(default_text="211552.031768453")
        lonMinutesBox = sg.InputText(default_text="211552.031768453")
        lonSecondsBox = sg.InputText(default_text="211552.031768453")
        layout = [  [sg.Text('Latitude  '),latDegreeBox,latMinutesBox,latSecondsBox ],
                    [sg.Text('Longitude'), lonDegreeBox,lonMinutesBox,lonSecondsBox],
                    [sg.Button('Ok'), sg.Button('Cancel')] ]

        # Create the Window
        window = sg.Window('SpaceEYE', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if values[0]!="" and values[1]!="":
                try:
                    latdegrees=float(values[0])
                    latminutes = float(values[1])
                    latseconds = float(values[2])
                    londegrees = float(values[3])
                    lonminutes = float(values[4])
                    lonseconds = float(values[5])
                    lat=latdegrees+latminutes/60+latseconds/3600
                    lon=londegrees + lonminutes / 60 + latseconds / 3600
                    self.controller.parse_coords(lat,lon)
                except ValueError:
                    sg.popup("Coordinates need to be numbers")
                    latDegreeBox.update(value="",background_color='red')
                    latMinutesBox.update(value="",background_color='red')
                    latSecondsBox.update(value="",background_color='red')
                    lonDegreeBox.update(value="",background_color='red')
                    lonMinutesBox.update(value="",background_color='red')
                    lonSecondsBox.update(value="",background_color='red')


