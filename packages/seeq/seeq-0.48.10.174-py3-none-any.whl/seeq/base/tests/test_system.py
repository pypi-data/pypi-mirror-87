import configuration.helpers as conf
import pytest

from seeq.base.system import human_readable_byte_count


@pytest.mark.unit
def test_human_readable_byte_count_base_ten():
    '''
    Make sure we get the same results as SystemInfoTest#testHumanReadableByteCountBaseTen
    '''
    assert human_readable_byte_count(0, False, False) == '0 B'
    assert human_readable_byte_count(10, False, False) == '10 B'
    assert human_readable_byte_count(900, False, False) == '900 B'
    assert human_readable_byte_count(999, False, False) == '999 B'

    assert human_readable_byte_count(1000, False, False) == '1.00 KB'
    assert human_readable_byte_count(2000, False, False) == '2.00 KB'
    assert human_readable_byte_count(1000 * 1000 - 10, False, False) == '999.99 KB'

    assert human_readable_byte_count(1000 * 1000, False, False) == '1.00 MB'
    assert human_readable_byte_count(50 * 1000 * 1000, False, False) == '50.00 MB'
    assert human_readable_byte_count(1000 * 1000 * 1000 - 10000, False, False) == '999.99 MB'

    assert human_readable_byte_count(1000 * 1000 * 1000, False, False) == '1.00 GB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000, False, False) == '50.00 GB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 - 10000000, False, False) == '999.99 GB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000, False, False) == '1.00 TB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 TB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 - 1e10, False, False) == '999.99 TB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000, False, False) == '1.00 PB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 PB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000 - 1e13, False, False) == '999.99 PB'

    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '1.00 EB'
    assert human_readable_byte_count(50 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000, False, False) == '50.00 EB'
    assert human_readable_byte_count(1000 * 1000 * 1000 * 1000 * 1000 * 1000 * 1000 - 1e16, False, False) == '999.99 EB'


@pytest.mark.unit
def test_calculate_default_optimal_heap_sizes():
    # 64-bit, 8 cpu cores for screenshot purposes
    test_64_bit_values_8_cores = [
        # physical, appserver, cassandra, jmvLink, postgres, netLink, topics, webserver, supervisor, os
        [4000, 1200, 500, 250, 500, 250, 500, 250, 300, 250],
        [8000, 2700, 1000, 500, 1000, 500, 1000, 500, 300, 500],
        [12000, 4200, 1500, 750, 1500, 750, 1500, 750, 300, 750],
        [16000, 5700, 2000, 1000, 2000, 1000, 2000, 1000, 300, 1000],
        [32000, 11700, 4000, 2000, 4000, 2000, 4000, 2000, 300, 2000],
        [64000, 27700, 8000, 4000, 8000, 4000, 4000, 4000, 300, 4000],
        [128000, 67700, 8000, 8000, 16000, 8000, 4000, 8000, 300, 8000],
        [256000, 147700, 8000, 16000, 32000, 16000, 4000, 16000, 300, 16000]
    ]

    conf.set_option('Cpu/Count', 8, '')

    for test_set in test_64_bit_values_8_cores:
        conf.set_option('Memory/System/Total', test_set[0], '')

        assert conf.get_option('Memory/Appserver/Size') == test_set[1]
        assert conf.get_option('Memory/Cassandra/Size') == test_set[2]
        assert conf.get_option('Memory/JvmLink/Size') == test_set[3]
        assert conf.get_option('Memory/Postgres/Size') == test_set[4]
        assert conf.get_option('Memory/NetLink/Size') == test_set[5]
        assert conf.get_option('Memory/Topics/Size') == test_set[6]
        assert conf.get_option('Memory/Webserver/Size') == test_set[7]
        assert conf.get_option('Memory/Supervisor/Size') == test_set[8]
        assert conf.get_option('Memory/OperatingSystem/Size') == test_set[9]
        # Uncomment the following when needing to update the test
        # print(test_set[0], end=",")
        # print(conf.get_option('Memory/Appserver/Size'), end=",")
        # print(conf.get_option('Memory/Cassandra/Size'), end=",")
        # print(conf.get_option('Memory/JvmLink/Size'), end=",")
        # print(conf.get_option('Memory/Postgres/Size'), end=",")
        # print(conf.get_option('Memory/NetLink/Size'), end=",")
        # print(conf.get_option('Memory/Topics/Size'), end=",")
        # print(conf.get_option('Memory/Webserver/Size'), end=",")
        # print(conf.get_option('Memory/Supervisor/Size'), end=",")
        # print(conf.get_option('Memory/OperatingSystem/Size'), end=",")
        # print("")

    # 64-bit, 64 cpu cores for screenshot purposes
    test_64_bit_values_64_cores = [
        # physical, appserver, cassandra, jmvLink, postgres, netLink, topics, webserver, supervisor, os
        [4000, 1200, 500, 250, 500, 250, 500, 250, 300, 250],
        [8000, 2700, 1000, 500, 1000, 500, 1000, 500, 300, 500],
        [12000, 4200, 1500, 750, 1500, 750, 1500, 750, 300, 750],
        [16000, 5700, 2000, 1000, 2000, 1000, 2000, 1000, 300, 1000],
        [32000, 11700, 4000, 2000, 4000, 2000, 4000, 2000, 300, 2000],
        [64000, 23700, 8000, 4000, 8000, 4000, 8000, 4000, 300, 4000],
        [128000, 55700, 8000, 8000, 16000, 8000, 16000, 8000, 300, 8000],
        [256000, 119700, 8000, 16000, 32000, 16000, 32000, 16000, 300, 16000],
        [512000, 279700, 8000, 32000, 64000, 32000, 32000, 32000, 300, 32000],
    ]

    conf.set_option('Cpu/Count', 64, '')
    for test_set in test_64_bit_values_64_cores:
        conf.set_option('Memory/System/Total', test_set[0], '')

        assert conf.get_option('Memory/Appserver/Size') == test_set[1]
        assert conf.get_option('Memory/Cassandra/Size') == test_set[2]
        assert conf.get_option('Memory/JvmLink/Size') == test_set[3]
        assert conf.get_option('Memory/Postgres/Size') == test_set[4]
        assert conf.get_option('Memory/NetLink/Size') == test_set[5]
        assert conf.get_option('Memory/Topics/Size') == test_set[6]
        assert conf.get_option('Memory/Webserver/Size') == test_set[7]
        assert conf.get_option('Memory/Supervisor/Size') == test_set[8]
        assert conf.get_option('Memory/OperatingSystem/Size') == test_set[9]
        # Uncomment the following when needing to update the test
        # print(test_set[0], end=",")
        # print(conf.get_option('Memory/Appserver/Size'), end=",")
        # print(conf.get_option('Memory/Cassandra/Size'), end=",")
        # print(conf.get_option('Memory/JvmLink/Size'), end=",")
        # print(conf.get_option('Memory/Postgres/Size'), end=",")
        # print(conf.get_option('Memory/NetLink/Size'), end=",")
        # print(conf.get_option('Memory/Topics/Size'), end=",")
        # print(conf.get_option('Memory/Webserver/Size'), end=",")
        # print(conf.get_option('Memory/Supervisor/Size'), end=",")
        # print(conf.get_option('Memory/OperatingSystem/Size'), end=",")
        # print("")

    conf.unset_option('Cpu/Count')
    conf.unset_option('Memory/System/Total')
    # Uncomment the following when needing to update the test
    # assert False
