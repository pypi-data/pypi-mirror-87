from math import pi, sqrt, atan
import io
from rocketprops.rocket_prop import get_prop
from rocketprops.unit_conv_data import get_value # for any units conversions
from rocketisp.efficiency.calc_noz_kinetics import calc_IspODK
from rocketisp.efficiency.eff_vaporization import calc_C1_C2, fracVaporized

# acoustic mode multipliers
modeSvnD = {'1T':1.8413,'2T':3.0543,'1R':3.8317,'3T':4.2012,'4T':5.3175,
    '1T1R':5.3313,'2T1R':6.7060,'2R':7.0156,'3T1R':8.0151,'1T2R':8.5263}

        
def temperature_clamp(value, name, min_value, max_value):
    """Check to see if name is limited in range."""
    if value < min_value:
        s = 'WARNING... %s set to %g degR (MUST be >=%g and <=%g'%(name, min_value, min_value, max_value)
        print( s )
        return min_value*1.001, s
    if value > max_value:
        s = 'WARNING... %s set to %g degR (MUST be >=%g and <=%g'%(name, max_value, min_value, max_value)
        print( s )
        return max_value*0.999, s
        
    return value, ''


class Injector:
    """
    Injector object holds basic information about the injector.
    Injector design features are calculated
    including chamber losses due to the injector, Em, Mix and Vap.

    :param coreObj: CoreStream object 
    :param Tox: degR, temperature of oxidizer
    :param Tfuel: degR, temperature of fuel
    :param elemEm: intra-element Rupe mixing factor (0.7 below ave, 0.8 ave, 0.9 above ave)
    :param fdPinjOx: fraction of Pc used as oxidizer injector pressure drop
    :param fdPinjFuel: fraction of Pc used as fuel injector pressure drop
    :param dpOxInp: psia,input value of injector pressure drop for oxidizer (overrides fdPinjOx)
    :param dpFuelInp: psia,input value of injector pressure drop for fuel (overrides fdPinjFuel)
    :param setNelementsBy: flag determines how to calculate number of elements ( "acoustics", "elem_density", "input")
    :param elemDensInp: elem/in**2, input value for element density (setNelementsBy == "elem_density")
    :param NelementsInp: input value for number of elements (setNelementsBy == "input")
    :param OxOrfPerEl: number of oxidizer orifices per element
    :param FuelOrfPerEl: number of fuel orifices per element
    :param lolFuelElem: flag for like-on-like fuel element (determines strouhal multiplier)
    :param setAcousticFreqBy: flag indicating how to determine design frequency. (can be "mode" or "freq")
    :param desAcousMode: driving acoustic mode of injector OR acoustic mode multiplier (setNelementsBy=="acoustics" and setAcousticFreqBy=="mode")
    :param desFreqInp: Hz, driving acoustic frequency of injector (sets D/V if setNelementsBy=="acoustics" and setAcousticFreqBy=="freq")
    
    :param CdOxOrf: flow coefficient of oxidizer orifices
    :param CdFuelOrf: flow coefficient of fuel orifices
    :param dropCorrOx: oxidizer drop size multiplier (showerhead=3.0, like-doublet=1.0, vortex=0.5, unlike-doublet=0.33)
    :param dropCorrFuel: fuel drop size multiplier (showerhead=3.0, like-doublet=1.0, vortex=0.5, unlike-doublet=0.33)
    :param DorfMin: in, minimum orifice diameter (lower limit)
    :param LfanOvDorfOx: fan length / oxidizer orifice diameter
    :param LfanOvDorfFuel: fan length / fuel orifice diameter
    :type coreObj: CoreStream
    :type Tox: None or float
    :type Tfuel: None or float
    :type elemEm: float
    :type fdPinjOx: float
    :type fdPinjFuel: float
    :type dpOxInp: None or float
    :type dpFuelInp: None or float
    :type setNelementsBy: str
    :type elemDensInp: float
    :type NelementsInp: float
    :type OxOrfPerEl: float
    :type FuelOrfPerEl: float
    :type lolFuelElem: bool
    :type setAcousticFreqBy: str
    :type desAcousMode: str or float
    :type desFreqInp: None or float
    :type CdOxOrf: float
    :type CdFuelOrf: float
    :type dropCorrOx: float
    :type dropCorrFuel: float
    :type DorfMin: float
    :type LfanOvDorfOx: float
    :type LfanOvDorfFuel: float
    :return: Injector object
    :rtype: Injector        
    """
    
    def __init__(self, coreObj, # CoreStream object
        Tox=None, Tfuel=None, elemEm=0.8,
        fdPinjOx=0.25, fdPinjFuel=0.25, dpOxInp=None, dpFuelInp=None,
        setNelementsBy='acoustics', # can be "acoustics", "elem_density", "input"
        elemDensInp=5, NelementsInp=100,
        OxOrfPerEl=1.0, FuelOrfPerEl=1.0, 
        lolFuelElem=False, 
        setAcousticFreqBy='mode', # can be "mode" or "freq"
        desAcousMode='3T', desFreqInp=5000, 
        CdOxOrf=0.75, CdFuelOrf=0.75, dropCorrOx=0.33, dropCorrFuel=0.33,
        DorfMin=0.008,
        LfanOvDorfOx=20.0, LfanOvDorfFuel=20.0):
        """
        Injector object holds basic information about the injector.
        Injector design features are calculated
        including chamber losses due to the injector, Em, Mix and Vap.
        """
        self.coreObj        = coreObj
        self.geomObj        = coreObj.geomObj
        
        # build propellant  objects
        self.oxProp   = get_prop( self.coreObj.oxName )
        self.fuelProp = get_prop( self.coreObj.fuelName )
        
        self.TminOx,   self.TmaxOx   = self.oxProp.T_data_range()
        self.TminFuel, self.TmaxFuel = self.fuelProp.T_data_range()
        
        self.Tox_warning = ''
        self.Tfuel_warning = ''
        
        if Tox is None: 
            Tox = min(530.0, self.oxProp.Tnbp)
        else:
            Tox, self.Tox_warning = temperature_clamp(Tox, 'Tox', self.TminOx,   self.TmaxOx)
        self.Tox            = Tox
        
        if Tfuel is None: 
            Tfuel = min(530.0, self.fuelProp.Tnbp)
        else:
            Tfuel,self.Tfuel_warning = temperature_clamp(Tfuel, 'Tfuel', self.TminFuel,   self.TmaxFuel)
        self.Tfuel          = Tfuel
        
        self.elemEm         = min(1.0, elemEm) # intra-element mixing parameter for injector
        self.fdPinjOx       = fdPinjOx
        self.fdPinjFuel     = fdPinjFuel
        self.dpOxInp        = dpOxInp
        self.dpFuelInp      = dpFuelInp
        self.setNelementsBy = setNelementsBy.lower() # just in case user screw up.
        self.used_Nelem_criteria = self.setNelementsBy # assume for now that intention is satisfied
        
        self.elemDensInp    = elemDensInp
        self.NelementsInp   = NelementsInp
        self.OxOrfPerEl     = OxOrfPerEl
        self.FuelOrfPerEl   = FuelOrfPerEl
        
        self.lolFuelElem    = lolFuelElem
        if lolFuelElem:
            self.strouhal_mult = 0.1 # LOL element uses 0.1 strouhal multiplier
        else:
            self.strouhal_mult = 0.2 # unlike element uses 0.2 strouhal multiplier
        
        self.desAcousMode   = desAcousMode
        if desAcousMode in modeSvnD:
            self.desAcousMult = modeSvnD[ desAcousMode ]
        else:
            self.desAcousMult = float( desAcousMode ) # let it raise exception if not a float
        self.desFreqInp     = desFreqInp
        
        self.setAcousticFreqBy = setAcousticFreqBy.lower() # can be "mode" or "freq"
        
        self.CdOxOrf        = CdOxOrf
        self.CdFuelOrf      = CdFuelOrf
        self.dropCorrOx     = dropCorrOx
        self.dropCorrFuel   = dropCorrFuel
        self.DorfMin        = DorfMin
        self.LfanOvDorfOx   = LfanOvDorfOx
        self.LfanOvDorfFuel = LfanOvDorfFuel
        
        # get oxidizer propellant properties
        self.sgOx = self.oxProp.SG_compressed( Tox, self.coreObj.Pc )  # g/ml
        self.dHvapOx = self.oxProp.HvapAtTdegR( Tox )     # BTU/lbm
        self.surfOx = self.oxProp.SurfAtTdegR( Tox )      # lbf/in
        
        self.viscOx = self.oxProp.ViscAtTdegR( Tox )      # poise
        self.viscOx = get_value( self.viscOx, 'poise', 'lbm/s/ft')
        
        self.MolWtOx = self.oxProp.MolWt
        #print('sgOx=',self.sgOx)
        
        # get fuel propellant properties
        self.sgFuel = self.fuelProp.SG_compressed( Tfuel, self.coreObj.Pc )  # g/ml
        self.dHvapFuel = self.fuelProp.HvapAtTdegR( Tfuel )     # BTU/lbm
        self.surfFuel = self.fuelProp.SurfAtTdegR( Tfuel )      # lbf/in
        self.viscFuel = self.fuelProp.ViscAtTdegR( Tfuel )      # poise
        self.viscFuel = get_value( self.viscFuel, 'poise', 'lbm/s/ft')
        
        self.MolWtFuel = self.fuelProp.MolWt
        #print('sgFuel=',self.sgFuel)
        
        # --------- start vaporization calcs --------
        self.rhoOx = rho = get_value( self.sgOx, 'SG', 'lbm/in**3' )
        self.rhoFuel = rho = get_value( self.sgFuel, 'SG', 'lbm/in**3' )
        
        self.calc_element_attr() # e.g. Nelements, injection velocities, elements diam, etc.
        #self.evaluate()
        
    def __call__(self, name):
        return getattr(self, name ) # let it raise exception if no name attr.

    def evaluate(self, DOREVAL=False):
        """
        Calculates chamber losses due to the injector, Em, Mix and Vap.
        """
        
        # recalc CoreStream in case a basic parameter has changed.
        self.coreObj.evaluate()
        
        self.calc_element_attr() # e.g. Nelements, injection velocities, elements diam, etc.
        
        effObj = self.coreObj.effObj
        
        # calc intra-element mixing efficiency and reset BasicThruster effEm
        #if self.calc_effEm:
        if not effObj['Em'].is_const:
            effEm = self.calculate_effEm() # calc intra-element mixing efficiency
            msg = 'Rupe Em=%g'%self.elemEm
            effObj.set_value( 'Em', effEm, value_src=msg, re_evaluate=DOREVAL)

        # calc inter-element mixing efficiency
        #if self.calc_effMix:
        if not effObj['Mix'].is_const:
            effMix = self.calculate_effMix() # calc inter-element mixing efficiency (2 deg estimate)
            msg = 'mixAngle=%.2f deg'%self.mixAngle
            effObj.set_value( 'Mix', effMix, value_src=msg, re_evaluate=DOREVAL)
        
        # vaporization efficiency
        #if self.calc_effVap:
        if not effObj['Vap'].is_const:
            effVap = self.calculate_effVap()
            msg = 'gen vaporized length'
            self.coreObj.effObj.set_value( 'Vap', effVap, value_src=msg, re_evaluate=DOREVAL)
        
        
        # recalc CoreStream in case a basic parameter has changed.
        # self.coreObj.evaluate() <-- handled by re_evaluate flags

    
    def calculate_effVap(self):
        """calculate vaporization efficiency"""
        self.C1fuel, self.C2fuel = calc_C1_C2(self.fuelProp, self.Tfuel, self.rhoFuel, self.dHvapFuel, 
                                              self.surfFuel, self.viscFuel, self.MolWtFuel)
        #print('C1fuel=%g, C2fuel=%g'%(self.C1fuel, self.C2fuel)  )
        
        self.C1ox, self.C2ox = calc_C1_C2(self.oxProp, self.Tox, self.rhoOx, self.dHvapOx, 
                                          self.surfOx, self.viscOx, self.MolWtOx)
        #print('C1ox=%g, C2ox=%g'%(self.C1ox, self.C2ox)  )
            
        # now figure out dropo sizes
        #C  MEDIAN DROPLET RADIUS
        self.rDropOx = 0.05 * self.DorfOx * self.C1ox * self.dropCorrOx
        self.rDropFuel = 0.05 * self.DorfFuel * self.C1fuel * self.dropCorrFuel
        
        CR = self.geomObj.CR
        #C  CHAMBER SHAPE FACTOR
        self.ShapeFact = (1.0 + 1.0/sqrt(CR) + 1./ CR )/3.

        #         GENERALIZED VAPORIZATION LENGTH
        #   Taken from Technical Report R-67, Propellant Vaporization as a Design Criterion
        #   for Rocket-Engine Combustion Chambers by Richard J. Priem and Marcus F. Heidmann
        #     see: https://digital.library.unt.edu/ark:/67531/metadc56386/
        #      or: https://www.google.com/books/edition/Propellant_Vaporization_as_a_Design_Crit/Jt4QAQAAIAAJ?hl=en&gbpv=1

        CFX = (self.geomObj.Lcham_cyl/CR**.44 + .83*self.geomObj.Lcham_conv/(CR**.22 * self.ShapeFact**.33))\
            *(self.coreObj.Pc/300.)**.66
        self.genVapLenOx = CFX/(self.C2ox*(self.rDropOx/.003)**1.45 * (self.velOx_ips/1200.)**.75)
        self.genVapLenFuel = CFX/(self.C2fuel*(self.rDropFuel/.003)**1.45 * (self.velFuel_ips/1200.)**.75)
        
        self.fracVapOx = fracVaporized( self.genVapLenOx )
        self.fracVapFuel = fracVaporized( self.genVapLenFuel )

        
        # get vaporized MR
        self.mrVap = self.coreObj.MRcore * self.fracVapOx / self.fracVapFuel
        
        # get total vaporized propellant (ox + fuel)
        self.fracVapTot = (self.fracVapOx*self.coreObj.wdotOx + self.fracVapFuel*self.coreObj.wdotFl) / \
                          self.coreObj.wdotTot
        
        # calc vaporization efficiency (protect against excess fracVapTot)
        if self.fracVapTot < 1.0:
            vapIsp = self.coreObj.ceaObj.get_Isp( Pc=self.coreObj.Pc, MR=self.mrVap, eps=self.geomObj.eps)
            effVap = min(1.0, self.fracVapTot * vapIsp / self.coreObj.IspODE)
        else:
            effVap = 1.0
            
        return effVap

    
    def calculate_effEm(self):
        """calc intra-element mixing efficiency"""
        
        if self.elemEm >= 1.0:
            self.effEm = 1.0
            return 1.0
        
        mrLow = self.coreObj.MRcore * self.elemEm
        mrHi = self.coreObj.MRcore / self.elemEm
        
        IspODK = calc_IspODK(self.coreObj.ceaObj, Pc=self.coreObj.Pc, eps=self.geomObj.eps, Rthrt=self.geomObj.Rthrt, 
                                    pcentBell=self.geomObj.pcentBell, MR=self.coreObj.MRcore)
        
        odkLoIsp = calc_IspODK(self.coreObj.ceaObj, Pc=self.coreObj.Pc, eps=self.geomObj.eps, Rthrt=self.geomObj.Rthrt, 
                                    pcentBell=self.geomObj.pcentBell, MR=mrLow)
        odkHiIsp = calc_IspODK(self.coreObj.ceaObj, Pc=self.coreObj.Pc, eps=self.geomObj.eps, Rthrt=self.geomObj.Rthrt, 
                                    pcentBell=self.geomObj.pcentBell, MR=mrHi)
                                  
        xm1=(1.+mrLow)/(1.+self.elemEm)/(1.+self.coreObj.MRcore)
        xm2=1.0-xm1
        effEm = (xm1*odkLoIsp + xm2*odkHiIsp) / IspODK

        return max(effEm, 0.00001)
            
    def calculate_effMix(self):
        """calc inter-element mixing efficiency"""
        DiamElem =  self.geomObj.Dinj * sqrt(pi/4.0/self.Nelements) - (self.DorfOx+self.DorfFuel)/2.0
        DiamElem = max(DiamElem,0.0)
        self.mixAngle = atan( DiamElem / self.geomObj.Lcham )*(180.0/pi)
        effMix = 1. - .01*(self.mixAngle/2.)**2
        #print('DiamElem',DiamElem, '    effMix',effMix, '   mixAngle',self.mixAngle, '   L', self.geomObj.Lcham )
        return max(effMix, 0.00001)
    
    def calc_element_attr(self):
        """calc Nelements, injection velocities, elements diam, etc."""
        
        if self.dpOxInp is None:
            self.dpOx = self.fdPinjOx * self.coreObj.Pc
        else:
            self.dpOx = self.dpOxInp
            self.fdPinjOx = self.dpOxInp / self.coreObj.Pc
        
        if self.dpFuelInp is None:
            self.dpFuel = self.fdPinjFuel * self.coreObj.Pc
        else:
            self.dpFuel = self.dpFuelInp
            self.fdPinjFuel = self.dpFuelInp / self.coreObj.Pc
        
        # calc chamber sonic velocity
        aODE = self.coreObj.ceaObj.get_SonicVelocities(Pc=self.coreObj.Pc, 
                                                       MR=self.coreObj.MRcore,
                                                       eps=self.geomObj.eps)[0]
        # estimate effective sonic velocity in chamber
        self.sonicVel = aODE * 0.9
        
        velFl_ips = sqrt( 24.0 * 32.174 * self.dpFuel / self.rhoFuel ) # in/sec
        
        self.used_Nelem_criteria = self.setNelementsBy
        # calc number of elements and element density
        if self.setNelementsBy == 'input':
            self.Nelements = self.NelementsInp
            self.NOxOrf = max( 1.0, self.Nelements * self.OxOrfPerEl)
            self.NFuelOrf = max( 1.0, self.Nelements * self.FuelOrfPerEl)
            self.elemDensCalc = self.Nelements / self.geomObj.Ainj
        
        elif self.setNelementsBy == 'acoustics':
            if self.setAcousticFreqBy == "mode":
                self.des_freq = self.desAcousMult * self.sonicVel / pi / (self.geomObj.Dinj/12.0)
            elif self.setAcousticFreqBy == "freq":
                self.des_freq = self.desFreqInp
            else:
                raise exception( 'setAcousticFreqBy = "%s", must be "mode" or "freq"'%self.setAcousticFreqBy )
                
            self.DorfFlForHzLimit = self.strouhal_mult * velFl_ips / self.des_freq
            self.dOrifMin = max(self.DorfMin, self.DorfFlForHzLimit)
            
            wdotFlOrif = velFl_ips * self.rhoFuel * self.CdFuelOrf * self.dOrifMin**2 * pi / 4.0
            
            self.NFuelOrf = float(int( 0.5 + max(1.0, self.coreObj.wdotFl / wdotFlOrif)))
            self.Nelements = max(1.0, self.NFuelOrf / self.FuelOrfPerEl)
            self.NOxOrf = max( 1.0, self.Nelements * self.OxOrfPerEl)
            self.elemDensCalc = self.Nelements / self.geomObj.Ainj
            
        elif self.setNelementsBy == 'elem_density':
            self.Nelements =float(int( 0.5 +  max( 1.0, self.elemDensInp * self.geomObj.Ainj )))
            self.NOxOrf = max( 1.0, self.Nelements * self.OxOrfPerEl)
            self.NFuelOrf = max( 1.0, self.Nelements * self.FuelOrfPerEl)
            self.elemDensCalc = self.elemDensInp
        else:
            raise Exception('setNelementsBy="%s" must be "acoustics", "elem_density" or "input"'%self.setNelementsBy)

        
        
        gcc = 32.174 * 12.0 * 2.0
        PIO4 = pi / 4.0
        self.velOx_ips = sqrt(gcc*self.dpOx/self.rhoOx)  # in/sec
        self.velFuel_ips = sqrt(gcc*self.dpFuel/self.rhoFuel) # in/sec
        self.AfloOx = self.coreObj.wdotOx/(self.rhoOx*self.CdOxOrf*self.velOx_ips)
        self.AfloFuel = self.coreObj.wdotFl/(self.rhoFuel*self.CdFuelOrf*self.velFuel_ips)
        self.DorfOx = sqrt(self.AfloOx/(PIO4*self.NOxOrf))
        self.DorfFuel = sqrt(self.AfloFuel/(PIO4*self.NFuelOrf))
        
        # calc (or recalc) des_freq based on actual fuel orifice
        self.des_freq = self.strouhal_mult * velFl_ips / self.DorfFuel
        self._3T_freq = modeSvnD['3T'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0)

        self.velOx_fps   = self.velOx_ips / 12.0  # convert from in/sec to ft/sec
        self.velFuel_fps = self.velFuel_ips / 12.0 # convert from in/sec to ft/sec
        
        # evaluate chug stability based on core stream properties
        mwODE,gamODE = self.coreObj.MWchm, self.coreObj.gammaChm
        cstarERE, TcombODE = self.coreObj.cstarERE, self.coreObj.TcODE
        
        self.tResid = cstarERE * self.geomObj.Vcham * mwODE / 18540.0 / TcombODE / self.geomObj.At / 32.174
        self.tauOx = self.LfanOvDorfOx * self.DorfOx / self.velOx_ips        # vel is in/sec
        self.tauFuel = self.LfanOvDorfFuel * self.DorfFuel / self.velFuel_ips
        
        self.tauOvResOx = self.tauOx / self.tResid
        self.tauOvResFuel = self.tauFuel / self.tResid
        
        def reqd_dPinjOvPc( tauOvRes ):
            C1 = 1.0/(0.4961 + 0.4031/tauOvRes)
            C2 = 1.0/(0.25 + 0.009649*tauOvRes)
            return 1.0/(C1 + C2/tauOvRes)
            
        self.fdPinjOxReqd = reqd_dPinjOvPc( self.tauOvResOx )
        self.fdPinjFuelReqd = reqd_dPinjOvPc( self.tauOvResFuel )

        if self.DorfFuel < 1.01*self.DorfMin:
            self.used_Nelem_criteria = 'DorfMin=%g'%self.DorfMin


    def summ_print(self, show_core_stream=True):
        """
        print to standard output, the current state of Injector instance.
        """
        print( self.get_summ_str() )
        
        
    def get_summ_str(self, show_core_stream=True):
        """
        return string of the current state of Injector instance.
        """
        output = io.StringIO()
        def add( *args, **kwargs ):
            print(*args, file=output, **kwargs)
        
        if show_core_stream:
            c = self.coreObj.get_summ_str()
            print(c, file=output)

        # calc 3T and 1L for printout only
        f3T = modeSvnD['3T'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0)
        freq1L = self.sonicVel * 12.0 / 2.0 / self.geomObj.Lcham
            
            
        add('---------------%s/%s injector-----------------------'%(self.coreObj.oxName, self.coreObj.fuelName))
        
        add('NOTE: number of elements set by ', self.setNelementsBy)
        if self.setNelementsBy == "acoustics":
            if self.setAcousticFreqBy == "mode":
                if self.desAcousMode in modeSvnD:
                    msg = self.desAcousMode + ' where: Svn mult = %g'%self.desAcousMult
                else:
                    msg = 'Svn multiplier = %g'%self.desAcousMult
            elif self.setAcousticFreqBy == "freq":
                msg = 'freq=%g Hz'%self.desFreqInp
            
            add('    Acoustic frequency set by %s'%msg)
        elif  self.setNelementsBy == "input":
            add('    Number of elements = %g'%self.NelementsInp)
        elif  self.setNelementsBy == "elem_density":
            add('    Element Density = %g elem/in**2'%self.elemDensInp)
            
        if self.setNelementsBy == 'acoustics':
            mil = get_value(self.DorfFlForHzLimit,'inch','mil')
            
            if self.DorfFuel < self.DorfFlForHzLimit * 0.999:
                add( 'WARNING... Fuel Orifice is Less Than D/V Requirement of %.1f mil'%mil )
            else:
                add( 'Fuel Orifice Meets Stability Requirement of >= %.1f mil'%mil )
            
        if self.des_freq >  f3T * 1.01:
            add( 'WARNING... Design frequency is above recommended 3T limit of %i Hz'%int(f3T) )
            
        if self.DorfOx <  self.DorfMin * 0.999:
            mil = get_value(self.DorfMin,'inch','mil')
            add( 'WARNING... Oxidizer Orifice is Less Than minimum limit of %.1f mil'%mil )
            
        if self.DorfFuel <  self.DorfMin * 0.999:
            mil = get_value(self.DorfMin,'inch','mil')
            add( 'WARNING... Fuel Orifice is Less Than minimum limit of %.1f mil'%mil )
            
        add('-------------------------------------------------------')
        
        
        
        add('           Tox =', '%g'%self.Tox, 'degR, temperature of oxidizer')
        if self.Tox_warning:
            add( ' '*15 + self.Tox_warning )
        add('         Tfuel =', '%g'%self.Tfuel, 'degR, temperature of fuel')
        if self.Tfuel_warning:
            add( ' '*15 + self.Tfuel_warning )
        add('        elemEm =', '%s'%self.elemEm, 'Rupe factor of injector')
        
        if self.dpOxInp is None:
            add('       fdPinjOx =', '%g'%self.fdPinjOx, '(dpOx=%.1f psia)'%self.dpOx)
        else:
            add('       dpOxInp =', '%.1f psia'%self.dpOxInp, '(fdPinjOx=%g)'%self.fdPinjOx)
        
        if self.dpFuelInp is None:
            add('     fdPinjFuel =', '%g'%self.fdPinjFuel, '(dpFuel=%.1f psia)'%self.dpFuel)
        else:
            add('     dpFuelInp =', '%.1f psia'%self.dpFuelInp, '(fdPinjFuel=%g)'%self.fdPinjFuel)
            
        add('    OxOrfPerEl =', '%g'%self.OxOrfPerEl, '')
        add('  FuelOrfPerEl =', '%g'%self.FuelOrfPerEl, '')
        add('   lolFuelElem =', '%s'%self.lolFuelElem, '')
        
        if self.desFreqInp is None:
            add('  desAcousMode =', '%s'%self.desAcousMode, '(Sv mult=%g)'%self.desAcousMult)
        else:
            add('    desFreqInp =', '%g'%self.desFreqInp, 'Hz')
            
        add('       CdOxOrf =', '%g'%self.CdOxOrf, '')
        add('     CdFuelOrf =', '%g'%self.CdFuelOrf, '')
        add('    dropCorrOx =', '%g'%self.dropCorrOx, '')
        add('  dropCorrFuel =', '%g'%self.dropCorrFuel, '')
        add('       DorfMin =', '%g'%self.DorfMin, 'in')
        add('  LfanOvDorfOx =', '%g'%self.LfanOvDorfOx, '')
        add('LfanOvDorfFuel =', '%g'%self.LfanOvDorfFuel, '')
        add()
        add('          sgOx =', '%g'%self.sgOx, 'g/ml')
        add('       dHvapOx =', '%g'%self.dHvapOx, 'BTU/lbm')
        add('        surfOx =', '%g'%self.surfOx, 'lbf/in')
        add('        viscOx =', '%g'%self.viscOx, 'poise')
        add('       MolWtOx =', '%g'%self.MolWtOx, 'g/gmole')
        add()
        add('        sgFuel =', '%g'%self.sgFuel, 'g/ml')
        add('     dHvapFuel =', '%g'%self.dHvapFuel, 'BTU/lbm')
        add('      surfFuel =', '%g'%self.surfFuel, 'lbf/in')
        add('      viscFuel =', '%g'%self.viscFuel, 'poise')
        add('     MolWtFuel =', '%g'%self.MolWtFuel, 'g/gmole') 
        add()
        add('          dpOx =', '%g'%self.dpOx, 'psid') 
        add('        dpFuel =', '%g'%self.dpFuel, 'psid') 
        
        
        add(' cham des_freq =', '%g'%int(self.des_freq), 'Hz (NOTE: 3T = %g Hz)'%int(f3T)) 
        
        if self.setNelementsBy == "acoustics":
            add('DorfFlForHzLim =', '%.4f'%self.DorfFlForHzLimit, 'in, fuel orifice D for frequency in Hewitt Corr.') 
            add('      dOrifMin =', '%.4f'%self.dOrifMin, 'in, min Dorifice allowed by stability & manufacturing') 

        add('     Nelements =', '%g'%self.Nelements, '(set by %s)'%self.setNelementsBy) 
        add('      NFuelOrf =', '%g'%self.NFuelOrf, '') 
        add('        NOxOrf =', '%g'%self.NOxOrf, '') 
        add('      elemDens =', '%g'%self.elemDensCalc, 'elem/in**2') 
        
        add('         velOx =', '%g'%self.velOx_fps, 'ft/sec') 
        add('       velFuel =', '%g'%self.velFuel_fps, 'ft/sec') 
        add('        AfloOx =', '%g'%self.AfloOx, 'in**2') 
        add('      AfloFuel =', '%g'%self.AfloFuel, 'in**2') 
        add('        DorfOx =', '%.4f'%self.DorfOx, 'in') 
        if self.DorfOx < self.DorfMin * 0.999:
            add( ' '*15 + 'WARNING... Ox Orifice is Less Than Min Requirement of %g '%self.DorfMin )
        add('      DorfFuel =', '%.4f'%self.DorfFuel, 'in') 
        if self.DorfFuel < self.DorfMin * 0.999:
            add( ' '*15 + 'WARNING... Fuel Orifice is Less Than Min Requirement of %g '%self.DorfMin )
        

        #if self.calc_effVap:
        if hasattr(self, 'rDropOx'):
            # only print internal vaporization values if calc'd
            add('        ---')
            add('       rDropOx =', '%g'%get_value(self.rDropOx,'inch','mil'), 'mil, median ox droplet radius') 
            add('     rDropFuel =', '%g'%get_value(self.rDropFuel,'inch','mil'), 'mil, median fuel droplet radius') 
            
            add(' chamShapeFact =', '%g'%self.ShapeFact, '') 
            
            add('   genVapLenOx =', '%g'%self.genVapLenOx, '')
            add(' genVapLenFuel =', '%g'%self.genVapLenFuel, '')
            add('     fracVapOx =', '%g'%self.fracVapOx, '')
            add('   fracVapFuel =', '%g'%self.fracVapFuel, '')
            
            add('         mrVap =', '%g'%self.mrVap, 'vaporized mixture ratio')
        
        
        add('        ---')
        add('        tResid =', '%g'%(self.tResid*1000.0,) , 'ms, residual time in chamber')
        add('         tauOx =', '%g'%(self.tauOx*1000.0,) , 'ms, oxidizer lag time (tau/tResid=%g)'%self.tauOvResOx)
        add('       tauFuel =', '%g'%(self.tauFuel*1000.0,) , 'ms, fuel lag time (tau/tResid=%g)'%self.tauOvResFuel)
        add('  fdPinjOxReqd =', '%g'%self.fdPinjOxReqd, 'required oxidizer dP/Pc')
        add('fdPinjFuelReqd =', '%g'%self.fdPinjFuelReqd, 'required fuel dP/Pc')
        add()
        add(' cham sonicVel =', '%g'%self.sonicVel, 'ft/sec') 
        
        
        add('    --- Acoustic Modes in Chamber ---')
        modeL = [(freq1L,'1L')] # list of (freq, name)
        
        modeL.append( ( 0.8 * modeSvnD['1T'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0), '80% of 1T') )
        modeL.append( ( 0.8 * modeSvnD['1R'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0), '80% of 1R') )
        modeL.append( ( 0.8 * modeSvnD['3T'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0), '80% of 3T') )
        modeL.append( ( 0.999999 * modeSvnD['3T'] * self.sonicVel / pi / (self.geomObj.Dinj/12.0), ' 3T') )
        
        modeL.append( (self.des_freq, '=====> DESIGN') )
        
        for name, mult in modeSvnD.items():
            modeL.append( (mult * self.sonicVel / pi / (self.geomObj.Dinj/12.0), name) )
        modeL.sort()
        for (freq, name) in modeL:
            comment = modeCommentD.get( name, '')
            add('    %10s ='%name, '%i'%int(freq), 'Hz '+comment)
            
        # collect string output
        contents = output.getvalue()
        output.close()
        return contents        
    
    def get_closest_mode(self):
        """Get the name and frequency of the closest mode to des_freq"""
        freq1L = self.sonicVel * 12.0 / 2.0 / self.geomObj.Lcham
        modeL = [(freq1L,'1L')] # list of (freq, name)
        for name, mult in modeSvnD.items():
            modeL.append( (mult * self.sonicVel / pi / (self.geomObj.Dinj/12.0), name) )
        
        diff = float('inf')
        mode = 'unknown'
        mode_freq = 0.0
        for freq, name in modeL:
            d = abs( self.des_freq - freq )
            if d < diff:
                diff = d
                mode = name
                mode_freq = freq
                
        if mode=='1T' and self.des_freq < mode_freq:
            mode = '%g%% 1T'%round( 100.0 * self.des_freq / mode_freq )
            mode_freq = self.des_freq
        return mode, mode_freq
        
    
        #print(' xxx =', '%g'%self.xxx, 'xxx')
modeCommentD = {'80% of 1T':'no damping required here',
                '80% of 1R':'baffles-only work here',
                '3T':'<== MAX FREQUENCY... KEEP Hz HERE OR BELOW',
                '80% of 3T':'cavities-only work here',
                '=====> DESIGN':'<== DESIGN IS HERE',
                ' 3T':'baffles + cavities OR multi-tuned cavities'}
        
        

if __name__ == '__main__':
    from rocketisp.geometry import Geometry
    from rocketisp.stream_tubes import CoreStream
    from rocketisp.efficiencies import Efficiencies
    
    geomObj = Geometry(Rthrt=5.868/2,
                       CR=2.5, eps=150,  pcentBell=80, 
                       RupThroat=1.5, RdwnThroat=1.0, RchmConv=1.0, cham_conv_deg=30,
                       LchmOvrDt=3.10, LchmMin=2.0, LchamberInp=16)
    
    effObj = Efficiencies()
    #effObj.set_const('ERE', 0.98)
    
    core = CoreStream( geomObj, effObj, oxName='N2O4', fuelName='MMH',  MRcore=1.85,
                 Pc=150, CdThroat=0.995,
                 pcentFFC=14.0, ko=0.035)
    
    I = Injector(core, elemEm=0.8, fdPinjOx=0.3, fdPinjFuel=0.3, elemDensInp=7.0, NelementsInp=676,
                 setNelementsBy='elem_density', # can be "acoustics", "elem_density", "input"
                 desFreqInp=2000,  Tox=9999, Tfuel=0,
                 setAcousticFreqBy='mode', desAcousMode='2T')
    I.evaluate()
    I.summ_print()
    