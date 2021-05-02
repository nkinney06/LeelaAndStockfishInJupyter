#!/usr/bin/env python3

import sys
from subprocess import Popen, PIPE

process = Popen(["/usr/bin/nvidia-smi", "--list-gpus"], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

number_gpus = len(output.split(b"\n")) -1

for gpu in range(0, number_gpus):
    print("""[program:lczero{gpu}]
process_name=%(program_name)s_%(process_num)02d
directory=/lczero
command=/usr/bin/nice /lczero/client_linux --backend-opts="cudnn(gpu={gpu})"
user=root
redirect_stderr=true
stdout_logfile=/lczero/log.log
stdout_logfile_maxbytes=100MB
numprocs=1
autostart=true
autorestart=true""".format(gpu=gpu))
