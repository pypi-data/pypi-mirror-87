#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Fast DAQ DLL Wrapper
#--------------------------------------------------------------------------
# Copyright (c) 2020 Light Conversion, UAB
# All rights reserved.
# www.lightcon.com
#==========================================================================

import clr   # pip install pythonnet
import numpy as np
import time

import os
dirname = os.path.dirname(__file__)
clr.AddReference(os.path.join(dirname, "LightConversion.Hardware.FastDaq.dll"))
clr.AddReference(os.path.join(dirname, "LightConversion.Abstractions.dll"))
clr.AddReference(os.path.join(dirname, "System.Threading.dll"))
clr.AddReference("mscorlib.dll")

from LightConversion.Hardware.FastDaq import FastDaq
from LightConversion.Abstractions import ClockChannel, SampleClockActiveEdge, TriggerChannel, DaqException
from System.Threading import CancellationTokenSource, CancellationToken
from System import TimeoutException

class FastDaqWrapper:
    '''
    DLL wrapper of FastDaq one-channel 2.5MHz ADC board.
    '''
    daq = None
    DaqException = DaqException
    TimeoutException = TimeoutException
    def __init__(self, device = 'Dev0'):
        devices = FastDaq.Devices
        if (device in devices):
            daq = FastDaq.LoadDevice(device)
            daq.Initialize()
            if daq.Connected:
                print ("Initialized", device, daq.Device.ProductType, daq.Device.SerialNumber)            
                self.daq = daq
                time.sleep(0.1)
            return
        
        print ("Harpia DAQ not found")

    def get_devices(self = None):
        return FastDaq.Devices

    def is_connected(self):
        return self.daq.Connected or False
        
    def set_timeout(self, timeout):
        '''
        Sets timeout in milliseconds
        
        Parameters
        ----------
        timeout : number
            Timeout value, given in milliseconds
        '''
        self.daq.AcquisitionTimeout = int(timeout)
        
    def configure_sample_clock(self, channel, active_edge):
        '''
        Configures clock for ADC acquisition
        
        Parameters
        ----------
        channel : str
            'internal' or 'PFI0'
        active_edge : str
            'rising' or 'falling'        
        '''
        my_clock_channel = ClockChannel.Internal
        if (channel == 'internal'):
            my_clock_channel = ClockChannel.Internal
        elif ((channel == 'PFI0')):
            my_clock_channel = ClockChannel.PFI0
            
        my_clock_active_edge = SampleClockActiveEdge.Rising
        if (active_edge == 'rising'):
            my_clock_active_edge = SampleClockActiveEdge.Rising
        else:
            my_clock_active_edge = SampleClockActiveEdge.Falling            
            
        self.daq.ConfigureSampleClock(my_clock_channel, 2.5e6, my_clock_active_edge, 1000)
            
            
    def configure_start_trigger(self, channel):
        '''
        Configures trigger for ADC acquisition
        
        Parameters
        ----------
        channel : str
            'internal' or 'PFI0'
        '''
        my_trigger_channel = TriggerChannel.Internal
        if (channel == 'internal'):
            my_trigger_channel = TriggerChannel.Internal
        elif ((channel == 'PFI0')):
            my_trigger_channel = TriggerChannel.PFI0

        self.daq.ConfigureStartTrigger(my_trigger_channel)
    
    
    def get_daq_data(self, n):
        '''
        Acquires n samples per enabled channel.
        
        Parameters
        ----------
        n : number
            Number of datapoints to acquire per channel
        
        Returns
        -------
        list (n):
            Values in volts
        '''
        self.daq.DatapointsPerChannel = n
        cts = CancellationTokenSource()
        ct = cts.Token

        data = self.daq.GetAnalogChannelsData(ct)        
        data = [item for item in data]        
        return data
    
    def set_external_trigger_delay(self, delay):
        '''
        Sets external trigger delay for sampling.
        
        Parameters
        ----------
        delay : number
            Delay value in nanoseconds
        '''
        self.daq.ExternalTriggerDelay = delay
        
    def close(self):
        self.daq.Dispose()