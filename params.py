
class Params:
    
    # Webdriver
    HEADLESS = True
    NO_SANDBOX = True
    TIMEOUT = 10
    
    # Crawler params
    URL = "https://cit.transit.gencat.cat/cit/AppJava/views/incidents.xhtml"
    DEMARCACIONES = ["Barcelona"]
    VIAS = ["AP-7", "B-23", "C-17", "B-20"]
    OBRAS = False
