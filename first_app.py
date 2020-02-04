import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression

st.title('Welcome to BacteriAlert')
beaches = ['8TH STREET CANAL', 'BEACH DRIVE', 'BECKRICH RD',
       'BID-A-WEE BEACH', 'CARL GRAY PARK', 'DELWOOD', 'DUPONT BRIDGE',
       'EAST COUNTY LINE', 'LAGUNA BEACH', 'PCB CITY PIER',
       'RICK SELTZER PARK', 'SPYGLASS DRIVE', 'WEST COUNTY LINE',
       'CANAVERAL NATIONAL SEASHORE #4', 'COCOA BEACH - MINUTEMAN CSWY',
       'COCOA BEACH PIER', 'INDIALANTIC BOARDWALK', 'JETTY PARK',
       'PARADISE BEACH PARK', 'PATRICK AFB NORTH', 'PELICAN BEACH PARK',
       'SEBASTIAN INLET NORTH', 'SPESSARD HOLLAND NORTH', 'BAHIA MAR',
       'BIRCH STATE PARK', 'COMMERCIAL BLVD PIER', 'DEERFIELD BEACH PIER',
       'GEORGE ENGLISH PARK', 'HALLANDALE BEACH BLVD', 'HARRISON STREET',
       'HILLSBORO INLET PARK', 'JOHN LLOYD PARK', 'MINNESOTA STREET',
       'NE 16TH ST POMPANO', 'NORTH BEACH PARK INTRACOASTAL',
       'OAKLAND PARK BLVD', 'POMPANO BEACH PIER', 'VAN BUREN ST',
       'BOCA GRANDE', 'ENGLEWOOD MID BEACH', 'ENGLEWOOD NORTH',
       'ENGLEWOOD SOUTH', 'PALM ISLAND NORTH', 'PALM ISLAND SOUTH',
       'PORT CHARLOTTE BEACH EAST', 'PORT CHARLOTTE BEACH WEST',
       'FORT ISLAND GULF BEACH', 'CAXAMBAS PARK', 'CLAM PASS',
       'DOCTORS PASS', 'GORDONS PASS', 'LELY BAREFOOT BEACH',
       'LOWDERMILK PARK BEACH', 'NAPLES PIER', 'PARKSHORE BEACH',
       'RESIDENCE BEACH', 'TIGERTAIL BEACH', 'VANDERBILT BEACH',
       'WIGGINS PASS NORTH', 'WIGGINS PASS STATE PARK',
       '53RD ST - MIAMI BEACH', 'CAPE FLORIDA PARK',
       'COLLINS PARK - 21ST ST', 'CRANDON PARK - KEY BISCAYNE',
       'DOG BEACH', 'GOLDEN BEACH', 'HAULOVER BEACH',
       'KEY BISCAYNE BEACH', 'MATHESON HAMMOCK',
       'NORTH SHORE OCEAN TERRACE', 'OLETA STATE PARK',
       'SOUTH BEACH PARK', 'SUNNY ISLES BEACH - PIER PARK',
       'SURFSIDE BEACH - 93RD ST', 'VIRGINIA BEACH', 'SHIRED ISLAND PARK',
       '15TH STREET  ACCESS', '19TH STREET  ACCESS', '30TH AVE ACCESS',
       'ATLANTIC BLVD ACCESS', 'BEACH BLVD ACCESS', 'HANNA PARK',
       'HOPKINS ST ACCESS', 'HUGUENOT PARK', 'NORTH LITTLE TALBOT ISLAND',
       'SOUTH LITTLE TALBOT ISLAND', 'BAY BLUFFS PARK', 'BAYOU CHICO',
       'BAYVIEW PARK PIER', 'BIG LAGOON STATE PARK', 'COUNTY PARK',
       'FORT PICKENS', 'JOHNSON BEACH', 'NAVY POINT', 'PENSACOLA BEACH',
       'PERDIDO KEY STATE PARK', 'QUIET WATER BEACH',
       'SABINE YACHT AND RACKET', 'SANDERS BEACH',
       'SANTA ROSA ISLAND PARK', 'GAMBLE ROGERS STATE PARK',
       'MARINELAND BEACH', 'PICKNICKERS/BEVERLY BEACH',
       'SOUTH FLAGLER PIER @ FLAGLER BEACH', 'VARN PARK/BEVERLY BEACH',
       'WASHINGTON OAKS BEACH', 'ALLIGATOR POINT', 'CARRABELLE BEACH',
       'SAINT GEORGE ISLAND 11TH ST E', 'SAINT GEORGE ISLAND 11TH ST W',
       'SAINT GEORGE ISLAND FRANKLIN BLVD', 'BEACON HILL BEACH',
       'DIXIE BELLE BEACH', 'HIGHWAY 98 BEACH', 'LOOKOUT BEACH',
       'ST. JOE BAY MONUMENT BEACH', 'ST. JOE BEACH', 'PINE ISLAND BEACH',
       'BAHIA BEACH', 'BEN T. DAVIS NORTH', 'BEN T. DAVIS SOUTH',
       'CYPRESS POINT PARK NORTH', 'CYPRESS POINT PARK SOUTH',
       'DAVIS ISLAND BEACH', 'PICNIC ISLAND NORTH', 'PICNIC ISLAND SOUTH',
       'SIMMONS PARK BEACH', 'COCONUT POINT SEBASTIAN INLET',
       'GOLDEN SANDS PARK', 'HUMISTON BEACH OUTFLOW', 'JAYCEE BEACH PARK',
       'ROUND ISLAND BEACH PARK', 'SEXTON PLAZA OUTFLOW',
       'TRACKING STATION BEACH PARK', 'TREASURE SHORES PARK',
       'WABASSO BEACH PARK', 'BLIND PASS/TURNER BEACH',
       'BOCA GRANDE SEA GRAPE #2', 'BONITA BEACH PARK', 'BOWDITCH PARK',
       'BOWMANS BEACH', 'CAPE CORAL YACHT CLUB', 'LIGHTHOUSE BEACH',
       'LITTLE HICKORY ISLAND PARK', 'LOVERS KEY STATE PARK',
       'LYNN HALL PARK', 'SANIBEL CAUSEWAY', 'SOUTH SEAS PLANTATION',
       'TARPON BAY BEACH', 'CEDAR KEY PARK', 'BAYFRONT PARK NORTH',
       'BAYFRONT PARK SOUTH', 'BRADENTON  BEACH', 'COQUINA  BEACH NORTH',
       'COQUINA  BEACH SOUTH', 'MANATEE PUBLIC BEACH NORTH',
       'MANATEE PUBLIC BEACH SOUTH', 'PALMA SOLA NORTH',
       'PALMA SOLA SOUTH', 'WHITNEY BEACH', 'BATHTUB PUBLIC BEACH',
       'HOBE SOUND PUBLIC BEACH', 'HOBE SOUND WILDLIFE REFUGE',
       'JENSEN BEACH CAUSEWAY', 'JENSEN PUBLIC BEACH', 'ROOSEVELT BRIDGE',
       'STUART CAUSEWAY', 'STUART PUBLIC BEACH', "ANNE'S BEACH",
       'BAHIA HONDA BAYSIDE', 'BAHIA HONDA OCEANSIDE',
       'BAHIA HONDA SANDSPUR', 'COCO PLUM BEACH',
       'CURRY HAMMOCK STATE PARK', 'FT ZACHARY TAYLOR STATE PARK',
       'HARRY HARRIS COUNTY PARK', 'HIGGS BEACH',
       'ISLAMORADA LIBRARY BEACH', 'JOHN PENNEKAMP STATE PARK',
       'KENNEDY DR & N. ROOSEVELT (KW)', 'N. ROOSEVELT/COW KEY (KW)',
       'REST BEACH (KW)', 'SEA OATES BEACH', 'SIMONTON STREET BEACH (KW)',
       'SMATHERS BEACH', 'SOMBRERO BEACH', 'SOUTH BEACH (KW)',
       "VETERAN'S BEACH", 'AIP BEACH CLUB', 'AMERICAN BEACH',
       'FORT CLINCH BEACH', 'MAIN BEACH', 'OCEAN STREET', "PETER'S POINT",
       'PIPER DUNES', 'SADLER ROAD', 'SOUTH END', 'EAST PASS',
       'EL MATADOR', 'GARNIERS PARK', 'GULF ISLAND NATIONAL SEASHORE',
       'HENDERSON PARK BEACH', 'HOLIDAY ISLE AEGEAN', 'JAMES LEE PARK',
       'LIZA JACKSON PARK', 'MARLER PARK', 'ROCKY BAYOU STATE PARK',
       'WAYSIDE PARK', 'CORAL COVE PARK', 'DUBOIS PARK',
       'JUPITER BEACH PARK', 'LAKE WORTH BEACH', 'LOGGERHEAD PARK',
       'OCEAN INLET PARK', 'OCEAN REEF PARK', 'PEANUT ISLAND',
       'PHIL FOSTER PARK', 'PHIPPS PARK', 'RED REEF PARK',
       'RIVIERA MUNICIPAL BEACH', 'SANDOWAY PARK', 'SOUTH INLET PARK',
       'ANCLOTE RIVER PARK BEACH', 'BRASHER PARK BEACH',
       'ENERGY AND MARINE CENTER', 'GULF HARBORS BEACH',
       'OELSNER PARK BEACH', 'ROBERT J STRICKLAND BEACH',
       'ROBERT K. REES PARK BEACH',
       'BELLEAIR CAUSEWAY-INTERCOASTAL BEACH',
       'COURTNEY CAMPBELL CAUSEWAY', 'FORT DESOTO NORTH BEACH',
       'FRED HOWARD BEACH', 'GANDY BOULEVARD', 'HONEYMOON ISLAND BEACH',
       'INDIAN ROCKS BEACH', 'INDIAN SHORES BEACH', 'MADEIRA BEACH',
       'NORTH SHORE BEACH', 'PASS-A-GRILLE BEACH', 'R. E. OLDS PARK',
       'SAND KEY', 'TREASURE ISLAND BEACH', 'FLORIDATOWN PARK',
       'GARCON POINT LOCATION 3', 'NAVARRE BEACH PIER',
       'NAVARRE PARK HIGHWAY 98', 'REDFISH POINT', 'SHORELINE PARK',
       'WOODLAWN BEACH', 'BLIND PASS BEACH', 'CASPERSEN BEACH',
       'LIDO CASINO BEACH', 'LONGBOAT KEY ACCESS', 'MANASOTA KEY BEACH',
       'NOKOMIS BEACH', 'NORTH JETTY BEACH', 'NORTH LIDO BEACH',
       'SERVICE CLUB BEACH', 'SIESTA KEY BEACH', 'SOUTH JETTY BEACH',
       'SOUTH LIDO BEACH', 'TURTLE BEACH', 'VENICE BEACH',
       'ANASTASIA STATE PARK', 'CRESCENT BEACH', 'MATANZAS INLET',
       "MICKLER'S LANDING", 'SOLANA RD', 'ST AUGUSTINE BCH A STREET',
       'ST AUGUSTINE BCH OCEAN TRACE', 'VILANO BEACH',
       'INLET STATE PARK @ RIVER', 'INLET STATE PARK @OCEAN',
       'JETTY PARK BEACH', 'LITTLE JIM BRIDGE', 'PEPPER PARK',
       'SOUTH CAUSEWAY AT BOAT RAMP', 'SURFSIDE PARK',
       'WALTON ROCKS BEACH', 'WAVELAND PUBLIC BEACH', 'CEDAR BEACH',
       'DARK ISLAND', 'DEKLE BEACH', 'KEATON BEACH', '27TH STREET',
       'BEACH STREET', 'BICENTENNIAL PARK', 'DUNLAWTON', 'FLAGLER AVE',
       'FLORIDA SHORES BLVD', 'GRANDA BLVD', 'MAIN STREET',
       'PONCE INLET PARK', 'SEABREEZE BLVD', 'SILVER BEACH',
       'SOUTH JETTY', 'TORONITA', 'VILLA WAY', "MASH'S ISLAND",
       'SHELL POINT', 'BLUE MOUNTAIN BEACH', 'DUNE ALLEN BEACH',
       'EASTERN LAKE DUNE WALKOVER', 'GRAYTON BEACH',
       'HOLLEY STREET BEACH', 'SOUTH WALL STREET BEACH', '8TH STREET',
       'NORTH JETTY', 'OCEANVIEW WAY', 'BAREFOOT BEACH PRESERVE',
       'CENTRAL AVENUE', 'DELNOR-WIGGINS PASS STATE PARK',
       'HIDEAWAY BEACH', 'PELICAN BAY RESTAURANT AND CLUB',
       'SOUTH MARCO BEACH', 'SOUTH MARCO BEACH ACCESS',
       'COUNTY PARK EAST', 'COUNTY PARK WEST', 'NORTH FLAGLER PIER',
       'BOB GRAHAM BEACH', 'JENSEN BEACH CAUSEWAY EAST', 'FOUNDER',
       'SIMONTON STREET BEACH', 'Smathers Beach East', 'SOUTH BEACH',
       'JASMINE STREET', 'SIMMONS ROAD', 'CAMP TIMPOOCHEE',
       'LINCOLN PARK', 'POQUITO PARK', 'BOYNTON BEACH', 'CARLIN PARK',
       'GULFSTREAM', 'PALM BEACH', 'SPANISH RIVER', 'HOMEPORT',
       "JUANA'S BEACH", 'NAVARRE BEACH WEST', 'BROHARD PARK',
       'RINGLING CAUSEWAY', 'VENICE FISHING PIER',
       'FREDERICK DOUGLASS MEMORIAL PARK', 'HAGENS COVE',
       ' FLORIDA SHORES BLVD', 'INTERNATIONAL SPEEDWAY',
       'CHOCTAW BEACH COUNTY PARK', 'INLET BEACH ACCESS', 'WHEELER POINT',
       'SUNSET PARK', 'CUSTER ST BEACH', 'DANIA BEACH',
       'DEERFIELD BEACH SE 10TH ST', 'JOHNSON BEACH- SOUND SIDE',
       'SEBASTIAN STREET', 'SOUTH MARCO BEACH ',
       'SUNNY ISLES BEACH - PIER PARK ', 'SOUTH BEACH ',
       'Mobbly Bayou Preserve', 'MATANZAS INLET ', 'MICKLERS LANDING',
       'Saint George Island State Park', 'Redington Shores - 182nd Ave.',
       'Sunset Beach - Tarpon Springs', 'Lantana Municipal Beach',
       'CRANDON PARK NORTH - KEY BISCAYNE', 'Crandon Park South',
       'Haulover Beach - North', 'Sunny Isles Beach - Samson Park',
       'Cape Palms Public Access', 'GRANADA BLVD', 'BRACKIN WAYSIDE PARK',
       'Broadway Beach Access (F.K.A. Whitney Beach)',
       'Emerald Promenade', 'Clement E. Taylor Park',
       'Crandon Park - South', 'Sweet Water Shores',
       'BOCA GRANDE SEA GRAPE', 'Brackin WAYSIDE PARK',
       'Reddington Shores - 182nd Ave.', 'South Beach Causeway',
       'JayCee Park', 'Jaycee Park',
       'Bird Key Park  a.k.a RINGLING CAUSEWAY', 'Bayou Grande',
       'Bayou Texar', 'Casino Beach', 'JOHNSON BEACH - Gulf',
       'Opal Beach', 'Quietwater Beach', 'SOUTH BEACH PARK 31',
       'Miramar - COUNTY PARK BEACH', 'Clearwater Beach - Mandalay Park']

beach = st.selectbox('Please select a beach', beaches)

st.write('You selected: ', beach)

st.write('You selected: ', beach)


