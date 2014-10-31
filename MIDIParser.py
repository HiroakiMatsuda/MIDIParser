#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
# This module has been tested on python ver.2.6.6.
# ver0.141030
# (C) 2014 Matsuda Hiroaki 

"""
 @file MIDIParser.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import MIDI

import smf_parser

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
midiparser_spec = ["implementation_id", "MIDIParser", 
		 "type_name",         "MIDIParser", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Hiroaki Matsuda", 
		 "category",          "MID", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.midi_file", "./midifile/simpletest.mid",
		 "conf.__widget__.midi_file", "text",
		 ""]
# </rtc-template>

##
# @class MIDIParser
# @brief ModuleDescription
# 
#
class DeltaTime():

        def __init__(self, division):
        
                self.division = division
                self.tempo = 500000.0
        
        def convert_s(self, delta_time):
                tempo_s = self.tempo / 1000000.0            # s / 4note
                delta_time_per_s = tempo_s / self.division  # value / s
             
                return delta_time_per_s * delta_time        # s

        def set_tempo(self, tempo):
                self.tempo = tempo

        def calc_track_time(slef, track_data):

                total_time = 0
        
                for midi_data in track_data:
                    total_time += midi_data.time

                return total_time

class MIDIParser(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_message = MIDI.MIDIMessage(RTC.Time(0,0),
                                                   '',
                                                   MIDI.ChannelMessage(0, 0, 0, 0, 0, 0, 0, 0, 0),
                                                   MIDI.SystemMessage("", 0,"","","","","",
                                                                      "","","","", 0, 0, 0,
                                                                       0, 0, 0, 0, 0, 0, 0))
		"""
		"""
		self._midi_outOut = OpenRTM_aist.OutPort("midi_out", self._d_message)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  midi_file
		 - DefaultValue: ./midifile/simpletest.mid
		"""
		self._midi_file = ['./midifile/simpletest.mid']
		
		# </rtc-template>

	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("midi_file", self._midi_file, "./midifile/simpletest.mid")
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("midi_out",self._midi_outOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

	
		return RTC.RTC_OK
	

	def onActivated(self, ec_id):

                self.smf = smf_parser.Parser(self._midi_file[0])
                self.smf.print_header()

                self.midi_time = DeltaTime(self.smf.division)
                self.serialized_midi_data = self.smf.get_serialized_midi_data()

                self.start = time.time()
                self.counter = 0
                self.midi_length = len(self.serialized_midi_data)
	
		return RTC.RTC_OK

	
	def onDeactivated(self, ec_id):
                	
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):

                now = time.time()

                while True:
                        if self.counter > self.midi_length - 1:
                            break
            
                        difference = self.midi_time.convert_s(self.serialized_midi_data[self.counter].time) - (now - self.start)

                        if difference <= 0:
                                midi_data = self.serialized_midi_data[self.counter]

                                if midi_data.event == 'Tempo':
                                        self._d_message.event = midi_data.event
                                        self.midi_time.set_tempo(midi_data.tempo)
                                        OpenRTM_aist.setTimestamp(self._d_message)
                                        self._midi_outOut.write()

                                elif midi_data.event == 'Note On':
                                        self._d_message.event = midi_data.event
                                        self._d_message.ch.channel     = midi_data.channel
                                        self._d_message.ch.note_number = midi_data.note_number
                                        self._d_message.ch.velocity    = midi_data.velocity
                                        OpenRTM_aist.setTimestamp(self._d_message)
                                        self._midi_outOut.write()

                                elif midi_data.event == 'Note Off':
                                        self._d_message.event = midi_data.event
                                        self._d_message.ch.channel     = midi_data.channel
                                        self._d_message.ch.note_number = midi_data.note_number
                                        self._d_message.ch.velocity    = midi_data.velocity
                                        OpenRTM_aist.setTimestamp(self._d_message) 
                                        self._midi_outOut.write()
                                
                                self.counter += 1

                        else:
                            break
	
		return RTC.RTC_OK
	

	def onAborting(self, ec_id):
	
		return RTC.RTC_OK
	

def MIDIParserInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=midiparser_spec)
    manager.registerFactory(profile,
                            MIDIParser,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    MIDIParserInit(manager)

    # Create a component
    comp = manager.createComponent("MIDIParser")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

