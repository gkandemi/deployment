"""
ReqMgr only configuration file.
Everything configurable in ReqMgr is defined here.

"""


from WMCore.Configuration import Configuration
from os import path

config = Configuration()

main = config.section_("main")
srv = main.section_("server")
srv.thread_pool = 30
main.application = "reqmgr2"
main.port = 8246 # main application port it listens on
main.index = "ui"
# Defaults to allow any CMS authenticated user. Write APIs should require
# additional roles in SiteDB (i.e. "Admin" role for the "ReqMgr" group)
main.authz_defaults = {"role": None, "group": None, "site": None}

sec = main.section_("tools").section_("cms_auth")
sec.key_file = "%s/auth/wmcore-auth/header-auth-key" % __file__.rsplit('/', 3)[0]

# this is where the application will be mounted, where the REST API
# is reachable and this features in CMS web frontend rewrite rules
app = config.section_(main.application) # string containing "reqmgr2"
app.admin = "cms-service-webtools@cern.ch"
app.description = "CMS data operations Request Manager."
app.title = "CMS Request Manager (ReqMgr)"

views = config.section_("views")

# practical to have this kind of configuration values not in
# service related RPM (difficult/impossible to change in CMS web
# deployment) but in the deployment configuration for the service

# redirector for the REST API implemented handlers
data = views.section_("data")
data.object = "WMCore.ReqMgr.Service.RestApiHub.RestApiHub"
# The couch host is defined during deployment time.
data.couch_host = "@@COUCH_HOST@@"
# main ReqMgr CouchDB database containing all requests with spec files attached
data.couch_reqmgr_db = "reqmgr_workload_cache"
# ReqMgr database containing groups, teams, software, etc
data.couch_reqmgr_aux_db = "reqmgr_auxiliary"
# ConfigCache - database with configuration documents
data.couch_config_cache_db = "reqmgr_config_cache"
data.couch_workload_summary_db = "workloadsummary"
data.couch_wmstats_db = "wmstats"
# number of past days since when to display requests in the default view
data.default_view_requests_since_num_days = 30 # days
# resource to fetch CMS software versions and scramarch info from
data.tag_collector_url = "https://cmssdt.cern.ch/SDT/cgi-bin/ReleasesXML?anytype=1"
# another source at TC, returns directly JSON, but strangely formatted (e.g.
# keys are not present at easy item but defined in a dedicated item ...)
# https://cmssdt.cern.ch/tc/getReleasesInformation?release_state=Announced

# request related settings (e.g. default injection arguments)
data.default_sw_version = "CMSSW_5_2_5"
data.default_sw_scramarch = "slc5_amd64_gcc434"
data.dqm_url = "https://cmsweb.cern.ch/dqm/dev"
data.dbs_url = "https://cmsweb.cern.ch/dbs/prod/global/DBSReader"

# web user interface
ui = views.section_("ui")
ui.object = "WMCore.ReqMgr.WebGui.FrontPage.FrontPage"
ui.static_content_dir = path.join(path.abspath(__file__.rsplit('/', 3)[0]),
                                 "apps",
                                 main.application,
                                 "data")
