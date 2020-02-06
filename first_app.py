import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression

st.title('Welcome to BacteriAlert')

counties = ['Bay','Brevard','Broward','Charlotte','Citrus','Collier','Dade','Dixie','Duval','Escambia','Franklin','Gulf',
 'Hernando','Hillsborough', 'Indian River','Lee', 'Levy','Manatee','Martin', 'Monroe', 'Nassau','Okaloosa',
 'Palm Beach','Pasco','Pinellas','Santa Rosa','Sarasota','St Johns','St Lucie','Taylor','Volusia','Wakulla','Walton']

lists = [['BEACH DRIVE','BECKRICH RD','BID-A-WEE BEACH','CARL GRAY PARK','DELWOOD','DUPONT BRIDGE','EAST COUNTY LINE',
'LAGUNA BEACH','PCB CITY PIER','RICK SELTZER PARK','SPYGLASS DRIVE','WEST COUNTY LINE','SUNSET PARK'],
 ['COCOA BEACH PIER', 'JETTY PARK'],
 ['BAHIA MAR','GEORGE ENGLISH PARK','BIRCH STATE PARK','COMMERCIAL BLVD PIER','HALLANDALE BEACH BLVD','HARRISON STREET',
  'MINNESOTA STREET','NORTH BEACH PARK INTRACOASTAL','OAKLAND PARK BLVD','POMPANO BEACH PIER','VAN BUREN ST',
  'DEERFIELD BEACH PIER','HILLSBORO INLET PARK','NE 16TH ST POMPANO','CUSTER ST BEACH','DANIA BEACH',
  'DEERFIELD BEACH SE 10TH ST','SEBASTIAN STREET'],
 ['BOCA GRANDE','ENGLEWOOD MID BEACH','ENGLEWOOD NORTH','ENGLEWOOD SOUTH','PALM ISLAND NORTH','PALM ISLAND SOUTH',
  'PORT CHARLOTTE BEACH EAST','PORT CHARLOTTE BEACH WEST'],
 ['FORT ISLAND GULF BEACH'],
 ['CLAM PASS','DOCTORS PASS','LOWDERMILK PARK BEACH','NAPLES PIER','PARKSHORE BEACH','RESIDENCE BEACH','TIGERTAIL BEACH',
  'VANDERBILT BEACH','BAREFOOT BEACH PRESERVE','HIDEAWAY BEACH','CENTRAL AVENUE','PELICAN BAY RESTAURANT AND CLUB'],
 ['53RD ST - MIAMI BEACH','CAPE FLORIDA PARK','COLLINS PARK - 21ST ST','CRANDON PARK - KEY BISCAYNE','DOG BEACH',
  'GOLDEN BEACH','KEY BISCAYNE BEACH','MATHESON HAMMOCK','NORTH SHORE OCEAN TERRACE','OLETA STATE PARK','SOUTH BEACH PARK',
  'SUNNY ISLES BEACH - PIER PARK','SURFSIDE BEACH - 93RD ST','VIRGINIA BEACH','HAULOVER BEACH','SUNNY ISLES BEACH - PIER PARK ',
  'CRANDON PARK NORTH - KEY BISCAYNE','Crandon Park South','Haulover Beach - North','Sunny Isles Beach - Samson Park',
  'Crandon Park - South'],
 ['SHIRED ISLAND PARK'],
 ['15TH STREET  ACCESS','30TH AVE ACCESS','BEACH BLVD ACCESS','HOPKINS ST ACCESS'],
 ['BAY BLUFFS PARK',
  'BAYOU CHICO',
  'BAYVIEW PARK PIER',
  'BIG LAGOON STATE PARK',
  'COUNTY PARK',
  'FORT PICKENS',
  'JOHNSON BEACH',
  'NAVY POINT',
  'PENSACOLA BEACH',
  'PERDIDO KEY STATE PARK',
  'QUIET WATER BEACH',
  'SANDERS BEACH',
  'COUNTY PARK WEST',
  'JOHNSON BEACH- SOUND SIDE'],
 ['ALLIGATOR POINT',
  'CARRABELLE BEACH',
  'SAINT GEORGE ISLAND 11TH ST E',
  'SAINT GEORGE ISLAND 11TH ST W',
  'SAINT GEORGE ISLAND FRANKLIN BLVD',
  'Saint George Island State Park'],
 ['BEACON HILL BEACH',
  'DIXIE BELLE BEACH',
  'HIGHWAY 98 BEACH',
  'LOOKOUT BEACH',
  'ST. JOE BAY MONUMENT BEACH',
  'ST. JOE BEACH',
  'Cape Palms Public Access',
  'Sweet Water Shores'],
 ['PINE ISLAND BEACH'],
 ['BAHIA BEACH',
  'BEN T. DAVIS NORTH',
  'BEN T. DAVIS SOUTH',
  'DAVIS ISLAND BEACH',
  'PICNIC ISLAND NORTH',
  'PICNIC ISLAND SOUTH',
  'SIMMONS PARK BEACH',
  'CYPRESS POINT PARK NORTH',
  'CYPRESS POINT PARK SOUTH'],
 ['COCONUT POINT SEBASTIAN INLET',
  'HUMISTON BEACH OUTFLOW',
  'SEXTON PLAZA OUTFLOW',
  'SOUTH BEACH PARK'],
 ['BLIND PASS/TURNER BEACH',
  'BOCA GRANDE SEA GRAPE #2',
  'BONITA BEACH PARK',
  'BOWDITCH PARK',
  'BOWMANS BEACH',
  'CAPE CORAL YACHT CLUB',
  'LIGHTHOUSE BEACH',
  'LOVERS KEY STATE PARK',
  'LYNN HALL PARK',
  'SANIBEL CAUSEWAY',
  'SOUTH SEAS PLANTATION',
  'TARPON BAY BEACH'],
 ['CEDAR KEY PARK'],
 ['BAYFRONT PARK NORTH',
  'BAYFRONT PARK SOUTH',
  'BRADENTON  BEACH',
  'COQUINA  BEACH NORTH',
  'MANATEE PUBLIC BEACH NORTH',
  'MANATEE PUBLIC BEACH SOUTH',
  'PALMA SOLA NORTH',
  'PALMA SOLA SOUTH'],
 ['BATHTUB PUBLIC BEACH',
  'HOBE SOUND PUBLIC BEACH',
  'HOBE SOUND WILDLIFE REFUGE',
  'JENSEN PUBLIC BEACH',
  'ROOSEVELT BRIDGE',
  'STUART CAUSEWAY',
  'STUART PUBLIC BEACH',
  'BOB GRAHAM BEACH'],
 ["ANNE'S BEACH",
  'BAHIA HONDA BAYSIDE',
  'BAHIA HONDA OCEANSIDE',
  'BAHIA HONDA SANDSPUR',
  'COCO PLUM BEACH',
  'CURRY HAMMOCK STATE PARK',
  'FT ZACHARY TAYLOR STATE PARK',
  'HARRY HARRIS COUNTY PARK',
  'HIGGS BEACH',
  'ISLAMORADA LIBRARY BEACH',
  'JOHN PENNEKAMP STATE PARK',
  'SMATHERS BEACH',
  'SOMBRERO BEACH',
  "VETERAN'S BEACH",
  'FOUNDER',
  'SIMONTON STREET BEACH',
  'SOUTH BEACH',
  'SOUTH BEACH '],
 ['AIP BEACH CLUB',
  'AMERICAN BEACH',
  'MAIN BEACH',
  'OCEAN STREET',
  "PETER'S POINT",
  'PIPER DUNES',
  'SADLER ROAD',
  'SOUTH END',
  'JASMINE STREET'],
 ['EAST PASS',
  'GARNIERS PARK',
  'GULF ISLAND NATIONAL SEASHORE',
  'HENDERSON PARK BEACH',
  'JAMES LEE PARK',
  'LIZA JACKSON PARK',
  'MARLER PARK',
  'ROCKY BAYOU STATE PARK',
  'WAYSIDE PARK',
  'CAMP TIMPOOCHEE',
  'LINCOLN PARK',
  'POQUITO PARK',
  'Emerald Promenade',
  'Clement E. Taylor Park',
  'Brackin WAYSIDE PARK'],
 ['DUBOIS PARK',
  'JUPITER BEACH PARK',
  'LAKE WORTH BEACH',
  'OCEAN INLET PARK',
  'PEANUT ISLAND',
  'PHIL FOSTER PARK',
  'RIVIERA MUNICIPAL BEACH',
  'SANDOWAY PARK',
  'SOUTH INLET PARK',
  'BOYNTON BEACH',
  'CARLIN PARK',
  'GULFSTREAM',
  'PALM BEACH',
  'SPANISH RIVER',
  'Lantana Municipal Beach'],
 ['ANCLOTE RIVER PARK BEACH',
  'BRASHER PARK BEACH',
  'ENERGY AND MARINE CENTER',
  'GULF HARBORS BEACH',
  'OELSNER PARK BEACH',
  'ROBERT J STRICKLAND BEACH',
  'ROBERT K. REES PARK BEACH'],
 ['BELLEAIR CAUSEWAY-INTERCOASTAL BEACH',
  'COURTNEY CAMPBELL CAUSEWAY',
  'FORT DESOTO NORTH BEACH',
  'FRED HOWARD BEACH',
  'GANDY BOULEVARD',
  'HONEYMOON ISLAND BEACH',
  'INDIAN ROCKS BEACH',
  'INDIAN SHORES BEACH',
  'MADEIRA BEACH',
  'NORTH SHORE BEACH',
  'PASS-A-GRILLE BEACH',
  'R. E. OLDS PARK',
  'SAND KEY',
  'TREASURE ISLAND BEACH',
  'Mobbly Bayou Preserve',
  'Redington Shores - 182nd Ave.',
  'Sunset Beach - Tarpon Springs'],
 ['NAVARRE BEACH PIER',
  'NAVARRE PARK HIGHWAY 98',
  'SHORELINE PARK',
  'WOODLAWN BEACH',
  "JUANA'S BEACH"],
 ['BLIND PASS BEACH',
  'CASPERSEN BEACH',
  'LIDO CASINO BEACH',
  'LONGBOAT KEY ACCESS',
  'MANASOTA KEY BEACH',
  'NOKOMIS BEACH',
  'NORTH JETTY BEACH',
  'NORTH LIDO BEACH',
  'SERVICE CLUB BEACH',
  'SIESTA KEY BEACH',
  'TURTLE BEACH',
  'VENICE BEACH',
  'SOUTH LIDO BEACH',
  'BROHARD PARK',
  'RINGLING CAUSEWAY',
  'VENICE FISHING PIER',
  'Bird Key Park  a.k.a RINGLING CAUSEWAY'],
 ['CRESCENT BEACH',
  "MICKLER'S LANDING",
  'SOLANA RD',
  'VILANO BEACH',
  'MATANZAS INLET '],
 ['JETTY PARK BEACH',
  'PEPPER PARK',
  'WALTON ROCKS BEACH',
  'FREDERICK DOUGLASS MEMORIAL PARK',
  'South Beach Causeway',
  'Jaycee Park'],
 ['CEDAR BEACH', 'DEKLE BEACH', 'KEATON BEACH', 'HAGENS COVE'],
 ['27TH STREET',
  'DUNLAWTON',
  'FLAGLER AVE',
  'FLORIDA SHORES BLVD',
  'GRANDA BLVD',
  'MAIN STREET',
  'SEABREEZE BLVD',
  'SILVER BEACH',
  'TORONITA',
  'NORTH JETTY',
  'OCEANVIEW WAY',
  'INTERNATIONAL SPEEDWAY',
  'GRANADA BLVD'],
 ["MASH'S ISLAND", 'SHELL POINT'],
 ['BLUE MOUNTAIN BEACH',
  'COUNTY PARK',
  'DUNE ALLEN BEACH',
  'EASTERN LAKE DUNE WALKOVER',
  'GRAYTON BEACH',
  'HOLLEY STREET BEACH',
  'CHOCTAW BEACH COUNTY PARK',
  'INLET BEACH ACCESS',
  'WHEELER POINT']]

county = st.selectbox('Please select a county:', counties)

beaches = lists[counties.index(county)]

beach = st.selectbox('Now please select a location: ', beaches)

model = pickle.load(open('prediction_model', 'rb'))
df = pd.read_csv('Locations')
#abc


st.write("Here are our predictions, based on Florida health department's historical beach water test data:")




for n in range(7):
 s = df[df['SPLocation'] == beach].T.squeeze()
 s[2] = pd.datetime.now().month
 s[3] = (pd.datetime.now().month -1) * 30 + pd.datetime.now().day + n
 if model.predict(s[1:].values.reshape(1, -1)) == [1]:
  tarih = datetime.date.today() + datetime.timedelta(days = n)
  st.write('We do not expect pollution at this location on', tarih'.')
 else:
  st.write('We expect this location to be polluted on', tarih'.')
#
#t = df[df['SPLocation'] == beach].T.squeeze()
#t[2] = pd.datetime.now().month
#t[3] = (pd.datetime.now().month -1) * 30 + pd.datetime.now().day+1
#if model.predict(t[1:].values.reshape(1, -1)) == [1]:
 #st.write('We do not expect pollution at this location tomorrow.')
#else:
 #st.write('We expect this location to be polluted tomorrow.')
#st.write('Our prediction for tomorrow is: ')
#st.text(model.predict(t[1:].values.reshape(1, -1)))


