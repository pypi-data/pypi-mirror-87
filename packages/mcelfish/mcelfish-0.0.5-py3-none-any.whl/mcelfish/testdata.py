from collections import namedtuple


## catches, est_zippin, est_carle_strub, cathability: q = 1-p,
Catch = namedtuple("Catch", "data hat_nz hat_ncs p x ci")

# note: x is the _weighted_sum defined by
#
# lambda data : sum((len(data) - (1 + i)) * e for (i, e) in enumerate(data))

catches = []

#
# 0
#
catches.append(
    Catch(
        data=[100, 10, 1, 1, 0, 0],
        hat_nz=112,
        hat_ncs=112,
        p=0.9,
        x=-1,
        ci=1,
    )  ## ???
)


#
# 1
#
catches.append(
    Catch(
        data=[19, 17, 13, 1, 1],
        hat_nz=53,
        hat_ncs=53,
        p=0.46,
        x=154,
        ci=4.4,
    )
)


#
# 2
#
catches.append(
    Catch(
        data=[10, 20, 30, 24, 2, 7],
        hat_nz=156,
        hat_ncs=145,
        p=0.14,
        x=270,
        ci=80.29,
    )
)

#
# 3
#
catches.append(
    Catch(
        data=[5, 1, 0, 0, 0, 0, 0],
        hat_nz=6,
        hat_ncs=6,
        p=0.86,
        x=35,
        ci=0.00529,
    )
)


#
# 4
#
catches.append(
    Catch(
        data=[34, 46, 22, 26, 18, 16, 20, 12],
        hat_nz=268,
        hat_ncs=264,
        p=0.1454,
        x=834,
        ci=56.33,
    )
)

# laks (5)
catches.append(
    Catch(
        data=[32, 40, 12, 19, 9, 7, 8, 5, 2, 3, 1, 1, 0],
        hat_nz=141,
        hat_ncs=140,
        p=None,
        x=None,
        ci=3.38,
    )
)

# orre (6)
catches.append(
    Catch(
        data=[22, 9, 3, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        hat_ncs=38,
        hat_nz=38,
        p=None,
        x=None,
        ci=0.06,
    )
)
