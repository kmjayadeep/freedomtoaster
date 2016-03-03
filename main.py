import os,sys
import gi
import isolist as iso
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class FlowBoxWindow(Gtk.Window):

    def __init__(self,list_of_isos):
        Gtk.Window.__init__(self, title="FlowBox Demo")
        self.set_border_width(10)
        self.set_default_size(300, 250)

        header = Gtk.HeaderBar(title="Flow Box")
        header.set_subtitle("Sample FlowBox app")
        header.props.show_close_button = True

        self.set_titlebar(header)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(30)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)

        self.create_flowbox(flowbox)

        scrolled.add(flowbox)

        self.add(scrolled)
        self.show_all()



    def create_flowbox(self, flowbox):
        for i in list_of_isos:
            
            button = Gtk.Button()
            grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

            label = Gtk.Label()
            label.set_text(i.name)
            label.set_justify(Gtk.Justification.CENTER)       

            img = Gtk.Image()
            img.set_from_file ("iso/"+i.image)
            img.set_pixel_size(400)
            grid.add(img)

            grid.add(label)
            # grid.attach_next_to(button, label, Gtk.PositionType.BOTTOM)

            button.add(grid)
            button.add(label)
            flowbox.add(button)



list_of_isos=iso.getIsoList()
win = FlowBoxWindow(list_of_isos)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()