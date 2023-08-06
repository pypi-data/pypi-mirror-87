#!/usr/bin/env python3

import os
import pypact as pp
from pypact import InputData,LOG_SEVERITY_WARNING,PROJECTILE_NEUTRON



#https://stackoverflow.com/questions/52155062/python-convert-scientific-notation-string-to-float-retaining-decimal-places
import re

def ada_compliant_float_as_string(f):
    if type(f) is str: return f
    if f>1e+5:
        return "{:.2E}".format(f)
    else:
        return "{}".format(f)
    return "{:.2E}".format(f) if re.match("^-?[^\.]e",str(f)) else str(f)
#for f in [-1e-5,1e-5,1.4e-5,-12e4,1,1.0]:
#   print(ada_compliant_float_as_string(f))



    
#
# I subclass the input to remove xsthreshold
#
class InputData2(InputData):
    def _serialize(self, f):
        """
            The serialization method
            f: file object
        """
        inputdata = []
        
        def addnewline():
            inputdata.append("")
        
        def addcomment(comment):
            pass #print("D")
            #inputdata.append("{} {} {}".format(COMMENT_START, comment, COMMENT_END))
        
        def addkeyword(keyword, args=[]):
            #strargs = ' '.join([str(a) for a in args])
            strargs = ' '.join([ada_compliant_float_as_string(a) for a in args])
            #if keyword=="FLUX":print("XX",strargs)
            inputdata.append("{} {}".format(keyword, strargs))



            
        
        # control keywords
        addcomment("CONTROL PHASE")
        if self._json:
            addcomment("enable JSON output")
            addkeyword('JSON')
                
        if self._overwrite:
            addcomment("overwrite existing output files of same name")
            addkeyword('CLOBBER')
        
        if self._readgammagroup:
            addcomment("read gamma groups from file, specify ggbins in files file")
            addkeyword('READGG')
        
        if self._readspontfission:
            addcomment("read spontaneous fission from file, specify sf_endf in files file")
            addkeyword('READSF')
        
        if self._useeaf:
            addcomment("use EAF nuclear data libraries")
            addkeyword('LIBVERSION', args=[0])
        
        if self._usecumfissyield:
            addcomment("use cumulative fission yield data mt=459 instead of mt=454")
            addkeyword('CUMFYLD')
            
        if self._enablemonitor:
            addcomment("monitor FISPACT-II progress")
            addkeyword('MONITOR', args=[1])
        
        addcomment("the minimum cross section (barns) for inclusion in pathways analysis")
        #addkeyword('XSTHRESHOLD', args=[self._xsthreshold])
        
        if not self._ignorecollapse:
            if self._group != 0:
                addcomment("perform collapse")
                addkeyword('GETXS', args=[-1 if self._binaryxs and not self._useeaf else 1, self._group])
            else:
                addcomment("don't do collapse, just read the existing file")
                addkeyword('GETXS', args=[0])

        if not self._ignorecondense:
            addcomment("get decay data")
            addkeyword('GETDECAY', args=[1 if self._condense else 0])
    
        if self._loglevel != LOG_SEVERITY_WARNING:
            addcomment("enable logging at level {}".format(self._loglevel))
            addkeyword('LOGLEVEL', args=[self._loglevel])

        if self._approxgamma:
            addcomment("approximate spectra when not available")
            addkeyword('SPEK')
        
        if self._ignoreuncert:
            addcomment("ignore uncertainties")
            addkeyword('NOERROR')
    
        if self._projectile != PROJECTILE_NEUTRON:
            addcomment("set projectile (n=1, d=2, p=3, a=4, g=5)")
            addkeyword('PROJ', args=[self._projectile])
        
        # end control phase
        addcomment("end control")
        addkeyword('FISPACT')
        addkeyword('*', args=[self.name])

        # initial phase
        addnewline()
        addcomment("INITIALIZATION PHASE")
        if self._outputhalflife:
            addcomment("output half life values")
            addkeyword('HALF')

        if self._outputhazards:
            addcomment("output ingestion and inhalation values")
            addkeyword('HAZARDS')

        if self._clearancedata:
            addcomment("include clearance data of radionuclides to be input")
            addkeyword('CLEAR')

            
        addnewline()
    
        if self._inventoryismass and not self._inventoryisfuel:
            if self._inventorymass.totalMass > 0.0:
                addcomment("set the target via MASS")
                addkeyword(str(self._inventorymass))

        if self._inventoryisfuel and not self._inventoryismass:
            if self._density > 0.0:
                addcomment("set the target via FUEL")
                addkeyword(str(self._inventoryfuel))  
        
        if self._density > 0.0:
            addcomment("set the target density")
            addkeyword('DENSITY', args=[self._density])

        addnewline()

        if self._atomsthreshold > 0.0:
            addcomment("set the threshold for atoms in the inventory")
            addkeyword('MIND', args=[self._atomsthreshold])
            
        addkeyword('UNCERT', args=[2]) # ARTIFITIALLY ADDED UNCERTAINTY
        
        if self._initialinventory:
            addcomment("output the initial inventory")
            addkeyword('ATOMS')

            
        # EXTRA ALWAYS================ UNCERT 2; ATWO
        addkeyword('ATWO', args=[])
        addkeyword('GRAPH', args=[1,2,1,1])
        #addkeyword('ALTWO', args=[])
        
            
        # inventory phase
        addnewline()
        addcomment("INVENTORY PHASE")
        if len(self._irradschedule) > 0:
            addcomment("irradiation schedule")
            for time, fluxamp in self._irradschedule:
                addkeyword('FLUX', args=[fluxamp])
                addkeyword('TIME', args=[time, 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of irradiation")

            addkeyword('FLUX', args=[0.0])
            addkeyword('ZERO')
            for time in self._coolingschedule:
                addkeyword('TIME', args=[time, 'SECS'])
                addkeyword('ATOMS')
            addcomment("end of cooling")

        # end file
        addnewline()
        addcomment("end of input")
        addkeyword('END')
        addkeyword('*', args=['end'])
        
        for line in inputdata:
            f.write("{}\n".format(line))



    
#id = pp.InputData(name='test')
id = InputData2(name='test')

# control setup
id.enableJSON()
id.overwriteExisting()
id.enableSystemMonitor()
#id.approxGammaSpectrum() # adds SPEK. I dont want
#id.readXSData(709)  # GETXS 1 709, I need GETXS 0
id.readXSData(0)  # GETXS0

id.readDecayData(0) # I added 0, gives GETDECAY 0 now
#===== writes FISPACT HERE


# set target
#id.setMass(1.0)
#id.addElement('Ti', percentage=80.0)
#id.addElement('Fe', percentage=14.8)
#id.addElement('Cr', percentage=5.2)
#id.setDensity(19.5)

#id.setMass(1.0)
#id.addElement('Al', percentage=100)
#id.setDensity(2.7)

id.setMass(5.0)
id.addElement('Al', percentage=95)
id.addElement('Si', percentage=0.4)
id.addElement('Fe', percentage=0.4)
id.addElement('Cu', percentage=0.1)
id.addElement('Mn', percentage=1)
id.addElement('Mg', percentage=5)
id.addElement('Cr', percentage=0.25)
id.addElement('Zn', percentage=0.25)
id.addElement('Ti', percentage=0.15)
id.setDensity(2.7)

#id.addElement('Cu', percentage=100)
#id.setDensity(8.96)

#id.setMass(1.0)
#id.addElement('Cu', percentage=94)
#id.addElement('Al', percentage=3)
#id.addElement('N', percentage=3)
#id.setDensity(8.96)


#id.setProjectile(pp.PROJECTILE_NEUTRON) #DOES NOTHING

#id.readGammaGroup() # puts READGG that i dont need
id.enableInitialInventoryInOutput()  # ? puts 1x ATOMS after MIND?
#id.setLogLevel(pp.LOG_SEVERITY_ERROR)

id.enableHazardsInOutput()   #HAZARDS
id.enableHalflifeInOutput()  # HALF

# thresholds
#id.setXSThreshold(1e-12) # i want to remove from _serialize
#id.setAtomsThreshold(1e5) # MIND --- i have 1e-4
id.setAtomsThreshold(1E-4) # MIND --- i have 1e-4

# irradiate and cooling times
id.addIrradiation(3600.0, 2e9)
id.addCooling(100.0)
id.addCooling(1000.0)
id.addCooling(2000.0)
id.addCooling(4000.0)
id.addCooling(8000.0)
id.addCooling(10000.0)
id.addCooling(20000.0)
id.addCooling(40000.0)
id.addCooling(80000.0)
id.addCooling(100000.0)
id.addCooling(200000.0)
id.addCooling(400000.0)
id.addCooling(800000.0)
id.addCooling(1000000.0)
id.addCooling(2000000.0)
id.addCooling(4000000.0)
#
# validate data
id.validate()

print(pp.to_string(id))

# write to file
pp.to_file(id, os.path.join('', '{}.i'.format(id.name)))
