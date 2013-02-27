from mobiletrans.mtdistmap.dijkstra.transit_network import TransitNetwork

"""
from mobiletrans.mtdistmap import cta_conn
tn = cta_conn.load_transitnetwork()
tn.shortest_path("Red_40330", 'Red_40900')
tn.shortest_path("Red_40900", 'Red_40330')

tn.shortest_path("Red_41320", 'Red_40650')
tn.shortest_path("Red_40650", 'Red_41320')


tn.shortest_path("Brn_41290", 'Brn_40710')
tn.shortest_path('Brn_40710', 'Brn_41290')

tn.shortest_path("Red_41090", 'Brn_41440').pprint()
tn.shortest_path("Red_41090", 'Brn_41440', reverse=True).pprint()

tn.shortest_path("Blue_40890", 'Blue_40490', reverse=False).pprint()
tn.shortest_path("Blue_40890", 'Blue_40490', reverse=True).pprint()

"""

def load_transitnetwork():
    tn = TransitNetwork() 
    wait_time = 5.0
    # transfer time for blue line to library at Jackson
    bluelib_wait_time = 10.0
    # transfer time for red line to library at Jackson
    redlib_wait_time = 10.0
    # transfer time between red line and blue line at Jackson
    red_blue_jackson_wait_time = 10.0
    
    #>>> trans(['Brn', 'P'], '40460', desc="Merchandise Mart")
    tn.add_station('Brn_40460', {'P_40460':wait_time, 'Brn_40730':2, 'Brn_40710':2, }, desc='Merchandise Mart')  # done
    tn.add_station('P_40460', {'Brn_40460':wait_time, 'P_40380':3 }, desc='Merchandise Mart')   # done loop
    
    #>>> trans(['Brn', 'P', 'Org', 'Pink'], '40730', desc="Washington/Wells")
    tn.add_station('Brn_40730', {'Org_40730':wait_time, 'P_40730':wait_time, 'Pink_40730':wait_time, 'Brn_40040':1, }, desc='Washington/Wells') # done
    tn.add_station('P_40730', {'Brn_40730':wait_time, 'Org_40730':wait_time, 'Pink_40730':wait_time, 'P_40460':2, }, desc='Washington/Wells')   # done
    tn.add_station('Org_40730', {'Brn_40730':wait_time, 'P_40730':wait_time, 'Pink_40730':wait_time, 'Org_40380':3 }, desc='Washington/Wells')  # done
    tn.add_station('Pink_40730', {'Brn_40730':wait_time, 'Org_40730':wait_time, 'P_40730':wait_time, 'Pink_41160':3}, desc='Washington/Wells')  # done clinton estimate
    
    #>>> trans(['Brn', 'P', 'Org', 'Pink'], '40040', desc="Quincy")
    tn.add_station('Brn_40040', {'Pink_40040':wait_time, 'P_40040':wait_time, 'Org_40040':wait_time, 'Brn_40160':1, }, desc='Quincy') # done
    tn.add_station('P_40040', {'Brn_40040':wait_time, 'Pink_40040':wait_time, 'Org_40040':wait_time, 'P_40730':1, }, desc='Quincy', ) # done
    tn.add_station('Org_40040', {'Brn_40040':wait_time, 'Pink_40040':wait_time, 'P_40040':wait_time, 'Org_40730':1, }, desc='Quincy') # done
    tn.add_station('Pink_40040', {'Brn_40040':wait_time, 'P_40040':wait_time, 'Org_40040':wait_time, 'Pink_40730':1 }, desc='Quincy') # done
    
    #>>> trans(['Brn', 'P', 'Org', 'Pink'], '40160', desc="LaSalle")
    tn.add_station('Brn_40160', {'P_40160':wait_time, 'Pink_40160':wait_time, 'Org_40160':wait_time, 'Brn_40850':1, }, desc='LaSalle') # done
    tn.add_station('P_40160', {'Pink_40160':wait_time, 'Brn_40160':wait_time, 'Org_40160':wait_time, 'P_40040':1, }, desc='LaSalle') # done
    tn.add_station('Org_40160', {'P_40160':wait_time, 'Pink_40160':wait_time, 'Brn_40160':wait_time, 'Org_40040':1, }, desc='LaSalle') # done
    tn.add_station('Pink_40160', {'P_40160':wait_time, 'Brn_40160':wait_time, 'Org_40160':wait_time, 'Pink_40040':1 }, desc='LaSalle') # done
    
    #>>> trans(['Brn', 'P', 'Org', 'Pink'], '40850', desc="Library")
    tn.add_station('Brn_40850', {'Pink_40850':wait_time, 'P_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Brn_40680':2, }, desc='Library') # done
    tn.add_station('P_40850', {'Brn_40850':wait_time, 'Pink_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'P_40160':1, }, desc='Library')  # done
    tn.add_station('Org_40850', {'Brn_40850':wait_time, 'Pink_40850':wait_time, 'P_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Org_40160':1, }, desc='Library')  # done
    tn.add_station('Pink_40850', {'Brn_40850':wait_time, 'P_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Pink_40160':1, }, desc='Library') # done
    
    #>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40680', desc="Adams/Wabash")
    tn.add_station('Brn_40680', {'P_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'Brn_40640':1, }, desc='Adams/Wabash') # done
    tn.add_station('P_40680', {'Brn_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'P_40850':2, }, desc='Adams/Wabash') # done
    tn.add_station('Org_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'G_40680':wait_time, 'Pink_40680':wait_time, 'Org_41400':4, }, desc='Adams/Wabash') # done
    tn.add_station('G_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'G_41400':3, 'G_40640':1, }, desc='Adams/Wabash') # done
    tn.add_station('Pink_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40850':2, }, desc='Adams/Wabash') # done
    
    #>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40640', desc="Maddison/Wabash")
    tn.add_station('Brn_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Pink_40640':wait_time, 'G_40640':wait_time, 'Brn_40200':1, }, desc='Maddison/Wabash') # done
    tn.add_station('P_40640', {'Org_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'P_40680':1, }, desc='Maddison/Wabash') # done
    tn.add_station('Org_40640', {'P_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'Org_40680':1, }, desc='Maddison/Wabash') # done
    tn.add_station('G_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40680':1, 'G_40200':1, }, desc='Maddison/Wabash') # done
    tn.add_station('Pink_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'Pink_40680':1, }, desc='Maddison/Wabash')  # done
    
    #>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40200', desc="Randolph/Wabash")
    tn.add_station('Brn_40200', {'G_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'Brn_40260':1, }, desc='Randolph/Wabash') # done
    tn.add_station('P_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'P_40640':1, }, desc='Randolph/Wabash') # done
    tn.add_station('Org_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'P_40200':wait_time, 'Pink_40200':wait_time, 'Org_40640':1, }, desc='Randolph/Wabash') # done
    tn.add_station('G_40200', {'Brn_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'G_40640':1,  'G_40260':1, }, desc='Randolph/Wabash') # done
    tn.add_station('Pink_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40640':1 }, desc='Randolph/Wabash') # done
    
    #>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40260', desc="State/Lake")
    tn.add_station('Brn_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Pink_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Brn_40380':1 }, desc='State/Lake')  # done
    tn.add_station('P_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'Red_41660':wait_time, 'P_40200':1, }, desc='State/Lake')  # done
    tn.add_station('Org_40260', {'G_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Org_40200':1 }, desc='State/Lake')  # done
    tn.add_station('G_40260', {'Org_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'G_40200':1, 'G_40380':1 }, desc='State/Lake') # done
    tn.add_station('Pink_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Pink_40200':1 }, desc='State/Lake')  # done
    
    #>>> trans(['Brn', 'P', 'Org', 'G', 'Blue', 'Pink'], '40380', desc="Clark/Lake")
    tn.add_station('Brn_40380', {'Blue_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Brn_40460':4, }, desc='Clark/Lake')  # done
    tn.add_station('P_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40260':1, }, desc='Clark/Lake')  # done
    tn.add_station('Org_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Org_40260':1, }, desc='Clark/Lake')  # done
    tn.add_station('G_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'P_40380':wait_time, 'G_40260': 1, 'G_41160':2 }, desc='Clark/Lake')  # done
    tn.add_station('Blue_40380', {'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Blue_40490':2, 'Blue_40370':2 }, desc='Clark/Lake') # done
    tn.add_station('Pink_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Pink_40260':1, }, desc='Clark/Lake') # done
    
    #>>> trans(['Red', 'Org', 'G', ], '41400', desc="Roosevelt")
    tn.add_station('Red_41400', {'Org_41400':wait_time, 'G_41400':wait_time, }, desc='Roosevelt')
    tn.add_station('Org_41400', {'Red_41400':wait_time, 'G_41400':wait_time, 'Org_40850':3 }, desc='Roosevelt')  # done loop
    tn.add_station('G_41400', {'Org_41400':wait_time, 'Red_41400':wait_time, 'G_40680':3, }, desc='Roosevelt')  # done loop
    
    #>>> trans(['Pink', 'G', ], '41160', desc="Clinton")
    tn.add_station('Pink_41160', {'G_41160':wait_time, 'Pink_40380':2, 'Pink_morgan':1}, desc='Clinton') # done loop
    tn.add_station('G_41160', {'Pink_41160':wait_time, 'G_40380':2, 'G_morgan':1, }, desc='Clinton') # done loop
    
    # Harrison Red
    tn.add_station('Red_41490', { 'Red_41400':1, 'Red_40560':1 }, desc='Harrison')  # done
    
    # Jackson Red
    tn.add_station('Red_40560', { 'Red_41490':1, 'Red_41090':2, 'Blue_40070':red_blue_jackson_wait_time, 'Brn_40850':redlib_wait_time, 'P_40850':redlib_wait_time, 'Org_40850':redlib_wait_time, 'Pink_40850':redlib_wait_time }, desc='Jackson')  # done
    
    # Monroe Red
    tn.add_station('Red_41090', { 'Red_40560':2, 'Red_41660':1 }, desc='Monroe')  # done
    
    # Lake Red 
    tn.add_station('Red_41660', { 'Red_41090':1, 'Red_40330':1,'Brn_40260':wait_time, 'P_40260':wait_time, 'Org_40260':wait_time, 'G_40260':wait_time, 'Pink_40260':wait_time, }, desc='Lake Red')  # done 
    
    # Grand Red
    tn.add_station('Red_40330', { 'Red_41660':1, 'Red_41450':1, }, desc='Grand Red')  # done loop
    
    # Grand Blue
    tn.add_station('Blue_40490', { 'Blue_40380':2, 'Blue_41410':2 }, desc='Grand Blue')  # done loop
    
    # Washington Blue
    tn.add_station('Blue_40370', { 'Blue_40380':2, 'Blue_40790':1 }, desc='Washington')  # done
    
    # Monroe Blue
    tn.add_station('Blue_40790', { 'Blue_40070':1, 'Blue_40370':1 }, desc='Monroe')  # done
    
    # Jackson Blue
    tn.add_station('Blue_40070', { 'Blue_40790':1, 'Blue_41340':1, 'Red_40560':red_blue_jackson_wait_time, 'Brn_40850':bluelib_wait_time, 'P_40850':bluelib_wait_time, 'Org_40850':bluelib_wait_time, 'Pink_40850':bluelib_wait_time}, desc='Jackson')  # done
    
    # VanBuren Blue
    tn.add_station('Blue_41340', { 'Blue_40070':1, 'Blue_40430':1, }, desc='VanBuren')  # done loop
    
    ### Red North Side ###########################################################
    
    # Chicago Red
    tn.add_station('Red_41450', { 'Red_40330':1, 'Red_40630':2 }, desc='Chicago Red')     # done

    # Clark/Division Red
    tn.add_station('Red_40630', { 'Red_41450':2, 'Red_40650':3 }, desc='Clark/Division Red')  # done

    # North/Clybourn Red 
    tn.add_station('Red_40650', { 'Red_40630':3, 'Red_41220':2 }, desc='North/Clybourn Red')   # done
    
    # Fullerton 
    tn.add_station('Red_41220', { 'Red_40650':2, 'Red_41320':3, 'Brn_41220':wait_time, 'P_41220':wait_time, }, desc='Fullerton')  # done

    # Belmont 
    tn.add_station('Red_41320', { 'Red_41220':3, 'Red_41420':2, 'Brn_41320':wait_time, 'P_41320':wait_time, }, desc='Belmont')  # done

    # Addison Red  
    tn.add_station('Red_41420', { 'Red_41320':2, 'Red_40080':2 }, desc='Addison Red')  # done 
    
    # Sheridan Red 
    tn.add_station('Red_40080', { 'Red_41420':2, 'Red_40540':3 }, desc='Sheridan Red')  # done

    # Wilson Red 
    tn.add_station('Red_40540', { 'Red_40080':3, 'Red_40770':1 }, desc='Wilson Red')  # done

    # Lawrence Red 
    tn.add_station('Red_40770', { 'Red_40540':1, 'Red_41200':1 }, desc='Lawrence Red')  # done

    # Argyle Red 
    tn.add_station('Red_41200', { 'Red_40770':1, 'Red_40340':1 }, desc='Argyle Red') # done

    # Berwyn Red 
    tn.add_station('Red_40340', { 'Red_41200':1, 'Red_41380':1 }, desc='Berwyn Red') # done

    # Bryn Mawr Red 
    tn.add_station('Red_41380', { 'Red_40340':1, 'Red_40880':2 }, desc='Bryn Mawr Red')  # done

    # Thorndale Red 
    tn.add_station('Red_40880', { 'Red_41380':2, 'Red_40760':1 }, desc='Thorndale Red')  # done

    # Granville Red 
    tn.add_station('Red_40760', { 'Red_40880':1, 'Red_41300':2 }, desc='Granville Red')  # done

    # Loyola Red 
    tn.add_station('Red_41300', { 'Red_40760':2, 'Red_40100':2 }, desc='Loyola Red')  # done

    # Morse Red 
    tn.add_station('Red_40100', { 'Red_41300':2, 'Red_41190':1 }, desc='Morse Red')  # done

    # Jarvis Red 
    tn.add_station('Red_41190', { 'Red_40100':1, 'Red_40900':2 }, desc='Jarvis Red')  # done

    # Howard Red 
    tn.add_station('Red_40900', { 'Red_41190':2, 'P_40900':wait_time, }, desc='Howard Red')  # done north side

    ### Brown North Side ###########################################################
    
    # Chicago Brown
    tn.add_station('Brn_40710', { 'Brn_40460':2, 'Brn_40800':4, 'P_40710':wait_time, }, desc='Chicago Brown')  # done
    
    # Sedgwic Brown
    tn.add_station('Brn_40800', { 'Brn_40710':4, 'Brn_40660':3, 'P_40800':wait_time }, desc='Sedgwic Brown')  # done
        
    # Armitage Brown
    tn.add_station('Brn_40660', { 'Brn_40800':3, 'Brn_41220':2, 'P_40660':wait_time, }, desc='Armitage Brown')  # done  
    
    # Fullerton Brown
    tn.add_station('Brn_41220', { 'Brn_40660':2, 'Brn_40530':1, 'Red_41220':wait_time, 'P_41220':wait_time, }, desc='Fullerton Brown')  # done  
    
    # Diversey Brown
    tn.add_station('Brn_40530', { 'Brn_41220':1, 'Brn_41210':1, 'P_40530':wait_time,  }, desc='Diversey Brown')  # done
    
    # Wellington Brown
    tn.add_station('Brn_41210', { 'Brn_40530':1, 'Brn_41320':1, 'P_41210':wait_time }, desc='Wellington Brown')  # done
    
    # Belmont Brown
    tn.add_station('Brn_41320', { 'Brn_41210':1, 'Brn_40360':2, 'Red_41320':wait_time, 'P_41320':wait_time }, desc='Belmont Brown')  # done
    
    # Southbort Brown
    tn.add_station('Brn_40360', { 'Brn_41320':2, 'Brn_41310':1, }, desc='Southport Brown')  # done 

    # Paulina Brown
    tn.add_station('Brn_41310', { 'Brn_40360':1, 'Brn_41440':2, }, desc='Paulina Brown')  # done

    # Addison Brown
    tn.add_station('Brn_41440', { 'Brn_41310':2, 'Brn_41460':1, }, desc='Addison Brown')  # done

    # Irving Park Brown
    tn.add_station('Brn_41460', { 'Brn_41440':1, 'Brn_41500':1, }, desc='Irving Park Brown')  # done

    # Montrose Brown
    tn.add_station('Brn_41500', { 'Brn_41460':1, 'Brn_40090':2, }, desc='Montrose Brown')  # done

    # Damen Brown
    tn.add_station('Brn_40090', { 'Brn_41500':2, 'Brn_41480':1, }, desc='Damen Brown')  # done

    # Western Brown
    tn.add_station('Brn_41480', { 'Brn_40090':1, 'Brn_41010':2, }, desc='Western Brown')  # done 

    # Rockwell Brown
    tn.add_station('Brn_41010', { 'Brn_41480':2, 'Brn_40870':1, }, desc='Rockwell Brown')  # done

    # Fransisco Brown
    tn.add_station('Brn_40870', { 'Brn_41010':1, 'Brn_41180':1, }, desc='Fransisco Brown')  # done

    # Kedzie Brown
    tn.add_station('Brn_41180', { 'Brn_40870':1, 'Brn_41290':2, }, desc='Kedzie Brown')  # done

    # Kimball Brown
    tn.add_station('Brn_41290', { 'Brn_41180':2,  }, desc='Kimball Brown')  # done

    ### Purple North Side ###########################################################
    
    # Chicago Purple
    tn.add_station('P_40710', { 'P_40460':2, 'P_40800':4, 'Brn_40710':wait_time }, desc='Chicago Purple')  # done
    
    # Sedgwick Purple
    tn.add_station('P_40800', { 'P_40710':4, 'P_40660':3, 'Brn_40800':wait_time }, desc='Sedgwick Purple')  # done

    # Armitage Purple
    tn.add_station('P_40660', { 'P_40800':3, 'P_41220':2, 'Brn_40660':wait_time, }, desc='Armitage Purple')  # done

    # Fullerton Purple
    tn.add_station('P_41220', { 'P_40660':2, 'P_40530':1, 'Brn_41220':wait_time, 'Red_41220':wait_time }, desc='Fullerton Purple')  # done

    # Diversy Purple
    tn.add_station('P_40530', { 'P_41220':1, 'P_41210':1, 'Brn_40530':wait_time,}, desc='Diversy Purple')  # done

    # Wellington Purple
    tn.add_station('P_41210', { 'P_40530':1, 'P_41320':1, 'Brn_41210':wait_time,}, desc='Wellington Purple')  # done

    # Belmont Purple
    tn.add_station('P_41320', { 'P_41210':1, 'P_40900':14, 'Brn_41320':wait_time, 'Red_41320':wait_time, }, desc='Belmont Purple')  # done 

    # Howard Purple
    tn.add_station('P_40900', { 'P_41320':14, 'Red_40900':wait_time }, desc='Howard Purple')  # done with north side, needs purple north

    ### Blue West Side ###########################################################
    
    # O'Hare Blue
    tn.add_station('Blue_40890', { 'Blue_40820':5, }, desc="O'Hare Blue")  # done 
 
    # Rosemont Blue
    tn.add_station('Blue_40820', { 'Blue_40890':5, 'Blue_40230':2  }, desc="Rosemont Blue")   # done

    # Cumberland Blue
    tn.add_station('Blue_40230', { 'Blue_40820':2, 'Blue_40750':3  }, desc="Cumberland Blue")   # done

    # Harlem Blue
    tn.add_station('Blue_40750', { 'Blue_40230':3, 'Blue_41280':4  }, desc="Harlem Blue")  # done

    # Jefferson Park Blue
    tn.add_station('Blue_41280', { 'Blue_40750':4, 'Blue_41330':2  }, desc="Jefferson Park Blue")  # done

    # Montrose Blue
    tn.add_station('Blue_41330', { 'Blue_41280':2, 'Blue_40550':2  }, desc="Montrose Blue")  # done 

    # Irving Park Blue
    tn.add_station('Blue_40550', { 'Blue_41330':2, 'Blue_41240':2  }, desc="Irving Park Blue")  # done

    # Addison Blue
    tn.add_station('Blue_41240', { 'Blue_40550':2, 'Blue_40060':2  }, desc="Addison Blue")  # done

    # Belmont Blue
    tn.add_station('Blue_40060', { 'Blue_41240':2, 'Blue_41020':2  }, desc="Belmont Blue")  # done

    # Logan Square Blue
    tn.add_station('Blue_41020', { 'Blue_40060':2, 'Blue_40570':2  }, desc="Logan Square Blue")  # done

    # California Blue
    tn.add_station('Blue_40570', { 'Blue_41020':2, 'Blue_40670':2  }, desc="California Blue")  # done

    # Western Blue
    tn.add_station('Blue_40670', { 'Blue_40570':2, 'Blue_40590':1  }, desc="Western Blue")  # done

    # Damen Blue
    tn.add_station('Blue_40590', { 'Blue_40670':1, 'Blue_40320':1  }, desc="Damen Blue")  # done

    # Division Blue
    tn.add_station('Blue_40320', { 'Blue_40590':1, 'Blue_41410':2  }, desc="Division Blue")  # done

    # Chicago Blue
    tn.add_station('Blue_41410', { 'Blue_40320':2, 'Blue_40490':2  }, desc="Chicago Blue")  # done

    ### Green West Side ###########################################################

    # Harlem/Lake Green
    tn.add_station('G_40020', { 'G_41350':1, }, desc="Harlem/Lake Green")  # done

    # Oak Park Green
    tn.add_station('G_41350', { 'G_40020':1, 'G_40610':2 }, desc="Oak Park Green")  # done

    # Ridgeland Green
    tn.add_station('G_40610', { 'G_41350':2, 'G_41260':1 }, desc="Ridgeland Green")  # done

    # Austin Green
    tn.add_station('G_41260', { 'G_40610':1, 'G_40280':2 }, desc="Austin Green")  # done

    # Central Green
    tn.add_station('G_40280', { 'G_41260':2, 'G_40700':2 }, desc="Central Green")  # done

    # Laramie Green
    tn.add_station('G_40700', { 'G_40280':2, 'G_40480':1 }, desc="Laramie Green")  # done

    # Cicero Green
    tn.add_station('G_40480', { 'G_40700':1, 'G_40030':2 }, desc="Cicero Green")  # done

    # Pulaski Green
    tn.add_station('G_40030', { 'G_40480':2, 'G_41670':2 }, desc="Pulaski Green")  # done

    # Conservatory Green
    tn.add_station('G_41670', { 'G_40030':2, 'G_41070':1 }, desc="Conservatory Green")  # done

    # Kedzie Green
    tn.add_station('G_41070', { 'G_41670':1, 'G_41360':1 }, desc="Kedzie Green")  # done

    # California Green
    tn.add_station('G_41360', { 'G_41070':1, 'G_40170':3 }, desc="California Green")  # done

    # Ashland Green
    tn.add_station('G_40170', { 'G_41360':3, 'G_morgan':2, 'Pink_40170':wait_time }, desc="Ashland Green")  # partial

    # Morgan Green
    tn.add_station('G_morgan', { 'G_40170':2, 'G_41160':1 }, desc="Morgan Green")  # partial

    ### Blue South West Side ###########################################################

    # Forest Park Blue
    tn.add_station('Blue_40390', { 'Blue_40980':2,  }, desc="Forest Park Blue")  # done  

    # Harlem Blue
    tn.add_station('Blue_40980', { 'Blue_40390':2, 'Blue_40180':2 }, desc="Harlem Blue")  # done  

    # Oak Park Blue
    tn.add_station('Blue_40180', { 'Blue_40980':2, 'Blue_40010':2 }, desc="Oak Park Blue")  # done

    # Austin Blue
    tn.add_station('Blue_40010', { 'Blue_40180':2, 'Blue_40970':3 }, desc="Austin Blue")  # done

    # Cicero Blue
    tn.add_station('Blue_40970', { 'Blue_40010':3, 'Blue_40920':3 }, desc="Cicero Blue")  # done

    # Pulaski Blue
    tn.add_station('Blue_40920', { 'Blue_40970':3, 'Blue_40250':2 }, desc="Pulaski Blue")  # done

    # Kedzie Blue
    tn.add_station('Blue_40250', { 'Blue_40920':2, 'Blue_40220':3 }, desc="Kedzie Blue")  # done

    # Western Blue
    tn.add_station('Blue_40220', { 'Blue_40250':3, 'Blue_40810':3 }, desc="Western Blue")  # done

    # Illinois Medical Center Blue
    tn.add_station('Blue_40810', { 'Blue_40220':3, 'Blue_40470':3 }, desc="Illinois Medical Center Blue")   # done

    # Racine Blue
    tn.add_station('Blue_40470', { 'Blue_40810':3, 'Blue_40350':1 }, desc="Racine Blue")  # done

    # UIC Blue
    tn.add_station('Blue_40350', { 'Blue_40470':1, 'Blue_40430':2 }, desc="UIC Blue")  # done

    # Clinton Blue
    tn.add_station('Blue_40430', { 'Blue_40350':2, 'Blue_41340':1 }, desc="Clinton Blue")  # done

   ### Pink Side ###########################################################

    # 54th/Cermac Pink
    tn.add_station('Pink_40580', { 'Pink_40420':1, }, desc="54th/Cermac Pink")  # done

    # Cicero Pink
    tn.add_station('Pink_40420', { 'Pink_40580':1, 'Pink_40600':2 }, desc="Cicero Pink")  # done

    # Kostner Pink
    tn.add_station('Pink_40600', { 'Pink_40420':2, 'Pink_40150':1 }, desc="Kostner Pink")  # done

    # Pulaski Pink
    tn.add_station('Pink_40150', { 'Pink_40600':1, 'Pink_40780':2 }, desc="Pulaski Pink")  # done

    # Central Park Pink
    tn.add_station('Pink_40780', { 'Pink_40150':2, 'Pink_41040':1 }, desc="Central Park Pink")  # done

    # Kedzie Pink
    tn.add_station('Pink_41040', { 'Pink_40780':1, 'Pink_40440':2 }, desc="Kedzie Pink")  # done

    # California Pink
    tn.add_station('Pink_40440', { 'Pink_41040':2, 'Pink_40740':2 }, desc="California Pink")  # done

    # Western Pink
    tn.add_station('Pink_40740', { 'Pink_40440':2, 'Pink_40210':1 }, desc="Western Pink")  # done

    # Damen Pink
    tn.add_station('Pink_40210', { 'Pink_40740':1, 'Pink_40830':2 }, desc="Damen Pink")  # done

    # 18th Pink
    tn.add_station('Pink_40830', { 'Pink_40210':2, 'Pink_41030':2 }, desc="18th Pink")  # done

    # Polk Pink
    tn.add_station('Pink_41030', { 'Pink_40830':2, 'Pink_40170':3 }, desc="Polk Pink")  # done

    # Ashland Pink
    tn.add_station('Pink_40170', { 'Pink_41030':3, 'Pink_morgan':2, 'G_40170':wait_time}, desc="Ashland Pink")  # done

    # Morgan Pink
    tn.add_station('Pink_morgan', { 'Pink_40170':2, 'Pink_41160':1, 'G_morgan':wait_time}, desc="Morgan Pink")

    return tn
