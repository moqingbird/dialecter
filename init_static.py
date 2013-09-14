import pymongo
from pymongo import MongoClient
from MongoConnection import MongoConnection

db=MongoConnection().get().dialect_db
db.parameters.save({"name":"n", "value":3})
db.parameters.save({"name":"k", "value":10})
db.parameters.save({"classification_threshold","value":0})
publications={}

publications[1]={"_id":"REDDIT","name":"Reddit","url":"http://www.reddit.com","read_robots":False}
publications[2]={"_id":"DECTE","name":"The Diachronic Electronic Corpus of Tyneside English", "url":"http://research.ncl.ac.uk/decte/corpusfiles/dectefiles.htm", "read_robots":False}
publications[3]={"_id":"TWITTER","name":"Twitter", "url":None, "read_robots": False}

for i in publications:
    db.publications.save(publications[i])

regions={}
regions[1]={"_id":"BRI","name":"British Isles"}
regions[2]={"_id":"GBR","name":"Great Britain","parent_id":"BRI"}
regions[3]={"_id":"ENG","name":"England", "parent_id":"GBR"}
regions[4]={"_id":"SCO","name":"Scotland", "parent_id":"GBR"}
regions[5]={"_id":"WAL","name":"Wales", "parent_id":"GBR"}
regions[6]={"_id":"IRE","name":"Ireland", "parent_id":"BRI"}
regions[7]={"_id":"NI","name":"Northern Ireland", "parent_id":"IRE"}
regions[8]={"_id":"EIRE","name":"Irish Republic", "parent_id":"IRE"}
regions[9]={"_id":"CHI","name":"Channel Islands", "parent_id":"BRI"}
regions[10]={"_id":"JER","name":"Jersey", "parent_id":"CHI"}
regions[11]={"_id":"GUER","name":"Guernsey", "parent_id":"CHI"}
regions[12] = {"_id": "HI_SCO","name": "Highlands","parent_id": "SCO"}
regions[13] = {"_id": "SCI","name": "Scottish Isles","parent_id": "HI"}
regions[14] = {"_id": "ORK","name": "Orkney","parent_id": "SCI"}
regions[15] = {"_id": "SHET","name": "Shetland","parent_id": "SCI"}
regions[16] = {"_id": "CAITH","name": "Caithness","parent_id": "HI"}
regions[17] = {"_id": "NO_SCO","name": "Northern Scots","parent_id": "SCO"}
regions[18] = {"_id": "NE_SCO","name": "North East Scots","parent_id": "NO_SCO"}
regions[19] = {"_id": "ABN","name": "Aberdeen","parent_id": "NE_SCO"}
regions[20] = {"_id": "INV","name": "Inverness","parent_id": "NE_SCO"}
regions[21] = {"_id": "EA_SCO","name": "East Angus","parent_id": "NO_SCO"}
regions[22] = {"_id": "LO_SCO","name": "Lowland Scots","parent_id": "SCO"}
regions[23] = {"_id": "CEN_SCO","name": "Central Scots","parent_id": "LO_SCO"}
regions[24] = {"_id": "WC_SCO","name": "West Central Scots","parent_id": "CEN_SCO"}
regions[25] = {"_id": "EKIL","name": "East Kilbride","parent_id": "WC_SCO"}
regions[26] = {"_id": "GLAS","name": "Glasgow","parent_id": "WC_SCO"}
regions[27] = {"_id": "ECN_SCO","name": "East Central North Scots","parent_id": "CEN_SCO"}
regions[28] = {"_id": "DUND","name": "Dundee","parent_id": "ECN_SCO"}
regions[29] = {"_id": "STAN","name": "St Andrews","parent_id": "ECN_SCO"}
regions[30] = {"_id": "EC_SCO","name": "East Central Scots","parent_id": "CEN_SCO"}
regions[31] = {"_id": "EDB","name": "Edinburgh","parent_id": "EC_SCO"}
regions[32] = {"_id": "SC_SCO","name": "South Central Scots","parent_id": "CEN_SCO"}
regions[33] = {"_id": "SO_SCO","name": "Southern Scots","parent_id": "SCO"}
regions[34] = {"_id": "MIDU","name": "Mid Ulster English","parent_id": "NI"}
regions[35] = {"_id": "BELF","name": "Belfast","parent_id": "MIDU"}
regions[36] = {"_id": "DERRY","name": "Derry","parent_id": "MIDU"}
regions[37] = {"_id": "ULS","name": "Ulster Scots","parent_id": "IRE"}
regions[38] = {"_id": "EIRE","name": "Republic of Ireland","parent_id": "IRE"}
regions[39] = {"_id": "BOR_IRE","name": "Irish Border","parent_id": "EIRE"}
regions[40] = {"_id": "SO_ULS","name": "South Ulster","parent_id": "EIRE"}
regions[41] = {"_id": "EA_IRE","name": "East Irelend","parent_id": "EIRE"}
regions[42] = {"_id": "DUB","name": "Dublin","parent_id": "EA_IRE"}
regions[43] = {"_id": "SE_IRE","name": "South East Ireland","parent_id": "EIRE"}
regions[44] = {"_id": "WATER","name": "Waterford","parent_id": "SE_IRE"}
regions[45] = {"_id": "WE_IRE","name": "West Ireland","parent_id": "EIRE"}
regions[46] = {"_id": "GAL","name": "Galway","parent_id": "WE_IRE"}
regions[47] = {"_id": "SLI","name": "Sligo","parent_id": "WE_IRE"}
regions[48] = {"_id": "MID_IRE","name": "Irish Midlands","parent_id": "EIRE"}
regions[49] = {"_id": "SW_IRE","name": "South West Ireland","parent_id": "EIRE"}
regions[50] = {"_id": "LIM","name": "Limerick","parent_id": "SW_IRE"}
regions[51] = {"_id": "COR","name": "Cork","parent_id": "SW_IRE"}
regions[52] = {"_id": "DON","name": "Donegal","parent_id": "EIRE"}
regions[53] = {"_id": "ABR","name": "Aberystwtyh","parent_id": "WAL"}
regions[54] = {"_id": "SO_WAL","name": "South Wales","parent_id": "WAL"}
regions[55] = {"_id": "CAR","name": "Cardiff","parent_id": "SO_WAL"}
regions[56] = {"_id": "GOW","name": "Gower","parent_id": "SO_WAL"}
regions[57] = {"_id": "NO_ENG","name": "Northern England","parent_id": "ENG"}
regions[58] = {"_id": "CHE","name": "Cheshire","parent_id": "NO_ENG"}
regions[59] = {"_id": "CHES","name": "Chester","parent_id": "CHE"}
regions[60] = {"_id": "CUMB","name": "Cumbria","parent_id": "NO_ENG"}
regions[61] = {"_id": "TYN","name": "Tyneside","parent_id": "NO_ENG"}
regions[62] = {"_id": "NEWC","name": "Newcastle","parent_id": "TYN"}
regions[63] = {"_id": "LAN","name": "Lancashire","parent_id": "NO_ENG"}
regions[64] = {"_id": "LANC","name": "Lancaster","parent_id": "LAN"}
regions[65] = {"_id": "WIG","name": "Wigan","parent_id": "LAN"}
regions[66] = {"_id": "PRES","name": "Preston","parent_id": "LAN"}
regions[67] = {"_id": "SUND","name": "Sunderland","parent_id": "NO_ENG"}
regions[68] = {"_id": "MANC","name": "Manchester","parent_id": "NO_ENG"}
regions[69] = {"_id": "NTHU","name": "Northumberland","parent_id": "NO_ENG"}
regions[70] = {"_id": "LVP","name": "Liverpool","parent_id": "NO_ENG"}
regions[71] = {"_id": "TEE","name": "Teeside","parent_id": "NO_ENG"}
regions[72] = {"_id": "YRK","name": "Yorkshire","parent_id": "NO_ENG"}
regions[73] = {"_id": "LEED","name": "Leeds","parent_id": "YRK"}
regions[74] = {"_id": "YORK","name": "York","parent_id": "YRK"}
regions[75] = {"_id": "SHEF","name": "Sheffield","parent_id": "YRK"}
regions[76] = {"_id": "HARR","name": "Harrogate","parent_id": "YRK"}
regions[77] = {"_id": "BRAD","name": "Bradford","parent_id": "YRK"}
regions[78] = {"_id": "HULL","name": "Hull","parent_id": "YRK"}
regions[79] = {"_id": "EA_ANG","name": "East Anglia","parent_id": "ENG"}
regions[80] = {"_id": "NORF","name": "Norfolk","parent_id": "EA_ANG"}
regions[81] = {"_id": "NORW","name": "Norwich","parent_id": "NORF"}
regions[82] = {"_id": "SUFF","name": "Suffolk","parent_id": "EA_ANG"}
regions[83] = {"_id": "IPS","name": "Ipswitch","parent_id": "SUFF"}
regions[84] = {"_id": "SE_ENG","name": "South East England","parent_id": "ENG"}
regions[85] = {"_id": "ESX","name": "Essex","parent_id": "SE_ENG"}
regions[86] = {"_id": "EST","name": "Thames Estuary","parent_id": "SE_ENG"}
regions[87] = {"_id": "READ","name": "Reading","parent_id": "EST"}
regions[88] = {"_id": "KENT","name": "Kent","parent_id": "SE_ENG"}
regions[89] = {"_id": "RAMS","name": "Ramsgate","parent_id": "KENT"}
regions[90] = {"_id": "ASH","name": "Ashford","parent_id": "KENT"}
regions[91] = {"_id": "CANT","name": "Canterbury","parent_id": "KENT"}
regions[92] = {"_id": "SUSX","name": "Sussex","parent_id": "SE_ENG"}
regions[93] = {"_id": "BRGT","name": "Brighton","parent_id": "SUSX"}
regions[94] = {"_id": "ISLW","name": "Isle of Wight","parent_id": "SE_ENG"}
regions[95] = {"_id": "PORT","name": "Portsmouth","parent_id": "SE_ENG"}
regions[96] = {"_id": "SURY","name": "Surrey","parent_id": "SE_ENG"}
regions[97] = {"_id": "OXF","name": "Oxford","parent_id": "SE_ENG"}
regions[98] = {"_id": "MILK","name": "Milton Keynes","parent_id": "SE_ENG"}
regions[99] = {"_id": "WE_ENG","name": "West Country (England)","parent_id": "ENG"}
regions[100] = {"_id": "DEV","name": "Devon","parent_id": "WE_ENG"}
regions[101] = {"_id": "EXE","name": "Exeter","parent_id": "DEV"}
regions[102] = {"_id": "CORN","name": "Cornwall","parent_id": "WE_ENG"}
regions[103] = {"_id": "FALM","name": "Falmouth","parent_id": "CORN"}
regions[104] = {"_id": "BRIS","name": "Bristol","parent_id": "WE_ENG"}
regions[105] = {"_id": "DORS","name": "Dorset","parent_id": "WE_ENG"}
regions[106] = {"_id": "BRNM","name": "Bournemouth","parent_id": "DORS"}
regions[107] = {"_id": "POOL","name": "Poole","parent_id": "DORS"}
regions[108] = {"_id": "BATH","name": "Bath","parent_id": "WE_ENG"}
regions[109] = {"_id": "GLOS","name": "Gloucestershire","parent_id": "WE_ENG"}
regions[110] = {"_id": "SWIN","name": "Swindon","parent_id": "WE_ENG"}
regions[111] = {"_id": "SOUTH","name": "Southampton","parent_id": "ENG"}
regions[112] = {"_id": "MID_ENG","name": "English Midlands","parent_id": "ENG"}
regions[113] = {"_id": "EMID_ENG","name": "East Midlands","parent_id": "MID_ENG"}
regions[114] = {"_id": "GRIM","name": "Grimsby","parent_id": "EMID_ENG"}
regions[115] = {"_id": "LINC","name": "Lincolnshire","parent_id": "EMID_ENG"}
regions[116] = {"_id": "DERB","name": "Derbyshire","parent_id": "EMID_ENG"}
regions[117] = {"_id": "NHMP","name": "Northamptonshire","parent_id": "EMID_ENG"}
regions[118] = {"_id": "NTHM","name": "Notthingham","parent_id": "EMID_ENG"}
regions[119] = {"_id": "LEIC","name": "Leicester","parent_id": "EMID_ENG"}
regions[120] = {"_id": "WMID_ENG","name": "West Midlands","parent_id": "MID_ENG"}
regions[121] = {"_id": "BLKC","name": "Black Country","parent_id": "WMID_ENG"}
regions[122] = {"_id": "BRUM","name": "Birmingham","parent_id": "WMID_ENG"}
regions[123] = {"_id": "STAFF","name": "Staffordshire","parent_id": "WMID_ENG"}
regions[124] = {"_id": "TELF","name": "Telford","parent_id": "WMID_ENG"}
regions[125] = {"_id": "SHROP","name": "Shropshire","parent_id": "TELF"}
regions[126] = {"_id": "COVN","name": "Coventry","parent_id": "WMID_ENG"}
regions[127] = {"_id": "CHI","name": "Channel Islands","parent_id": "BRI"}
regions[128] = {"_id": "GUER","name": "Guernsey","parent_id": "CHI"}
regions[129] = {"_id": "JER","name": "Jersey","parent_id": "CHI"}
regions[130] = {"_id": "MANX","name": "Isle of Man","parent_id": "BRI"}
regions[131] = {"_id": "SWAN","name": "Swansea","parent_id": "GOW"}

for i in regions:
    db.regions.save(regions[i])

region_pubs = {}

region_pubs[1] = {"_id": "/r/aberdeen", "publication": "REDDIT", "region": "ABN","url":"/r/aberdeen/new/.rss?sort=new"}
region_pubs[2] = {"_id": "/r/aberystwyth", "publication": "REDDIT", "region": "ABR","url":"/r/aberystwyth/new/.rss?sort=new"}
region_pubs[3] = {"_id": "/r/AshfordKent", "publication": "REDDIT", "region": "ASH","url":"/r/AshfordKent/new/.rss?sort=new"}
region_pubs[4] = {"_id": "/r/bath", "publication": "REDDIT", "region": "BATH","url":"/r/bath/new/.rss?sort=new"}
region_pubs[5] = {"_id": "/r/belfast", "publication": "REDDIT", "region": "BELF","url":"/r/belfast/new/.rss?sort=new"}
region_pubs[6] = {"_id": "/r/brum", "publication": "REDDIT", "region": "BRUM","url":"/r/brum/new/.rss?sort=new"}
region_pubs[7] = {"_id": "/r/theblackcountry", "publication": "REDDIT", "region": "BLKC","url":"/r/theblackcountry/new/.rss?sort=new"}
region_pubs[9] = {"_id": "/r/bradford", "publication": "REDDIT", "region": "BRAD","url":"/r/bradford/new/.rss?sort=new"}
region_pubs[10] = {"_id": "/r/brighton", "publication": "REDDIT", "region": "BRGT","url":"/r/brighton/new/.rss?sort=new"}
region_pubs[11] = {"_id": "/r/bristol", "publication": "REDDIT", "region": "BRIS","url":"/r/bristol/new/.rss?sort=new"}
region_pubs[12] = {"_id": "/r/canterbury", "publication": "REDDIT", "region": "CANT","url":"/r/canterbury/new/.rss?sort=new"}
region_pubs[13] = {"_id": "/r/Cardiff", "publication": "REDDIT", "region": "CAR","url":"/r/Cardiff/new/.rss?sort=new"}
region_pubs[14] = {"_id": "/r/channelislands", "publication": "REDDIT", "region": "CHI","url":"/r/channelislands/new/.rss?sort=new"}
region_pubs[15] = {"_id": "/r/cheshire", "publication": "REDDIT", "region": "CHE","url":"/r/cheshire/new/.rss?sort=new"}
region_pubs[16] = {"_id": "/r/chester", "publication": "REDDIT", "region": "CHES","url":"/r/chester/new/.rss?sort=new"}
region_pubs[17] = {"_id": "/r/cork", "publication": "REDDIT", "region": "COR","url":"/r/cork/new/.rss?sort=new"}
region_pubs[18] = {"_id": "/r/Cornwall", "publication": "REDDIT", "region": "CORN","url":"/r/Cornwall/new/.rss?sort=new"}
region_pubs[19] = {"_id": "/r/Kernow", "publication": "REDDIT", "region": "CORN","url":"/r/Kernow/new/.rss?sort=new"}
region_pubs[20] = {"_id": "/r/coventry", "publication": "REDDIT", "region": "COVN","url":"/r/coventry/new/.rss?sort=new"}
region_pubs[21] = {"_id": "/r/cumbria", "publication": "REDDIT", "region": "CUMB","url":"/r/cumbria/new/.rss?sort=new"}
region_pubs[22] = {"_id": "/r/derbyshire", "publication": "REDDIT", "region": "DERB","url":"/r/derbyshire/new/.rss?sort=new"}
region_pubs[23] = {"_id": "/r/DerryLondonderry", "publication": "REDDIT", "region": "DERRY","url":"/r/DerryLondonderry/new/.rss?sort=new"}
region_pubs[24] = {"_id": "/r/devonuk", "publication": "REDDIT", "region": "DEV","url":"/r/devonuk/new/.rss?sort=new"}
region_pubs[25] = {"_id": "/r/Donegal", "publication": "REDDIT", "region": "DON","url":"/r/Donegal/new/.rss?sort=new"}
region_pubs[26] = {"_id": "/r/Dorset", "publication": "REDDIT", "region": "DORS","url":"/r/Dorset/new/.rss?sort=new"}
region_pubs[27] = {"_id": "/r/Dublin", "publication": "REDDIT", "region": "DUB","url":"/r/Dublin/new/.rss?sort=new"}
region_pubs[28] = {"_id": "/r/dundee", "publication": "REDDIT", "region": "DUND","url":"/r/dundee/new/.rss?sort=new"}
region_pubs[29] = {"_id": "/r/EastAnglia", "publication": "REDDIT", "region": "EA_ANG","url":"/r/EastAnglia/new/.rss?sort=new"}
region_pubs[30] = {"_id": "/r/eastkilbride", "publication": "REDDIT", "region": "EKIL","url":"/r/eastkilbride/new/.rss?sort=new"}
region_pubs[31] = {"_id": "/r/Edinburgh", "publication": "REDDIT", "region": "EDB","url":"/r/Edinburgh/new/.rss?sort=new"}
region_pubs[32] = {"_id": "/r/midlands", "publication": "REDDIT", "region": "MID_ENG","url":"/r/midlands/new/.rss?sort=new"}
region_pubs[33] = {"_id": "/r/Essex", "publication": "REDDIT", "region": "ESX","url":"/r/Essex/new/.rss?sort=new"}
region_pubs[34] = {"_id": "/r/Exeter", "publication": "REDDIT", "region": "EXE","url":"/r/Exteer/new/.rss?sort=new"}
region_pubs[35] = {"_id": "/r/Falmouth", "publication": "REDDIT", "region": "FALM","url":"/r/Falmouth/new/.rss?sort=new"}
region_pubs[36] = {"_id": "/r/galway", "publication": "REDDIT", "region": "GAL","url":"/r/galway/new/.rss?sort=new"}
region_pubs[37] = {"_id": "/r/galwayevents", "publication": "REDDIT", "region": "GAL","url":"/r/galwayevents/new/.rss?sort=new"}
region_pubs[38] = {"_id": "/r/glasgow", "publication": "REDDIT", "region": "GLAS","url":"/r/glasgow/new/.rss?sort=new"}
region_pubs[39] = {"_id": "/r/gloucestershire", "publication": "REDDIT", "region": "GLOS","url":"/r/gloucestershire/new/.rss?sort=new"}
region_pubs[40] = {"_id": "/r/Grimsby", "publication": "REDDIT", "region": "GRIM","url":"/r/Grimsby/new/.rss?sort=new"}
region_pubs[41] = {"_id": "/r/guernsey", "publication": "REDDIT", "region": "GUER","url":"/r/guernsey/new/.rss?sort=new"}
region_pubs[42] = {"_id": "/r/harrogate", "publication": "REDDIT", "region": "HARR","url":"/r/harrogate/new/.rss?sort=new"}
region_pubs[43] = {"_id": "/r/Hull", "publication": "REDDIT", "region": "HULL","url":"/r/Hull/new/.rss?sort=new"}
region_pubs[44] = {"_id": "/r/inverness", "publication": "REDDIT", "region": "INV","url":"/r/inverness/new/.rss?sort=new"}
region_pubs[45] = {"_id": "/r/IpswichUK", "publication": "REDDIT", "region": "IPS","url":"/r/IpswichUK/new/.rss?sort=new"}
region_pubs[46] = {"_id": "/r/IsleofMan", "publication": "REDDIT", "region": "MANX","url":"/r/IsleofMan/new/.rss?sort=new"}
region_pubs[47] = {"_id": "/r/isleofwight", "publication": "REDDIT", "region": "ISLW","url":"/r/isleofwight/new/.rss?sort=new"}
region_pubs[48] = {"_id": "/r/BritishKent", "publication": "REDDIT", "region": "KENT","url":"/r/BritishKent/new/.rss?sort=new"}
region_pubs[49] = {"_id": "/r/Thanet", "publication": "REDDIT", "region": "KENT","url":"/r/Thanet/new/.rss?sort=new"}
region_pubs[50] = {"_id": "/r/lancaster_uk", "publication": "REDDIT", "region": "LANC","url":"/r/lancaster_uk/new/.rss?sort=new"}
region_pubs[51] = {"_id": "/r/RUG_leeds", "publication": "REDDIT", "region": "LEED","url":"/r/RUG_leeds/new/.rss?sort=new"}
region_pubs[52] = {"_id": "/r/leicester", "publication": "REDDIT", "region": "LEIC","url":"/r/leicester/new/.rss?sort=new"}
region_pubs[53] = {"_id": "/r/limerickcity", "publication": "REDDIT", "region": "LIM","url":"/r/limerickcity/new/.rss?sort=new"}
region_pubs[54] = {"_id": "/r/Lincolnshire", "publication": "REDDIT", "region": "LINC","url":"/r/Lincolnshire/new/.rss?sort=new"}
region_pubs[55] = {"_id": "/r/Liverpool", "publication": "REDDIT", "region": "LVP","url":"/r/Liverpool/new/.rss?sort=new"}
region_pubs[56] = {"_id": "/r/manchester", "publication": "REDDIT", "region": "MANC","url":"/r/manchester/new/.rss?sort=new"}
region_pubs[57] = {"_id": "/r/miltonkeynes", "publication": "REDDIT", "region": "MILK","url":"/r/miltonkeynes/new/.rss?sort=new"}
region_pubs[58] = {"_id": "/r/NewcastleUponTyne", "publication": "REDDIT", "region": "NEWC","url":"/r/NewcastleUponTyne/new/.rss?sort=new"}
region_pubs[59] = {"_id": "/r/northamptonians", "publication": "REDDIT", "region": "NHMP","url":"/r/northamptonians/new/.rss?sort=new"}
region_pubs[60] = {"_id": "/r/northernireland", "publication": "REDDIT", "region": "NI","url":"/r/northernireland/new/.rss?sort=new"}
region_pubs[61] = {"_id": "/r/Norwich", "publication": "REDDIT", "region": "NORW","url":"/r/Norwich/new/.rss?sort=new"}
region_pubs[62] = {"_id": "/r/nottingham", "publication": "REDDIT", "region": "NTHM","url":"/r/nottingham/new/.rss?sort=new"}
region_pubs[63] = {"_id": "/r/orkney", "publication": "REDDIT", "region": "ORK","url":"/r/orkney/new/.rss?sort=new"}
region_pubs[64] = {"_id": "/r/oxford", "publication": "REDDIT", "region": "OXF","url":"/r/oxford/new/.rss?sort=new"}
region_pubs[65] = {"_id": "/r/poole", "publication": "REDDIT", "region": "POOL","url":"/r/poole/new/.rss?sort=new"}
region_pubs[66] = {"_id": "/r/Portsmouth", "publication": "REDDIT", "region": "PORT","url":"/r/Portsmouth/new/.rss?sort=new"}
region_pubs[67] = {"_id": "/r/Preston", "publication": "REDDIT", "region": "PRES","url":"/r/Preston/new/.rss?sort=new"}
region_pubs[68] = {"_id": "/r/Ramsgate", "publication": "REDDIT", "region": "RAMS","url":"/r/Ramsgate/new/.rss?sort=new"}
region_pubs[69] = {"_id": "/r/Reading_Berkshire", "publication": "REDDIT", "region": "READ","url":"/r/Reading_Berkshire/new/.rss?sort=new"}
region_pubs[70] = {"_id": "/r/RofI", "publication": "REDDIT", "region": "EIRE","url":"/r/RofI/new/.rss?sort=new"}
region_pubs[71] = {"_id": "/r/ireland", "publication": "REDDIT", "region": "EIRE","url":"/r/ireland/new/.rss?sort=new"}
region_pubs[72] = {"_id": "/r/scotland", "publication": "REDDIT", "region": "SCO","url":"/r/scotland/new/.rss?sort=new"}
region_pubs[73] = {"_id": "/r/Sheffield", "publication": "REDDIT", "region": "SHEF","url":"/r/Sheffield/new/.rss?sort=new"}
region_pubs[74] = {"_id": "/r/shetland", "publication": "REDDIT", "region": "SHET","url":"/r/shetland/new/.rss?sort=new"}
region_pubs[75] = {"_id": "/r/Shropshire", "publication": "REDDIT", "region": "SHROP","url":"/r/Shropshire/new/.rss?sort=new"}
region_pubs[76] = {"_id": "/r/Sligo", "publication": "REDDIT", "region": "SLI","url":"/r/Sligo/new/.rss?sort=new"}
region_pubs[77] = {"_id": "/r/SouthEast", "publication": "REDDIT", "region": "SE_IRE","url":"/r/SouthEast/new/.rss?sort=new"}
region_pubs[78] = {"_id": "/r/SunnySoutheast", "publication": "REDDIT", "region": "SE_IRE","url":"/r/SunnySoutheast/new/.rss?sort=new"}
region_pubs[79] = {"_id": "/r/southwales", "publication": "REDDIT", "region": "SO_WAL","url":"/r/southwales/new/.rss?sort=new"}
region_pubs[80] = {"_id": "/r/Southampton", "publication": "REDDIT", "region": "SOUTH","url":"/r/Southampton/new/.rss?sort=new"}
region_pubs[81] = {"_id": "/r/standrews", "publication": "REDDIT", "region": "STAN","url":"/r/standrews/new/.rss?sort=new"}
region_pubs[82] = {"_id": "/r/surrey", "publication": "REDDIT", "region": "SURY","url":"/r/surrey/new/.rss?sort=new"}
region_pubs[83] = {"_id": "/r/swansea", "publication": "REDDIT", "region": "SWAN","url":"/r/swansea/new/.rss?sort=new"}
region_pubs[84] = {"_id": "/r/swindon", "publication": "REDDIT", "region": "SWIN","url":"/r/swindon/new/.rss?sort=new"}
region_pubs[85] = {"_id": "/r/Teesside", "publication": "REDDIT", "region": "TEE","url":"/r/Teesside/new/.rss?sort=new"}
region_pubs[86] = {"_id": "/r/northeast", "publication": "REDDIT", "region": "TYN","url":"/r/northeast/new/.rss?sort=new"}
region_pubs[87] = {"_id": "/r/tyneside", "publication": "REDDIT", "region": "TYN","url":"/r/tyneside/new/.rss?sort=new"}
region_pubs[88] = {"_id": "/r/wales", "publication": "REDDIT", "region": "WAL","url":"/r/wales/new/.rss?sort=new"}
region_pubs[89] = {"_id": "/r/Wigan", "publication": "REDDIT", "region": "WIG","url":"/r/Wigan/new/.rss?sort=new"}
region_pubs[90] = {"_id": "/r/york", "publication": "REDDIT", "region": "YORK","url":"/r/york/new/.rss?sort=new"}
region_pubs[91] = {"_id": "/r/Yorkshire", "publication": "REDDIT", "region": "YRK","url":"/r/Yorkshire/new/.rss?sort=new"}
region_pubs[92] = {"_id": "/r/bournemouth", "publication": "REDDIT", "region": "BRNM","url":"/r/bournemouth/new/.rss?sort=new"}

for i in region_pubs:
    db.region_pubs.save(region_pubs[i])
