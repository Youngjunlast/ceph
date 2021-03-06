
from mgr_module import MgrModule


class Module(MgrModule):
    COMMANDS = [
        {
            "cmd": "iostat",
            "desc": "Get IO rates",
            "perm": "r",
            "poll": "true"
        },
        {
            "cmd": "iostat self-test",
            "desc": "Run a self test the iostat module",
            "perm": "r"
        }
    ]


    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)


    def handle_command(self, command):
        rd = 0
        wr = 0
        ops = 0
        ret = ''

        if command['prefix'] == 'iostat':
            r = self.get('io_rate')

            stamp_delta = float(r['pg_stats_delta']['stamp_delta'])
            if (stamp_delta > 0):
                rd = int(r['pg_stats_delta']['stat_sum']['num_read_kb']) / stamp_delta
                wr = int(r['pg_stats_delta']['stat_sum']['num_write_kb']) / stamp_delta
                ops = ( int(r['pg_stats_delta']['stat_sum']['num_write']) + int(r['pg_stats_delta']['stat_sum']['num_read']) ) / stamp_delta

            ret = "wr: {0} kB/s, rd: {1} kB/s, iops: {2}".format(int(wr), int(rd), int(ops))

        elif command['prefix'] == 'iostat self-test':
            r = self.get('io_rate')
            assert('pg_stats_delta' in r)
            assert('stamp_delta' in r['pg_stats_delta'])
            assert('stat_sum' in r['pg_stats_delta'])
            assert('num_read_kb' in r['pg_stats_delta']['stat_sum'])
            assert('num_write_kb' in r['pg_stats_delta']['stat_sum'])
            assert('num_write' in r['pg_stats_delta']['stat_sum'])
            assert('num_read' in r['pg_stats_delta']['stat_sum'])
            ret = 'iostat self-test OK'

        return 0, '', ret
