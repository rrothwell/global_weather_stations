'''
Created on 31 Jul. 2021

@author: richardrothwell
'''
from io import StringIO
import csv

from library.world.continent import Continent
from library.world.country import Country
from library.world.state import State
    
'''
Fields:
Continent_Name,Continent_Code,Country_Name,Two_Letter_Country_Code,Three_Letter_Country_Code,Country_Number
'''

WORLD_CSV = (        
'Asia,AS,"Afghanistan, Islamic Republic of",AF,AFG,4\n'
'Europe,EU,"Albania, Republic of",AL,ALB,8\n'
'Antarctica,AN,Antarctica (the territory South of 60 deg S),AQ,ATA,10\n'
'Africa,AF,"Algeria, People\'s Democratic Republic of",DZ,DZA,12\n'
'Oceania,OC,American Samoa,AS,ASM,16\n'
'Europe,EU,"Andorra, Principality of",AD,AND,20\n'
'Africa,AF,"Angola, Republic of",AO,AGO,24\n'
'North America,NA,Antigua and Barbuda,AG,ATG,28\n'
'Europe,EU,"Azerbaijan, Republic of",AZ,AZE,31\n'
'Asia,AS,"Azerbaijan, Republic of",AZ,AZE,31\n'
'South America,SA,"Argentina, Argentine Republic",AR,ARG,32\n'
'Oceania,OC,"Australia, Commonwealth of",AU,AUS,36\n'
'Europe,EU,"Austria, Republic of",AT,AUT,40\n'
'North America,NA,"Bahamas, Commonwealth of the",BS,BHS,44\n'
'Asia,AS,"Bahrain, Kingdom of",BH,BHR,48\n'
'Asia,AS,"Bangladesh, People\'s Republic of",BD,BGD,50\n'
'Europe,EU,"Armenia, Republic of",AM,ARM,51\n'
'Asia,AS,"Armenia, Republic of",AM,ARM,51\n'
'North America,NA,Barbados,BB,BRB,52\n'
'Europe,EU,"Belgium, Kingdom of",BE,BEL,56\n'
'North America,NA,Bermuda,BM,BMU,60\n'
'Asia,AS,"Bhutan, Kingdom of",BT,BTN,64\n'
'South America,SA,"Bolivia, Republic of",BO,BOL,68\n'
'Europe,EU,Bosnia and Herzegovina,BA,BIH,70\n'
'Africa,AF,"Botswana, Republic of",BW,BWA,72\n'
'Antarctica,AN,Bouvet Island (Bouvetoya),BV,BVT,74\n'
'South America,SA,"Brazil, Federative Republic of",BR,BRA,76\n'
'North America,NA,Belize,BZ,BLZ,84\n'
'Asia,AS,British Indian Ocean Territory (Chagos Archipelago),IO,IOT,86\n'
'Oceania,OC,Solomon Islands,SB,SLB,90\n'
'North America,NA,British Virgin Islands,VG,VGB,92\n'
'Asia,AS,Brunei Darussalam,BN,BRN,96\n'
'Europe,EU,"Bulgaria, Republic of",BG,BGR,100\n'
'Asia,AS,"Myanmar, Union of",MM,MMR,104\n'
'Africa,AF,"Burundi, Republic of",BI,BDI,108\n'
'Europe,EU,"Belarus, Republic of",BY,BLR,112\n'
'Asia,AS,"Cambodia, Kingdom of",KH,KHM,116\n'
'Africa,AF,"Cameroon, Republic of",CM,CMR,120\n'
'North America,NA,Canada,CA,CAN,124\n'
'Africa,AF,"Cape Verde, Republic of",CV,CPV,132\n'
'North America,NA,Cayman Islands,KY,CYM,136\n'
'Africa,AF,Central African Republic,CF,CAF,140\n'
'Asia,AS,"Sri Lanka, Democratic Socialist Republic of",LK,LKA,144\n'
'Africa,AF,"Chad, Republic of",TD,TCD,148\n'
'South America,SA,"Chile, Republic of",CL,CHL,152\n'
'Asia,AS,"China, People\'s Republic of",CN,CHN,156\n'
'Asia,AS,Taiwan,TW,TWN,158\n'
'Asia,AS,Christmas Island,CX,CXR,162\n'
'Asia,AS,Cocos (Keeling) Islands,CC,CCK,166\n'
'South America,SA,"Colombia, Republic of",CO,COL,170\n'
'Africa,AF,"Comoros, Union of the",KM,COM,174\n'
'Africa,AF,Mayotte,YT,MYT,175\n'
'Africa,AF,"Congo, Republic of the",CG,COG,178\n'
'Africa,AF,"Congo, Democratic Republic of the",CD,COD,180\n'
'Oceania,OC,Cook Islands,CK,COK,184\n'
'North America,NA,"Costa Rica, Republic of",CR,CRI,188\n'
'Europe,EU,"Croatia, Republic of",HR,HRV,191\n'
'North America,NA,"Cuba, Republic of",CU,CUB,192\n'
'Europe,EU,"Cyprus, Republic of",CY,CYP,196\n'
'Asia,AS,"Cyprus, Republic of",CY,CYP,196\n'
'Europe,EU,Czech Republic,CZ,CZE,203\n'
'Africa,AF,"Benin, Republic of",BJ,BEN,204\n'
'Europe,EU,"Denmark, Kingdom of",DK,DNK,208\n'
'North America,NA,"Dominica, Commonwealth of",DM,DMA,212\n'
'North America,NA,Dominican Republic,DO,DOM,214\n'
'South America,SA,"Ecuador, Republic of",EC,ECU,218\n'
'North America,NA,"El Salvador, Republic of",SV,SLV,222\n'
'Africa,AF,"Equatorial Guinea, Republic of",GQ,GNQ,226\n'
'Africa,AF,"Ethiopia, Federal Democratic Republic of",ET,ETH,231\n'
'Africa,AF,"Eritrea, State of",ER,ERI,232\n'
'Europe,EU,"Estonia, Republic of",EE,EST,233\n'
'Europe,EU,Faroe Islands,FO,FRO,234\n'
'South America,SA,Falkland Islands (Malvinas),FK,FLK,238\n'
'Antarctica,AN,South Georgia and the South Sandwich Islands,GS,SGS,239\n'
'Oceania,OC,"Fiji, Republic of the Fiji Islands",FJ,FJI,242\n'
'Europe,EU,"Finland, Republic of",FI,FIN,246\n'
'Europe,EU,Ã…land Islands,AX,ALA,248\n'
'Europe,EU,"France, French Republic",FR,FRA,250\n'
'South America,SA,French Guiana,GF,GUF,254\n'
'Oceania,OC,French Polynesia,PF,PYF,258\n'
'Antarctica,AN,French Southern Territories,TF,ATF,260\n'
'Africa,AF,"Djibouti, Republic of",DJ,DJI,262\n'
'Africa,AF,"Gabon, Gabonese Republic",GA,GAB,266\n'
'Europe,EU,Georgia,GE,GEO,268\n'
'Asia,AS,Georgia,GE,GEO,268\n'
'Africa,AF,"Gambia, Republic of the",GM,GMB,270\n'
'Asia,AS,"Palestinian Territory, Occupied",PS,PSE,275\n'
'Europe,EU,"Germany, Federal Republic of",DE,DEU,276\n'
'Africa,AF,"Ghana, Republic of",GH,GHA,288\n'
'Europe,EU,Gibraltar,GI,GIB,292\n'
'Oceania,OC,"Kiribati, Republic of",KI,KIR,296\n'
'Europe,EU,"Greece, Hellenic Republic",GR,GRC,300\n'
'North America,NA,Greenland,GL,GRL,304\n'
'North America,NA,Grenada,GD,GRD,308\n'
'North America,NA,Guadeloupe,GP,GLP,312\n'
'Oceania,OC,Guam,GU,GUM,316\n'
'North America,NA,"Guatemala, Republic of",GT,GTM,320\n'
'Africa,AF,"Guinea, Republic of",GN,GIN,324\n'
'South America,SA,"Guyana, Co-operative Republic of",GY,GUY,328\n'
'North America,NA,"Haiti, Republic of",HT,HTI,332\n'
'Antarctica,AN,Heard Island and McDonald Islands,HM,HMD,334\n'
'Europe,EU,Holy See (Vatican City State),VA,VAT,336\n'
'North America,NA,"Honduras, Republic of",HN,HND,340\n'
'Asia,AS,"Hong Kong, Special Administrative Region of China",HK,HKG,344\n'
'Europe,EU,"Hungary, Republic of",HU,HUN,348\n'
'Europe,EU,"Iceland, Republic of",IS,ISL,352\n'
'Asia,AS,"India, Republic of",IN,IND,356\n'
'Asia,AS,"Indonesia, Republic of",ID,IDN,360\n'
'Asia,AS,"Iran, Islamic Republic of",IR,IRN,364\n'
'Asia,AS,"Iraq, Republic of",IQ,IRQ,368\n'
'Europe,EU,Ireland,IE,IRL,372\n'
'Asia,AS,"Israel, State of",IL,ISR,376\n'
'Europe,EU,"Italy, Italian Republic",IT,ITA,380\n'
'Africa,AF,"Cote d\'Ivoire, Republic of",CI,CIV,384\n'
'North America,NA,Jamaica,JM,JAM,388\n'
'Asia,AS,Japan,JP,JPN,392\n'
'Europe,EU,"Kazakhstan, Republic of",KZ,KAZ,398\n'
'Asia,AS,"Kazakhstan, Republic of",KZ,KAZ,398\n'
'Asia,AS,"Jordan, Hashemite Kingdom of",JO,JOR,400\n'
'Africa,AF,"Kenya, Republic of",KE,KEN,404\n'
'Asia,AS,"Korea, Democratic People\'s Republic of",KP,PRK,408\n'
'Asia,AS,"Korea, Republic of",KR,KOR,410\n'
'Asia,AS,"Kuwait, State of",KW,KWT,414\n'
'Asia,AS,Kyrgyz Republic,KG,KGZ,417\n'
'Asia,AS,Lao People\'s Democratic Republic,LA,LAO,418\n'
'Asia,AS,"Lebanon, Lebanese Republic",LB,LBN,422\n'
'Africa,AF,"Lesotho, Kingdom of",LS,LSO,426\n'
'Europe,EU,"Latvia, Republic of",LV,LVA,428\n'
'Africa,AF,"Liberia, Republic of",LR,LBR,430\n'
'Africa,AF,Libyan Arab Jamahiriya,LY,LBY,434\n'
'Europe,EU,"Liechtenstein, Principality of",LI,LIE,438\n'
'Europe,EU,"Lithuania, Republic of",LT,LTU,440\n'
'Europe,EU,"Luxembourg, Grand Duchy of",LU,LUX,442\n'
'Asia,AS,"Macao, Special Administrative Region of China",MO,MAC,446\n'
'Africa,AF,"Madagascar, Republic of",MG,MDG,450\n'
'Africa,AF,"Malawi, Republic of",MW,MWI,454\n'
'Asia,AS,Malaysia,MY,MYS,458\n'
'Asia,AS,"Maldives, Republic of",MV,MDV,462\n'
'Africa,AF,"Mali, Republic of",ML,MLI,466\n'
'Europe,EU,"Malta, Republic of",MT,MLT,470\n'
'North America,NA,Martinique,MQ,MTQ,474\n'
'Africa,AF,"Mauritania, Islamic Republic of",MR,MRT,478\n'
'Africa,AF,"Mauritius, Republic of",MU,MUS,480\n'
'North America,NA,"Mexico, United Mexican States",MX,MEX,484\n'
'Europe,EU,"Monaco, Principality of",MC,MCO,492\n'
'Asia,AS,Mongolia,MN,MNG,496\n'
'Europe,EU,"Moldova, Republic of",MD,MDA,498\n'
'Europe,EU,"Montenegro, Republic of",ME,MNE,499\n'
'North America,NA,Montserrat,MS,MSR,500\n'
'Africa,AF,"Morocco, Kingdom of",MA,MAR,504\n'
'Africa,AF,"Mozambique, Republic of",MZ,MOZ,508\n'
'Asia,AS,"Oman, Sultanate of",OM,OMN,512\n'
'Africa,AF,"Namibia, Republic of",NA,NAM,516\n'
'Oceania,OC,"Nauru, Republic of",NR,NRU,520\n'
'Asia,AS,"Nepal, State of",NP,NPL,524\n'
'Europe,EU,"Netherlands, Kingdom of the",NL,NLD,528\n'
'North America,NA,Netherlands Antilles,AN,ANT,530\n'
'North America,NA,CuraÃ§ao,CW,CUW,531\n'
'North America,NA,Aruba,AW,ABW,533\n'
'North America,NA,Sint Maarten (Netherlands),SX,SXM,534\n'
'North America,NA,"Bonaire, Sint Eustatius and Saba",BQ,BES,535\n'
'Oceania,OC,New Caledonia,NC,NCL,540\n'
'Oceania,OC,"Vanuatu, Republic of",VU,VUT,548\n'
'Oceania,OC,New Zealand,NZ,NZL,554\n'
'North America,NA,"Nicaragua, Republic of",NI,NIC,558\n'
'Africa,AF,"Niger, Republic of",NE,NER,562\n'
'Africa,AF,"Nigeria, Federal Republic of",NG,NGA,566\n'
'Oceania,OC,Niue,NU,NIU,570\n'
'Oceania,OC,Norfolk Island,NF,NFK,574\n'
'Europe,EU,"Norway, Kingdom of",NO,NOR,578\n'
'Oceania,OC,"Northern Mariana Islands, Commonwealth of the",MP,MNP,580\n'
'Oceania,OC,United States Minor Outlying Islands,UM,UMI,581\n'
'North America,NA,United States Minor Outlying Islands,UM,UMI,581\n'
'Oceania,OC,"Micronesia, Federated States of",FM,FSM,583\n'
'Oceania,OC,"Marshall Islands, Republic of the",MH,MHL,584\n'
'Oceania,OC,"Palau, Republic of",PW,PLW,585\n'
'Asia,AS,"Pakistan, Islamic Republic of",PK,PAK,586\n'
'North America,NA,"Panama, Republic of",PA,PAN,591\n'
'Oceania,OC,"Papua New Guinea, Independent State of",PG,PNG,598\n'
'South America,SA,"Paraguay, Republic of",PY,PRY,600\n'
'South America,SA,"Peru, Republic of",PE,PER,604\n'
'Asia,AS,"Philippines, Republic of the",PH,PHL,608\n'
'Oceania,OC,Pitcairn Islands,PN,PCN,612\n'
'Europe,EU,"Poland, Republic of",PL,POL,616\n'
'Europe,EU,"Portugal, Portuguese Republic",PT,PRT,620\n'
'Africa,AF,"Guinea-Bissau, Republic of",GW,GNB,624\n'
'Asia,AS,"Timor-Leste, Democratic Republic of",TL,TLS,626\n'
'North America,NA,"Puerto Rico, Commonwealth of",PR,PRI,630\n'
'Asia,AS,"Qatar, State of",QA,QAT,634\n'
'Africa,AF,Reunion,RE,REU,638\n'
'Europe,EU,Romania,RO,ROU,642\n'
'Europe,EU,Russian Federation,RU,RUS,643\n'
'Asia,AS,Russian Federation,RU,RUS,643\n'
'Africa,AF,"Rwanda, Republic of",RW,RWA,646\n'
'North America,NA,Saint Barthelemy,BL,BLM,652\n'
'Africa,AF,Saint Helena,SH,SHN,654\n'
'North America,NA,"Saint Kitts and Nevis, Federation of",KN,KNA,659\n'
'North America,NA,Anguilla,AI,AIA,660\n'
'North America,NA,Saint Lucia,LC,LCA,662\n'
'North America,NA,Saint Martin,MF,MAF,663\n'
'North America,NA,Saint Pierre and Miquelon,PM,SPM,666\n'
'North America,NA,Saint Vincent and the Grenadines,VC,VCT,670\n'
'Europe,EU,"San Marino, Republic of",SM,SMR,674\n'
'Africa,AF,"Sao Tome and Principe, Democratic Republic of",ST,STP,678\n'
'Asia,AS,"Saudi Arabia, Kingdom of",SA,SAU,682\n'
'Africa,AF,"Senegal, Republic of",SN,SEN,686\n'
'Europe,EU,"Serbia, Republic of",RS,SRB,688\n'
'Africa,AF,"Seychelles, Republic of",SC,SYC,690\n'
'Africa,AF,"Sierra Leone, Republic of",SL,SLE,694\n'
'Asia,AS,"Singapore, Republic of",SG,SGP,702\n'
'Europe,EU,Slovakia (Slovak Republic),SK,SVK,703\n'
'Asia,AS,"Vietnam, Socialist Republic of",VN,VNM,704\n'
'Europe,EU,"Slovenia, Republic of",SI,SVN,705\n'
'Africa,AF,"Somalia, Somali Republic",SO,SOM,706\n'
'Africa,AF,"South Africa, Republic of",ZA,ZAF,710\n'
'Africa,AF,"Zimbabwe, Republic of",ZW,ZWE,716\n'
'Europe,EU,"Spain, Kingdom of",ES,ESP,724\n'
'Africa,AF,South Sudan,SS,SSD,728\n'
'Africa,AF,Western Sahara,EH,ESH,732\n'
'Africa,AF,"Sudan, Republic of",SD,SDN,736\n'
'South America,SA,"Suriname, Republic of",SR,SUR,740\n'
'Europe,EU,Svalbard & Jan Mayen Islands,SJ,SJM,744\n'
'Africa,AF,"Swaziland, Kingdom of",SZ,SWZ,748\n'
'Europe,EU,"Sweden, Kingdom of",SE,SWE,752\n'
'Europe,EU,"Switzerland, Swiss Confederation",CH,CHE,756\n'
'Asia,AS,Syrian Arab Republic,SY,SYR,760\n'
'Asia,AS,"Tajikistan, Republic of",TJ,TJK,762\n'
'Asia,AS,"Thailand, Kingdom of",TH,THA,764\n'
'Africa,AF,"Togo, Togolese Republic",TG,TGO,768\n'
'Oceania,OC,Tokelau,TK,TKL,772\n'
'Oceania,OC,"Tonga, Kingdom of",TO,TON,776\n'
'North America,NA,"Trinidad and Tobago, Republic of",TT,TTO,780\n'
'Asia,AS,United Arab Emirates,AE,ARE,784\n'
'Africa,AF,"Tunisia, Tunisian Republic",TN,TUN,788\n'
'Europe,EU,"Turkey, Republic of",TR,TUR,792\n'
'Asia,AS,"Turkey, Republic of",TR,TUR,792\n'
'Asia,AS,Turkmenistan,TM,TKM,795\n'
'North America,NA,Turks and Caicos Islands,TC,TCA,796\n'
'Oceania,OC,Tuvalu,TV,TUV,798\n'
'Africa,AF,"Uganda, Republic of",UG,UGA,800\n'
'Europe,EU,Ukraine,UA,UKR,804\n'
'Europe,EU,"Macedonia, The Former Yugoslav Republic of",MK,MKD,807\n'
'Africa,AF,"Egypt, Arab Republic of",EG,EGY,818\n'
'Europe,EU,United Kingdom of Great Britain & Northern Ireland,GB,GBR,826\n'
'Europe,EU,"Guernsey, Bailiwick of",GG,GGY,831\n'
'Europe,EU,"Jersey, Bailiwick of",JE,JEY,832\n'
'Europe,EU,Isle of Man,IM,IMN,833\n'
'Africa,AF,"Tanzania, United Republic of",TZ,TZA,834\n'
'North America,NA,United States of America,US,USA,840\n'
'North America,NA,United States Virgin Islands,VI,VIR,850\n'
'Africa,AF,Burkina Faso,BF,BFA,854\n'
'South America,SA,"Uruguay, Eastern Republic of",UY,URY,858\n'
'Asia,AS,"Uzbekistan, Republic of",UZ,UZB,860\n'
'South America,SA,"Venezuela, Bolivarian Republic of",VE,VEN,862\n'
'Oceania,OC,Wallis and Futuna,WF,WLF,876\n'
'Oceania,OC,"Samoa, Independent State of",WS,WSM,882\n'
'Asia,AS,Yemen,YE,YEM,887\n'
'Africa,AF,"Zambia, Republic of",ZM,ZMB,894\n'
'Oceania,OC,Disputed Territory,XX,,\n'
'Asia,AS,Iraq-Saudi Arabia Neutral Zone,XE,,\n'
'Asia,AS,United Nations Neutral Zone,XD,,\n'
'Asia,AS,Spratly Islands,XS,,\n'
)

'''
US states, districts, and outlying areas
The fields are:
contiguous_usa, category, code, name
'''
US_STATES_CSV = (
'True,state,AL,Alabama\n'
'False,state,AK,Alaska\n'
'False,"outlying area",AS,"American Samoa"\n' #see also separate country code entry under AS.
'True,state,AZ,Arizona\n'
'True,state,AR,Arkansas\n'
'True,state,CA,California\n'
'True,state,CO,Colorado\n'
'True,state,CT,Connecticut\n'
'True,state,DE,Delaware\n'
'True,district,DC,"District of Columbia"\n'
'True,state,FL,Florida\n'
'True,state,GA,Georgia\n'
'False,"outlying area",GU,Guam\n' # See also separate country code entry under GU.
'False,state,HI,Hawaii\n'
'True,state,ID,Idaho\n'
'True,state,IL,Illinois\n'
'True,state,IN,Indiana\n'
'True,state,IA,Iowa\n'
'True,state,KS,Kansas\n'
'True,state,KY,Kentucky\n'
'True,state,LA,Louisiana\n'
'True,state,ME,Maine\n'
'True,state,MD,Maryland\n'
'True,state,MA,Massachusetts\n'
'True,state,MI,Michigan\n'
'True,state,MN,Minnesota\n'
'True,state,MS,Mississippi\n'
'True,state,MO,Missouri\n'
'True,state,MT,Montana\n'
'True,state,NE,Nebraska\n'
'True,state,NV,Nevada\n'
'True,state,NH,"New Hampshire"\n'
'True,state,NJ,"New Jersey"\n'
'True,state,NM,"New Mexico"\n'
'True,state,NY,"New York"\n'
'True,state,NC,"North Carolina"\n'
'True,state,ND,"North Dakota"\n'
'False,"outlying area",MP,"Northern Mariana Islands"\n' # See also separate country code entry under MP.
'True,state,OH,Ohio\n'
'True,state,OK,Oklahoma\n'
'True,state,OR,Oregon\n'
'True,state,PA,Pennsylvania\n'
'False,"outlying area",PR,"Puerto Rico"\n' # See also separate country code entry under PR.
'True,state,RI,"Rhode Island"\n'
'True,state,SC,"South Carolina"\n'
'True,state,SD,"South Dakota"\n'
'True,state,TN,Tennessee\n'
'True,state,TX,Texas\n'
'False,"outlying area",UM,"United States Minor Outlying Islands"\n' # See also separate country code entry under UM.
'True,state,UT,Utah\n'
'True,state,state,VT,Vermont\n'
'False,"outlying area",VI,"Virgin Islands, U.S."\n' # See also separate country code entry under VI.
'True,state,VA,Virginia\n'
'True,state,WA,Washington\n'
'True,state,WV,"West Virginia"\n'
'True,state,WI,Wisconsin\n'
'True,state,WY,Wyoming\n'
)


def parse_world_csv(world_csv):
    country_record = []
    file_handle = StringIO(world_csv)
    reader = csv.reader(file_handle, delimiter=',')
    for row in reader:
        country_record.append(row)
    return country_record


def parse_us_states_csv(us_state_csv):
    state_record = []
    file_handle = StringIO(us_state_csv)
    reader = csv.reader(file_handle, delimiter=',', dialect='excel')
    for row in reader:
        row[0] = row[0] == 'True'
        state_record.append(row)
    return state_record


class World(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = 'Earth'
        self.continents = dict()
       
    def __repr__(self):
        return 'World: ' + str(self.name)

    def __eq__(self, other):
        if not isinstance(other, World):
            return False
        return other.name == self.name
            
    def __ne__(self, other):
        if not isinstance(other, World):
            return False
        return other.name != self.name
        
    def add_continent(self, continent):
        key = continent.code
        self.continents[key] = continent

    @staticmethod
    def build():
        world = World()
        country_records = parse_world_csv(WORLD_CSV)
        for country_record in country_records:

            continent_name = country_record[0]
            continent_code = country_record[1]
            continent = Continent(continent_name, continent_code)
            
            country_name = country_record[2]
            country_code_2 = country_record[3]
            country_code_3 = country_record[4]
            number_str = country_record[5]
            country_number = int(number_str) if number_str != '' else 0
            country = Country(country_name, country_code_2, country_code_3, country_number)
            
            if country_code_2 == 'US':
                state_records = parse_us_states_csv(US_STATES_CSV)
                for state_record in state_records:
                    is_contiguous = state_record[0]
                    state_category = state_record[1]
                    state_code = state_record[2]
                    state_name = state_record[3]
                    state = State(state_name, state_code, is_contiguous, state_category)
                    country.add_state(state)

            continent.add_country(country)            
            world.add_continent(continent)
        return world

# Modules are singletons, so this global shold be also.
WORLD = World.build()
    
    