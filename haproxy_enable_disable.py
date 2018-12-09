import os
import sys
from pssh.clients import ParallelSSHClient
import logging

def run(haproxy, cmd, bg, backend):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(haproxy)
  client.run_command(cmd, stop_on_errors=False)
  for h in haproxy:
    if 'disable' in cmd:
      print 'On proxy %s, %s is set to MAINT mode for %s!' % (h, backend, bg)
    elif 'enable' in cmd:
      print 'On proxy %s, %s is set to ACTIVE mode for %s!' % (h, backend, bg)

def main():
  args = sys.argv[1:]
  usage = ('Usage: haproxy_enable_disable.py [ACTION] [COLO] [CLUSTER]\n'
           'Example - batch: haproxy_enable_disable.py [enable|disable] [snc|dub|snc] [c1|c2|c3|c4]\n'
           'Example - Trans: haproxy_enable_disable.py [enable|disable] [snc|dub|sac] [c1_tx|c2_tx]')
  if not args or len(args) < 3:
    print usage 
    sys.exit(1)     
  path = '/usr/local/lib/haproxyctl/haproxyctl'
  haproxyctl = os.path.abspath(path)

  ####################################################SNC################################################
  haproxy_snc = []
  msys_group_snc_c1 = {}
  msys_group_snc_c2 = {}
  msys_group_snc_tx_c1 = {}
  msys_group_snc_tx_c2 = {}
  
  msys_group_snc_tx_c1['msys_transactional'] = ['email-msys-trans1', 'email-msys-trans2', 'email-msys-trans3']
  msys_group_snc_tx_c1['msys_unclean'] = ['email-msys-trans1', 'email-msys-trans2', 'email-msys-trans3']
  
  msys_group_snc_tx_c2['msys_transactional'] = ['email-msys-trans4', 'email-msys-trans5', 'email-msys-trans6']
  msys_group_snc_tx_c2['msys_unclean'] = ['email-msys-trans4', 'email-msys-trans5', 'email-msys-trans6']

  msys_group_snc_c1['msys_mx'] = ['email-msys31', 'email-msys32', 'email-msys33']
  msys_group_snc_c1['msys_co'] = ['email-msys28', 'email-msys29', 'email-msys30']
  msys_group_snc_c1['msys_cl'] = ['email-msys25', 'email-msys26', 'email-msys27']
  msys_group_snc_c1['msys_pe'] = ['email-msys32', 'email-msys33', 'email-msys34']
  msys_group_snc_c1['msys'] = ['email-msys25', 'email-msys26', 'email-msys27',
                               'email-msys28', 'email-msys29', 'email-msys30',
                               'email-msys31', 'email-msys32', 'email-msys33', 'email-msys34']

  msys_group_snc_c2['msys_mx'] = ['email-msys41', 'email-msys42', 'email-msys43']
  msys_group_snc_c2['msys_co'] = ['email-msys38', 'email-msys39', 'email-msys40']
  msys_group_snc_c2['msys_cl'] = ['email-msys35', 'email-msys36', 'email-msys37']
  msys_group_snc_c2['msys_pe'] = ['email-msys42', 'email-msys43', 'email-msys44']
  msys_group_snc_c2['msys'] = ['email-msys35', 'email-msys36', 'email-msys37',
                               'email-msys38','email-msys39', 'email-msys40',
                              'email-msys41', 'email-msys42', 'email-msys43', 'email-msys44']

  for i in range(8):
    haproxy_snc.append('mta-haproxy' + str(i + 1) + '.snc1')

  #################################################SAC################################################
  haproxy_sac = []
  msys_group_sac_c1 = {}
  msys_group_sac_c2 = {}
  msys_group_sac_tx_c1 = {}
  msys_group_sac_tx_c2 = {}

  msys_group_sac_tx_c1['msys_transactional'] = ['email-msys-trans10', 'email-msys-trans11', 'email-msys-trans12']
  msys_group_sac_tx_c1['msys_unclean'] = ['email-msys-trans10', 'email-msys-trans11', 'email-msys-trans12']

  msys_group_sac_tx_c2['msys_transactional'] = ['email-msys-trans20', 'email-msys-trans21', 'email-msys-trans22']
  msys_group_sac_tx_c2['msys_unclean'] = ['email-msys-trans20', 'email-msys-trans21', 'email-msys-trans22']

  msys_group_sac_c1['msys_mx'] = ['email-msys16', 'email-msys17', 'email-msys18']
  msys_group_sac_c1['msys_co'] = ['email-msys13', 'email-msys14', 'email-msys15']
  msys_group_sac_c1['msys_cl'] = ['email-msys10', 'email-msys11', 'email-msys12']
  msys_group_sac_c1['msys_pe'] = ['email-msys17', 'email-msys18', 'email-msys19']
  msys_group_sac_c1['msys'] = ['email-msys10', 'email-msys11', 'email-msys12',
                               'email-msys13', 'email-msys14', 'email-msys15',
                               'email-msys16', 'email-msys17', 'email-msys18', 'email-msys19']


  msys_group_sac_c2['msys_mx'] = ['email-msys26', 'email-msys27', 'email-msys28']
  msys_group_sac_c2['msys_co'] = ['email-msys23', 'email-msys24', 'email-msys25']
  msys_group_sac_c2['msys_cl'] = ['email-msys20', 'email-msys21', 'email-msys22']
  msys_group_sac_c2['msys_pe'] = ['email-msys27', 'email-msys28', 'email-msys29']
  msys_group_sac_c2['msys'] = ['email-msys20', 'email-msys21', 'email-msys22',
                               'email-msys23','email-msys24', 'email-msys25',
                              'email-msys26', 'email-msys27', 'email-msys28', 'email-msys29']

  for i in range(6):
    haproxy_sac.append('mta-haproxy' + str(i + 1) + '.sac1')

  ############################DUB################################################
  haproxy_dub = []
  msys_group_dub_c1 = {}
  msys_group_dub_c2 = {}
  msys_group_dub_c3 = {}
  msys_group_dub_c4 = {}
  msys_group_dub_tx_c1 = {}
  msys_group_dub_tx_c2 = {}

  msys_group_dub_tx_c1['msys_doi'] = ['email-msys-trans51', 'email-msys-trans52']
  msys_group_dub_tx_c1['msys_welcome'] = ['email-msys-trans50', 'email-msys-trans51', 'email-msys-trans52']
  msys_group_dub_tx_c1['msys_transactional'] = ['email-msys-trans50', 'email-msys-trans51', 'email-msys-trans52']
  msys_group_dub_tx_c1['msys_transactional1'] = ['email-msys-trans50', 'email-msys-trans51']
  msys_group_dub_tx_c1['msys_transactional2'] = ['email-msys-trans50', 'email-msys-trans52']
  msys_group_dub_tx_c1['msys_unclean'] = ['email-msys-trans51', 'email-msys-trans52'] 
  
  msys_group_dub_tx_c2['msys_doi'] = ['email-msys-trans61', 'email-msys-trans62']
  msys_group_dub_tx_c2['msys_welcome'] = ['email-msys-trans60', 'email-msys-trans61', 'email-msys-trans62']
  msys_group_dub_tx_c2['msys_transactional'] = ['email-msys-trans60', 'email-msys-trans61', 'email-msys-trans62']
  msys_group_dub_tx_c2['msys_transactional1'] = ['email-msys-trans60', 'email-msys-trans61']
  msys_group_dub_tx_c2['msys_transactional2'] = ['email-msys-trans60', 'email-msys-trans62']
  msys_group_dub_tx_c2['msys_unclean'] = ['email-msys-trans61', 'email-msys-trans62']

  msys_group_dub_c1['msys_sg'] = ['email-msys83', 'email-msys84']
  msys_group_dub_c1['msys_my'] = ['email-msys86', 'email-msys87']
  msys_group_dub_c1['msys_jp'] = ['email-msys86', 'email-msys87']
  msys_group_dub_c1['msys_ar'] = ['email-msys80', 'email-msys81']
  msys_group_dub_c1['msys_ae'] = ['email-msys87', 'email-msys88']
  msys_group_dub_c1['msys_il'] = ['email-msys87', 'email-msys88']
  msys_group_dub_c1['msys_ie'] = ['email-msys87', 'email-msys88']
  msys_group_dub_c1['msys_nz'] = ['email-msys83', 'email-msys84']
  msys_group_dub_c1['msys_nl'] = ['email-msys88', 'email-msys89']
  msys_group_dub_c1['msys_ca'] = ['email-msys86', 'email-msys89']
  msys_group_dub_c1['msys_hk'] = ['email-msys81', 'email-msys82']
  msys_group_dub_c1['msys_br'] = ['email-msys86', 'email-msys87', 'email-msys88']
  msys_group_dub_c1['msys_fr'] = ['email-msys80', 'email-msys81', 'email-msys82', 'email-msys83', 'email-msys84',
                                  'email-msys85']
  msys_group_dub_c1['msys_de'] = ['email-msys82', 'email-msys83', 'email-msys84', 'email-msys85', 'email-msys86',
                                  'email-msys87',  'email-msys88', 'email-msys89']

  msys_group_dub_c2['msys_es'] = ['email-msys94', 'email-msys95']
  msys_group_dub_c2['msys_be'] = ['email-msys96', 'email-msys97', 'email-msys98']
  msys_group_dub_c2['msys_pl'] = ['email-msys97', 'email-msys98', 'email-msys99']
  msys_group_dub_c2['msys_it'] = ['email-msys96', 'email-msys97', 'email-msys98']
  msys_group_dub_c2['msys_uk'] = ['email-msys90', 'email-msys91', 'email-msys92', 'email-msys93']
  msys_group_dub_c2['msys_au'] = ['email-msys90', 'email-msys91', 'email-msys92', 'email-msys93']

  msys_group_dub_c3['msys_sg'] = ['email-msys103', 'email-msys104']
  msys_group_dub_c3['msys_my'] = ['email-msys106', 'email-msys107']
  msys_group_dub_c3['msys_jp'] = ['email-msys106', 'email-msys107']
  msys_group_dub_c3['msys_ar'] = ['email-msys100', 'email-msys101']
  msys_group_dub_c3['msys_ae'] = ['email-msys107', 'email-msys108']
  msys_group_dub_c3['msys_il'] = ['email-msys107', 'email-msys108']
  msys_group_dub_c3['msys_ie'] = ['email-msys107', 'email-msys108']
  msys_group_dub_c3['msys_nz'] = ['email-msys103', 'email-msys104']
  msys_group_dub_c3['msys_nl'] = ['email-msys108', 'email-msys109']
  msys_group_dub_c3['msys_ca'] = ['email-msys106', 'email-msys109']
  msys_group_dub_c3['msys_hk'] = ['email-msys101', 'email-msys102']
  msys_group_dub_c3['msys_br'] = ['email-msys106', 'email-msys107', 'email-msys108']
  msys_group_dub_c3['msys_fr'] = ['email-msys100', 'email-msys101', 'email-msys102', 'email-msys103', 'email-msys104',
                                  'email-msys105']
  msys_group_dub_c3['msys_de'] = ['email-msys102', 'email-msys103', 'email-msys104', 'email-msys105', 'email-msys106',
                                  'email-msys107',  'email-msys108', 'email-msys109']

  msys_group_dub_c4['msys_es'] = ['email-msys114', 'email-msys115']
  msys_group_dub_c4['msys_be'] = ['email-msys116', 'email-msys117', 'email-msys118']
  msys_group_dub_c4['msys_pl'] = ['email-msys117', 'email-msys118', 'email-msys119']
  msys_group_dub_c4['msys_it'] = ['email-msys116', 'email-msys117', 'email-msys118']
  msys_group_dub_c4['msys_uk'] = ['email-msys110', 'email-msys111', 'email-msys112', 'email-msys113']
  msys_group_dub_c4['msys_au'] = ['email-msys110', 'email-msys111', 'email-msys112', 'email-msys113']

  for i in range(12):
    haproxy_dub.append('mta-haproxy' + str(i + 1) + '.dub1')

  ######Conditionals based on user arguments###############

  if args[1] == 'snc' and args[2] == 'c1':
    for bg in msys_group_snc_c1.keys():
      for backend in msys_group_snc_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_snc, cmd, bg, backend)
  
  elif args[1] == 'snc' and args[2] == 'c2':
    for bg in msys_group_snc_c2.keys():
      for backend in msys_group_snc_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_snc, cmd, bg, backend)

  elif args[1] == 'snc' and args[2] == 'c1_tx':
    for bg in msys_group_snc_tx_c1.keys():
      for backend in msys_group_snc_tx_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_snc, cmd, bg, backend)

  elif args[1] == 'snc' and args[2] == 'c2_tx':
    for bg in msys_group_snc_tx_c2.keys():
      for backend in msys_group_snc_tx_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_snc, cmd, bg, backend)

  elif args[1] == 'sac' and args[2] == 'c1':
    for bg in msys_group_sac_c1.keys():
      for backend in msys_group_sac_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)

  elif args[1] == 'sac' and args[2] == 'c2':
    for bg in msys_group_sac_c2.keys():
      for backend in msys_group_sac_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)

  elif args[1] == 'sac' and args[2] == 'c1_tx':
    for bg in msys_group_sac_tx_c1.keys():
      for backend in msys_group_sac_tx_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)

  elif args[1] == 'sac' and args[2] == 'c2_tx':
    for bg in msys_group_sac_tx_c2.keys():
      for backend in msys_group_sac_tx_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)

  elif args[1] == 'dub' and args[2] == 'c1':
    for bg in msys_group_dub_c1.keys():
      for backend in msys_group_dub_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_dub, cmd, bg, backend)

  elif args[1] == 'dub' and args[2] == 'c2':
    for bg in msys_group_dub_c2.keys():
      for backend in msys_group_dub_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_dub, cmd, bg, backend)

  elif args[1] == 'dub' and args[2] == 'c3':
    for bg in msys_group_dub_c3.keys():
      for backend in msys_group_dub_c3[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_dub, cmd, bg, backend)

  elif args[1] == 'dub' and args[2] == 'c4':
    for bg in msys_group_dub_c4.keys():
      for backend in msys_group_dub_c4[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_dub, cmd, bg, backend)
  
  elif args[1] == 'dub' and args[2] == 'c1_tx':
    for bg in msys_group_dub_tx_c1.keys():
      for backend in msys_group_dub_tx_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)

  elif args[1] == 'dub' and args[2] == 'c2_tx':
    for bg in msys_group_dub_tx_c2.keys():
      for backend in msys_group_dub_tx_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        run(haproxy_sac, cmd, bg, backend)
  
  else:
    print usage 


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
