import tensorly as tl
from ...random import check_random_state, random_cp
from ...testing import assert_

from .._cp_power import parafac_power_iteration


def test_parafac_power_iteration():
    """Test for symmetric Parafac optimized with robust tensor power iterations"""
    rng = check_random_state(1234)
    tol_norm_2 = 10e-1
    tol_max_abs = 10e-1
    
    shape = (5, 3, 4)
    rank = 4
    tensor = random_cp(shape, rank=rank, full=True, random_state=rng)
    ktensor = parafac_power_iteration(tensor, rank=10, n_repeat=10, n_iteration=10)

    rec = tl.cp_to_tensor(ktensor)
    error = tl.norm(rec - tensor, 2)/tl.norm(tensor, 2)
    assert_(error < tol_norm_2,
            f'Norm 2 of reconstruction error={error} higher than tol={tol_norm_2}.')
    error = tl.max(tl.abs(rec - tensor))
    assert_(error < tol_max_abs,
            f'Absolute norm of reconstruction error={error} higher than tol={tol_max_abs}.')
