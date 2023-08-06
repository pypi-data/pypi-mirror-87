'''
Created on 18.04.2012

SSAS Tests are done against the Adventure Works DW 2008R2, 
tested against ssas version 10.50.2500.0 (comes with sqlserver 2008 R2)
Mondrian was test with version 3.3.0.14703

@author: norman

n.b.:
  Mondrian is running with a mysql backend. 
  Using the embedded derby backend (as distributed by mondrian) fails in 
  MDSchemaMembers with an internal error (when a subselect is executed in 
  the read-only container where the database lives).
  
'''

import unittest
from nose.tools import *
import olap.xmla.xmla as xmla
from requests.auth import HTTPBasicAuth

from olap.xmla.connection import xmla1_1_rowsets
import tests.mockhelper as mockhelper
import tests.integration.discover_mondrian as discover_mondrian
import tests.integration.discover_ssas as discover_ssas

mock_location = "mock://somewhere/over/the/rainbow"

mondrian={
    "type":"mondrian",
    "auth": None,
    "location":"http://localhost:8080/xmondrian/xmla",
    # Datasourcename depends on distribution
    #"ds": "Provider=Mondrian;DataSource=MondrianFoodMart;",
    "ds": "Foodmart",
    "catalog":"FoodMart",
    "restrict_cube":"HR",
    "restrict_dim":"Position",
    "restrict_unique_dim":"[Gender]",
    "cubes_expected":7,
    "restrict_funcname":"||",
    "restrict_hier":"Time",
    "restrict_level_unique_name":"[Employees].[Employee Id]",
    "restrict_hierarchy_unique_name":"[Time]",
    "cube_measures":5,
    "schema_levels":3,
    "schema_sets":1,
    "schema_sets_needs_cubename":False,
    "schema_tables":1,
    "flow_catalog":"FoodMart",
    "flow_cube":"Sales",
    "flow_hier":"[Product]",
    "flow_level":"[Product].[Product Category]",
    "flow_member":"[Product].[Drink].[Alcoholic Beverages].[Beer and Wine]",
    "flow_member_name":"Beer and Wine",
    "conversation":discover_mondrian,
}

ssas={
    "type":"ssas",
    "location":"http://dwh-bi/olap/msmdpump.dll",
    "auth" : None,
    "ds":"DWH-BI",
    "catalog":"Adventure Works DW 2008R2",
    "restrict_cube":"Adventure Works",
    "restrict_dim":"Account",
    "restrict_unique_dim":"[Account]",
    "cubes_expected":7,
    "restrict_funcname":"TRIM",
    "restrict_hier":"Account Number",
    "restrict_level_unique_name":"[Customer].[Customer Geography].[Country]",
    "restrict_hierarchy_unique_name":"[Customer].[Customer Geography]",
    "cube_measures": 51,
    "schema_levels":6,
    "schema_sets":1,
    "schema_sets_needs_cubename":True, # not really, but if you have a few DBs on your server this will bring it to it's knees
    "schema_tables":1,
    "flow_catalog":"Adventure Works DW 2008R2",
    "flow_cube":"Adventure Works",
    "flow_hier":"[Product].[Category]",
    "flow_level":"[Product].[Category].[Category]",
    "flow_member":"[Product].[Category].&[3]",
    "flow_member_name":"Clothing",
    "conversation":discover_ssas
}

import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


class XMLA(object):
    be = None
    logreq = None
    record = False

    def setUp(self):
        testname = self.id().split(".")[-1]
        session = mockhelper.mockedsession(self.be["conversation"], testname)
        self.p = xmla.XMLAProvider()
        if self.logreq:
            self.logreq.prefix=testname
        kw = {
            "log":self.logreq,
            "session":session
        }
        self.c = self.p.connect(location=self.be["location"], 
                                auth=self.be["auth"], **kw)
        #self.c.BeginSession()
        self.getSchemaRowsetSupport()
         
    def getSchemaRowsetSupport(self):
        if self.supported is None:
            self.supported=[x["SchemaName"] for x in self.c.getSchemaRowsets()]
            self.proprietary = [x for x in self.supported if not(x in xmla1_1_rowsets)]
            self.conform = [x for x in self.supported if (x in xmla1_1_rowsets)]
            self.unsupported = [x for x in xmla1_1_rowsets if not (x in self.supported)]
    
    def tearDown(self):
        #self.c.EndSession()
        if self.logreq and self.record:
            self.logreq.saveConversation(fname="try_discover_"+self.be["type"] +".py")
    
    def testGetDatasources(self):
        #self.log.enable()
        erg=self.c.getDatasources()
        #e = erg[0]
        #print(type(e))
        #print(e)
        self.assertTrue(len(erg) == 1, "One Datasource is expected")
        self.assertEqual(self.be["ds"], erg[0]["DataSourceName"])
        
    def testGetProperties(self):
        erg=self.c.getProperties()
        # check for required xmla properties
        req = """AxisFormat,BeginRange,Catalog,Content,Cube,DataSourceInfo,
                 EndRange,Format,LocaleIdentifier,MDXSupport,Password,
                 ProviderName,ProviderVersion,StateSupport,Timeout,UserName"""
        # of those required icCube only returns ProviderVersion and Catalog
        # if self.be == iccube: req = "Catalog,ProviderVersion"
        propnames = [x["PropertyName"] for x in erg]
        for p in req.split(","):
            self.assertIn(p.strip(), propnames)

    def testGetDBSchemaCatalogs(self):
        #self.log.enable()
        erg=self.c.getDBSchemaCatalogs()
        self.assertTrue(len(erg) > 0, "One Catalog is expected - at least")
        self.assertIn(self.be["catalog"], [x["CATALOG_NAME"] for x in erg])
        
    
    def testGetDBSchemaColumns(self):
        if "DBSCHEMA_COLUMNS" in self.conform:
            erg=self.c.getDBSchemaColumns()
            self.assertTrue(len(erg) > 0, 
                            "There must be at least one column, really!")
        
    def testGetDBSchemaTables(self):
        erg=self.c.getDBSchemaTables()
        self.assertTrue(len(erg) >= self.be["schema_tables"], 
                        "There must be at least one table")

    def testGetDBSchemaProviderTypes(self):
        if "DBSCHEMA_PROVIDER_TYPES" in self.conform:
            erg=self.c.getDBSchemaProviderTypes()
            msg="There should be at least one type like INTEGER for example"
            self.assertTrue(len(erg) > 0, msg)
        
    def testGetDBSchemaTablesInfo(self):
        if "DBSCHEMA_TABLES_INFO" in self.conform:
            erg=self.c.getDBSchemaTablesInfo()
            self.assertTrue(len(erg) > 0, 
                            "There must be at least one tablesinfo")

    def testGetMDSchemaActions(self):
        erg=self.c.getMDSchemaActions(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], "COORDINATE":self.be["restrict_cube"], "COORDINATE_TYPE":1})
        self.assertTrue(len(erg)==0, "no actions expected")

    def testGetMDSchemaCubes(self):
        # oh my, mondrian doesn't know what do do with Catalog in the Proplist ... 
        # but only when requesting cubes, other rowset requests are going 
        # through just fine (are probably ignored on the server side)
        props = {"Catalog":self.be["catalog"]}
        erg=self.c.getMDSchemaCubes(properties=props)
        self.assertEqual(len(erg), self.be["cubes_expected"])
        #self.log.enable()
        erg=self.c.getMDSchemaCubes(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties=props)
        self.assertEqual(len(erg), 1)

    def testGetSchemaRowsets(self):
        erg=self.c.getSchemaRowsets()
        self.assertTrue(len(erg)>0, "at least one schema is expected")
        
    def testGetMDSchemaFunctions(self):
        erg=self.c.getMDSchemaFunctions()
        self.assertTrue(len(erg)> 1, 
                        "There should be more than one function description.")
        erg=self.c.getMDSchemaFunctions(
            restrictions={"FUNCTION_NAME":self.be["restrict_funcname"]})
        self.assertEqual(len(erg), 1)
        
    def testGetMDSchemaMembers(self):
        erg=self.c.getMDSchemaMembers(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
                          "LEVEL_UNIQUE_NAME":self.be["restrict_level_unique_name"]}, 
            properties={"Catalog":self.be["catalog"]})
        self.assertTrue(len(erg)> 1, 
                        "There should be more than one dimension member.")

    def testGetMDSchemaProperties(self):
        erg=self.c.getMDSchemaProperties(
            {"CUBE_NAME":self.be["restrict_cube"], 
             'LEVEL_UNIQUE_NAME': self.be["restrict_level_unique_name"]}, 
            properties={"Catalog":self.be["catalog"]})
        self.assertTrue(len(erg)> 1, 
                        "There should be more than one schema property.")

    def testGetMDSchemaSets(self):
        if self.be["schema_sets_needs_cubename"]:
            erg=self.c.getMDSchemaSets(restrictions={"CUBE_NAME":self.be["restrict_cube"]})
        else:
            erg=self.c.getMDSchemaSets()
        
        self.assertTrue(len(erg)>= self.be["schema_sets"], 
                        "There should be a schema set.")

    def testGetEnumerators(self):
        if "DISCOVER_ENUMERATORS" in self.conform:
            erg = self.c.getEnumerators()
            msg = "There should be at least one enumerator."
            self.assertTrue(len(erg)> 0, msg)
        
    def testGetLiterals(self):
        erg = self.c.getLiterals()
        self.assertTrue(len(erg)> 0, "There should be at least one literal.")
        
    def testGetKeywords(self):
        # instead of not listing the KEYWORDS Rowset in a call to 
        # DISCOVER_SCHEMA_ROWSETS, iccube throws an exceptions
        if "DISCOVER_KEYWORDS" in self.conform:
            erg = self.c.getKeywords()
            self.assertTrue(len(erg)> 0, 
                            "There should be at least one keyword.")
        

    def testGetMDSchemaDimensions(self):
        erg=self.c.getMDSchemaDimensions(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
                          "DIMENSION_NAME":self.be["restrict_dim"]},
            properties={"Catalog":self.be["catalog"]})
        self.assertEqual(len(erg), 1)
        
    def testGetMDSchemaHierarchies(self):
        erg=self.c.getMDSchemaHierarchies(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        self.assertTrue(len(erg)> 1, 
                        "There should be more than one hierarchy.")
        erg=self.c.getMDSchemaHierarchies(
            restrictions={"HIERARCHY_NAME":self.be["restrict_hier"], 
                          "CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        self.assertEqual(len(erg), 1)

    def testGetMDSchemaMeasures(self):
        erg=self.c.getMDSchemaMeasures(
            restrictions={"CUBE_NAME":self.be["restrict_cube"]}, 
            properties={"Catalog":self.be["catalog"]})
        self.assertEqual(len(erg), self.be["cube_measures"])

    def testGetSchemaLevels(self):
        #self.log.enable()
        erg = self.c.getMDSchemaLevels(
            restrictions={"CUBE_NAME":self.be["restrict_cube"], 
             'HIERARCHY_UNIQUE_NAME': self.be["restrict_hierarchy_unique_name"]},
            properties={"Catalog":self.be["catalog"]})
        self.assertEqual(len(erg), self.be["schema_levels"])
    
    def testGetDBSchemaSchemata(self):
        if "DBSCHEMA_SCHEMATA" in self.supported:
            erg = self.c.Discover("DBSCHEMA_SCHEMATA")

    def testFlow(self):
        cat=self.c.getCatalog(self.be["flow_catalog"])
        cube=cat.getCube(self.be["flow_cube"])
        hier=cube.getHierarchy(self.be["flow_hier"])
        level=hier.getLevel(self.be["flow_level"])
        member=level.getMember(self.be["flow_member"])
        self.assertEqual(member.MEMBER_NAME, self.be["flow_member_name"])

try:
    from testconfig import config
    server=config['xmla']['server'] or ""
    server = server.split(",")
    for server_section in server:
        if server_section in globals():
            globals()[server_section].update(config.get(server_section, {}))

    do_record=(config['xmla']['record'] or "no") == "yes"
    if "ssas" in server:
        from requests_kerberos import HTTPKerberosAuth
        ssas["auth"] = HTTPKerberosAuth()
            
except:
    # we mock responses
    server=["mondrian", "ssas"]
    config = {}
    mondrian["location"]=mock_location
    ssas["location"]=mock_location
    do_record = False

if "mondrian" in server:
    class TestMondrian(XMLA, unittest.TestCase):
        be = mondrian
        supported = proprietary = conform = unsupported = None
        logreq = mockhelper.LogRequest(False)
        record = do_record

if "ssas" in server:
    class TestSSAS(XMLA, unittest.TestCase):
        be = ssas
        supported = proprietary = conform = unsupported = None
        logreq = mockhelper.LogRequest(False)
        record = do_record

