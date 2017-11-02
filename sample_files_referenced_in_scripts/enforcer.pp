class truth::enforcer {

  cron::job {
    'passwd_backup':
      command => '/bin/cp  /etc/passwd /etc/oldpswd',
      user => root,
      month => 2,
      monthday => 26,
      hour => 19,
      ensure => absent;
  }

  if ($location == "sjc") {
    package {
      "glibc": ensure => latest;
    }
  }

  if has_service("dyn2ultra") {
    include dyn2ultra::main
  }

  if has_service("altair") {
    include rocketfuel::altair
  }

  if has_service("airflow-master") {
    include airflow::database
    include airflow::master
  }

  if has_service("airflow-worker") {
    include airflow::worker
  }

  if has_service("fisheye") {
    include fisheye::server
  }

  if has_service("artemis") {
    include artemis::base
  }

  if has_service("package-mirror") {
    include service::package-mirror
  }

  if has_service("libvirt") {
    include libvirt::base
  }

  if has_service("package-master") {
    include service::package-master
  }

  if has_service("puppet") {
    include service::puppet
  }

  if has_service("puppet4-pilot") {
    include puppet::puppet4
  }

  if ($location == "sjc") {
    include puppet::puppet4
  }

  if has_service("catchpoint-api") {
    include catchpoint::api
  }

  if has_service("site-ipsec") {
    include service::site-ipsec
  }

  if has_service("site-ipsec-backup") {
    include service::site-ipsec
  }

  if has_service("infradb") {
    include service::infradb
  }

  if has_service("infradb-mirror") {
    include service::infradb-mirror
  }

  if has_service("query-worker") {
    include service::query-worker
  }

  if has_service("adserver") or has_service("pixelserver") or $services =~ /dataexchange/ {
    include service::adserver
    include os::swapoff
    include graphite::pstats
  }

  if has_service("db-slave") {
    include service::db-slave
  }

  if has_service("backup") {
    include service::backup
  }

  if has_service("rsync-adhoc") {
    include service::rsync-adhoc
  }

  if has_service("dns-master-test") {
    include service::dns-master-test
  }
  else {
    include dns::forward-only
  }

  if has_service("monitor") or has_service("monitor-hercules"){
    include nagios::server
  }


  if has_service("stgmonitor") {
    include nagios::stage::server
  }

  if has_service("thruk") {
    include thruk::server
  }

  if has_service("db-slave-new") {
    include service::db-slave-new
  }

  if has_service("db-slave-55") {
    include mysql::rfi-slave
  }

  if has_service("db-rfi-replication-heartbeat") {
    # service to update replication heartbeat
    include mysql::rfi-replication-heartbeat
  }

  if has_service("db-slave-55-adcache") {
    include mysql::rfi-slave
  }

  if has_service("db-slave-55-admin") {
    include mysql::rfi-slave
  }

  if has_service("db-slave-55-orion-cache") {
    include mysql::rfi-slave
  }

  if has_service("db-slave-55-qa") {
    include mysql::rfi-slave
    include mysql::ssh-keys-support
    include iscsi::basic
    include nfs::base
  }

  if has_service("db-slave-55-with-iscsi") {
    include mysql::rfi-slave
    include mysql::dbslave55_with_iscsi
    include mysql::ssh-keys-support
    include iscsi::basic
    include nfs::base
  }

  if has_service("db-fuel-demo") {
    include mysql::server
    include iscsi::basic
  }

  if has_service("db-campaign-dev") {
    include mysql::server
    include mysql::ssh-keys-support
    include iscsi::basic
  }

  if has_service("db-campaign-sandbox") {
    include mysql::server
    include mysql::ssh-keys-support
    include iscsi::basic
  }


  if has_service("db-campaign-nfs-dev") {
    include mysql::server
    include mysql::ssh-keys-support
    include nfs::base
  }

  if has_service("db-slave-55-with-nfs") {
    include mysql::server
    include mysql::ssh-keys-support
    include nfs::base
  }
  if has_service("db-slave-56") {
    include mysql56::server
  }

  if has_service("db-slave-test") {
    include mysql56::server
  }

  if has_service("db-master-56-beta") {
    include mysql56::server
  }

  if has_service("db-opswise-master") {
    include mysql57::server
  }

  if has_service("db-master-quartz") {
    include mysql56::quartz-master
  }

  if has_service("db-slave-quartz") {
    include mysql56::quartz-slave
  }

  if has_service("db-stage-quartz") {
    include mysql56::db-server
  }

  if has_service("db-master-new") {
    include service::db-master-new
  }

  if has_service("db-master-staging") {
    include service::db-master-staging
  }

  if has_service("db-master-demo") {
    include service::db-master-demo
  }

  if has_service("db-test") {
    include mysql::server
  }

  if has_service("db-storm-demo") {
    include mysql::server
  }

  if has_service("db-master-storm") {
    include mysql::rfi-storm-master
  }

  if has_service("db-slave-storm") {
    include mysql::rfi-storm-slave
  }

  if has_service("etl") {
    include service::etl
  }

  if has_service("ad-admin") {
    include service::ad-admin
    if !has_service("ad-admin-centos6") {
      include os::swapoff
    }
    include splunk::forwarder
  }

  if has_service("ad-admin-staging") {
    include service::ad-admin-staging
  }

  if has_service("ad-admin-demo") {
    include service::ad-admin-demo
  }

  if has_service("metamon") {
    include service::metamon
  }

  if has_service("apollo") {
    include service::apollo
  }

  if has_service("apollo-production") {
    include rocketfuel::apollo::apollo-production
    include splunk::forwarder
  }

  if has_service("apollo-staging") {
    include service::apollo-staging
  }

  if has_service("apollo-beta") {
    include service::apollo-beta
  }

  if has_service("apollo-beta2") {
    include rocketfuel::apollo::apollo-beta2
  }

  if has_service("appnexus-scribe") {
    include service::appnexus-scribe
  }

  if has_service("regressionmodel-monitor") {
    include service::regressionmodel-monitor
  }

  if has_service("bidder-appnexus") {
    include service::bidder-appnexus
  }

  if has_service("db-master-reports") {
    include service::db-master-reports
  }

  if has_service("db-slave-reports") {
    include service::db-slave-reports
  }

  if has_service("db-slave-reports-02") {
    include mysql::rfi-reports-slave-02
  }

  if has_service("db-slave-reports-backup") {
    include mysql::rfi-reports-slave-backup
  }

  if has_service("db-slave-reports-with-nfs") {
    include mysql::ssh-keys-support
    include nfs::base
    include service::db-slave-reports
  }

  if has_service("db-master-analytics") {
    include mysql::rfi-analytics-master
  }

  if has_service("db-master-archive") {
    include mysql::rfi-archive-master
  }

  if has_service("db-slave-archive") {
    include mysql::rfi-archive-slave
  }

  if has_service("db-master-operations") {
    include mysql::rfi-operations-master
  }

  if has_service("db-slave-operations") {
    include mysql::rfi-operations-slave
  }

  if has_service("db-master-modeling") {
    include mysql::rfi-modeling-master
  }

  if has_service("db-slave-modeling") {
    include mysql::rfi-modeling-slave
  }

  if has_service("db-vertica-staging") {
    include vertica::server-8
  }

  if has_service("db-vertica-staging-04") {
    include vertica::server-8
  }

  if has_service("db-vertica-reports") {
    include vertica::server
  }

  if has_service("db-vertica-staging-refresh") {
    include vertica::staging_refresh
  }

  if has_service("db-vertica-client") {
    include vertica::client
  }

  if has_service("db-vertica-dataservice") {
    include vertica::dataservice
  }

  if has_service("db-vertica-copy-reportsdb") {
    include vertica::copy-reportsdb
  }

  if has_service("db-vertica-admin") {
    include vertica::admin
  }

  if has_service("db-vertica-analytics") {
    include vertica::analytics
  }

  if has_service("tungsten-vertica-slave") {
    include tungsten::replicator
  }

  if has_service("tungsten-mysql-master") {
    include tungsten::replicator
  }

  if has_service("fuel2-production") {
    include vertica::fuel-monitor
  }

  if has_service("dev") {
    include service::dev
  }

  if has_service("roc-charts") {
    include service::roc-charts
  }

  if has_service("model-perf-stats") {
    include service::model-perf-stats
  }

  if has_service("model-refresh") {
    include service::model-refresh
  }

  if has_service("model-refresh2") {
    include service::model-refresh2
  }

  if has_service("activemq") {
    include service::activemq
  }

  if has_service("memcache") {
    include service::memcache
  }

  if has_service("cdt") {
    include cdt::base
  }

  if has_service("selenium") {
    include service::selenium
  }

  if has_service("adtester") {
    include service::adtester
  }

  if has_service("citrusleaf") {
    include citrusleaf::base
  }

  if has_service("cyclops") {
    include service::cyclops
  }

  if has_service("apollo-git") {
    include service::apollo-git
  }

  if has_service("fantrack") {
    include service::fantrack
  }

  if has_service("openmanage") {
    include service::openmanage
  }

  if has_service("budget-manager") {
    include budgetmanager::master
    include rocketfuel::budget-manager
  }

  if has_service("local-budget-manager") {
    include budgetmanager::local
  }

  if has_service("stats-aggregate-server") {
    include statsaggregator
  }

  if has_service("real-time-bidder") {
    include service::real-time-bidder
    include os::swapoff
    include graphite::pstats
  }

  if has_service("real-time-bidder-apx") {
  }

  if has_service("regulus") {
    include rocketfuel::regulus
  }

  if has_service("skyline") {
    include skyline::base
  }

  if has_service("winhandler") {
    include winhandler::base
  }

  if has_service("user-bid-cache") {
    if $services =~ /memcached/ {
      include rocketfuel::memcached::server
    } else {
      include winhandler::base
    }
  }

  if has_service("dco-selection-service") {
    include rocketfuel::dco-selection-service
  }

  if has_service("ad-admin-apx") {
  }

  if has_service("nfs-server-hadoop") {
    include service::nfs-server-hadoop
  }

  if has_service("nfs-client-hadoop") {
    include service::nfs-client-hadoop
  }

  if has_service("collectd") {
    include collectd::server
  }

  if !has_service("collectd") {
    include collectd::node
  }

  if has_service("git") {
    #include git::gerrit::master
    #include git::server
    include collectd::node
  }
  else {
    include git::base
  }

  if has_service("gerrit-slave") {
    include git::gerrit::slave
  }

  if has_service("site-kickstart") and (!has_service("puppet4-pilot")) {
    include service::tftp
  }
  if has_service("site-kickstart") {
    include service::dhcp
  }

  if has_service("etl-data-proc") {
    include grid::etl-data-proc::etl-nagios-checks
    include grid::etl-data-proc::etl
  }

  if has_service("lsv-etl-data-proc") {
    include grid::lsv-etl-data-proc::lsv-etl
    include grid::lsv-etl-data-proc::lsv-etl-nagios-checks
  }

  if has_service("lsv-rtd-hailstorm") {
    include grid::lsv-rtd-hailstorm::lsv-rtd-hailstorm
  }

  if has_service("inw-etl-dashboard") {
    include grid::inw-etl-dashboard::base
  }

  if has_service("etl-dashboard-ui") {
    include grid::etl-dashboard-ui::base
  }

  if has_service("lsv-etl-dashboard") {
    include grid::lsv-etl-dashboard::base
  }

  if has_service("lsv-etl-misc") {
    include grid::lsv-etl-data-proc::misc
  }

  if has_service("qa-rfiserver-checks") {
    include rocketfuel::qa-rfiserver-checks::qa-nagios-checks
  }

  if has_service("hadoop2Master") {
    include grid::hadoop2::master
    include os::swapoff
  }

  if has_service("hdfsMaster") {
    if !has_yarn() {
       fail("Installing yarn master on a non yarn cluster")
    }
    include yarn::hadoop::master
    include os::swapoff
  }

  if has_service("resourcemanager") or has_service("yarn-rm1") or has_service("yarn-rm2") {
    include yarn::hadoop::resourcemanager
  }

  if has_service("historyserver") {
    include yarn::hadoop::historyserver
  }

  if has_service("hahdfs1") or has_service("hahdfs2")  {
    if has_yarn() {
      include yarn::hadoop::hahdfs
    } else {
      include grid::hadoop2::hahdfs
    }
    include os::swapoff
  }

 if has_service("hdfsdu-manager") {
   include grid::hdfsdu::base
 }

  if !has_environment("reserved") {
    if (has_yarn()) {
      include yarn::hadoop::client
    }
  }

  if has_service("httpfsServer") {
    if has_yarn() {
    include yarn::hadoop::httpfs
    } else {
    include grid::hadoop2::httpfs
    }
  }

  if has_service("httpfsServer-test") {
    include grid::hadoop2::httpfs
  }

  if has_service("journalnode")  {
   if has_yarn() {
    include yarn::hadoop::journal
    } else {
    include grid::hadoop2::journal
    }
  }

  if has_service("jobtracker") {
    include grid::hadoop2::jobtracker
  }

  if has_service("white-elephant-server") {
    include grid::whiteelephant::server
    include grid::whiteelephant::executor
  }

  if has_service("hadoop2Worker") {
    if has_yarn() {
      include yarn::hadoop::worker
      include os::swapoff
      if ( has_environment("production") and ( has_cluster("inw-hercules") or has_cluster("lsv-hercules") ) ) {
        include luke::l1service
      } else {
         daemontools::service {
               'l1service':
                  ensure => "absent";
         }
      }
    } else {
      include grid::hadoop2::worker
      include os::swapoff
    }
  }

  if has_service("storm-worker") {
    if ( has_environment("production") and ( has_cluster("inw-hercules") or has_cluster("lsv-hercules") ) ) {
      include luke::l1service
    } else {
       daemontools::service {
             'l1service':
                ensure => "absent";
       }
    }
  }

  if has_service("sparkhs") {
    include yarn::spark::historyserver
  }

  if has_service("tez-ui") {
    include yarn::tez::tez-ui
  }

  if has_service("hadoop2-opsgw") {
    if has_yarn() {
      include yarn::hadoop::gateway
      include yarn::hadoop::ops_gateway
    } else {
      include grid::hadoop2::gateway
      include grid::hadoop2::ops_gateway
    }
  }

  if has_service("yarn-schedimprov-gw") {
    if has_yarn() {
      include yarn::hadoop::gateway
      include yarn::hadoop::sched_improv_proj_gateway
    }
  }

  if has_service("hadoopMaster") {
    include service::hadoopMaster
    include os::swapoff
  }

  if has_service("hadoopWorker") {
    include service::hadoopWorker
    include os::swapoff
  }

  if has_service("hiveMaster") {
    include service::hiveMaster
    if (has_yarn()) {
      include yarn::spark::base
    }
    include grid::hive::logs_cleanup
  }

  if has_service("hiveMaster") or has_service("hueServer") {
    include grid::hive::server2_check
  }

  if has_service("hiveClient") {
   if (has_yarn()) {
      include yarn::hive::worker
      include yarn::spark::base
    } else {
      include service::hiveClient
    }
    include grid::hive::logs_cleanup
  }

  if has_service("hiveTest") {
   if (has_yarn()) {
      include yarn::hive::worker
    } else {
      include service::hiveClient
    }
  }

  if has_service("hiverepl") {
    include grid::hive::repl
  }

  if has_service("hiverepl-lsv2inw") {
    include grid::hive::lsv_to_inw_repl
  }

  if has_service("oozieClient") or has_service("hueServer") {
    include grid::oozie::oozieuser
  }

  if has_service("hueServer") or has_service("hueServerTest") {
    include service::hueServer
    include service::hiveOperations
  }

  if has_service("oozieServer") {
    include service::oozieServer
  }

  if has_service("oozieClient") {
    include grid::oozie::client
  }

  if has_service("mahout") {
    include service::mahout
  }

  if has_service("pigServer") {
    include service::pigServer
  }

  if has_service("hbaseWorker") {
    include service::hbaseWorker
    include os::swapoff
  }

  if has_service("hbaseWorker92") {
    include service::hbaseWorker92
    include os::swapoff
  }

  if has_service("hbaseMaster") {
    include service::hbaseMaster
    include os::swapoff
  }

  if has_service("hbaseMaster92") {
    include service::hbaseMaster92
    include os::swapoff
  }

  if has_service("zookeeperServer") {
    include service::zookeeperServer
  }

  if has_service("stella") {
    include service::stella
  }

  if has_service("rtd-zookeeper") {
    include grid::zookeeper::rtd-zookeeper
  }

  if has_service("rtb-model-refresh") {
    include service::rtb-model-refresh
  }

  if has_service("rtb-large-model-refresh") {
    include service::rtb-large-model-refresh
  }

  if has_service("jenkins-slave") {
    include build::base2
  }

  if has_service("megaraid_sas") {
    include service::megaraid_sas
  }

  if has_service("threeware_sas") {
    include service::threeware_sas
  }

  if has_service("budget-optimizer") {
    include rocketfuel::budget-optimizer
  }

  if has_service("postgres") {
    include postgresql::old
  }

  if has_service("postgres-master") {
    include postgresql::new
    include postgresql::master
  }

  if has_service("devops") {
    include devops::base
    include redis::devops
  }

  if has_service("devops-gw") {
    include devops-gw::base
  }

  if has_service("ldap-master") {
    include ldap::master
  }

  if has_service("ldap-master-new") {
    include ldap::master
    include ldap::pwm
  }

  if has_service("ldap-staging") {
    include ldap::server
  }

  if has_service("db-master-ha") {
    include service::db-master-ha
  }

  if has_service("db-master-lsv") {
    include mysql::rfi-master
  }

  if has_service("db-master-lsv-standby") {
    include mysql::rfi-master
  }

  if has_service("db-master-inw") {
    include mysql::rfi-master
  }

  if has_service("db-master-inw-standby") {
    include mysql::rfi-master
  }

  if has_service("db-master-ha-lsv") {
    include service::db-master-ha-lsv
  }

  if has_service("linux-ha-a") {
    include service::linux-ha-a
  }

  if has_service("linux-ha-b") {
    include service::linux-ha-b
  }

  if has_service("graphite") {
    include graphite::server
    include graphite::client
  }

  if ($location != "XXX") {
    include graphite::client
    include devops::dt-monitor
    if ($lsbmajdistrelease == "6") {
      include devops::rfi_info::rfi_info_collector
    }
    if ($lsbmajdistrelease == "6") {
        include logstash::agent_240
    }
    include ruby::packages
  }

  if has_service("fuel-demo") {
    include fuel::apps::demo
  }

  if has_service("fuel-labs") {
    include fuel::apps::labs
  }

  if has_service("botfinder-staging") {
    include botfinder::staging
  }

  if has_service("botfinder-production") {
    include botfinder::production
  }

  if has_service("fuel2-dev") {
    include fuel2::apps::dev
  }

  if has_service("fuel2-qa") {
    include fuel2::apps::qa
  }

  if has_service("fuel2-demo") {
    include fuel2::apps::demo
  }

  if has_service("fuel2-sandbox") {
    include fuel2::apps::sandbox
  }
  if has_service("fuel2-labs") {
    include fuel2::apps::labs
  }

  if has_service("fuel2-staging") {
    include fuel2::apps::staging
  }

  if has_service("fuel2-beta") {
    include fuel2::apps::beta
  }

  if has_service("fuel2-production") {
    include fuel2::apps::production
  }

  if has_service("analytics-dev") {
    include analytics::apps::dev
  }

  if has_service("analytics-qa") {
    include analytics::apps::qa
  }

  if has_service("analytics-demo") {
    include analytics::apps::demo
  }

  if has_service("analytics-sandbox") {
    include analytics::apps::sandbox
  }

  if has_service("analytics-labs") {
    include analytics::apps::labs
  }

  if has_service("analytics-staging") {
    include analytics::apps::staging
  }

  if has_service("analytics-beta") {
    include analytics::apps::beta
  }

  if has_service("analytics-production") {
    include analytics::apps::production
  }

  if has_service("missioncontrol-dev") {
    include missioncontrol::apps::dev
  }

  if has_service("missioncontrol-qa") {
    include missioncontrol::apps::qa
  }

  if has_service("missioncontrol-demo") {
    include missioncontrol::apps::demo
  }

  if has_service("missioncontrol-sandbox") {
    include missioncontrol::apps::sandbox
  }

  if has_service("missioncontrol-labs") {
    include missioncontrol::apps::labs
  }

  if has_service("missioncontrol-staging") {
    include missioncontrol::apps::staging
  }

  if has_service("missioncontrol-production") {
    include missioncontrol::apps::production
  }

  if has_service("orion-dev") {
    include orion::apps::dev
  }

  if has_service("orion-qa") {
    include orion::apps::qa
  }
  if has_service("orion-beta") {
    include orion::apps::beta
  }

  if has_service("orion-staging") {
    include orion::apps::staging
  }

  if has_service("orion-production") {
    include orion::apps::production
  }

  if has_service("orion-demo") {
    include orion::apps::demo
  }

  if has_service("orion-sandbox") {
    include orion::apps::sandbox
  }

  if has_service("rtstats") {
    include rtstats::server
  }

  if has_service("redis") or has_service("redis-standalone") {
    include redis::master
  }

  if has_service("redis-bid_sync-master") {
    include redis::bid_sync2::master
  }

  if has_service("redis-dev-bid_sync-master") {
    include redis::bid_sync2::master
  }

  if has_service("redis-bidperf-bid_sync-master") {
    include redis::bid_sync2::master
  }

  if has_service("redis-bid-sync") {
    include redis::bid_sync
  }

  if has_service("redis-slave") {
    include redis::slave
  }

  if has_service("redis-multislave") {
    include redis::multislave
  }

  # ospf phase out - GC-7643
  include ospf::absent

  if has_service("snmp-monitor") {
    include collectd::snmp
  }

  if has_service("site-router") {
    include network::meshping
  }

  if has_service("site-router-backup") {
    include network::meshping
  }

  if has_service("mongo-server") {
    include mongo::server
  }

  if has_service("storm-master") {
    include yarn::storm::master
 }

  if has_service("storm-ui") {
    include yarn::storm::ui
 }

  if has_service("storm-worker") {
    include yarn::storm::worker
 }

  if has_service("kafka-broker") {
    include kafka::base
  }

  if has_service("kafka-manager"){
    include kafka::manager
  }

  if has_service("gerrit") {
    include gerrit::base
  }

  if has_service("real-time-bidder") or has_service("adserver") or has_service("regulus") {
    include devops::unclean
    include devops::lander
    include devops::orbiter
    include devops::v-monitor
    include devops::log_monitor
  }

  if has_service("tuned-bidder") {
    include tuners::isolcpu
  }

  if has_service("redis-cache") {
    include redis::cache
  }

  if has_service("logstash-prod") {
    include elasticsearch::logstash
    include logstash::indexer
    include logstash::agent_240
  }

  if has_service("elk-master") {
    include elasticsearch::logstash
    include logstash::agent_240
  }

  if has_service("elk-client") {
    include elasticsearch::logstash
    include logstash::agent_240
  }

  if has_service("logstash-stage") {
    include elasticsearch::logstash
    include logstash::indexer
    include logstash::agent_240
  }

  if has_service("kibana-stage") {
    include kibana::kibana
  }

  if has_service("kibana-prod") {
    include kibana::kibana
  }

  if has_service("pixelchecker") {
    include pixelchecker::base
  }

  if has_service("si-nagios-summary") {
    include si-nagios-summary::base
  }

  if has_service("pixelcrawler-dashboard") {
    include pixelcrawlerdashboard::base
  }

  if has_service("adserverproxy") {
    include serverproxy::base
  }

  if has_service("bidderproxy") {
    include bidderproxy::base
  }

  if has_service("solr") {
    include solr::tcollector
  }

  if has_service("fish"){
    include fish::tcollector
  }
  if has_service("fishnet"){
    include fishnet::base
  }

  if has_service("http-fwd-misc") {
    include httpd::httpfwdmisc
  }

  if has_service("jira") {
    include atlassian::jira
  }

  if has_service("jira-beta") {
    include postgresql::new
  }

  if has_service("confluence") {
    include atlassian::confluence
  }

  if has_service("data-proc") {
    if $hostname == "inw-15" {
      include storm::user
    }
  }

  if has_service("anti-redis-slave") {
    include redis::anti-slave
  }

  if has_service("nexus") {
    include nexus::base
  }

  if has_service("redis-budget-master") {
    include redis::budget::master_pair
  }

  if has_service("redis-delivery_stats-master") {
    include redis::delivery_stats::master_pair
  }

  if has_service("redis-local_budget-master") {
    include redis::local_budget::master
  }

  if has_service("redis-dev-local_budget-master") {
    include redis::local_budget::master
  }

  if has_service("redis-bidperf-local_budget-master") {
    include redis::local_budget::master
  }

  if has_service("redis-delivery_stats_aggregator-master") {
    include redis::delivery_stats_aggregator::master
  }

  if has_service("redis-dev-delivery_stats_aggregator-master") {
    include redis::delivery_stats_aggregator::master
  }

  if has_service("redis-bidperf-delivery_stats_aggregator-master") {
    include redis::delivery_stats_aggregator::master
  }

  if has_service("redis-delivery_stats-slave") {
    if ($location == "pnc") {
      include redis::delivery_stats::slave_step
    } else {
      include redis::delivery_stats::slave_normal
    }
  }

  if has_service("anti-redis-budget-master") {
    include redis::budget::anti_master_pair
  }

  if has_service("anti-redis-budget-slave") {
    include redis::budget::anti_slave
  }

  if has_service("redis-budget-slave") {
    include redis::budget::slave
  }

  if has_service("redis-bid-sync-slave") {
    include redis::bid_sync_slave
  }

  if has_service("redis-bid_sync-slave") {
    include redis::bid_sync2::slave
  }

  if has_service("peer_test") {
    include qa::peer_test
  }

  if has_service("usersim") {
    include qa::usersim
  }

  if has_service("jenkins-master") {
    include build::master
    include user::jenkins-master
  } else {
    include user::jenkins-normal
  }

  if has_service("rfi_info") {
    include devops::rfi_info
  }

  if has_service("opengrok") {
    include devops::opengrok
  }

  if has_service("model-building-env") {
    include user::perseus
    include rocketfuel::model::model-building-env
  }

  if has_service("model-building") {
     if ($location == "lsv") {
       include rocketfuel::model::lsv-model-building
    } else {
       include rocketfuel::model::model-building
    }
  }

  if has_service("athena-model-building") {
    include rocketfuel::model::athena-model-building
  }

  if has_service("perseus") {
    include user::perseus
    if ($location == "lsv") {
      include rocketfuel::model::perseus
    } else {
      include rocketfuel::model::inw-perseus
    }
  }

  if has_service("opentsdb") {
    include opentsdb::tsdb
    include opentsdb::varnish
  }

  if has_service("opentsdb-ro") {
    include opentsdb::tsdb
    include opentsdb::varnish
  }

  if has_service("statuswolf") {
    include opentsdb::statuswolf
  }

 if has_service("hannibal") {
    include grid::hbase92::hannibal
  }

  if has_service("huahin-manager") {
    include grid::huahinmanager::init
  }

  if has_service("calvin") {
    include modeling::calvin
  }

  if has_service("unravel") {
    include unravel::base
  }

  if has_service("datamon") {
    include ei::datamon
  }

  if has_service("mobile-data-proc") {
    include mobile::mobile-data-proc
  }

  if has_service("mobile-clustering") {
    include mobile::mobile-clustering
  }

  if has_service("mobile-data-proc-lsv") {
    include mobile::mobile-data-proc-lsv
  }

  if has_service("mobile-clustering-lsv") {
    include mobile::mobile-clustering-lsv
  }

  if has_service("localsim") {
    include ei::localsim
  }

  if has_service("dashing") {
    include dashing::base
  }

  if has_service("git-mirror") {
    include git-mirror::base
  }

  if has_service("sonar") {
    include sonar::base
  }

  if has_service("onlinestore-stats-manager") {
    include grid::deathstar::stats-manager
  }

  if has_service("blackbird-gateway") {
    include grid::hbase92::blackbird-gateway
  }

  if has_service("onlinestore-ssv-service") {
    include grid::deathstar::onlinestore-ssv-service
  }

  if has_service("audit") {
    include rocketfuel::audit
    include devops::v-monitor
  }

  if has_service("restriction") {
    include rocketfuel::restriction
    include devops::v-monitor
  }

  if has_service("video") {
    include rocketfuel::video
    include devops::v-monitor
  }

  if has_service("diagnosis") {
    include rocketfuel::diagnosis
    include devops::v-monitor
  }

  if has_service("ai") {
    include rocketfuel::ai
    include devops::v-monitor
  }

  if has_service("facebook") {
    include rocketfuel::facebook
    include devops::v-monitor
  }

  if has_service("auth") {
    include rocketfuel::auth
  }

  if has_service("baogao") {
    include rocketfuel::baogao
    include devops::v-monitor
  }

  if has_service("adpreview") {
    include rocketfuel::adpreview
    include devops::v-monitor
  }

  if has_service("macro") {
    include rocketfuel::macro
    include devops::v-monitor
  }

  if has_service("jobs") {
    include rocketfuel::jobs
  }

  if has_service("modeling-uploader") {
    include rocketfuel::modeling-uploader
  }

  if has_service("api-gateway") {
    include rocketfuel::api-gateway
  }

  if has_service("api-proxy") {
    include rocketfuel::api-proxy
  }

  if has_service("dataexchange-bulkload") {
    include rocketfuel::dataexchange::dataexchange-bulkload
  }

  if has_service("dataver") {
    include qa::dataver
  }

  if has_service("servermon") {
    include qa::servermon
  }

  if has_service("nimbus_metrics") {
    include grid::nimbus_metrics::init
  }

  if has_service("epiphany") {
    include grid::epiphany::epiphany
    include grid::epiphany::dashboard
  }

  if has_service("externalreport") {
    if ($location == "lsv") {
      include yarn::spark::base
    }
    include grid::externalreport::externalreport
    include grid::externalreport::externalreport-nagios-checks
  }

  if has_service("externalreport-test") {
    if ($location == "lsv") {
      include yarn::spark::base
    }
    include grid::externalreport::externalreport-test
  }

  if has_service("rtd-transducer") {
    include grid::rtd-transducer::rtd-transducer
  }

  if has_service("altair") {
    include altair::base
  }

  if has_service("demeter") {
    include dynamic_creative::demeter
  }

  if has_service("demeter-cron") {
    include dynamic_creative::demeter-cron
  }

  if has_service("persephone") {
    include dynamic_creative::persephone
  }

  if has_service("tailored-audiences") {
    include rocketfuel::tailored-audiences
  }

  if has_service("metric-transform") {
    include metric-transform::service
  }

  if has_service("zipkin") {
      include zipkin::collector
      include zipkin::query
      include zipkin::web
  }

  if has_service("ddclient") {
      include ddclient::base
  }

  if has_service("stgkeyhole") {
      include redis::keyhole
      include keyhole::stage::base
  }

  if has_service("keyhole") {
      include redis::keyhole
      include keyhole::base
  }

  if has_service("bcp_devops") {
      include bcp_devops::base
      include redis::bcp_devops
  }

  if has_service("bcp_gerrit") {
      include bcp_gerrit::base
      include splunk::forwarder
  }

  if has_service("bcp_nexus") {
      include bcp_nexus::base
  }

  if has_service("bcp_opengrok") {
      include bcp_opengrok::base
  }

  if has_service("bcp_gitpaste") {
      include bcp_gitpaste::base
  }

  if has_service("bcp_servercheck") {
      include bcp_servercheck::base
  }

  if has_service("bcp_sonar") {
      include bcp_sonar::base
  }

  if has_service("bcp_grack") {
      include bcp_grack::base
  }

  if has_service("bcp_kibana-ruby") {
      include bcp_kibana-ruby::base
  }

  if has_service("nagira") {
      include nagira::base
  }

  if has_service("graphite-haproxy") {
      include graphite-haproxy::base
  }

  if has_service("haproxy-apps-dev") {
      include haproxy-apps-dev::base
  }

  if has_service("npm-sinopia"){
      include npm-sinopia::base
  }

  if has_service("secmon") {
      include security::secmon
  }

  if has_service("clock") {
      include ntp::clock
  }
  if has_service("dragnet") {
    include rocketfuel::dragnet
    include devops::v-monitor
  }

  if has_service("crawler") {
    include rocketfuel::crawler
    include devops::v-monitor
  }

  if has_service("spiderstat") {
    include rocketfuel::spiderstat
    include devops::v-monitor
  }

  if has_service("alice") {
    include rocketfuel::alice
    include devops::v-monitor
  }

  if has_service("data-retention") {
    include yarn::tools::retention
    include yarn::data-retention::retention
  }

  if has_service("brand-ag-modeling") {
    include brand::ag_modeling::co
  }

  if has_service("brand-ag-reporting") {
    include brand::ag_reporting::services
  }

  if has_service("brand-veenome") {
    include brand::veenome::services
  }

  if has_service("audience-service") {
    include grid::audience-service
  }

  if has_service("approval-check") {
    include bcp_gerrit::approval-check
  }

  if has_service("owner-check") {
    include ei::owner-check
  }

  if has_service("iplookup") {
    include rocketfuel::iplookup
    include devops::v-monitor
  }

  if has_service("dbcache") {
    include rocketfuel::dbcache
    include devops::log_monitor
    include devops::unclean
    include devops::v-monitor
  }

  if has_service("log-collector") {
    include redis::log_collector
    include rocketfuel::error-log-alert
  }

  if has_service("seshat") {
    #Break this down further into individual service if need comes
    if ( has_environment("production") ) {
      include seshat::rest
      include seshat::webapp
      include seshat::dbserver
      include seshat::dataaggregation
    } elsif ( has_environment("dev") ) {
      include seshat::rest
      include seshat::webapp
      include seshat::dataaggregation
    }
  }

  if has_service("luke-squeeze") {
    include luke::squeeze
  }

  if has_service("luke-ops") {
    include luke::ops
  }

  #TODO(shrijeet): At some point we should rename the DNS name to l2service
  if has_service("luke-pageservice") {
    include luke::l2service
  }

  if has_service("slider") {
    include grid::slider::base
  }

  if has_service("deathstar") {
    include grid::deathstar::base
  }

  if has_service("helios") {
    include grid::deathstar::helios
  }

  if has_service("opentsdb-manager") {
    include opentsdb::manager
  }

  if has_service("phoneutria") {
    include dynamic_creative::phoneutria
  }

  if has_service("dp-dev-gateway") {
    include grid::dp-dev-gateway::grid-conf
  }

  if has_service("graphite-store") {
    include graphite::cluster::store
  }

  if has_service("graphite-relay") {
    include graphite::cluster::relay
  }

  if has_service("graphite-haproxy-cluster") {
    include graphite::cluster::haproxy
  }

  if has_service("graphite-web") {
    include graphite::cluster::webapp
  }

  if has_service("grid-origin-gateway") {
    include grid::origin::gateway
  }

  if has_service("server-etl"){
    include server_etl::base
  }

  if has_service("gcdash-staging") {
    include gcdash::staging
  }

  if has_service("rocketSpider") {
    include rocketspider::base
  }

  if has_service("rocketScanner") {
    include rocketscanner::base
  }

  if has_service("sftp-dynamicc") {
    include sftp::server
  }

 if has_service("adops-tools") {
   include httpd::common
  }

 if has_service("dbcache") {
   include dbcache::base
   include dbcache::monitor
  }

 if has_service("optimization") {
    include yarn::tools::retention
    if ($location == "lsv") {
      include rocketfuel::model::optimization-crons
    }
 }

  if has_service("scheduled-report-controller"){
    include grid::scheduled-report-controller::init
  }

  if has_service("dmp-scrubplus"){
    include grid::dmp::mestor::init
    include grid::dmp::scrubplus::init
  }

  if has_service("quasar") {
    include grid::quasar::base
  }

  if has_service("keychain") {
    include keychain::base
  }

  if has_service("ssvadapter") {
    include grid::dmp::ssvadapter::base
  }

  if has_service("acceptscookie") {
    include grid::dmp::acceptscookie::base
  }

  if has_service("crossdevice_syndication") {
    include grid::dmp::crossdevice_syndication::base
  }

  if has_service("facebook_syndication") {
    include grid::dmp::facebook_syndication::base
  }

  if has_service("dayclose") {
    include grid::dmp::dayclose::base
  }

  if has_service("context-broker") {
    include contextbroker::service
    include graphite::pstats
  }

  if has_service("dvuploader") {
    include dvuploader::service
  }

  if ($location == "pnc") or ($location == "tca") or ($location == "fra") or ($location == "lax") or ($location == "ewr") or ($location == "sjc") or ($location == "eqv") or ($location == "inw" )  or ($location == "lsv") {
    if !has_service("ossec") {
    include ossec::agent
    }
  }

  if has_service("hiveAnalytics") {
    include service::hiveAnalytics
  }

  if has_service("hiveMetricsdb") {
    include yarn::hive::metricsdb
  }

  if has_service("user-onboarding") {
    include httpd::base
    include onboarding::vhost
  }

  if has_service("hiveNotification") {
    include service::hiveNotification
  }

  if has_service("appsmon") {
    include appsmon::base
  }

  if has_service("c2-origin") {
    include httpd::c2-origin
  }

  if has_service("bcp_household_pipeline") {
    include mobile::bcp_household_pipeline
  }

  if has_service("bcp_mobile_app_repo_pipeline") {
    include mobile::bcp_mobile_app_repo_pipeline
  }

  if has_service("ldappass") {
    include ldappass::base
  }

  if has_service("package-mirror") or has_service("package-master") {
    include yum::mrepo-monitor
  }

  if has_service("bcp_xd_reports_pipeline") {
    include mobile::bcp_xd_reports_pipeline
  }

  if has_service("ldapadmin") {
    include ldapadmin::base
    include ldaphaproxy::base
  }

  if has_service("rt-modeling") {
    include rocketfuel::model::rt-modeling
  }

  if has_service("bt-modeling") {
    include rocketfuel::model::bt-modeling
  }

  if has_service("ossec") {
    include rsyslog::base
  }

  if has_service("pixel-monitor") {
    include pixel-monitor::service
  }

  if has_service("dr-elephant") {
    include yarn::hadoop::drelephant
  }

  if has_service("modeleval") {
    include modeleval::base
  }

  if has_service("restrictioneval") {
    include restrictioneval::base
  }

  if has_service("db-vgc-monitor") {
    include mysql::db-vgc-monitor
   }

  if has_service("rundeck") {
    include rundeck::server
  }

  if has_service("timelineserver") {
    include yarn::hadoop::timelineserver
  }

  if has_service("snaplogic") {
    include java::jdk
  }

  if has_service("haproxy-iwsclient") or has_service("iwsproxy") {
    include haproxy::iwsclient
  }

  if has_service("service-haproxy") {
    include service-haproxy::base
  }

  if has_service("gc-dashboards") {
    include gc-dashboards::base
  }

  if has_service("marvel") {
    include elasticsearch::logstash
    include kibana::kibana
    include logstash::agent_240
  }

  if has_service("origin-lsv") {
    include origin-lsv::base
  }

  if has_service("origin-qa") {
    include origin-lsv::qa
  }

  if has_service("origin-demo") {
    include origin-inw::demo
  }

  if has_service("origin-sandbox") {
    include origin-lsv::sandbox
  }

  if $boardmanufacturer == 'Dell Inc.' {
    notice("Looks like a Dell Machine !!")
    include yum::dellrepo
  } else {
    include yum::dellrepo_remove
  }

  if $interfaces =~ /bond\d.*/ {
    notice("Looks like a machine with Bonding adapter !!")
    include opentsdb::network-bonding-stats
  }

  if has_service("x-ssv") {
    include smartserve::base
  }

  if has_service("x-ssvwr") {
    include dmp-ssvwr::base
  }

  if has_service("x-util") {
    include dmp-util::base
  }

  if has_service("x-etl") {
    include dmp-etl::base
  }

  if has_service("x-cgd") {
    include dmp-cgd::base
  }

  if has_service("dmp-demo") {
    include origin-lsv::dmp-demo
  }

  if has_service("dmp-custom-segment-manager") {
    include grid::dmp::hdfs::init
  }

 if has_service("dmp-prod") {
   include dmp-compat::base
   include origin-lsv::dmp-prod
  }

  if has_service("converged-ssv") {
    include java::jdk
  }

# pulling the ldapclient::base from all systems - it prevents creation of new users GC-14225
#  if ( ( has_service("real-time-bidder") and  $location == "sjc" ) or ( !has_environment("production") and $location != "xchi" ) )  {
#    include ldapclient::client
#  } 
#  else {
    include rldapclient::base
#  }

  if has_service("dmp-citi") {
    include origin-lsv::dmp-citi
  }

  if has_service("dmp-sandbox") {
    include origin-lsv::dmp-sandbox
  }

  if has_service("dmp-staging") {
    include origin-lsv::dmp-staging
  }

  if has_service("dmp-tpdmaint") {
    include origin-lsv::dmp-tpdmaint
  }

#  if has_service("ewrupgrade") {
#    include network::ewrupgrade
#  } else {
#    include network::ewrupgradedone
#  }

  if has_service("inwupgrade") {
    include network::inwupgrade
  } else {
    include network::inwupgradedone
  }

  if has_service("x-vertica") {
    include dmp-vertica::base
  }

  if has_service("x-vertica-lb") {
    include dmp-vertica::lb
  }

  if has_service("dmp-discover") {
    include dmp-discover::base
  }
  
  if has_service("dmp-apps") {
    include dmp-apps::base
  }

  if has_service("logfile-reporting-manager") {
    include grid::logfile-reporting::manager
  }
}
