"""
This package calculates the total number of IOPS needed for your raid configuration.
"""

def get_total_iops(iops_required, read_percentage, raid_config):
    """

    :param iops_required: Positive integer of IOPS needed.
    :param read_percentage: Float between 0 and 1
    :param raid_config: Number representing RAID configuration. 0, 1, 5, 6, and 10 are accepted
    :return: Total iops

    Examples:

    >>> get_total_iops(400, .35, 1)
    660

    >>> get_total_iops(400, .35, 6)
    1700
    """
    if iops_required < 0:
        exit("Iops required should be a positive integer")
    elif read_percentage < 0 or read_percentage > 1:
        exit("Read percentage should be a float between 0 and 1")
    elif raid_config not in [0, 1, 5, 6, 10]:
        exit("Raid config should be 0, 1, 5, 6, 10")
    raid = {0:1, 1:2, 5:4, 6:6, 10:2}
    iops = (iops_required * read_percentage) + (iops_required * (1 - read_percentage) * raid[raid_config])
    return int(iops)

if __name__ == "__main__":
    import doctest
    doctest.testmod()