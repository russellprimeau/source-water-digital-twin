  Deltares, DELWAQ  Version  5.10.00.142431, Jan 26 2023, 11:26:39
 Execution start: 2024/09/17 12:06:35 
                                                                                
 found -p command line switch                                                   

 Info: This processes definition file does not contain standard names and units for NetCDF files.

 
 Using process definition file : C:\Program Files\Deltares\Delft3D FM Suite 2023.02 HMWQ\plugins\DeltaShell.Dimr\kernels\x64\dwaq\default\proc_def
 Version number                :       5.00
 Serial                        :   20130101
 
                                                                                
 found -eco command line switch                                                 
 using eco input file:C:\Program Files\Deltares\Delft3D FM Suite 2023.02 HMWQ\pl


 Model :            Water quality calculation               
                                                            


 Run   :                                                    
                    T0: 2024.01.13 00:00:00  (scu=       1s)


# scanning input for old process definitions
 Added process [Conselac            ] based on activated process [WM_DetC             ]
 Added process [Sed_Opal            ] based on activated process [SedN_Det            ]
 Replaced default [SWOxCon             ] based on activated process [WM_DetC             ]
 Replaced default [SO4                 ] based on activated process [WM_DetC             ]
 Replaced default [b_poc1poc2          ] based on activated process [WM_DetC             ]
 Replaced default [b_poc1doc           ] based on activated process [WM_DetC             ]
 Replaced default [SWOMDec             ] based on activated process [WM_DetC             ]
 Replaced default [kl_dFdcC20          ] based on activated process [WM_DetC             ]
 Replaced default [ku_dFdcC20          ] based on activated process [WM_DetC             ]
 Replaced default [kl_dFdcN20          ] based on activated process [WM_DetN             ]
 Replaced default [ku_dFdcN20          ] based on activated process [WM_DetN             ]
 Replaced default [kl_dFdcP20          ] based on activated process [WM_DetP             ]
 Replaced default [ku_dFdcP20          ] based on activated process [WM_DetP             ]
 Replaced default [VSedPOC1            ] based on activated process [SedDetC             ]
 Replaced default [VSedOpal            ] based on activated process [SedDetC             ]
 Replaced default [ExtVLPOC1           ] based on activated process [ExtPODVL            ]
 Replaced default [ExtVLPOC2           ] based on activated process [ExtPODVL            ]
 Process [Compos              ] activated based on old name [POC_DYN             ]
 Process [DecFast             ] activated based on old name [WM_DetC             ]
 Process [Sed_POC1            ] activated based on old name [SedDetC             ]
 Process [SedNPOC1            ] activated based on old name [SedN_Det            ]
 Process [ExtPOGVL            ] activated based on old name [ExtPODVL            ]
 Process [Extinc_VLG          ] activated based on old name [Extinc_VL           ]
 Process [S12traIM1           ] activated based on old name [Res_IM1             ]
 Substance name [DetC                ] replace by new name [POC1                ]
 Substance name [DetN                ] replace by new name [PON1                ]
 Substance name [DetP                ] replace by new name [POP1                ]
 Constant name [RcDetC              ] replace by new name [kl_dFdcC20          ]
 Constant name [TcDetC              ] replace by new name [kT_dec              ]
 Constant name [RcDetN              ] replace by new name [kl_dFdcN20          ]
 Constant name [TcDetN              ] replace by new name [kT_dec              ]
 Constant name [RcDetP              ] replace by new name [kl_dFdcP20          ]
 Constant name [TcDetP              ] replace by new name [kT_dec              ]
 Constant name [VSedDetC            ] replace by new name [VSedPOC1            ]
 Constant name [TauCSDetC           ] replace by new name [TaucSPOC1           ]
 Constant name [ExtVLDetC           ] replace by new name [ExtVLPOC1           ]
 Activated process [WM_DetN             ] obsolete, see documentation remark no:         6
 Activated process [WM_DetP             ] obsolete, see documentation remark no:         6
 Activated process [ExtPOGVL            ] obsolete, see documentation remark no:         0
 no BLOOM algae were found, switching off eco mode.                             
 found only_active constant                                                     
 only activated processes are switched on                                       
 Replaced default [SWOxCon             ]
 current value     :  0.00000    
 replaced by       :  1.00000    
 based on old process definition
 Replaced default [SO4                 ]
 current value     :  0.00000    
 replaced by       :  0.00000    
 based on old process definition
 Replaced default [b_poc1poc2          ]
 current value     :  0.00000    
 replaced by       :  0.00000    
 based on old process definition
 Replaced default [b_poc1doc           ]
 current value     :  0.00000    
 replaced by       :  0.00000    
 based on old process definition
 Replaced default [SWOMDec             ]
 current value     :  0.00000    
 replaced by       :  1.00000    
 based on old process definition
 Replaced default [kl_dFdcC20          ]
 current value     : 0.120000    
 replaced by       : 0.120000    
 based on old process definition
 Replaced default [ku_dFdcC20          ]
 current value     : 0.180000    
 replaced by       : 0.120000    
 based on old process definition
 Replaced default [kl_dFdcN20          ]
 current value     : 0.120000    
 replaced by       : 0.120000    
 based on old process definition
 Replaced default [ku_dFdcN20          ]
 current value     : 0.180000    
 replaced by       : 0.120000    
 based on old process definition
 Replaced default [kl_dFdcP20          ]
 current value     : 0.120000    
 replaced by       : 0.800000E-01
 based on old process definition
 Replaced default [ku_dFdcP20          ]
 current value     : 0.180000    
 replaced by       : 0.800000E-01
 based on old process definition
 Replaced default [VSedPOC1            ]
 current value     : 0.500000    
 replaced by       : 0.100000    
 based on old process definition
 Replaced default [VSedOpal            ]
 current value     : 0.500000    
 replaced by       : 0.100000    
 based on old process definition
 Replaced default [ExtVLPOC1           ]
 current value     : 0.100000    
 replaced by       : 0.470000    
 based on old process definition
 Replaced default [ExtVLPOC2           ]
 current value     : 0.100000    
 replaced by       : 0.600000E-01
 based on old process definition
 Input item  [ku_dFdcC20          ] replaced by [kl_dFdcC20          ] for process [DecFast   ]
 Input item  [ku_dFdcN20          ] replaced by [kl_dFdcN20          ] for process [DecFast   ]
 Input item  [ku_dFdcP20          ] replaced by [kl_dFdcP20          ] for process [DecFast   ]
 Input item  [VSedOpal            ] replaced by [VSedPOC1            ] for process [Sed_Opal  ]
 Input item  [TaucSOpal           ] replaced by [TauCSPOC1           ] for process [Sed_Opal  ]
 Input item  [VSedOpal            ] replaced by [VSedPOC1            ] for process [Sed_Opal  ]
  WARNING: activated process not found in process definition file
  process ID: ExtPOGVL            
 
total number of substances with fractions :  0
# Determining which processes can be switched on                                                    
                                                                                                    
 Input for [DynDepth            ] dynamic calculation of the depth                                  
   Process is activated                                                                             
   Process subroutine: DDEPTH                                                                       
                                                                                                    
 Input for [TotDepth            ] depth water column                                                
   Process is activated                                                                             
   Process subroutine: TOTDEP                                                                       
                                                                                                    
 Input for [Veloc               ] Horizontal flow velocity                                          
   Process is activated                                                                             
   Process subroutine: VELOC                                                                        
                                                                                                    
 Input for [VertDisp            ] Vertical dispersion (segment -> exchange)                         
   Process is activated                                                                             
   Process subroutine: STOX3D                                                                       
                                                                                                    
 Input for [CalTau              ] Calculation of bottom friction                                    
   Process is activated                                                                             
   Process subroutine: CALTAU                                                                       
                                                                                                    
 Input for [ExtPhDVL            ] Extinction of visible light by algae (Dynamo)                     
   Process is activated                                                                             
   Process subroutine: EXTINA                                                                       
                                                                                                    
 Input for [Extinc_VLG          ] Extinction of visible-light (370-680nm) DLWQ-G                    
   Process is activated                                                                             
   Process subroutine: EXTINC                                                                       
                                                                                                    
 Input for [CalcRad             ] Radiation at segment upper and lower boundaries                   
   Process is activated                                                                             
   Process subroutine: CLCRAD                                                                       
                                                                                                    
 Input for [Phy_dyn             ] Computation of phytoplankton - Dynamo                             
   Process is activated                                                                             
   Process subroutine: PHCOMP                                                                       
                                                                                                    
 Input for [S1_Comp             ] Composition sediment layer S1                                     
   Process is activated                                                                             
   Process subroutine: SEDCOM                                                                       
                                                                                                    
 Input for [Compos              ] Composition                                                       
   Process is activated                                                                             
   Process subroutine: WKCOMP                                                                       
                                                                                                    
 Input for [AdsPO4AAP           ] Ad(De)Sorption ortho phosphorus to inorg. matter                  
   Process is activated                                                                             
   Process subroutine: ADSPO4                                                                       
                                                                                                    
 Input for [DenWat_NO3          ] Denitrification in water column                                   
   Process is activated                                                                             
   Process subroutine: DENWAT                                                                       
                                                                                                    
 Input for [Nitrif_NH4          ] Nitrification of ammonium                                         
   Process is activated                                                                             
   Process subroutine: NITRIF                                                                       
                                                                                                    
 Input for [SaturOXY            ] Saturation concentration oxygen                                   
   Process is activated                                                                             
   Process subroutine: SATOXY                                                                       
                                                                                                    
 Input for [RearOXY             ] Reaeration of oxygen                                              
   Process is activated                                                                             
   Process subroutine: REAR                                                                         
                                                                                                    
 Input for [DecFast             ] Mineralization fast decomp. detritus POC1                         
   Process is activated                                                                             
   Process subroutine: DECDET                                                                       
                                                                                                    
 Input for [SedOXYDem           ] Sediment oxygen demand                                            
   Process is activated                                                                             
   Process subroutine: SEDOX                                                                        
                                                                                                    
 Input for [TF_Green            ] Temperature functions for green algae                             
   Process is activated                                                                             
   Process subroutine: TFALG                                                                        
                                                                                                    
 Input for [DL_Green            ] Daylength function for green algae                                
   Process is activated                                                                             
   Process subroutine: DLALG                                                                        
                                                                                                    
 Input for [NLGreen             ] Nutrient limiation function for green algae                       
   Process is activated                                                                             
   Process subroutine: NLALG                                                                        
                                                                                                    
 Input for [Rad_Green           ] Light efficiency function green algae                             
   Process is activated                                                                             
   Process subroutine: RADALG                                                                       
                                                                                                    
 Input for [GroMrt_Gre          ] DYNAMO: Nett primary prod. and mort. green algae                  
   Process is activated                                                                             
   Process subroutine: PRIPRO                                                                       
                                                                                                    
 Input for [PPrLim              ] Limitation (numerical) on primary production                      
   Process is activated                                                                             
   Process subroutine: PPRLIM                                                                       
                                                                                                    
 Input for [NutUpt_Alg          ] Uptake of nutrients by growth of algae                            
   Process is activated                                                                             
   Process subroutine: NUTUPT                                                                       
                                                                                                    
 Input for [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae                
   Process is activated                                                                             
   Process subroutine: NUTREL                                                                       
                                                                                                    
 Input for [CONSELAC            ] Consumption oxygen/other electron acceptors                       
   Process is activated                                                                             
   Process subroutine: CSELAC                                                                       
                                                                                                    
 Input for [Sed_IM1             ] Sedimentation IM1                                                 
   Process is activated                                                                             
   Process subroutine: SEDIM                                                                        
                                                                                                    
 Input for [Sed_Gre             ] Sedimentation green algae                                         
   Process is activated                                                                             
   Process subroutine: SEDCAR                                                                       
                                                                                                    
 Input for [Sed_Opal            ] Sedimentation Opal 3d                                             
   Process is activated                                                                             
   Process subroutine: SEDIM                                                                        
                                                                                                    
 Input for [Sed_POC1            ] Sedimentation POC1 3d                                             
   Process is activated                                                                             
   Process subroutine: SEDIM                                                                        
                                                                                                    
 Input for [SedNPOC1            ] Sedim. nutrients in POC1                                          
   Process is activated                                                                             
   Process subroutine: SEDNU2                                                                       
                                                                                                    
 Input for [Sed_AAP             ] Sedimentation AAP (adsorbed PO4)                                  
   Process is activated                                                                             
   Process subroutine: SEDAAP                                                                       
                                                                                                    
 Input for [S12TraIM1           ] Resuspension, transport in S1-S2 IM1                              
   Process is activated                                                                             
   Process subroutine: S12TIM                                                                       
                                                                                                    
 Input for [PosOXY              ] Positive oxygen concentration                                     
   Process is activated                                                                             
   Process subroutine: POSOXY                                                                       
                                                                                                    
 Input for [Secchi              ] Secchi depth for visible-light (370-680nm)                        
   Process is activated                                                                             
   Process subroutine: SECCHI                                                                       
                                                                                                    
                                                                                                    
# Determining the processes to model the substances.                                                
                                                                                                    
-fluxes for [AAP                 ]                                                                  
 found flux  [dAdsPO4AAP          ] adsorption flux PO4 to AAP                                      
   from proces [AdsPO4AAP           ] Ad(De)Sorption ortho phosphorus to inorg. matter              
   process is switched on.                                                                          
 found flux  [dSedAAP             ] sedimentation flux AAP towards S1                               
   from proces [Sed_AAP             ] Sedimentation AAP (adsorbed PO4)                              
   process is switched on.                                                                          
 found flux  [dSedAAPS2           ] sedimentation flux AAP towards S2                               
   from proces [Sed_AAP             ] Sedimentation AAP (adsorbed PO4)                              
   process is switched on.                                                                          
-dispersion for [AAP                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [AAP                 ]                                                                
 found velocity [VxSedAAP            ] sedimentation velocity AAP                                   
   from proces [Sed_AAP             ] Sedimentation AAP (adsorbed PO4)                              
   process is switched on.                                                                          
                                                                                                    
-fluxes for [POC1                ]                                                                  
 found flux  [dCnvPPOC1           ] conversion flux POC1 to POC2                                    
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dCnvDPOC1           ] conversion flux POC1 to DOC                                     
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMinPOC1G           ] mineralization flux POC1 to CO2                                 
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMortDetC           ] production of DetC by mortality phytoplankton                   
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
 found flux  [dSedPOC1            ] sedimentation flux POC1                                         
   from proces [Sed_POC1            ] Sedimentation POC1 3d                                         
   process is switched on.                                                                          
 found flux  [dSedPOC1S2          ] sedimentation flux POC1                                         
   from proces [Sed_POC1            ] Sedimentation POC1 3d                                         
   process is switched on.                                                                          
-dispersion for [POC1                ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [POC1                ]                                                                
 found velocity [VxSedPOC1           ] sedimentation velocity POC1                                  
   from proces [Sed_POC1            ] Sedimentation POC1 3d                                         
   process is switched on.                                                                          
                                                                                                    
-fluxes for [PON1                ]                                                                  
 found flux  [dCnvPPON1           ] conversion flux PON1 to PON2                                    
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dCnvDPON1           ] conversion flux PON1 to DON                                     
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMinPON1            ] mineralization flux PON1 to NH4                                 
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMortDetN           ] production of DetN by mortality phytoplankton                   
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
 found flux  [dSedPON1            ] sedimentation flux PON1                                         
   from proces [SedNPOC1            ] Sedim. nutrients in POC1                                      
   process is switched on.                                                                          
 found flux  [dSedPON1S2          ] sedimentation flux PON1                                         
   from proces [SedNPOC1            ] Sedim. nutrients in POC1                                      
   process is switched on.                                                                          
-dispersion for [PON1                ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [PON1                ]                                                                
 found velocity [VxSedPOC1           ] sedimentation velocity POC1                                  
   from proces [Sed_POC1            ] Sedimentation POC1 3d                                         
   process is switched on.                                                                          
                                                                                                    
-fluxes for [POP1                ]                                                                  
 found flux  [dCnvPPOP1           ] conversion flux POP1 to POP2                                    
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dCnvDPOP1           ] conversion flux POP1 to DOP                                     
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMinPOP1            ] mineralization flux POP1 to PO4                                 
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dMortDetP           ] production of DetP by mortality phytoplankton                   
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
 found flux  [dSedPOP1            ] sedimentation flux POP1                                         
   from proces [SedNPOC1            ] Sedim. nutrients in POC1                                      
   process is switched on.                                                                          
 found flux  [dSedPOP1S2          ] sedimentation flux POP1                                         
   from proces [SedNPOC1            ] Sedim. nutrients in POC1                                      
   process is switched on.                                                                          
-dispersion for [POP1                ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [POP1                ]                                                                
 found velocity [VxSedPOC1           ] sedimentation velocity POC1                                  
   from proces [Sed_POC1            ] Sedimentation POC1 3d                                         
   process is switched on.                                                                          
                                                                                                    
-fluxes for [GREEN               ]                                                                  
 found flux  [dPPGreen            ] net primary production of Greens                                
   from proces [GroMrt_Gre          ] DYNAMO: Nett primary prod. and mort. green algae              
   process is switched on.                                                                          
 found flux  [dMrtGreen           ] mortality of Greens                                             
   from proces [GroMrt_Gre          ] DYNAMO: Nett primary prod. and mort. green algae              
   process is switched on.                                                                          
 found flux  [dcPPGreen           ] correction flux Greens growth                                   
   from proces [PPrLim              ] Limitation (numerical) on primary production                  
   process is switched on.                                                                          
 found flux  [dSedGreen           ] sedimentation flux Greens                                       
   from proces [Sed_Gre             ] Sedimentation green algae                                     
   process is switched on.                                                                          
-dispersion for [GREEN               ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [GREEN               ]                                                                
 found velocity [VxSedGreen          ] sedimentation velocity Greens                                
   from proces [Sed_Gre             ] Sedimentation green algae                                     
   process is switched on.                                                                          
                                                                                                    
-fluxes for [NH4                 ]                                                                  
 found flux  [dNITRIF             ] nitrification flux                                              
   from proces [Nitrif_NH4          ] Nitrification of ammonium                                     
   process is switched on.                                                                          
 found flux  [dMinPON1            ] mineralization flux PON1 to NH4                                 
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dNH4Upt             ] NH4 uptake by algae growth                                      
   from proces [NutUpt_Alg          ] Uptake of nutrients by growth of algae                        
   process is switched on.                                                                          
 found flux  [dNH4Aut             ] autolysis flux of NH4                                           
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
-dispersion for [NH4                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [NH4                 ]                                                                
 no velocity found                                                                                  
                                                                                                    
-fluxes for [NO3                 ]                                                                  
 found flux  [dDenitWat           ] denitrification flux in the water column                        
   from proces [DenWat_NO3          ] Denitrification in water column                               
   process is switched on.                                                                          
 found flux  [dNITRIF             ] nitrification flux                                              
   from proces [Nitrif_NH4          ] Nitrification of ammonium                                     
   process is switched on.                                                                          
 found flux  [dNO3Upt             ] uptake of NO3 by algae growth                                   
   from proces [NutUpt_Alg          ] Uptake of nutrients by growth of algae                        
   process is switched on.                                                                          
 found flux  [dNiDen              ] mineralisation flux oxidised with nitrate                       
   from proces [CONSELAC            ] Consumption oxygen/other electron acceptors                   
   process is switched on.                                                                          
-dispersion for [NO3                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [NO3                 ]                                                                
 no velocity found                                                                                  
                                                                                                    
-fluxes for [PO4                 ]                                                                  
 found flux  [dAdsPO4AAP          ] adsorption flux PO4 to AAP                                      
   from proces [AdsPO4AAP           ] Ad(De)Sorption ortho phosphorus to inorg. matter              
   process is switched on.                                                                          
 found flux  [dMinPOP1            ] mineralization flux POP1 to PO4                                 
   from proces [DecFast             ] Mineralization fast decomp. detritus POC1                     
   process is switched on.                                                                          
 found flux  [dPO4Upt             ] PO4 uptake by algae growth                                      
   from proces [NutUpt_Alg          ] Uptake of nutrients by growth of algae                        
   process is switched on.                                                                          
 found flux  [dPO4Aut             ] autolysis of PO4                                                
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
-dispersion for [PO4                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [PO4                 ]                                                                
 no velocity found                                                                                  
                                                                                                    
-fluxes for [OXY                 ]                                                                  
 found flux  [dDenitWat           ] denitrification flux in the water column                        
   from proces [DenWat_NO3          ] Denitrification in water column                               
   process is switched on.                                                                          
 found flux  [dNITRIF             ] nitrification flux                                              
   from proces [Nitrif_NH4          ] Nitrification of ammonium                                     
   process is switched on.                                                                          
 found flux  [dREAROXY            ] reaeration flux of dissolved oxygen                             
   from proces [RearOXY             ] Reaeration of oxygen                                          
   process is switched on.                                                                          
 found flux  [dOxSOD              ] oxygen consumption from SOD                                     
   from proces [SedOXYDem           ] Sediment oxygen demand                                        
   process is switched on.                                                                          
 found flux  [dPPGreen            ] net primary production of Greens                                
   from proces [GroMrt_Gre          ] DYNAMO: Nett primary prod. and mort. green algae              
   process is switched on.                                                                          
 found flux  [dcPPGreen           ] correction flux Greens growth                                   
   from proces [PPrLim              ] Limitation (numerical) on primary production                  
   process is switched on.                                                                          
 found flux  [dcPPDiat            ] correction flux Diatoms growth                                  
   from proces [PPrLim              ] Limitation (numerical) on primary production                  
   process is switched on.                                                                          
 found flux  [dNO3Upt             ] uptake of NO3 by algae growth                                   
   from proces [NutUpt_Alg          ] Uptake of nutrients by growth of algae                        
   process is switched on.                                                                          
 found flux  [dOxCon              ] mineralisation flux oxidised with DO                            
   from proces [CONSELAC            ] Consumption oxygen/other electron acceptors                   
   process is switched on.                                                                          
-dispersion for [OXY                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [OXY                 ]                                                                
 no velocity found                                                                                  
                                                                                                    
-fluxes for [Cl                  ]                                                                  
 no fluxes found                                                                                    
-dispersion for [Cl                  ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [Cl                  ]                                                                
 no velocity found                                                                                  
                                                                                                    
-fluxes for [IM1                 ]                                                                  
 found flux  [dSedIM1             ] sedimentation flux of IM1 towards S1                            
   from proces [Sed_IM1             ] Sedimentation IM1                                             
   process is switched on.                                                                          
 found flux  [dSedIM1S2           ] sedimentation flux of IM1 towards S2                            
   from proces [Sed_IM1             ] Sedimentation IM1                                             
   process is switched on.                                                                          
 found flux  [dResS1IM1           ] resuspension flux IM1 from layer S1                             
   from proces [S12TraIM1           ] Resuspension, transport in S1-S2 IM1                          
   process is switched on.                                                                          
 found flux  [dResS2IM1           ] resuspension flux IM1 from layer S2                             
   from proces [S12TraIM1           ] Resuspension, transport in S1-S2 IM1                          
   process is switched on.                                                                          
-dispersion for [IM1                 ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [IM1                 ]                                                                
 found velocity [VxSedIm1            ] sedimentation velocity IM1                                   
   from proces [Sed_IM1             ] Sedimentation IM1                                             
   process is switched on.                                                                          
                                                                                                    
-fluxes for [Opal                ]                                                                  
 found flux  [dMortDetSi          ] production of DetSi by mortality phytoplankton                  
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
 found flux  [dMortOOSi           ] production of OOSi by mortality phytoplankton                   
   from proces [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae            
   process is switched on.                                                                          
 found flux  [dSedOpal            ] sedimentation flux of Opal                                      
   from proces [Sed_Opal            ] Sedimentation Opal 3d                                         
   process is switched on.                                                                          
 found flux  [dSedOpalS2          ] sedimentation flux of Opal                                      
   from proces [Sed_Opal            ] Sedimentation Opal 3d                                         
   process is switched on.                                                                          
-dispersion for [Opal                ]                                                              
 found dispersion[VertDisp            ] vertical dispersion                                         
   from proces [VertDisp            ] Vertical dispersion (segment -> exchange)                     
   process is switched on.                                                                          
-velocity for [Opal                ]                                                                
 found velocity [VxSedOpal           ] sedimentation velocity Opal                                  
   from proces [Sed_Opal            ] Sedimentation Opal 3d                                         
   process is switched on.                                                                          
                                                                                                    
-fluxes for [SOD                 ]                                                                  
 found flux  [dSOD                ] decay flux of SOD                                               
   from proces [SedOXYDem           ] Sediment oxygen demand                                        
   process is switched on.                                                                          
-dispersion for [SOD                 ]                                                              
 no dispersions found                                                                               
-velocity for [SOD                 ]                                                                
 no velocity found                                                                                  
                                                                                                    
# locating processes for requested output                                                           
                                                                                                    
# determining the input for the processes (in reversed order)                                       
                                                                                                    
 Input for [Secchi              ] Secchi depth for visible-light (370-680nm)                        
       [ExtVl               ] total extinction coefficient visible light                            
       Using output from proces [Extinc_VLG          ]                                              
       [IM1                 ] inorganic matter (IM1)                                                
       Using substance nr  11                                                                       
       [IM2                 ] inorganic matter (IM2)                                                
       using default value:  0.00000                                                                
       [IM3                 ] inorganic matter (IM3)                                                
       using default value:  0.00000                                                                
       [POC1                ] POC1 (fast decomposing fraction)                                      
       Using substance nr   2                                                                       
       [POC2                ] POC2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [POC3                ] POC3 (slow decomposing fraction)                                      
       using default value:  0.00000                                                                
       [POC4                ] POC4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
       [ExtVlODS            ] VL extinction by DOC                                                  
       Using output from proces [Extinc_VLG          ]                                              
       [Chlfa               ] Chlorophyll-a concentration                                           
       Using output from proces [Phy_dyn             ]                                              
       [SW_Uitz             ] Extinction by Uitzicht On (1) or Off (0)                              
       using default value:  0.00000                                                                
       [UitZDEPT1           ] Z1 (depth)                                                            
       using default value:  1.20000                                                                
       [UitZDEPT2           ] Z2 (depth)                                                            
       using default value:  1.00000                                                                
       [UitZCORCH           ] CORa correction factor                                                
       using default value:  2.50000                                                                
       [UitZC_DET           ] C3 coeff. absorption ash weight & detritus                            
       using default value: 0.260000E-01                                                            
       [UitZC_GL1           ] C1 coeff. absorption ash weight & detritus                            
       using default value: 0.730000                                                                
       [UitZC_GL2           ] C2 coeff. absorption ash weight & detritus                            
       using default value:  1.00000                                                                
       [UitZHELHM           ] Hel_h constant                                                        
       using default value: 0.140000E-01                                                            
       [UitZTAU             ] Tau constant calculation transparency                                 
       using default value:  7.80000                                                                
       [UitZangle           ] Angle of incidence solar radiation                                    
       using default value:  30.0000                                                                
       [DMCFDetC            ] DM:C ratio DetC                                                       
       using default value:  2.50000                                                                
       [PAConstant          ] Poole-Atkins constant                                                 
       using default value:  1.70000                                                                
                                                                                                    
 Input for [PosOXY              ] Positive oxygen concentration                                     
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
                                                                                                    
 Input for [S12TraIM1           ] Resuspension, transport in S1-S2 IM1                              
       [FrIM1S1             ] fraction IM1 in layer S1                                              
       Using output from proces [S1_Comp             ]                                              
       [ScalCar             ] scale factor for primary variable                                     
       using default value:  1.00000                                                                
       [FrIM1S2             ] fraction IM1 in layer S2                                              
       using default value:  0.00000                                                                
       [ScalCar             ] scale factor for primary variable                                     
       using default value:  1.00000                                                                
       [FrIM1S3             ] fraction IM1 in layer S3                                              
       using default value:  0.00000                                                                
       [ScalCar             ] scale factor for primary variable                                     
       using default value:  1.00000                                                                
       [fResS1DM            ] total resuspension flux DM from layer S1                              
       Using constant nr 77 with value:  0.00000                                                    
       [fResS2DM            ] total resuspension flux DM from layer S2                              
       using default value:  0.00000                                                                
       [fBurS1DM            ] total burial flux DM from layer S1                                    
       using default value:  0.00000                                                                
       [fBurS2DM            ] total burial flux DM from layer S2                                    
       using default value:  0.00000                                                                
       [fDigS1DM            ] total digging flux DM to layer S1                                     
       using default value:  0.00000                                                                
       [fDigS2DM            ] total digging flux DM to layer S2                                     
       using default value:  0.00000                                                                
       [SWDigS1             ] switch for digging S1 (0=actual, 1=deeper)                            
       using default value:  0.00000                                                                
       [SWDigS2             ] switch for digging S2 (0=actual, 1=deeper)                            
       using default value:  0.00000                                                                
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [SedZoneSW           ] SWITCH 0=no SWITCH, <0 per segment, >0 per zone                       
       using default value:  0.00000                                                                
       [SWResIM1            ] switch resuspension IM1 (0=resdm, 1=resim1)                           
       using default value:  0.00000                                                                
       [SWResusp            ] switch resuspension (0=z+f, 1=min(z,f))                               
       using default value:  0.00000                                                                
       [IM1S1               ] IM1 in layer S1                                                       
       using default value:  0.00000                                                                
       [IM1S2               ] IM1 in layer S2                                                       
       using default value:  0.00000                                                                
       [ZResIM1             ] zeroth-order resuspension flux IM1                                    
       using default value:  0.00000                                                                
       [VResIM1             ] first order resuspension velocity IM1                                 
       using default value:  0.00000                                                                
       [Tau                 ] total bottom shear stress                                             
       Using output from proces [CalTau              ]                                              
       [TaucRS1IM1          ] critical shear stress for resuspension IM1S1                          
       using default value: 0.200000                                                                
       [TaucRS2IM1          ] critical shear stress for resuspension IM1S2                          
       using default value: 0.500000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [MinDepth            ] minimum waterdepth for sedimentation/resuspension                     
       using default value: 0.100000                                                                
                                                                                                    
 Input for [Sed_AAP             ] Sedimentation AAP (adsorbed PO4)                                  
       [fSedIM1             ] sedimentation flux IM1 towards S1                                     
       Using output from proces [Sed_IM1             ]                                              
       [fSedIM2             ] sedimentation flux IM2 towards S1                                     
       using default value:  0.00000                                                                
       [fSedIM3             ] sedimentation flux IM3 towards S1                                     
       using default value:  0.00000                                                                
       [fSedIM1S2           ] sedimentation flux IM1 towards S2                                     
       Using output from proces [Sed_IM1             ]                                              
       [fSedIM2S2           ] sedimentation flux IM2 towards S2                                     
       using default value:  0.00000                                                                
       [fSedIM3S2           ] sedimentation flux IM3 towards S2                                     
       using default value:  0.00000                                                                
       [QPIM1               ] quality IM1 for P                                                     
       Using output from proces [AdsPO4AAP           ]                                              
       [QPIM2               ] quality IM2 for P                                                     
       Using output from proces [AdsPO4AAP           ]                                              
       [QPIM3               ] quality IM3 for P                                                     
       Using output from proces [AdsPO4AAP           ]                                              
       [FPIM1               ] fraction of P adsorbed on IM1                                         
       Using output from proces [AdsPO4AAP           ]                                              
       [FPIM2               ] fraction of P adsorbed on IM2                                         
       Using output from proces [AdsPO4AAP           ]                                              
       [FPIM3               ] fraction of P adsorbed on IM3                                         
       Using output from proces [AdsPO4AAP           ]                                              
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [SedZoneSW           ] SWITCH 0=no SWITCH, <0 per segment, >0 per zone                       
       using default value:  0.00000                                                                
       [VxSedIM1            ] sedimentation velocity IM1                                            
       Using output from proces [Sed_IM1             ]                                              
       [VxSedIM2            ] sedimentation velocity IM2                                            
       using default value:  0.00000                                                                
       [VxSedIM3            ] sedimentation velocity IM3                                            
       using default value:  0.00000                                                                
                                                                                                    
 Input for [SedNPOC1            ] Sedim. nutrients in POC1                                          
       [fSedPOC1            ] sedimentation flux POC1                                               
       Using output from proces [Sed_POC1            ]                                              
       [fSedPOC1S2          ] sedimentation flux POC1 to S2                                         
       Using output from proces [Sed_POC1            ]                                              
       [C-NPOC1             ] C:N ratio fast decaying detritus                                      
       Using output from proces [Compos              ]                                              
       [C-PPOC1             ] C:P ratio fast decaying detritus                                      
       Using output from proces [Compos              ]                                              
       [C-SPOC1             ] C:S ratio fast decaying detritus                                      
       Using output from proces [Compos              ]                                              
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
                                                                                                    
 Input for [Sed_POC1            ] Sedimentation POC1 3d                                             
       [POC1                ] POC1 (fast decomposing fraction)                                      
       Using substance nr   2                                                                       
       [ZSedPOC1            ] zeroth-order sedimentation flux POC1                                  
       using default value:  0.00000                                                                
       [VSedPOC1            ] sedimentation velocity POC1                                           
       Using constant nr 48 with value: 0.100000E-01                                                
       [Tau                 ] total bottom shear stress                                             
       Using output from proces [CalTau              ]                                              
       [TaucSPOC1           ] critical shear stress for sedimentation POC1                          
       Using constant nr 49 with value: 0.100000                                                    
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [MinDepth            ] minimum waterdepth for sedimentation/resuspension                     
       using default value: 0.100000                                                                
       [FrPO1SedS2          ] fraction sedimentation POC1 towards S2                                
       using default value:  0.00000                                                                
       [FrPOMS2             ] fraction POM in layer S2                                              
       using default value:  0.00000                                                                
       [FrPOMS2Max          ] maximum fraction POM in layer S2 pick-up                              
       using default value:  1.00000                                                                
       [PsedminPO1          ] minimum sedimentation probability                                     
       using default value:  0.00000                                                                
       [VSedPOC1            ] sedimentation velocity POC1                                           
       Using constant nr 48 with value: 0.100000E-01                                                
                                                                                                    
 Input for [Sed_Opal            ] Sedimentation Opal 3d                                             
       [Opal                ] Opal-Si                                                               
       Using substance nr  12                                                                       
       [ZSedOpal            ] zeroth-order sedimentation flux Opal                                  
       using default value:  0.00000                                                                
       [VSedPOC1            ] sedimentation velocity POC1                                           
       Using constant nr 48 with value: 0.100000E-01                                                
       [Tau                 ] total bottom shear stress                                             
       Using output from proces [CalTau              ]                                              
       [TaucSPOC1           ] critical shear stress for sedimentation POC1                          
       Using constant nr 49 with value: 0.100000                                                    
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [MinDepth            ] minimum waterdepth for sedimentation/resuspension                     
       using default value: 0.100000                                                                
       [FrOplSedS2          ] fraction sedimentation Opal towards S2                                
       using default value:  0.00000                                                                
       [FrPOMS2             ] fraction POM in layer S2                                              
       using default value:  0.00000                                                                
       [FrPOMS2Max          ] maximum fraction POM in layer S2 pick-up                              
       using default value:  1.00000                                                                
       [PsedminOpl          ] minimum sedimentation probability                                     
       using default value:  0.00000                                                                
       [VSedPOC1            ] sedimentation velocity POC1                                           
       Using constant nr 48 with value: 0.100000E-01                                                
                                                                                                    
 Input for [Sed_Gre             ] Sedimentation green algae                                         
       [Green               ] Algae (non-Diatoms) (DYNAMO)                                          
       Using substance nr   5                                                                       
       [ZSedGreen           ] zeroth-order sedimentation flux Greens                                
       using default value:  0.00000                                                                
       [VSedGreen           ] sedimentation velocity Greens                                         
       using default value:  0.00000                                                                
       [Tau                 ] total bottom shear stress                                             
       Using output from proces [CalTau              ]                                              
       [TaucSGreen          ] critical shear stress for sedimentation Greens                        
       using default value: 0.100000                                                                
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [MinDepth            ] minimum waterdepth for sedimentation/resuspension                     
       using default value: 0.100000                                                                
       [VSedGreen           ] sedimentation velocity Greens                                         
       using default value:  0.00000                                                                
                                                                                                    
 Input for [Sed_IM1             ] Sedimentation IM1                                                 
       [IM1                 ] inorganic matter (IM1)                                                
       Using substance nr  11                                                                       
       [ZSedIM1             ] zeroth-order sedimentation flux IM1                                   
       using default value:  0.00000                                                                
       [VSedIM1             ] sedimentation velocity IM1                                            
       Using constant nr 75 with value: 0.100000                                                    
       [Tau                 ] total bottom shear stress                                             
       Using output from proces [CalTau              ]                                              
       [TaucSIM1            ] critical shear stress for sedimentation IM1                           
       Using constant nr 76 with value: 0.100000                                                    
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [MinDepth            ] minimum waterdepth for sedimentation/resuspension                     
       using default value: 0.100000                                                                
       [FrIM1SedS2          ] fraction sedimentation IM1 towards S2                                 
       using default value:  0.00000                                                                
       [FrTIMS2             ] fraction TIM in layer S2                                              
       using default value:  0.00000                                                                
       [FrTIMS2Max          ] maximum fraction TIM in layer S2 pick-up                              
       using default value:  1.00000                                                                
       [PsedminIM1          ] minimum sedimentation probability                                     
       using default value:  0.00000                                                                
       [VSedIM1             ] sedimentation velocity IM1                                            
       Using constant nr 75 with value: 0.100000                                                    
                                                                                                    
 Input for [CONSELAC            ] Consumption oxygen/other electron acceptors                       
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [FeIIIpa             ] particulate amorphous oxidizing iron                                  
       using default value:  0.00000                                                                
       [SO4                 ] sulphate (SO4)                                                        
       using default value:  0.00000                                                                
       [f_minPOC1           ] mineralization flux POC1                                              
       Using output from proces [DecFast             ]                                              
       [f_minPOC2           ] mineralization flux POC2                                              
       using default value:  0.00000                                                                
       [f_minPOC3           ] mineralization flux POC3                                              
       using default value:  0.00000                                                                
       [f_minPOC4           ] mineralization flux POC4                                              
       using default value:  0.00000                                                                
       [f_minPOC5           ] mineralization flux POC5 submerged                                    
       using default value:  0.00000                                                                
       [f_minDOC            ] mineralization flux DOC                                               
       using default value:  0.00000                                                                
       [KsOxCon             ] half saturation constant for DO limitation                            
       using default value:  2.00000                                                                
       [KsNiDen             ] half saturation constant for nitrate cons.                            
       using default value: 0.500000                                                                
       [KsFeRed             ] half saturation constant for Fe limitation                            
       using default value:  2.00000                                                                
       [KsSuRed             ] half saturation constant for SO4 limitation                           
       using default value:  2.00000                                                                
       [KsOxDenInh          ] half saturation constant for oxygen inhib.                            
       using default value: 0.200000                                                                
       [KsNiIRdInh          ] half sat. const. NO3 inhib. iron reduction                            
       using default value: 0.200000                                                                
       [KsNiSRdInh          ] half sat. const. NO3 inhib. SO4 reduction                             
       using default value: 0.200000                                                                
       [KsSuMetInh          ] half saturation constant for SO4 inhibition                           
       using default value:  1.00000                                                                
       [TcOxCon             ] temperature coeff. for oxygen consumption                             
       using default value:  1.07000                                                                
       [TcDen               ] temperature coefficient for denitrification                           
       using default value:  1.12000                                                                
       [TcIRed              ] temperature coeff. for iron reduction                                 
       using default value:  1.12000                                                                
       [TcSRed              ] temperature coeff. for sulphate reduction                             
       using default value:  1.12000                                                                
       [TcMet               ] temperature coeff. for methanogenesis                                 
       using default value:  1.12000                                                                
       [RedFacDen           ] reduction factor for denitrif. at low temp.                           
       using default value:  1.00000                                                                
       [RedFacIRed          ] reduction factor for iron red. at low temp.                           
       using default value:  1.00000                                                                
       [RedFacSRed          ] reduction factor for sulph. red. at low temp.                         
       using default value:  1.00000                                                                
       [RedFacMet           ] reduction factor for methanog. at low temp.                           
       using default value:  1.00000                                                                
       [CoxDenInh           ] crit. diss. ox. conc. for inhib. denitrif.                            
       using default value:  1.00000                                                                
       [CoxIRedInh          ] crit. diss. ox. conc. for inhib. iron red.                            
       using default value: 0.200000                                                                
       [CoxSRedInh          ] crit. diss. ox. conc. for inhib. sulph. red.                          
       using default value: 0.200000                                                                
       [CoxMetInh           ] crit. diss. ox. conc. for inhib. methanog.                            
       using default value: 0.200000E-01                                                            
       [CniMetInh           ] crit. nitrate conc. for inhib. methanog.                              
       using default value: 0.100000                                                                
       [CTBactAc            ] critical temp. for specific bacterial activity                        
       using default value:  3.00000                                                                
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [Poros               ] volumetric porosity                                                   
       using default value:  1.00000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [FrMetGeCH4          ] fraction of methanogenesis towards CH4                                
       using default value: 0.500000                                                                
       [SWOxCon             ] Switch: only OxCon (1) or not (0)                                     
       using default value:  1.00000                                                                
                                                                                                    
 Input for [NutRel_Alg          ] Release (nutrients/detritus) by of mortality algae                
       [fMrtGreen           ] mortality flux Greens                                                 
       Using output from proces [GroMrt_Gre          ]                                              
       [NCRatGreen          ] N:C ratio Greens                                                      
       Using constant nr 44 with value: 0.160000                                                    
       [PCRatGreen          ] P:C ratio Greens                                                      
       Using constant nr 45 with value: 0.200000E-01                                                
       [FrAutGreen          ] fraction autolysis Greens                                             
       Using constant nr 46 with value: 0.300000                                                    
       [FrDetGreen          ] fraction to detritus by mortality Greens                              
       Using constant nr 47 with value: 0.700000                                                    
       [fMrtDiat            ] mortality flux Diatoms                                                
       using default value:  0.00000                                                                
       [NCRatDiat           ] N:C ratio Diatoms                                                     
       using default value: 0.160000                                                                
       [PCRatDiat           ] P:C ratio Diatoms                                                     
       using default value: 0.200000E-01                                                            
       [SCRatDiat           ] Si:C ratio Diatoms                                                    
       using default value: 0.490000                                                                
       [FrAutDiat           ] fraction autolysis Diatoms                                            
       using default value: 0.300000                                                                
       [FrDetDiat           ] fraction detritus by mortality Diatoms                                
       using default value: 0.700000                                                                
                                                                                                    
 Input for [NutUpt_Alg          ] Uptake of nutrients by growth of algae                            
       [fcPPGreen           ] numerical maximum flux Greens                                         
       Using output from proces [PPrLim              ]                                              
       [NCRatGreen          ] N:C ratio Greens                                                      
       Using constant nr 44 with value: 0.160000                                                    
       [PCRatGreen          ] P:C ratio Greens                                                      
       Using constant nr 45 with value: 0.200000E-01                                                
       [fcPPDiat            ] numerical maximum flux Diatoms                                        
       Using output from proces [PPrLim              ]                                              
       [NCRatDiat           ] N:C ratio Diatoms                                                     
       using default value: 0.160000                                                                
       [PCRatDiat           ] P:C ratio Diatoms                                                     
       using default value: 0.200000E-01                                                            
       [SCRatDiat           ] Si:C ratio Diatoms                                                    
       using default value: 0.490000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [NH4                 ] Ammonium (NH4)                                                        
       Using substance nr   6                                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [NH4KRIT             ] critical NH4 concentration                                            
       using default value: 0.100000E-01                                                            
                                                                                                    
 Input for [PPrLim              ] Limitation (numerical) on primary production                      
       [fPPGreen            ] net primary production of Greens                                      
       Using output from proces [GroMrt_Gre          ]                                              
       [NCRatGreen          ] N:C ratio Greens                                                      
       Using constant nr 44 with value: 0.160000                                                    
       [PCRatGreen          ] P:C ratio Greens                                                      
       Using constant nr 45 with value: 0.200000E-01                                                
       [fPPDiat             ] net primary production of Diatoms                                     
       using default value:  0.00000                                                                
       [NCRatDiat           ] N:C ratio Diatoms                                                     
       using default value: 0.160000                                                                
       [PCRatDiat           ] P:C ratio Diatoms                                                     
       using default value: 0.200000E-01                                                            
       [SCRatDiat           ] Si:C ratio Diatoms                                                    
       using default value: 0.490000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [NH4                 ] Ammonium (NH4)                                                        
       Using substance nr   6                                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [PO4                 ] Ortho-Phosphate (PO4)                                                 
       Using substance nr   8                                                                       
       [Si                  ] dissolved Silica (Si)                                                 
       using default value:  0.00000                                                                
                                                                                                    
 Input for [GroMrt_Gre          ] DYNAMO: Nett primary prod. and mort. green algae                  
       [Green               ] Algae (non-Diatoms) (DYNAMO)                                          
       Using substance nr   5                                                                       
       [LimDLGreen          ] daylength limitation function for Greens <0-1>                        
       Using output from proces [DL_Green            ]                                              
       [LimNutGree          ] nutrient limitation function Greens <0-1>                             
       Using output from proces [NLGreen             ]                                              
       [LimRadGree          ] radiation limitation function Greens <0-1>                            
       Using output from proces [Rad_Green           ]                                              
       [TFGroGreen          ] temperature function growth Greens <0-1>                              
       Using output from proces [TF_Green            ]                                              
       [TFMrtGreen          ] temperature function mortality Greens <0-1>                           
       Using output from proces [TF_Green            ]                                              
       [PPMaxGreen          ] maximum production rate Greens                                        
       Using constant nr 54 with value:  1.80000                                                    
       [MRespGreen          ] maintenance respiration Greens st.temp                                
       Using constant nr 55 with value: 0.450000E-01                                                
       [GRespGreen          ] growth respiration factor Greens                                      
       Using constant nr 56 with value: 0.150000                                                    
       [Mort0Green          ] mortality rate constant Greens                                        
       Using constant nr 57 with value: 0.350000                                                    
       [MortSGreen          ] mortality rate Greens at high salinity                                
       using default value: 0.350000                                                                
       [SalM1Green          ] lower salinity limit for mortality Greens                             
       Using constant nr 58 with value:  0.00000                                                    
       [SalM2Green          ] upper salinity limit for mortality Greens                             
       Using constant nr 59 with value:  0.00000                                                    
       [Salinity            ] Salinity                                                              
       using default value:  35.0000                                                                
       [MinGreen            ] Minimum level Greens in mortality                                     
       using default value:  0.00000                                                                
                                                                                                    
 Input for [Rad_Green           ] Light efficiency function green algae                             
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [Rad                 ] irradiation at the segment upper-boundary                             
       Using output from proces [CalcRad             ]                                              
       [RadSatGree          ] total radiation growth saturation greens                              
       Using constant nr 85 with value:  30.0000                                                    
       [ExtVl               ] total extinction coefficient visible light                            
       Using output from proces [Extinc_VLG          ]                                              
       [TFGroGreen          ] temperature function growth Greens <0-1>                              
       Using output from proces [TF_Green            ]                                              
                                                                                                    
 Input for [NLGreen             ] Nutrient limiation function for green algae                       
       [PrfNH4gree          ] ammonium preferency over nitrate Greens                               
       Using constant nr 82 with value:  1.00000                                                    
       [KMDINgreen          ] half-saturation value N Greens                                        
       Using constant nr 83 with value: 0.500000E-02                                                
       [KMPgreen            ] half-saturation value P Greens                                        
       Using constant nr 84 with value: 0.100000E-02                                                
       [KMSigreen           ] half-saturation value Si Greens                                       
       using default value: -1.00000                                                                
       [NH4                 ] Ammonium (NH4)                                                        
       Using substance nr   6                                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [PO4                 ] Ortho-Phosphate (PO4)                                                 
       Using substance nr   8                                                                       
       [Si                  ] dissolved Silica (Si)                                                 
       using default value: -1.00000                                                                
                                                                                                    
 Input for [DL_Green            ] Daylength function for green algae                                
       [DayL                ] daylength <0-1>                                                       
       Using constant nr 80 with value: 0.580000                                                    
       [OptDLGreen          ] daylength for growth saturation Greens                                
       Using constant nr 81 with value: 0.580000                                                    
                                                                                                    
 Input for [TF_Green            ] Temperature functions for green algae                             
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [TcGroGreen          ] temperature coeff. for growth processes Greens                        
       Using constant nr 86 with value:  1.04000                                                    
       [TcDecGreen          ] temp. coeff. for respiration and mortality Greens                     
       Using constant nr 87 with value:  1.07000                                                    
                                                                                                    
 Input for [SedOXYDem           ] Sediment oxygen demand                                            
       [fSODaut             ] autonomous SOD (no effect SOD stat.var)                               
       using default value:  0.00000                                                                
       [fSOD                ] zeroth-order sediment oxygen demand flux                              
       Using constant nr 73 with value:  0.00000                                                    
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [SOD                 ] Sediment oxygen demand (SOD)                                          
       Using substance nr  13                                                                       
       [RcSOD               ] decay rate SOD at 20 oC                                               
       Using constant nr 74 with value:  0.00000                                                    
       [TcSOD               ] temperature coefficient decay SOD                                     
       using default value:  1.04000                                                                
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [Volume              ] volume of computational cell                                          
       Using DELWAQ volume                                                                          
       [SwCH4bub            ] switch (1=include CH4 bubbles, 0=not)                                 
       using default value:  0.00000                                                                
       [HSED                ] Total sediment thickness                                              
       using default value: 0.100000                                                                
       [KAPC                ] constant                                                              
       using default value:  1.60000                                                                
       [thetak              ] temperature constant                                                  
       using default value:  1.07900                                                                
       [edwcsd              ] diffusion coefficient                                                 
       using default value: 0.250000E-03                                                            
       [diamb               ] Diameter of methane bubbles                                           
       using default value:  1.00000                                                                
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [kappad              ] transfer coefficient                                                  
       using default value: 0.300000E-02                                                            
       [dMinDetCS1          ] mineralisation flux DetCS1                                            
       using default value:  0.00000                                                                
       [dMinDetCS2          ] mineralisation flux DetCS2                                            
       using default value:  0.00000                                                                
       [dMinOOCS1           ] mineralisation flux OOCS1                                             
       using default value:  0.00000                                                                
       [dMinOOCS2           ] mineralisation flux OOCS2                                             
       using default value:  0.00000                                                                
       [TotalDepth          ] total depth water column                                              
       Using output from proces [TotDepth            ]                                              
       [COXSOD              ] critical oxygen concentration for SOD decay                           
       using default value:  0.00000                                                                
       [OOXSOD              ] optimum oxygen concentration for SOD decay                            
       using default value:  2.00000                                                                
                                                                                                    
 Input for [DecFast             ] Mineralization fast decomp. detritus POC1                         
       [POC1                ] POC1 (fast decomposing fraction)                                      
       Using substance nr   2                                                                       
       [PON1                ] PON1 (fast decomposing fraction)                                      
       Using substance nr   3                                                                       
       [POP1                ] POP1 (fast decomposing fraction)                                      
       Using substance nr   4                                                                       
       [POS1                ] POS1 (fast decomposing fraction)                                      
       using default value:  0.00000                                                                
       [IdDet1              ] identifier for detritus group POC1, POC2, POC3                        
       using default value:  1.00000                                                                
       [kl_dFdcC20          ] lower limit mineralization rate fast detr-C                           
       Using constant nr 41 with value: 0.100000                                                    
       [kl_dFdcC20          ] lower limit mineralization rate fast detr-C                           
       Using constant nr 41 with value: 0.100000                                                    
       [kl_dFdcN20          ] lower limit mineralization rate fast detr-N                           
       Using constant nr 50 with value: 0.100000                                                    
       [kl_dFdcN20          ] lower limit mineralization rate fast detr-N                           
       Using constant nr 50 with value: 0.100000                                                    
       [kl_dFdcP20          ] lower limit mineralization rate fast detr-P                           
       Using constant nr 52 with value: 0.100000                                                    
       [kl_dFdcP20          ] lower limit mineralization rate fast detr-P                           
       Using constant nr 52 with value: 0.100000                                                    
       [kT_dec              ] temperature coefficient for decomposition                             
       Using constant nr 42 with value:  1.05000                                                    
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [a_dNpr              ] target N:C ratio in refractory detritus                               
       using default value: 0.500000E-01                                                            
       [a_dPpr              ] target P:C ratio in refractory detritus                               
       using default value: 0.500000E-02                                                            
       [a_dSpr              ] target S:C ratio in refractory detritus                               
       using default value: 0.500000E-02                                                            
       [al_dNf              ] lower limit N:C ratio in fast decomp.  detr                           
       using default value: 0.100000                                                                
       [al_dPf              ] lower limit P:C ratio in fast decomp.  detr                           
       using default value: 0.100000E-01                                                            
       [au_dNf              ] upper limit N:C ratio in fast decomp.  detr                           
       using default value: 0.150000                                                                
       [au_dPf              ] upper limit P:C ratio in fast decomp.  detr                           
       using default value: 0.150000E-01                                                            
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [b_ni                ] attenuation factor decomp. in denitrifying zone                       
       using default value:  1.00000                                                                
       [b_su                ] attenuation factor decomp. in sulphate red.zone                       
       using default value:  1.00000                                                                
       [b_poc1poc2          ] fraction POC1 converted to POC2                                       
       using default value:  0.00000                                                                
       [b_poc1doc           ] fraction POC1 converted to DOC                                        
       using default value:  0.00000                                                                
       [SWOMDec             ] option: 0.0 for stripping, 1.0 for different rates                    
       using default value:  1.00000                                                                
                                                                                                    
 Input for [RearOXY             ] Reaeration of oxygen                                              
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [Velocity            ] horizontal flow velocity                                              
       Using output from proces [Veloc               ]                                              
       [VWind               ] wind speed                                                            
       Using constant nr 91 with value:  3.00000                                                    
       [SWRear              ] switch for oxygen reaeration formulation (1-13)                       
       Using constant nr 69 with value:  1.00000                                                    
       [KLRear              ] reaeration transfer coefficient                                       
       Using constant nr 70 with value: 0.350000                                                    
       [TCRear              ] temperature coefficient for rearation                                 
       Using constant nr 71 with value:  1.02400                                                    
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [SaturOXY            ] saturation concentration                                              
       Using output from proces [SaturOXY            ]                                              
       [Salinity            ] Salinity                                                              
       using default value:  35.0000                                                                
       [TotalDepth          ] total depth water column                                              
       Using output from proces [TotDepth            ]                                              
       [fcover              ] fraction of water surface covered <0-1>                               
       using default value:  0.00000                                                                
       [KLRearMax           ] maximum KLREAR oxygen for temp. correction                            
       using default value:  1000.00                                                                
       [KLRearMin           ] minimum rearation transfer coefficient oxygen                         
       using default value: 0.200000                                                                
       [Rain                ] rainfall rate                                                         
       using default value:  0.00000                                                                
       [coefAOxy            ] gas transfer Oxy coefficient transmission                             
       using default value:  1.66000                                                                
       [coefB1Oxy           ] gas transfer O2 coefficient wind scale 1                              
       using default value: 0.260000                                                                
       [coefB2Oxy           ] gas transfer O2 coefficient wind scale 2                              
       using default value:  1.00000                                                                
       [coefC1Oxy           ] gas transfer O2 coefficient rain scale 1                              
       using default value: 0.660000                                                                
       [coefC2Oxy           ] gas transfer O2 coefficient rain scale 2                              
       using default value:  1.00000                                                                
       [coefD1Oxy           ] fresh water coefficient1 for Schmidt nr Oxy                           
       using default value:  1800.06                                                                
       [coefD2Oxy           ] fresh water coefficient2 for Schmidt nr Oxy                           
       using default value:  120.100                                                                
       [coefD3Oxy           ] fresh water coefficient3 for Schmidt nr Oxy                           
       using default value:  3.78180                                                                
       [coefD4Oxy           ] fresh water coefficient4 for Schmidt nr Oxy                           
       using default value: 0.476080E-01                                                            
                                                                                                    
 Input for [SaturOXY            ] Saturation concentration oxygen                                   
       [Cl                  ] Chloride                                                              
       Using substance nr  10                                                                       
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [SWSatOXY            ] switch for oxygen saturation formulation (1, 2)                       
       using default value:  1.00000                                                                
       [Salinity            ] Salinity                                                              
       using default value:  35.0000                                                                
                                                                                                    
 Input for [Nitrif_NH4          ] Nitrification of ammonium                                         
       [ZNit                ] zeroth-order nitrification flux                                       
       using default value:  0.00000                                                                
       [NH4                 ] Ammonium (NH4)                                                        
       Using substance nr   6                                                                       
       [RcNit20             ] MM- nitrification rate at 20 oC                                       
       using default value: 0.100000                                                                
       [TcNit               ] temperature coefficient for nitrification                             
       Using constant nr 60 with value:  1.08000                                                    
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [KsAmNit             ] half saturation constant for ammonium cons.                           
       using default value: 0.500000                                                                
       [KsOxNit             ] half saturation constant for DO cons.                                 
       using default value:  1.00000                                                                
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [CTNit               ] critical temperature for nitrification                                
       Using constant nr 61 with value:  3.00000                                                    
       [Rc0NitOx            ] zero-order nitrification rate at neg. DO                              
       using default value:  0.00000                                                                
       [COXNIT              ] critical oxygen concentration for nitrification                       
       Using constant nr 62 with value:  1.00000                                                    
       [Poros               ] volumetric porosity                                                   
       using default value:  1.00000                                                                
       [SWVnNit             ] switch for old (0), new (1), TEWOR (2) version                        
       using default value:  0.00000                                                                
       [RcNit               ] first-order nitrification rate                                        
       Using constant nr 63 with value: 0.100000                                                    
       [OOXNIT              ] optimum oxygen concentration for nitrification                        
       Using constant nr 64 with value:  5.00000                                                    
       [CFLNIT              ] oxygen function level for oxygen below COXNIT                         
       using default value:  0.00000                                                                
       [CurvNit             ] curvature of DO function for nitrification                            
       using default value:  0.00000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
                                                                                                    
 Input for [DenWat_NO3          ] Denitrification in water column                                   
       [ZDenWat             ] zero-order denitrification rate in water column                       
       using default value:  0.00000                                                                
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [RcDen20             ] MM-denitrification reaction rate at 20 oC                             
       using default value: 0.100000                                                                
       [TcDenWat            ] temperature coefficient for denitrification                           
       Using constant nr 65 with value:  1.04500                                                    
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [KsNiDen             ] half saturation constant for nitrate cons.                            
       using default value: 0.500000                                                                
       [KsOxDen             ] half saturation constant for oxygen inhib.                            
       using default value:  1.00000                                                                
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [CTDEN               ] critical temperature for denitrification                              
       using default value:  2.00000                                                                
       [Rc0DenOx            ] zero-order denit. rate at low temperature                             
       using default value:  0.00000                                                                
       [COXDEN              ] critical oxygen concentration for denitrification                     
       Using constant nr 66 with value:  3.00000                                                    
       [Poros               ] volumetric porosity                                                   
       using default value:  1.00000                                                                
       [SWVnDen             ] switch to select old (0) or new (1) version                           
       using default value:  0.00000                                                                
       [RcDenWat            ] first-order denitrification rate in water column                      
       Using constant nr 67 with value: 0.100000                                                    
       [OOXDEN              ] optimum oxygen concentration for denitrification                      
       Using constant nr 68 with value:  1.00000                                                    
       [Curvat              ] curvature of DO function for denitrification                          
       using default value:  1.00000                                                                
                                                                                                    
 Input for [AdsPO4AAP           ] Ad(De)Sorption ortho phosphorus to inorg. matter                  
       [SWAdsP              ] switch PO4 adsorption <0=Kd|1=Langmuir|2=pHdep>                       
       Using constant nr 39 with value:  0.00000                                                    
       [PO4                 ] Ortho-Phosphate (PO4)                                                 
       Using substance nr   8                                                                       
       [AAP                 ] adsorbed ortho phosphate                                              
       Using substance nr   1                                                                       
       [IM1                 ] inorganic matter (IM1)                                                
       Using substance nr  11                                                                       
       [IM2                 ] inorganic matter (IM2)                                                
       using default value:  0.00000                                                                
       [IM3                 ] inorganic matter (IM3)                                                
       using default value:  0.00000                                                                
       [KdPO4AAP            ] distrib. coeff. (-) or ads. eq. const.                                
       Using constant nr 40 with value: 0.750000E-01                                                
       [MaxPO4AAP           ] adsorption capacity TIM for PO4                                       
       using default value: 0.150000                                                                
       [DELT                ] timestep for processes                                                
       Using DELWAQ timestep in days                                                                
       [KadsP_20            ] Adsorption equilibrium constant at 20 oC                              
       using default value:  3.80000                                                                
       [TCKadsP             ] temperature dependency constant Kads                                  
       using default value:  1.00000                                                                
       [RcAdPO4AAP          ] adsorption rate PO4 --> AAP                                           
       using default value:  1.00000                                                                
       [a_OH-PO4            ] OH-:PO4 ratio in sorption reaction                                    
       using default value: 0.200000                                                                
       [fr_FeIM1            ] fraction Fe in inorg. matter IM1                                      
       using default value: 0.300000E-01                                                            
       [fr_FeIM2            ] fraction Fe in inorg. matter IM2                                      
       using default value: 0.500000E-02                                                            
       [fr_FeIM3            ] fraction Fe in inorg. matter IM3                                      
       using default value: 0.100000E-02                                                            
       [fr_Feox             ] fraction reactive Fe of total Fe                                      
       using default value:  1.00000                                                                
       [OXY                 ] Dissolved Oxygen                                                      
       Using substance nr   9                                                                       
       [Cc_oxPsor           ] critical oxygen conc for P sorption                                   
       using default value:  0.00000                                                                
       [pH                  ] pH                                                                    
       using default value:  7.00000                                                                
       [Temp                ] ambient water temperature                                             
       Using segment function nr  2                                                                 
       [Poros               ] volumetric porosity                                                   
       using default value:  1.00000                                                                
       [SWVnAdsP            ] switch to select old(0) or new(1) version                             
       using default value:  0.00000                                                                
       [fr_Fe               ] fraction Fe in solid matter                                           
       using default value: 0.200000E-01                                                            
       [RCadsPgem           ] pseudo first-order rate PO4 sorption                                  
       using default value:  1.00000                                                                
                                                                                                    
 Input for [Compos              ] Composition                                                       
       [NO3                 ] Nitrate (NO3)                                                         
       Using substance nr   7                                                                       
       [NH4                 ] Ammonium (NH4)                                                        
       Using substance nr   6                                                                       
       [PO4                 ] Ortho-Phosphate (PO4)                                                 
       Using substance nr   8                                                                       
       [Si                  ] dissolved Silica (Si)                                                 
       using default value:  0.00000                                                                
       [IM1                 ] inorganic matter (IM1)                                                
       Using substance nr  11                                                                       
       [IM2                 ] inorganic matter (IM2)                                                
       using default value:  0.00000                                                                
       [IM3                 ] inorganic matter (IM3)                                                
       using default value:  0.00000                                                                
       [Phyt                ] total carbon in phytoplankton                                         
       Using output from proces [Phy_dyn             ]                                              
       [AlgN                ] total nitrogen in algae                                               
       Using output from proces [Phy_dyn             ]                                              
       [AlgP                ] total phosphorus in algae                                             
       Using output from proces [Phy_dyn             ]                                              
       [AlgSi               ] total silica in algae                                                 
       Using output from proces [Phy_dyn             ]                                              
       [AlgDM               ] total DM in algae                                                     
       Using output from proces [Phy_dyn             ]                                              
       [POC1                ] POC1 (fast decomposing fraction)                                      
       Using substance nr   2                                                                       
       [POC2                ] POC2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [POC3                ] POC3 (slow decomposing fraction)                                      
       using default value:  0.00000                                                                
       [POC4                ] POC4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
       [PON1                ] PON1 (fast decomposing fraction)                                      
       Using substance nr   3                                                                       
       [DOC                 ] Dissolved Organic Carbon (DOC)                                        
       using default value:  0.00000                                                                
       [DON                 ] Dissolved Organic Nitrogen (DON)                                      
       using default value:  0.00000                                                                
       [DOP                 ] Dissolved Organic Phosphorus (DOP)                                    
       using default value:  0.00000                                                                
       [DOS                 ] Dissolved Organic Sulphur (DOS)                                       
       using default value:  0.00000                                                                
       [AAP                 ] adsorbed ortho phosphate                                              
       Using substance nr   1                                                                       
       [VIVP                ] Vivianite-P                                                           
       using default value:  0.00000                                                                
       [APATP               ] Apatite-P                                                             
       using default value:  0.00000                                                                
       [DMCFIM1             ] DM:C ratio IM1                                                        
       using default value:  1.00000                                                                
       [DMCFIM2             ] DM:C ratio IM2                                                        
       using default value:  1.00000                                                                
       [DMCFIM3             ] DM:C ratio IM3                                                        
       using default value:  1.00000                                                                
       [PON2                ] PON2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [PON3                ] PON3 (slow decomposing fraction)                                      
       using default value:  0.00000                                                                
       [PON4                ] PON4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
       [POP1                ] POP1 (fast decomposing fraction)                                      
       Using substance nr   4                                                                       
       [POP2                ] POP2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [POP3                ] POP3 (slow decomposing fraction)                                      
       using default value:  0.00000                                                                
       [POP4                ] POP4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
       [POS1                ] POS1 (fast decomposing fraction)                                      
       using default value:  0.00000                                                                
       [POS2                ] POS2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [POS3                ] POS3 (slow decomposing  fraction)                                     
       using default value:  0.00000                                                                
       [POS4                ] POS4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
       [Opal                ] Opal-Si                                                               
       Using substance nr  12                                                                       
       [DmCfPOC1            ] DM:C ratio POC1                                                       
       using default value:  2.50000                                                                
       [DmCfPOC2            ] DM:C ratio POC2                                                       
       using default value:  2.50000                                                                
       [DmCfPOC3            ] DM:C ratio POC3                                                       
       using default value:  2.50000                                                                
       [DmCfPOC4            ] DM:C ratio POC4                                                       
       using default value:  2.50000                                                                
                                                                                                    
 Input for [S1_Comp             ] Composition sediment layer S1                                     
       [IM1S1               ] IM1 in layer S1                                                       
       using default value:  0.00000                                                                
       [IM2S1               ] IM2 in layer S1                                                       
       using default value:  0.00000                                                                
       [IM3S1               ] IM3 in layer S1                                                       
       using default value:  0.00000                                                                
       [DetCS1              ] DetC in layer S1                                                      
       using default value:  0.00000                                                                
       [OOCS1               ] OOC in layer S1                                                       
       using default value:  0.00000                                                                
       [DiatS1              ] Diatoms in layer S1 (DYNAMO)                                          
       using default value:  0.00000                                                                
       [GreenS1             ] Algae in layer S1 (DYNAMO)                                            
       using default value:  0.00000                                                                
       [AAPS1               ] adsorbed O-PO4 in layer S1                                            
       using default value:  0.00000                                                                
       [DMCFIM1             ] DM:C ratio IM1                                                        
       using default value:  1.00000                                                                
       [DMCFIM2             ] DM:C ratio IM2                                                        
       using default value:  1.00000                                                                
       [DMCFIM3             ] DM:C ratio IM3                                                        
       using default value:  1.00000                                                                
       [DMCFDetCS           ] DM:C ratio DetCS1 and DetCS2                                          
       using default value:  1.70000                                                                
       [DMCFOOCS            ] DM:C ratio POCS1 and POCS2                                            
       using default value:  1.70000                                                                
       [DMCFDiatS           ] DM:C ratio DiatS1 and DiatS2                                          
       using default value:  1.70000                                                                
       [DMCFGreenS          ] DM:C ratio GreenS1 and GreenS2                                        
       using default value:  1.70000                                                                
       [RHOIM1              ] bulk density IM1                                                      
       using default value: 0.260000E+07                                                            
       [RHOIM2              ] bulk density IM2                                                      
       using default value: 0.260000E+07                                                            
       [RHOIM3              ] bulk density IM3                                                      
       using default value: 0.260000E+07                                                            
       [RHODetC             ] bulk density DetC                                                     
       using default value: 0.130000E+07                                                            
       [RHOOOC              ] bulk density OOC                                                      
       using default value: 0.130000E+07                                                            
       [RHODiat             ] bulk density Diatoms                                                  
       using default value: 0.130000E+07                                                            
       [RHOGreen            ] bulk density Greens                                                   
       using default value: 0.130000E+07                                                            
       [PORS1               ] porosity of sediment layer S1                                         
       using default value:  0.00000                                                                
       [Surf                ] horizontal surface area of a DELWAQ segment                           
       Using parameter nr  1                                                                        
       [DetNS1              ] DetN in layer S1                                                      
       using default value:  0.00000                                                                
       [DetPS1              ] DetP in layer S1                                                      
       using default value:  0.00000                                                                
       [DetSiS1             ] DetSi in layer S1                                                     
       using default value:  0.00000                                                                
       [OONS1               ] OON in layer S1                                                       
       using default value:  0.00000                                                                
       [OOPS1               ] OOP in layer S1                                                       
       using default value:  0.00000                                                                
       [OOSiS1              ] OOSi in layer S1                                                      
       using default value:  0.00000                                                                
       [MPB1peliS1          ] MPB epipelic biomass in layer S1 (DYNAMO)                             
       using default value:  0.00000                                                                
       [MPB2psamS1          ] MPB epipsammic biomass in layer S1 (DYNAMO)                           
       using default value:  0.00000                                                                
       [DmCfMPB1            ] DM:C ratio MPB epipelic                                               
       using default value:  2.50000                                                                
       [DmCfMPB2            ] DM:C ratio MPB epipsammic                                             
       using default value:  2.50000                                                                
       [RhoOM               ] dry bulk density organic matter                                       
       using default value: 0.130000E+07                                                            
       [RhoOM               ] dry bulk density organic matter                                       
       using default value: 0.130000E+07                                                            
                                                                                                    
 Input for [Phy_dyn             ] Computation of phytoplankton - Dynamo                             
       [NAlgDynamo          ] number of algae types in DYNAMO                                       
       using default value:  4.00000                                                                
       [Diat                ] Diatoms (DYNAMO)                                                      
       using default value:  0.00000                                                                
       [Green               ] Algae (non-Diatoms) (DYNAMO)                                          
       Using substance nr   5                                                                       
       [MPB1peli            ] microphytobenthos epipelic (DYNAMO)                                   
       using default value:  0.00000                                                                
       [MPB2psam            ] microphytobenthos epipsammic (DYNAMO)                                 
       using default value:  0.00000                                                                
       [NCRatDiat           ] N:C ratio Diatoms                                                     
       using default value: 0.160000                                                                
       [NCRatGreen          ] N:C ratio Greens                                                      
       Using constant nr 44 with value: 0.160000                                                    
       [MPB1NCrat           ] N:C ratio MPB epipelic                                                
       using default value: 0.160000                                                                
       [MPB2NCrat           ] N:C ratio MPB epipsammic                                              
       using default value: 0.160000                                                                
       [PCRatDiat           ] P:C ratio Diatoms                                                     
       using default value: 0.200000E-01                                                            
       [PCRatGreen          ] P:C ratio Greens                                                      
       Using constant nr 45 with value: 0.200000E-01                                                
       [MPB1PCrat           ] P:C ratio MPB epipelic                                                
       using default value: 0.200000E-01                                                            
       [MPB2PCrat           ] P:C ratio MPB epipsammic                                              
       using default value: 0.200000E-01                                                            
       [SCRatDiat           ] Si:C ratio Diatoms                                                    
       using default value: 0.490000                                                                
       [SCRatGreen          ] Si:C ratio Greens                                                     
       using default value:  0.00000                                                                
       [MPB1SiCrat          ] Si:C ratio MPB epipelic                                               
       using default value: 0.490000                                                                
       [MPB2SiCrat          ] Si:C ratio MPB epipsammic                                             
       using default value: 0.490000                                                                
       [DMCFDiat            ] DM:C ratio Diatoms                                                    
       using default value:  2.50000                                                                
       [DMCFGreen           ] DM:C ratio GreenS                                                     
       using default value:  2.50000                                                                
       [DmCfMPB1            ] DM:C ratio MPB epipelic                                               
       using default value:  2.50000                                                                
       [DmCfMPB2            ] DM:C ratio MPB epipsammic                                             
       using default value:  2.50000                                                                
       [Ditochl             ] Chlorophyll-a:C ratio in Diatoms                                      
       using default value:  50.0000                                                                
       [Grtochl             ] Chlorophyll-a:C ratio in Greens                                       
       using default value:  50.0000                                                                
       [MPB1ToChl           ] chlorophyll-a:C ratio in MPB epipelic                                 
       using default value:  50.0000                                                                
       [MPB2ToChl           ] chlorophyll-a:C ratio in MPB epipsammic                               
       using default value:  50.0000                                                                
                                                                                                    
 Input for [CalcRad             ] Radiation at segment upper and lower boundaries                   
       [ExtVl               ] total extinction coefficient visible light                            
       Using output from proces [Extinc_VLG          ]                                              
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [RadSurf             ] irradiation at the water surface                                      
       Using constant nr 90 with value:  0.00000                                                    
       [a_enh               ] enhancement factor in radiation calculation                           
       using default value:  1.50000                                                                
       [Surf                ] horizontal surface area of a DELWAQ segment                           
       Using parameter nr  1                                                                        
       [SwEmersion          ] switch indicating submersion(0) or emersion(1)                        
       using default value:  0.00000                                                                
       [Rad                 ] irradiation at the segment upper-boundary                             
       Using output from proces [CalcRad             ]                                              
       [fRefl               ] fraction of radiation reflected at water surface                      
       using default value:  0.00000                                                                
                                                                                                    
 Input for [Extinc_VLG          ] Extinction of visible-light (370-680nm) DLWQ-G                    
       [ExtVlIM1            ] VL specific extinction coefficient IM1                                
       Using constant nr 78 with value: 0.100000E-01                                                
       [ExtVlIM2            ] VL specific extinction coefficient IM2                                
       using default value: 0.100000E-01                                                            
       [ExtVlIM3            ] VL specific extinction coefficient IM3                                
       using default value: 0.100000E-01                                                            
       [ExtVlPOC1           ] VL specific extinction coefficient POC1                               
       Using constant nr 88 with value: 0.470000                                                    
       [ExtVlBak            ] background extinction visible light                                   
       Using constant nr 79 with value: 0.800000E-01                                                
       [ExtVlPhBl           ] VL extinction by phytoplankton (BLOOM)                                
       using default value:  0.00000                                                                
       [ExtVlPhDyn          ] VL extinction by phytoplankton (DYNAMO)                               
       Using output from proces [ExtPhDVL            ]                                              
       [ExtVlPhPro          ] VL extinction by phytoplankton (Protist)                              
       using default value:  0.00000                                                                
       [ExtVlMacro          ] VL extinction by macrophytes                                          
       using default value:  0.00000                                                                
       [IM1                 ] inorganic matter (IM1)                                                
       Using substance nr  11                                                                       
       [IM2                 ] inorganic matter (IM2)                                                
       using default value:  0.00000                                                                
       [IM3                 ] inorganic matter (IM3)                                                
       using default value:  0.00000                                                                
       [POC1                ] POC1 (fast decomposing fraction)                                      
       Using substance nr   2                                                                       
       [POC2                ] POC2 (medium decomposing fraction)                                    
       using default value:  0.00000                                                                
       [SW_Uitz             ] Extinction by Uitzicht On (1) or Off (0)                              
       using default value:  0.00000                                                                
       [DOC                 ] Dissolved Organic Carbon (DOC)                                        
       using default value:  0.00000                                                                
       [ExtVlDOC            ] VL specific extinction coefficient DOC                                
       using default value:  0.00000                                                                
       [UitZDEPT1           ] Z1 (depth)                                                            
       using default value:  1.20000                                                                
       [UitZDEPT2           ] Z2 (depth)                                                            
       using default value:  1.00000                                                                
       [UitZCORCH           ] CORa correction factor                                                
       using default value:  2.50000                                                                
       [UitZC_DET           ] C3 coeff. absorption ash weight & detritus                            
       using default value: 0.260000E-01                                                            
       [UitZC_GL1           ] C1 coeff. absorption ash weight & detritus                            
       using default value: 0.730000                                                                
       [UitZC_GL2           ] C2 coeff. absorption ash weight & detritus                            
       using default value:  1.00000                                                                
       [UitZHELHM           ] Hel_h constant                                                        
       using default value: 0.140000E-01                                                            
       [UitZTAU             ] Tau constant calculation transparency                                 
       using default value:  7.80000                                                                
       [UitZangle           ] Angle of incidence solar radiation                                    
       using default value:  30.0000                                                                
       [DMCFDetC            ] DM:C ratio DetC                                                       
       using default value:  2.50000                                                                
       [ExtVLSal0           ] extra VL extinction at Salinity = 0                                   
       using default value:  0.00000                                                                
       [Salinity            ] Salinity                                                              
       using default value:  35.0000                                                                
       [SalExt0             ] salinity value for extra extinction = 0                               
       using default value:  34.9200                                                                
       [ExtVlPOC2           ] VL specific extinction coefficient POC2                               
       using default value: 0.600000E-01                                                            
       [ExtVlPOC3           ] VL specific extinction coefficient POC3                               
       using default value: 0.100000                                                                
       [ExtVlPOC4           ] VL specific extinction coefficient POC4                               
       using default value: 0.100000                                                                
       [POC3                ] POC3 (slow decomposing fraction)                                      
       using default value:  0.00000                                                                
       [POC4                ] POC4 (particulate refractory fraction)                                
       using default value:  0.00000                                                                
                                                                                                    
 Input for [ExtPhDVL            ] Extinction of visible light by algae (Dynamo)                     
       [NAlgDynamo          ] number of algae types in DYNAMO                                       
       using default value:  4.00000                                                                
       [SW_fixin_n          ] switch possible scaling of input, DO NOT EDIT                         
       using default value:  0.00000                                                                
       [Volume              ] volume of computational cell                                          
       Using DELWAQ volume                                                                          
       [ExtVlGreen          ] VL specific extinction coefficient Greens                             
       Using constant nr 89 with value: 0.150000                                                    
       [ExtVlDiat           ] VL specific extinction coefficient Diatoms                            
       using default value: 0.150000                                                                
       [ExtVlMPB1           ] VL specific extinction coefficient MPB epipelic                       
       using default value: 0.150000                                                                
       [ExtVlMPB2           ] VL specific extinction coefficient MPB epipsammic                     
       using default value: 0.150000                                                                
       [Green               ] Algae (non-Diatoms) (DYNAMO)                                          
       Using substance nr   5                                                                       
       [Diat                ] Diatoms (DYNAMO)                                                      
       using default value:  0.00000                                                                
       [MPB1peli            ] microphytobenthos epipelic (DYNAMO)                                   
       using default value:  0.00000                                                                
       [MPB2psam            ] microphytobenthos epipsammic (DYNAMO)                                 
       using default value:  0.00000                                                                
                                                                                                    
 Input for [CalTau              ] Calculation of bottom friction                                    
       [WaveHeight          ] calculated height of a wind induced wave                              
       using default value:  0.00000                                                                
       [WaveLength          ] calculated length of a wind induced wave                              
       using default value:  0.00000                                                                
       [WavePeriod          ] calculated period of a wind induced wave                              
       using default value:  0.00000                                                                
       [TauShip             ] bottom shear stress by ship movement                                  
       using default value:  0.00000                                                                
       [SWTauVeloc          ] Switch Tauveloc (1=calculate|2=TauFlow)                               
       using default value:  1.00000                                                                
       [TauFlow             ] bottom shear stress by FLOW                                           
       using default value:  0.00000                                                                
       [Velocity            ] horizontal flow velocity                                              
       Using output from proces [Veloc               ]                                              
       [CHEZY               ] Chezy coefficient                                                     
       Using constant nr 92 with value:  55.0000                                                    
       [TotalDepth          ] total depth water column                                              
       Using output from proces [TotDepth            ]                                              
       [SWTau               ] switch <1=Tamminga|2=Swart|3=Soulsby>                                 
       using default value:  1.00000                                                                
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
                                                                                                    
 Input for [VertDisp            ] Vertical dispersion (segment -> exchange)                         
       [VertDisper          ] vertical dispersion                                                   
       Using segment function nr  1                                                                 
       [ScaleVdisp          ] scaling factor for vertical diffusion                                 
       using default value:  1.00000                                                                
                                                                                                    
 Input for [Veloc               ] Horizontal flow velocity                                          
       [WSNoseg1            ] workspace array no. 1                                                 
       Using output from proces [Veloc               ]                                              
       [WSNoseg2            ] workspace array no. 2                                                 
       Using output from proces [Veloc               ]                                              
       [WSNoseg3            ] workspace array no. 3                                                 
       Using output from proces [Veloc               ]                                              
       [WSNoseg4            ] workspace array no. 4                                                 
       Using output from proces [Veloc               ]                                              
       [MaxVeloc            ] maximum horizontal flow velocity                                      
       using default value:  0.00000                                                                
       [Orient_1            ] orientation of main positive flow direction                           
       using default value: -1.00000                                                                
       [Orient_2            ] orientation of secondary positive flow direct                         
       using default value: -1.00000                                                                
       [SWCalcVelo          ] switch averaging (1=lin, 2=Flow, 3=Area, 4=Maxvel)                    
       using default value:  1.00000                                                                
       [SWAvgVelo           ] switch (1=Pythagoras, 2=Min, 3=Max)                                   
       using default value:  1.00000                                                                
       [XArea               ] exchange area                                                         
       Using DELWAQ exchange area                                                                   
       [Flow                ] flow rate                                                             
       Using DELWAQ flow                                                                            
                                                                                                    
 Input for [TotDepth            ] depth water column                                                
       [Depth               ] depth of segment                                                      
       Using output from proces [DynDepth            ]                                              
       [Surf                ] horizontal surface area of a DELWAQ segment                           
       Using parameter nr  1                                                                        
                                                                                                    
 Input for [DynDepth            ] dynamic calculation of the depth                                  
       [Volume              ] volume of computational cell                                          
       Using DELWAQ volume                                                                          
       [Surf                ] horizontal surface area of a DELWAQ segment                           
       Using parameter nr  1                                                                        
                                                                                                    
# determining the use of the delwaq input                                       
                                                                                
 info: constant [CTMin     ] is not used by the proces system                   
 info: constant [TcDetN    ] is not used by the proces system                   
 info: constant [TcDetP    ] is not used by the proces system                   
 info: constant [O2FuncBOD ] is not used by the proces system                   
 info: constant [NOTHREADS ] is not used by the proces system                   
 info: constant [DRY_THRESH] is not used by the proces system                   
                                                                                
# locating requested output from active processes                                                   
                                                                                                    
 output [AlgN                ] from proces [Phy_dyn   ]                                             
 output [AlgP                ] from proces [Phy_dyn   ]                                             
 output [SS                  ] from proces [Compos    ]                                             
 output [TotN                ] from proces [Compos    ]                                             
 output [KjelN               ] from proces [Compos    ]                                             
 output [TotP                ] from proces [Compos    ]                                             
 output [LimDLGreen          ] from proces [DL_Green  ]                                             
 output [LimNutGree          ] from proces [NLGreen   ]                                             
 output [LimRadGree          ] from proces [Rad_Green ]                                             
 output [Chlfa               ] from proces [Phy_dyn   ]                                             
 output [ExtVlPhyt           ] from proces [Extinc_VLG]                                             
                                                                                                    
